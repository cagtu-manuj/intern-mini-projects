from django.db.models import F
from django.db.models import Subquery
from .models import BracketInformation
from .models import UserTaxInformation
from .models import DeductionInformation
from .models import TaxCalculator
from django.test import TestCase
from django.db.models import Q, Sum


def populate_db():
    user_tax = UserTaxInformation(
        marital_status="single",
        income=1440000,
        festival_bonus=120000,
        allowance=960000,
        others=393000,
        pf_or_ssf="ssf",
        pf_or_ssf_amount=446400,
        citizen_investment_fund=300000,
        life_insurance=100000,
        medical_insurance=18000,
    )
    deduction_information = DeductionInformation(
        year=2079, pf_deduction_rate=0.1, pf_deduction_limit=300000, ssf_deduction_rate=0.31, ssf_deduction_limit=500000)
    BracketInformation(
        year=2079, limit=500000, difference=500000, rate=0.01, pf_or_ssf="pf", single_or_couple=""
    ).save()
    BracketInformation(
        year=2079, limit=500000, difference=500000, rate=0.00, pf_or_ssf="ssf", single_or_couple=""
    ).save()
    BracketInformation(
        year=2079, limit=700000, difference=200000, rate=0.1, pf_or_ssf="", single_or_couple="single"
    ).save()
    BracketInformation(
        year=2079, limit=1000000, difference=300000, rate=0.2, pf_or_ssf="", single_or_couple="single"
    ).save()
    BracketInformation(
        year=2079, limit=2000000, difference=1000000, rate=0.3, pf_or_ssf="", single_or_couple="single"
    ).save()
    BracketInformation(
        year=2079, limit=None, difference=None, rate=0.36, pf_or_ssf="", single_or_couple="single"
    ).save()

    deduction_information.save()
    user_tax.save()


# Create your tests here.
class TaxCalculatorTest(TestCase):
    def test_calculate_tax_single_ssf(self):
        tax_calculator = TaxCalculator(
            marital_status="single",
            income=1440000,
            festival_bonus=120000,
            allowance=960000,
            others=393000,
            pf_or_ssf="ssf",
            pf_or_ssf_amount=446400,
            citizenInvestmentFund=300000,
            lifeInsurance=100000,
            medicalInsurance=18000,
        )
        populate_db()
        total_income_obj = UserTaxInformation.objects.annotate(
            total=F('income')+F('festival_bonus') + F('allowance') + F('others')).first()
        total_income = getattr(total_income_obj, "total")
        ssf_or_pf = getattr(total_income_obj, "pf_or_ssf")
        income = getattr(total_income_obj, "income")
        single_or_couple = getattr(total_income_obj, "marital_status")

        if ssf_or_pf == "ssf":
            deduction_rate = getattr(
                DeductionInformation.objects.all().first(), "ssf_deduction_rate")
            deduction_limit = getattr(
                DeductionInformation.objects.all().first(), "ssf_deduction_limit")

        total_ssf_pf_cif = UserTaxInformation.objects.all().annotate(total_ssf_pf_cif=(
            F("income") * deduction_rate) + F("citizen_investment_fund")).values('total_ssf_pf_cif').first()['total_ssf_pf_cif']
        deduction = min(total_ssf_pf_cif, deduction_limit, total_income / 3)
        life_insurance = min(UserTaxInformation.objects.all().values(
            'life_insurance').first()['life_insurance'], 40000)
        medical_insurance = min(UserTaxInformation.objects.all().values(
            'medical_insurance').first()['medical_insurance'], 20000)

        total_deduction = deduction + life_insurance + medical_insurance
        total_taxable_income = total_income - total_deduction
        initial_tax = (BracketInformation.objects.filter(
            Q(limit__lt=total_taxable_income)).filter(Q(single_or_couple="single") | Q(pf_or_ssf="ssf")).order_by("rate").annotate(total=(F("rate") * F("difference"))).aggregate(Sum("total"))["total__sum"])
        leftover = total_taxable_income - (BracketInformation.objects.filter(
            Q(limit__lt=total_taxable_income)).filter(Q(single_or_couple="single") | Q(pf_or_ssf="ssf")).order_by("rate").aggregate(Sum("difference")))["difference__sum"]
        extra_tax = BracketInformation.objects.filter(
            Q(limit__gt=total_taxable_income) | Q(difference=None)).filter(Q(single_or_couple="single") | Q(pf_or_ssf="ssf")).order_by("rate").annotate(final=(F("rate") * leftover)).values("final").first()["final"]
        total_tax = initial_tax + extra_tax

        self.assertEqual(total_income, 2913000)
        self.assertEqual(total_deduction, 558000)
        self.assertEqual(
            total_taxable_income, 2355000)
        self.assertEqual(total_tax, 507800)

    def test_calculate_tax_married_ssf(self):
        tax_calculator = TaxCalculator(
            marital_status="married",
            income=1440000,
            festival_bonus=120000,
            allowance=960000,
            others=393000,
            pf_or_ssf="ssf",
            pf_or_ssf_amount=446400,
            citizenInvestmentFund=300000,
            lifeInsurance=100000,
            medicalInsurance=18000,
        )
        self.assertEqual(tax_calculator.calculate_total_income(), 2913000)
        self.assertEqual(tax_calculator.calculate_deductions(), 558000)
        self.assertEqual(
            tax_calculator.calculate_total_taxable_income(), 2355000)
        self.assertEqual(tax_calculator.calculate_total_tax(), 513800)

    def test_calculate_tax_single_pf(self):
        tax_calculator = TaxCalculator(
            marital_status="single",
            income=1440000,
            festival_bonus=120000,
            allowance=960000,
            others=249000,
            pf_or_ssf="pf",
            pf_or_ssf_amount=288000,
            citizenInvestmentFund=300000,
            lifeInsurance=100000,
            medicalInsurance=18000,
        )
        self.assertEqual(tax_calculator.calculate_total_income(), 2769000)
        self.assertEqual(tax_calculator.calculate_deductions(), 358000)
        self.assertEqual(
            tax_calculator.calculate_total_taxable_income(), 2411000)
        self.assertEqual(tax_calculator.calculate_total_tax(), 532960)

    def test_calculate_tax_married_pf(self):
        tax_calculator = TaxCalculator(
            marital_status="couple",
            income=1440000,
            festival_bonus=120000,
            allowance=960000,
            others=249000,
            pf_or_ssf="pf",
            pf_or_ssf_amount=288000,
            citizenInvestmentFund=300000,
            lifeInsurance=100000,
            medicalInsurance=18000,
        )
        self.assertEqual(tax_calculator.calculate_total_income(), 2769000)
        self.assertEqual(tax_calculator.calculate_deductions(), 358000)
        self.assertEqual(
            tax_calculator.calculate_total_taxable_income(), 2411000)
        self.assertEqual(tax_calculator.calculate_total_tax(), 538960)
