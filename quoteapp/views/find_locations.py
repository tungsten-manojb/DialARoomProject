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
from CorpRoomApp.send_sms import send_new_request_sms_to_property_owners
# from math import *
import math
import pdb

earth_radius = 6371.0  
degrees_to_radians = math.pi/180.0
radians_to_degrees = 180.0/math.pi

#SERVER_URL = 'http://192.168.0.121:8000'
SERVER_URL = 'http://dial-a-room.com'
VENDOR_REQUEST_URL = '/vendor/quote/request-details/?request_uid='


# @csrf_exempt
def nearby_properties(location, request_id):
#def nearby_poperties(request):
    print "in the find_locations "
    tpl1 = []

    locations = location.split('$')
    try:
        if len(locations)>1:
            property_obj = Property.objects.filter(property_location__in = locations)[0]
        else:
            property_obj = Property.objects.filter(property_location__icontains = ''.join(locations))[0]
        #property_obj = Property.objects.filter(property_location__icontains = location )[0]

        consumer_latitude=property_obj.longitude
        consumer_longitude=property_obj.latitude
        lon_max, lon_min, lat_max, lat_min = bounding_box(float(consumer_longitude),float(consumer_latitude),5) # Five KM Area
        print 'find_locations.py | nearby_locations | latitude - longitude ', lon_max, lon_min, lat_max, lat_min 

        properties=Property.objects.filter(latitude__range=[lat_min,lat_max], longitude__range=[lon_min,lon_max])

        quote_request=QuoteRequest.objects.get(quote_request_id=request_id)
        customer_list = []
        owner_numbers = []
        index = 0
        # Restrict to 5 Properties Only
        for prop in properties:
            if index == 5:
                break
            customer_list.append(prop.property_owner_id.cust_email)
            owner_numbers.append(prop.property_owner_id.cust_contact_no)
            requested_property_obj=RequestedProperty(
                property_id = prop,
                quote_request_id=quote_request,
                created_date=datetime.datetime.now(),
                created_by='admin',
                property_owner_id =  prop.property_owner_id
            )
            requested_property_obj.save()
            index = index + 1
            # Send SMS to respected owner
            send_new_request_sms_to_property_owners(prop.property_owner_id.cust_first_name,prop.property_owner_id.cust_contact_no, prop.property_actual_name,quote_request.quote_request_uid, quote_request.quote_start_date,quote_request.quote_end_date )
            # Send email to respected owners
            send_email_property_owner(quote_request,prop.property_owner_id.cust_email, prop.property_owner_id.cust_first_name,  prop.property_actual_name )
        data = {'success':'true'}
    except MySQLdb.OperationalError, e:
        print 'find_locations.py | nearby_locations | Exception : ', e
        data = {'success': 'false', 'BranchList': 'none', 'error_message':'Customer list Fail'}
    return data
#    return HttpResponse(json.dumps(data), content_type='application/json')

#functions to calculate min-max lat-long range

def change_in_latitude(distance):
    "Given a distance north, return the change in latitude."
    return (distance/earth_radius)*radians_to_degrees

def change_in_longitude(latitude, distance):
    "Given a latitude and a distance west, return the change in longitude."
    # Find the radius of a circle around the earth at given latitude.
    r = earth_radius*math.cos(latitude*degrees_to_radians)
    return (distance/r)*radians_to_degrees

def bounding_box(latitude, longitude, distance):
    print "bounding_box"
    lat_change = change_in_latitude(distance)
    lat_max = latitude + lat_change
    lat_min = latitude - lat_change
    lon_change = change_in_longitude(latitude, distance)
    lon_max = longitude + lon_change
    lon_min = longitude - lon_change
    print "in the end"
    return (lon_max, lon_min, lat_max, lat_min)


def send_email_property_owner(quote_request,customer_list, owner_name, property_name):
    print "in the send email"
    try:
        print "quote_request"
        table=''
        sg = sendgrid.SendGridClient(settings.SENDGRID_USER_NAME,settings.SENDGRID_PASSWORD)
        message = sendgrid.Mail()
        message.set_headers({'X-Sent-Using': 'SendGrid-API', 'X-Transport': 'web'})
        to_mail = ['manoj.bawane@tungstenbigdata.com', 'vikas@dial-a-room.com']
        #to_mail = ['cs@dial-a-room.com', 'nilesh@dial-a-room.com','prashant@dial-a-room.com']
        #to_mail.append(customer_list)
        message.add_to(customer_list)
        message.bcc=to_mail

        message.set_subject("Dial-A-Room : Received New Request for Quotation")
        message_to_send = 'Hi '+ owner_name +',<br>\
        You have received a new request for your property : '+ property_name +'<br><br>'
        message_to_send+='<p> Request For '+ str(quote_request.quote_category)+ '</p>\
            <p>Type       :'+ str(quote_request.quote_sub_category)+ '</p>\
            <p>Location   :'+ ' | '.join(quote_request.quote_location.split('$'))+ ','+ str(quote_request.quote_city)+'</p>\
            <p>Price Range:'+ str(quote_request.quote_lowest_price)+' to  '+ str(quote_request.quote_highest_price) +' </p>\
            <p>Date From:'+ str(quote_request.quote_start_date)+' to  '+ str(quote_request.quote_end_date) +' </p>\
            <p>No of Guest:'+ str(quote_request.quote_no_of_guest) + '<br>No of Rooms :'+ str(quote_request.quote_no_of_room) +'</p>\
            <p>Please <a href="'+ SERVER_URL + VENDOR_REQUEST_URL + quote_request.quote_request_uid +'"> Click Here'+ '</a> to view the detailed request details and respond quotation.<br>\
            <br><br><br><br>From <br> Dial-A-Room Team'
        message.set_html(message_to_send)
        message.set_text('Property Request Details')
        message.set_from('Dial-A-Room Admin<admin@dial-a-room.com>')
        status, msg = sg.send(message)
        print status
        data = {'success': 'true'}
    except Exception, e:
        print e
        data = {'success': 'false'}
    return HttpResponse(json.dumps(data), content_type='application/json')
