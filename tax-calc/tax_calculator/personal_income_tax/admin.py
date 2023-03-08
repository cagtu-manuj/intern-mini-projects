from django.contrib import admin

# Register your models here.
from .models import BracketInformation
from .models import DeductionInformation
from .models import UserTaxInformation

admin.site.register(BracketInformation)
admin.site.register(DeductionInformation)
admin.site.register(UserTaxInformation)
