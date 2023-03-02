from django.db import models

# Create your models here.


class TaxCalculator:
    def __init__(
        self,
        marital_status: str,
        income: int,
        festival_bonus: int,
        allowance: int,
        others: int,
        pf_or_ssf: str,
        pf_or_ssf_amount: int,
        citizenInvestmentFund: int,
        lifeInsurance: int,
        medicalInsurance: int,
    ):
        self.marital_status = marital_status

        self.income = income
        self.festival_bonus = festival_bonus
        self.allowance = allowance
        self.others = others

        self.pf_or_ssf_amount = pf_or_ssf_amount
        self.pf_or_ssf = pf_or_ssf
        self.citizenInvestmentFund = citizenInvestmentFund
        self.lifeInsurance = lifeInsurance
        self.medicalInsurance = medicalInsurance

    def calculate_total_income(self):
        return self.income + self.festival_bonus + self.allowance + self.others

    def calculate_deductions(self):
        if self.pf_or_ssf == "pf":
            pf_or_ssf_deduction = 0.1 * self.income
            deduction_limit = 300000
        else:
            pf_or_ssf_deduction = 0.31 * self.income
            deduction_limit = 500000
        total_ssf_pf_cif = pf_or_ssf_deduction + self.citizenInvestmentFund
        deduction = min(
            total_ssf_pf_cif, deduction_limit, self.calculate_total_income() / 3
        )
        lifeInsurance = min(self.lifeInsurance, 40000)
        medicalInsurance = min(self.medicalInsurance, 20000)
        return deduction + lifeInsurance + medicalInsurance

    def calculate_total_taxable_income(self):
        return self.calculate_total_income() - self.calculate_deductions()

    def calculate_total_tax(self):
        total_taxable_income = self.calculate_total_taxable_income()
        total_tax = 0
        if self.marital_status == "single":
            if total_taxable_income > 0:
                if self.pf_or_ssf == "pf":
                    total_tax += 0.01 * min(total_taxable_income, 500000)
                total_taxable_income -= 500000
            if total_taxable_income > 0:
                total_tax += 0.1 * min(total_taxable_income, 200000)
                total_taxable_income -= 200000

            if total_taxable_income > 0:
                total_tax += 0.2 * min(total_taxable_income, 300000)
                total_taxable_income -= 300000

            if total_taxable_income > 0:
                total_tax += 0.3 * min(total_taxable_income, 1000000)
                total_taxable_income -= 1000000

            if total_taxable_income > 0:
                total_tax += 0.36 * total_taxable_income

        else:
            if total_taxable_income > 0:
                if self.pf_or_ssf == "pf":
                    total_tax += 0.01 * min(total_taxable_income, 500000)
                total_taxable_income -= 500000
            if total_taxable_income > 0:
                total_tax += 0.1 * min(total_taxable_income, 200000)
                total_taxable_income -= 200000

            if total_taxable_income > 0:
                total_tax += 0.2 * min(total_taxable_income, 300000)
                total_taxable_income -= 300000

            if total_taxable_income > 0:
                total_tax += 0.3 * min(total_taxable_income, 900000)
                total_taxable_income -= 900000

            if total_taxable_income > 0:
                total_tax += 0.36 * total_taxable_income

        return total_tax
