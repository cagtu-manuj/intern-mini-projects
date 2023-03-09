from django.test import TestCase
from .models import TaxCalculator
from .models import DeductionInformation
from .models import UserTaxInformation
from .models import BracketInformation
from django.db.models import F


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
        year=2079, limit=500000, difference=500000, rate=0.01, pf_or_ssf="pf", single_or_couple="single"
    ).save()
    BracketInformation(
        year=2079, limit=500000, difference=500000, rate=0.00, pf_or_ssf="ssf", single_or_couple="single"
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
        print(BracketInformation.objects.all().values())
        print("\n\n\n\n")
        print(DeductionInformation.objects.all().values())
        total_obj = UserTaxInformation.objects.annotate(
            total=F('income')+F('festival_bonus') + F('allowance') + F('others')).first()
        total_income = getattr(total_obj, "total")
        self.assertEqual(total_income, 2913000)
        self.assertEqual(tax_calculator.calculate_deductions(), 558000)
        self.assertEqual(
            tax_calculator.calculate_total_taxable_income(), 2355000)
        self.assertEqual(tax_calculator.calculate_total_tax(), 507800)

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
