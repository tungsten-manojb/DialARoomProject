from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect

from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt

from django.contrib import auth
from quoteapp.models import *
from django.http import HttpResponse
from quoteapp.quote_constants import QuoteConstant
from CorpRoomApp.models import *
from CorpRoomApp.forms import *
from quoteapp.models import *
import pdb
import json

def quotation_list_page(request):
    print 'Quotation List Page'
    return render(request,'property-vendor/quote-request/vendor-quotation-list.html')


def get_quotation_list(request):
    data = {}
    try:
        quote_requests = QuoteRequest.objects.filter(customer_id=Customer.objects.get(id=request.session['apt_vendor_id']))
        quotations = QuotationResponse.objects.filter(request_id__in=quote_requests)
        data = { 'data' : [ q.get_quotation_info() for q in quotations ]}
    except Exception as err:
        print 'err', err
        data = {'data' : 'none'}
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
        data = {'quote_request' : qr, 'quotation': quotation, 'facility_list' : [q for q in quotation.property_id.property_facility.split(',') if q] }
    except Exception as err:
        print 'Hello : ',err
        data = {}
    return render(request,'property-vendor/quote-request/quotation-details.html',data)

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


def get_all_location(request):
    # print 'City Name', request.GET.get('city')
    area_list =[]
    try:
        city = City.objects.get(city_id=request.GET.get('city'))
        area_list = [location.get_location_info() for location in Location.objects.filter(city_id=city)]
        data = {'success': 'true','location':area_list}
    except Exception as err:
        print 'Exception ',err
        data = {'success': 'false'}
    return HttpResponse(json.dumps(data), content_type='application/json')   


def get_all_properties(request):
    print 'I am in function'
    print 'RE DATA : ',request.GET.get('location')
    data = []
    filter_args={}
    try:
        if request_data:
            if request_data['city_name']:
                filter_args['property_location__icontains'] = request.GET.get('location')
        filter_args['property_availability_status']=True

        print datetime.datetime.now()
        #property_list = Property.objects.filter(Q(property_id__in = Property.objects.filter(**filter_args)))
        property_list = Property.objects.filter(filter_args)
        property_rate =  1450.00
        for property in property_list:
            try:
                rates = PropertyRate.objects.get(property_id=property)
                property_rate = rates.single_occupancy_display_rate
            except Exception as err:
                print 'ERR',err
            pr = { 'property_id': property.property_id, 'property_name': property.property_display_name,
                'property_address':property.property_location, 'property_desc' : property.property_description, 'property_rate': property_rate,
                'property_rating' : property.star_category, 'airport_distance' : property.distance_from_airport,
                'railway_stop_distance' : property.distance_from_railway_station, 'star': str(property.star_category*20)  }
            data.append(pr)
        print datetime.datetime.now()
    except Exception as e:
        print 'Search Properties - Exception : ',e
    return data
