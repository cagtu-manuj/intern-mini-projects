from django.shortcuts import render
from django.db.models import F
from .models import BracketInformation
from .models import UserTaxInformation
from .models import DeductionInformation
from .models import TaxCalculator
from django.db.models import Q, Sum


def get_tax_from_db(pk):
    total_income_obj = UserTaxInformation.objects.annotate(
        total=F('income')+F('festival_bonus') + F('allowance') + F('others')).get(pk=pk)
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
    initial_tax = BracketInformation.objects.filter(
        Q(limit__lt=total_taxable_income)).filter(Q(single_or_couple="Single") | Q(pf_or_ssf="ssf")).order_by("rate").annotate(total=(F("rate") * F("difference"))).aggregate(Sum("total"))["total__sum"]
    leftover = total_taxable_income - (BracketInformation.objects.filter(
        Q(limit__lt=total_taxable_income)).filter(Q(single_or_couple="Single") | Q(pf_or_ssf="ssf")).order_by("rate").aggregate(Sum("difference")))["difference__sum"]
    extra_tax = BracketInformation.objects.filter(
        Q(limit__gt=total_taxable_income) | Q(difference=None)).filter(Q(single_or_couple="Single") | Q(pf_or_ssf="ssf")).order_by("rate").annotate(final=(F("rate") * leftover)).values("final").first()["final"]
    total_tax = initial_tax + extra_tax
    return (total_income, total_deduction, total_taxable_income, total_tax)


# Create your views here.
def index(request):
    if request.method == "POST":
        marital_status = request.POST.get("maritalStatus")

        income = float(request.POST.get("income"))
        festival_bonus = float(request.POST.get("festivalBonus"))
        allowance = float(request.POST.get("allowance"))
        others = float(request.POST.get("others"))

        pf_or_ssf = request.POST.get("pf_or_ssf")
        pf_or_ssf_amount = float(request.POST.get("pf_or_ssf_amount"))
        citizenInvestmentFund = float(
            request.POST.get("citizenInvestmentFund"))
        lifeInsurance = float(request.POST.get("lifeInsurance"))
        medicalInsurance = float(request.POST.get("medicalInsurance"))

        tax_calculator = TaxCalculator(
            marital_status,
            income,
            festival_bonus,
            allowance,
            others,
            pf_or_ssf,
            pf_or_ssf_amount,
            citizenInvestmentFund,
            lifeInsurance,
            medicalInsurance,
        )
        user_tax = UserTaxInformation(
            marital_status=marital_status,
            income=income,
            festival_bonus=festival_bonus,
            allowance=allowance,
            others=others,
            pf_or_ssf=pf_or_ssf,
            pf_or_ssf_amount=pf_or_ssf_amount,
            citizen_investment_fund=citizenInvestmentFund,
            life_insurance=lifeInsurance,
            medical_insurance=medicalInsurance
        )
        user_tax.save()

        tax_information = get_tax_from_db(user_tax.pk)
        total_income, total_deductions, total_taxable_income, total_tax_per_year = tax_information

        print(f"total_income: {total_income}")
        print(f"total_deductions: {total_deductions}")
        print(f"total_taxable_income: {total_taxable_income}")
        print(f"total_tax_per_year: {total_tax_per_year}")
        return render(
            request,
            "personal_income_tax/tax.html",
            {
                "total_income": total_income,
                "total_deductions": total_deductions,
                "total_taxable_income": total_taxable_income,
                "total_tax_per_year": total_tax_per_year,
            },
        )
    if request.method == "GET":
        return render(request, "personal_income_tax/index.html", {})
