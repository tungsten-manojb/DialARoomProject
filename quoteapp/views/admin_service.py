from django.shortcuts import render
from django.contrib.auth.models import User

import traceback # This is for exception stack-trace

# Create your views here.
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import cache_control
from django.contrib import auth
from django.core.context_processors import csrf
from django.core import serializers
import pdb
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import logout
from django.contrib.auth import login
from django.shortcuts import redirect
from django.template import RequestContext
from django.db.models import Count, Sum

from django.views.generic import TemplateView

# importing mysqldb and system packages
import MySQLdb, sys
from django.db.models import Q
from django.db.models import F
from django.db import transaction

import csv
import json
#importing exceptions
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from django.utils.datastructures import MultiValueDictKeyError
from CorpRoomApp.send_sms import send_new_quotation_sms_to_corporate_user

# imports date times
import datetime
import time
from datetime import date, timedelta

from django.http import HttpResponse
from django.http import HttpResponseRedirect
from CorpRoomApp.models import *
from CorpRoomApp.forms import *
from quoteapp.models import *
import json
from CorpRoomApp.send_mail import  *
import sendgrid
from quoteapp.quote_constants import QuoteConstant

from CorpRoomApp.common_functionality import PropertyCommonFunctionality

#SERVER_URL = 'http://192.168.0.121:8000'
SERVER_URL = 'http://dial-a-room.com'
CORPORATE_REQUEST_URL = '/corporate/quote/request-details/?request_uid='

pcf = PropertyCommonFunctionality()

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def request_list_page(request):
    if not request.user.is_authenticated():
        return redirect('/')
    return render(request,'admin/quote-request/request-list.html')



def get_request_list(request):
    data = {}
    try:
        quotes = QuoteRequest.objects.all()
        data = { 'data' :  [ q.get_quote_info() for q in quotes ]}
    except Exception as err:
        print 'err', err
        data = {'data' : []}
    return HttpResponse(json.dumps(data), content_type='application/json')

def request_quote_details(request):
    data = {}
    try:
        print 'Quotation Details'
        quote_req = QuoteRequest.objects.get(quote_request_uid=request.GET.get('request_uid'))
        locations = quote_req.quote_location.split('$')
        days = quote_req.quote_end_date - quote_req.quote_start_date
        
        if days.days == 0:
            no_of_days = 1
        else:
            no_of_days = days.days
        
        data = {'quote' : quote_req,
               'error_message': 'success',
               'success': 'true',
               'no_of_days':no_of_days,
               'property_list':get_properties_for_quote(request),
               'location_list':locations,
               'quoted_property_list':get_quoted_property(quote_req),
               'city_list': pcf.get_all_city_name()
            }
    except Exception as err:
        print 'Error : ',err
        data = {}
    return render(request,'admin/quote-request/admin-request-details.html',data)

def get_quoted_property(quote_req):
    data = {}
    quoted_property_list=[]
    try:
        quotations = QuotationResponse.objects.filter(request_id=quote_req)
        print "quotations"
        for property_info in quotations:
            if property_info.property_id.property_type == 0:
                prop_type='Service Apartment'
            if property_info.property_id.property_type == 1:
                prop_type='Hotel'
            #rack_rate = property_info.property_id.rack_rate if property_info.property_id.rack_rate > 0 else property_info.rate
            quoted_property_list.append({ 'property_id': property_info.property_id,
                'property_location':property_info.property_id.property_location,
                'property_name': property_info.property_id.property_actual_name,
                'rack_rate' : property_info.property_id.rack_rate,
                'rate' : property_info.rate, 'amount' : property_info.amount,
                'tax' : property_info.tax_amount, 'total_amt' : property_info.total_quote_amt,
                'property_type' :prop_type })
        return quoted_property_list
    except Exception as err:
        print 'err', err
        return quoted_property_list

    # return HttpResponse(json.dumps(data), content_type='application/json')


def get_properties_for_quote(request):
    try:
        print 'Property List'
        property_list=[]
        prop_list=[]
        prop_type=''
        status=''
        property_rate=0.0
        quote_req = QuoteRequest.objects.get(quote_request_uid=request.GET.get('request_uid'))
        locations = quote_req.quote_location.split('$')

        properties_list=CustomerFavoriteProperty.objects.filter(customer_id=Customer.objects.get(user_ptr_id=quote_req.customer_id))

        for prop in properties_list:
            prop_list.append(prop.property_id.property_id)

        apartment_list = Property.objects.filter(property_id__in=prop_list)
        for apartment in apartment_list:
            if apartment.property_type == 0:
                prop_type='Service Apartment'
            if apartment.property_type == 1:
                prop_type='Hotel'
            if apartment.property_status ==1:
                status='NOT AVAILABLE'
            if apartment.property_status ==0:
                status='AVAILABLE'
            property_list.append({ 'property_id': apartment.property_id,
                'property_location':apartment.property_location,
                'property_name': apartment.property_actual_name,
                'property_rate' : get_property_rate(apartment),
                'property_type' : prop_type,
                'status' :status
                })
    except Exception, e:
        print 'Admin_Service.py | get_properties_for_quote | Error ',e
    return property_list

def get_property_rate(property_obj):
    property_rate=0.0
    try:
        property_rate =property_obj.property_rates.get().property_display_rate
    except Exception as err:
        print 'err', err
    return property_rate



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def quotation_list_page(request):
    if not request.user.is_authenticated():
        return redirect('/')
    return render(request,'admin/quote-request/admin-quotation-list.html')

def get_quotation_list(request):
    data = {}
    try:
        quotations = QuotationResponse.objects.all()
        print "quotations"
        data = { 'data' : [ q.get_quotation_info() for q in quotations ]}
    except Exception as err:
        print 'err', err
        data = {'data' : 'none'}
    return HttpResponse(json.dumps(data), content_type='application/json')



@csrf_exempt
def send_quotation(request):
    print 'send_quotation'
    # print property_details[0]['Id']
    property_ids = request.POST.getlist('property_ids')
    rate      = request.POST.getlist('rate')
    amount    = request.POST.getlist('amt')
    tax       = request.POST.getlist('tax')
    total_amt = request.POST.getlist('total_amt')
    rack_rate = request.POST.getlist('rack_rate')
    
    index=0

    try:
        quote_req = QuoteRequest.objects.get(quote_request_uid=request.POST.get('request_id'))
        if property_ids:
            for prop_id in property_ids:
                property= Property.objects.get(property_id=prop_id)
                property.rack_rate = rack_rate[index]
                property.save()
                quotation = QuotationResponse(
                    request_id              = quote_req,
                    property_id             = property,
                    rate                    = rate[index],
                    amount                  = amount[index],
                    tax_amount              = tax[index],
                    property_rack_rate      = property.rack_rate,   # rack rate
                    total_quote_amt         = total_amt[index],
                    quote_date              = datetime.datetime.today(),
                    created_date            = datetime.datetime.today(),
                    created_by              = 'Admin',
                    is_new                  = True,
                    quotation_status        = 'QUOTED',
                    viewed_by_customer      = False
                    )
                index += 1
                quotation.save()
                quotation.quotation_uid='QT'+str(quotation.quotation_id).zfill(6)
                quotation.save()
            
            print 'Save'
            quote_req.quote_admin_status='QUOTED'
            quote_req.save()
            print 'Final done'
            
            location = quote_req.quote_location.split('$')[0]
            
            # Send Mail to Corporate User
            send_quotation_email(quotation,quote_req)
            # send SMS to Corporate User 
            send_new_quotation_sms_to_corporate_user(quote_req.customer_id.cust_contact_no, quote_req.quote_request_uid,
             location , quotation.property_id.property_actual_name,quote_req.customer_id.cust_first_name )
            return redirect('/business/quote/get-quotation-page/?status=0')
        else:
            print 'Admin Create Quotation -- No Property to quote'
            return redirect('/business/quote/get-quotation-page/?status=1')
    except Exception, e:
        print 'Exception : ',e
        data = {'sucess': 'false'}
    return redirect('/business/quote/get-quotation-page/?status=2')
    #return render(request,'admin/quote-request/admin-quotation-list.html')
    # return render(request,'quote-request/quotation.html',data, context_instance=RequestContext(request))

# @csrf_exempt
# This quotation mail sent to corporate user against request
def send_quotation_email(quotation,request_obj):
    print "in the send email"
    try:
        print "quotation.requested_property"
        table=''
        quotation_details=QuotationResponse.objects.filter(request_id=request_obj)
        first_name=request_obj.customer_id.cust_first_name
        customer_email=request_obj.customer_id.cust_email
        print customer_email

        sg = sendgrid.SendGridClient(settings.SENDGRID_USER_NAME,settings.SENDGRID_PASSWORD)
        message = sendgrid.Mail()
        message.set_headers({'X-Sent-Using': 'SendGrid-API', 'X-Transport': 'web'})
        to_mail = []
        to_mail.append(customer_email)
        message.add_to(to_mail)
        #message.bcc = ['cs@dial-a-room.com','nilesh@dial-a-room.com']
        message.bcc = ['manoj@bynry.com']
        
        message.set_subject("Dial-A-Room : Mail Alerts for New Quotation")
        message_to_send = '<html><style>tr td { border-bottom : 1px solid #ddd; padding : 5px; border-left : 1px solid #ccc; }</style><body> \
        <br> Hi '+ str(first_name)+',<br>\
        You have received a new Quotation '+ quotation.quotation_uid +' against your request '+ str(request_obj.quote_request_uid)+ ' <br><br>'
        message_to_send +='<table style="border : 1px solid #ccc;" width=100%>\
        <tr><th>Name </th><th>Location </th> <th>Rate </th><th> No. Of Rooms</th> <th>Amount </th><th>Tax</th> <th>Total Amount</th></tr>'
        for quot in quotation_details:
          message_to_send+='<tr style="border : 1px solid #ddd;"><td>'+ str(quot.property_id.property_actual_name)+ '</td>\
           <td>'+ str(quot.property_id.property_location) + '</td>\
           <td>'+ str(quot.rate) + '</td>\
           <td>'+ str(request_obj.quote_no_of_room) + '</td>\
           <td>'+ str(quot.amount) + '</td>\
           <td>'+ str(quot.tax_amount) + '</td>\
           <td>'+ str(quot.total_quote_amt) +'</td></tr>'
        message_to_send +='</table>'
        # add a link to request details.
        message_to_send +='<br> <a href="'+ SERVER_URL +'" > Click Here </a> to see more details.'
        message_to_send +='</body></html>'
        message.set_html(message_to_send)
        message.set_text('Hello')
        message.set_from('Dial-A-Room Admin<cs@dial-a-room.com>')
        status, msg = sg.send(message)
        
        print status
        data = {'success': 'true'}
    except Exception, e:
        print e
        data = {'success': 'false'}
    return HttpResponse(json.dumps(data), content_type='application/json')

def quotation_details(request):
    print 'Hello'
    data = {}
    try:
        qr = QuoteRequest.objects.get(quote_request_uid=request.GET.get('quote_request_uid'))
        if qr.quote_customer_status == QuoteConstant.REQUEST_SUBMITTED:
            qr.quote_customer_status = QuoteConstant.REQUEST_VIEWED
            qr.save()
        quotation = QuotationResponse.objects.get(quotation_uid=request.GET.get('quotation_uid'))
        data = {'quote_request' : qr,'quotation': quotation,
         'facility_list' : [q for q in quotation.property_id.property_facility.split(',') if q]
          }
    except Exception as err:
        print 'Hello : ',err
        data = {}
    return render(request,'admin/quote-request/quotation.html',data)


def get_all_location(request):
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
    # data = []
    prop_list=[]
    filter_args={}
    try:
        if request.GET.get('location'):
            filter_args['property_location__icontains'] = request.GET.get('location')
            # filter_args['property_availability_status']=True

        #property_list = Property.objects.filter(Q(property_id__in = Property.objects.filter(**filter_args)))
        property_list = Property.objects.filter(**filter_args)
        print 'property_list'
        print property_list
        for property in property_list:
            try:
                rates = PropertyRate.objects.get(property_id=property)
                property_rate = rates.single_occupancy_display_rate
            except Exception as err:
                print 'ERR',err
            prop_list.append({ 'property_id': property.property_id,
                   'property_name': property.property_actual_name,
                   # 'property_address':property.property_location,
                    # 'property_desc' : property.property_description,
                    # 'property_rate': property_rate,
                    # 'property_rating' : property.star_category,
                    # 'airport_distance' : property.distance_from_airport,
                    # 'railway_stop_distance' : property.distance_from_railway_station,
                    # 'star': str(property.star_category*20) 
                    })
        data={'prop_list':prop_list,'success':'true'}
        # print datetime.datetime.now()
    except Exception as e:
        print 'Search Properties - Exception : ',e
    return HttpResponse(json.dumps(data), content_type='application/json') 


def get_properties_details(request):
    print "get_properties_details"
    print request.GET.get('property_id')
    prop_details={}
    try:
        property_obj = Property.objects.get(property_id=request.GET.get('property_id'))
        print "property_obj"
        print property_obj
        try:
            rates = PropertyRate.objects.get(property_id=property_obj)
            property_rate = rates.single_occupancy_display_rate
        except Exception as err:
            print 'ERR',err
        prop_details={ 'property_id': property_obj.property_id,
               'property_name': property_obj.property_actual_name,
               'property_address':property_obj.property_location,
                # 'property_desc' : property.property_description,
                'property_rate': property_rate,
                'rack_rate' : property_obj.rack_rate,
                # 'property_rating' : property.star_category,
                # 'airport_distance' : property.distance_from_airport,
                # 'railway_stop_distance' : property.distance_from_railway_station,
                # 'star': str(property.star_category*20) 
                }
        data= { 'prop_details':prop_details,'success':'true' }
    except Exception as e:
        print 'Search Properties - Exception : ',e
    return HttpResponse(json.dumps(data), content_type='application/json')
