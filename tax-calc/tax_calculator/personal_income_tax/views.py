from django.shortcuts import render
from .models import TaxCalculator


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
        citizenInvestmentFund = float(request.POST.get("citizenInvestmentFund"))
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

        total_income = tax_calculator.calculate_total_income()
        total_deductions = tax_calculator.calculate_deductions()
        total_taxable_income = tax_calculator.calculate_total_taxable_income()
        total_tax_per_year = tax_calculator.calculate_total_tax()

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