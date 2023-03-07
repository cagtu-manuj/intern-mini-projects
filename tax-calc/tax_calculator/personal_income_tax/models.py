from django.db import models

# Create your models here.


class UserTaxInformation(models.Model):
    MARRIED = "Couple"
    SINGLE = "Single"
    MARITAL_STATUS_CHOICES = [
        (MARRIED, "Couple"),
        (SINGLE, "Single"),
    ]
    PF = "pf"
    SSF = "ssf"
    PF_OR_SSF_CHOICES = [
        (PF, "pf"),
        (SSF, "ssf"),
    ]
    marital_status = models.CharField(
        max_length=10, choices=MARITAL_STATUS_CHOICES, default=SINGLE
    )
    pf_or_ssf = models.CharField(max_length=3, choices=PF_OR_SSF_CHOICES, default=PF)
    income = models.DecimalField(decimal_places=3, max_digits=15, default=0)
    festival_bonus = models.DecimalField(decimal_places=3, max_digits=15, default=0)
    allowance = models.DecimalField(decimal_places=3, max_digits=15, default=0)
    others = models.DecimalField(decimal_places=3, max_digits=15, default=0)
    pf_or_ssf_amount = models.DecimalField(decimal_places=3, max_digits=15, default=0)
    citizen_investment_fund = models.DecimalField(
        decimal_places=3, max_digits=15, default=0
    )
    life_insurance = models.DecimalField(decimal_places=3, max_digits=15, default=0)
    medical_insurance = models.DecimalField(decimal_places=3, max_digits=15, default=0)

    total_income = models.DecimalField(decimal_places=3, max_digits=15, default=0)
    deductions = models.DecimalField(decimal_places=3, max_digits=15, default=0)
    total_taxable_income = models.DecimalField(
        decimal_places=3, max_digits=15, default=0
    )
    total_tax = models.DecimalField(decimal_places=3, max_digits=15, default=0)


class TaxInformation(models.Model):
    year = models.IntegerField(primary_key=True)
    pf_deduction_rate = models.DecimalField(
        decimal_places=3, max_digits=14, default=0.1
    )
    pf_deduction_limit = models.DecimalField(
        decimal_places=3, max_digits=15, default=300000
    )
    ssf_deduction_rate = models.DecimalField(
        decimal_places=3, max_digits=14, default=0.31
    )
    ssf_deduction_limit = models.DecimalField(
        decimal_places=3, max_digits=15, default=500000
    )

    first_bracket_limit_single = models.DecimalField(
        decimal_places=3, max_digits=15, default=500000
    )
    first_bracket_limit_couple = models.DecimalField(
        decimal_places=3, max_digits=15, default=500000
    )
    first_bracket_rate_pf = models.DecimalField(
        decimal_places=3, max_digits=15, default=0.01
    )
    first_bracket_rate_ssf = models.DecimalField(
        decimal_places=3, max_digits=15, default=0
    )

    second_bracket_limit_single = models.DecimalField(
        decimal_places=3, max_digits=15, default=200000
    )
    second_bracket_rate_single = models.DecimalField(
        decimal_places=3, max_digits=15, default=0.1
    )
    second_bracket_limit_couple = models.DecimalField(
        decimal_places=3, max_digits=15, default=200000
    )
    second_bracket_rate_single = models.DecimalField(
        decimal_places=3, max_digits=15, default=0.1
    )

    third_bracket_limit_single = models.DecimalField(
        decimal_places=3, max_digits=15, default=200000
    )
    third_bracket_rate_single = models.DecimalField(
        decimal_places=3, max_digits=15, default=0.1
    )
    third_bracket_limit_couple = models.DecimalField(
        decimal_places=3, max_digits=15, default=200000
    )
    third_bracket_rate_single = models.DecimalField(
        decimal_places=3, max_digits=15, default=0.1
    )

    fourth_bracket_limit_single = models.DecimalField(
        decimal_places=3, max_digits=15, default=200000
    )
    fourth_bracket_rate_single = models.DecimalField(
        decimal_places=3, max_digits=15, default=0.1
    )
    fourth_bracket_limit_couple = models.DecimalField(
        decimal_places=3, max_digits=15, default=200000
    )
    fourth_bracket_rate_single = models.DecimalField(
        decimal_places=3, max_digits=15, default=0.1
    )

    fifth_bracket_limit_single = models.DecimalField(
        decimal_places=3, max_digits=15, default=200000
    )
    fifth_bracket_rate_single = models.DecimalField(
        decimal_places=3, max_digits=15, default=0.1
    )
    fifth_bracket_limit_couple = models.DecimalField(
        decimal_places=3, max_digits=15, default=200000
    )
    fifth_bracket_rate_single = models.DecimalField(
        decimal_places=3, max_digits=15, default=0.1
    )


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
        self.citizen_investment_fund = citizenInvestmentFund
        self.life_insurance = lifeInsurance
        self.medical_insurance = medicalInsurance

    def calculate_total_income(self):
        return self.income + self.festival_bonus + self.allowance + self.others

    def calculate_deductions(self):
        if self.pf_or_ssf == "pf":
            pf_or_ssf_deduction = 0.1 * self.income
            deduction_limit = 300000
        else:
            pf_or_ssf_deduction = 0.31 * self.income
            deduction_limit = 500000
        total_ssf_pf_cif = pf_or_ssf_deduction + self.citizen_investment_fund
        deduction = min(
            total_ssf_pf_cif, deduction_limit, self.calculate_total_income() / 3
        )
        lifeInsurance = min(self.life_insurance, 40000)
        medicalInsurance = min(self.medical_insurance, 20000)
        return deduction + lifeInsurance + medicalInsurance

    def calculate_total_taxable_income(self):
        return self.calculate_total_income() - self.calculate_deductions()

    def calculate_total_tax(self):
        total_taxable_income = self.calculate_total_taxable_income()
        total_tax = 0
        tax_information_single = [
            (200000, 0.1),
            (300000, 0.2),
            (1000000, 0.3),
            (2000000, 0.36),
        ]
        tax_information_couple = [
            (200000, 0.1),
            (300000, 0.2),
            (900000, 0.3),
            (2000000, 0.36),
        ]
        # tax_information_single = [(200000, 0.1), (300000, 0.2), (900000, 0.3), (0, 0.36)]
        if self.marital_status == "single":
            if total_taxable_income > 0:
                if self.pf_or_ssf == "pf":
                    total_tax += 0.01 * min(total_taxable_income, 500000)
                total_taxable_income -= 500000
            for bracket, rate in tax_information_single:
                if total_taxable_income <= 0:
                    break
                total_tax += rate * min(total_taxable_income, bracket)
                total_taxable_income -= bracket

        else:
            if total_taxable_income > 0:
                if self.pf_or_ssf == "pf":
                    total_tax += 0.01 * min(total_taxable_income, 500000)
                total_taxable_income -= 500000

            for bracket, rate in tax_information_couple:
                if total_taxable_income <= 0:
                    break
                total_tax += rate * min(total_taxable_income, bracket)
                total_taxable_income -= bracket
        return total_tax
