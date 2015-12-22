from django.contrib import admin

# Register your models here.
from quoteapp.models import *


# class QuoteRequestAdmin(admin.ModelAdmin):
# list_display = ['cust_name']
# ,'cust_designation','cust_mobile_no','dar_executive','follow_up_count','follow_up_date']


# pass
# list_display = ['cust_name','cust_designation','cust_mobile_no','dar_executive','follow_up_count','follow_up_date']


admin.site.register(QuoteRequest)
admin.site.register(QuotationResponse)
admin.site.register(RequestedProperty)
admin.site.register(UserRequestStatisticTrack)
