
from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect

from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt

from django.contrib import auth
from quoteapp.models import *
from django.http import HttpResponse
from quoteapp.quote_constants import QuoteConstant
import pdb
import json
from django.template import Library


register = Library()


@register.filter
def get_range( value ):
    return range( value )

def quotation_list_page(request):
    print 'Quotation List Page'
    return render(request,'cam-user/quote-request/cam-quotation-list.html')


def get_quotation_list(request):
    data = {}
    try:
        quote_requests = QuoteRequest.objects.filter(customer_id=Customer.objects.get(id=request.session['user_id']))
        quotations = QuotationResponse.objects.filter(request_id__in=quote_requests)
        data = { 'data' : [ q.get_quotation_info() for q in quotations ]}
    except Exception as err:
        print 'err', err
        data = {'data' : []}
    return HttpResponse(json.dumps(data), content_type='application/json')

# Display quotation details and update the customer status for quote_request
def quotation_details(request):
    print 'Hello'
    data = {}
    try:
        qr = QuoteRequest.objects.get(quote_request_uid=request.GET.get('quote_request_uid'))
        if qr.quote_customer_status == QuoteConstant.REQUEST_SUBMITTED:
            qr.quote_customer_status = QuoteConstant.REQUEST_VIEWED
            qr.save()
        quotation = QuotationResponse.objects.get(quotation_uid=request.GET.get('quotation_uid'))
        property_type = 'HOTEL'
        if qr.quote_property_type == 0:
            property_type = 'Service Apartment'

        data = {'quote_request' : qr, 'quotation': quotation,'property_type':property_type,  'facility_list' : [q for q in quotation.property_id.property_facility.split(',') if q] }
    except Exception as err:
        print 'Hello : ',err
        data = {}
    return render(request,'cam-user/quote-request/quotation-details.html',data)

# This is for accepting the quotation
def accept_quotation(request):
    print 'Acceptin Quotation'
    try:
        print ''
        quotation = QuotationResponse.objects.get(quotation_uid=request.GET.get('quote_uid'))
        quotation.quotation_status = QuoteConstant.REQUEST_ACCEPTED
        quotation.save()
        data = {'success':'true'}
    except Exception as err:
        print 'Hello'
        data = {'success':'false'}
    return HttpResponse(json.dumps(data), content_type='application/json')

# This is for Rejecting the quotation
def reject_quotation(request):
    print 'Acceptin Quotation'
    try:
        print ''
        quotation = QuotationResponse.objects.get(quotation_uid=request.GET.get('quote_uid'))
        quotation.quotation_status = QuoteConstant.REQUEST_REJECTED
        quotation.save()
        data = {'success':'true'}
    except Exception as err:
        print 'Hello'
        data = {'success':'false'}
    return HttpResponse(json.dumps(data), content_type='application/json')

def check_for_new_quotation(request):
    print 'Checking for new Quotation'
    