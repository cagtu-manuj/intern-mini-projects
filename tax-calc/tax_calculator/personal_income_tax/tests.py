from django.test import TestCase
from .models import TaxCalculator


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
        self.assertEqual(tax_calculator.calculate_total_income(), 2913000)
        self.assertEqual(tax_calculator.calculate_deductions(), 558000)
        self.assertEqual(tax_calculator.calculate_total_taxable_income(), 2355000)
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
        self.assertEqual(tax_calculator.calculate_total_taxable_income(), 2355000)
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
        self.assertEqual(tax_calculator.calculate_total_taxable_income(), 2411000)
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
        self.assertEqual(tax_calculator.calculate_total_taxable_income(), 2411000)
        self.assertEqual(tax_calculator.calculate_total_tax(), 538960)
