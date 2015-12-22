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
import smtplib
from smtplib import SMTPException
import urllib
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
from smtplib import SMTPException
# imports date times
import datetime
import time
from datetime import date, timedelta

from django.http import HttpResponse
from django.http import HttpResponseRedirect
from CorpRoomApp.models import *
from CorpRoomApp.forms import *
from CorpRoomApp.constants import ExceptionMessages, ExceptionLabel


AVAILABLE          = 0
NOT_AVAILABLE      = 1
#SERVER_URL = "http://192.168.0.121:8000"
SERVER_URL = "http://dial-a-room.com"

ADMIN       = 0
CORPORATE   = 1
OWNER       = 2
RETAIL      = 3


def vendor_list_page(request):
    vendors = Customer.objects.filter(user_type=OWNER)
    vendor_list = [vendor.get_vendor_info() for vendor in vendors ]
    data = {'vendor_list' : vendor_list }
    return render(request, 'vendor-list.html', data)


def show_vendor_details(request):
    try:
        print 'Retrieving details of ', request.GET.get('vendor_id')
        vendor = Customer.objects.get(cust_unique_id=request.GET.get('vendor_id'))
        data = { 'success' : 1,  'uid' : vendor.cust_unique_id, 'fname' : vendor.cust_first_name, 'lname': vendor.cust_last_name  ,'email': vendor.cust_email,
        'contact_no' : vendor.cust_contact_no, 'city': vendor.cust_city , 'address': vendor.cust_address_line, 'age' : vendor.cust_age,
        'state': vendor.cust_state, 'country' : vendor.cust_country, 'gender' : vendor.cust_gender, 'pincode' : vendor.cust_pincode }
    except Exception as err:
        print 'Show Vendor Exception : ', err
        data = {'success' : 0, 'error_message': 'Error Occurred While Retrieving the Vendor Details'}
    return HttpResponse(json.dumps(data), content_type='application/json')


@csrf_exempt
def update_vendor_details(request):
    try:
        vendor = Customer.objects.get(cust_unique_id=request.POST.get('vendorIdToUpdate'))
        vendor.cust_first_name = request.POST.get('owner_first_name')
        vendor.cust_last_name = request.POST.get('owner_last_name')
        vendor.cust_email = request.POST.get('owner_email')
        vendor.cust_contact_no = request.POST.get('owner_contact')
        vendor.cust_city = request.POST.get('owner_city')
        vendor.cust_address_line = request.POST.get('owner_address')
        vendor.cust_state = request.POST.get('owner_state')
        vendor.cust_age = request.POST.get('owner_age')
        vendor.cust_country = request.POST.get('owner_country')
        vendor.cust_gender = request.POST.get('gender')
        vendor.cust_pincode = request.POST.get('owner_pincode')
        vendor.save()
        data = {'success' : 1 }
    except Exception as err:
        print 'In Update Vendor Section : ',err
        data = {'success' : 0 , 'error_message' : 'Unable to Update Vendor Details - Please Try Again' }
    return HttpResponse(json.dumps(data), content_type='application/json')


@csrf_exempt
def reset_vendor_password(request):
    try:
        vendor = Customer.objects.get(cust_unique_id=request.POST.get('vendorIdResetPassword'))
        vendor.username = request.POST.get('username')
        vendor.set_password(request.POST.get('owner_password'))
        vendor.save()
        send_user_id_creation_sms_to_owner(vendor.cust_contact_no, vendor.cust_first_name,vendor.username,request.POST.get('owner_password'))
        data = {'success' : 1 }
        return HttpResponse(json.dumps(data), content_type='application/json')
    except IntegrityError as err:
        data = {'success' : 0 , 'error_message' : 'Username is already exists, please take another ' }
        return HttpResponse(json.dumps(data), content_type='application/json')
    except Exception as err:
        print 'Exception ', err
        data = {'success' : 0 ,'error_message' : 'Server Error - Please Try again'}
        return HttpResponse(json.dumps(data), content_type='application/json')


# This method will send SMS to Property Owner
def send_user_id_creation_sms_to_owner(mobile_no, name, user_name, password):
    try:
        TEXT ="Hi "+ name 
        TEXT = TEXT + '\nYour Credentials to DIAL-A-ROOM are'
        TEXT = TEXT + '\nUser ID: '+ user_name
        TEXT = TEXT + '\nPassword: '+ password
        TEXT= TEXT + "\n Plz visit http://dial-a-room.com/vendor/"
        
        TEXT= TEXT + "\nNeed any Help Plz Contact: 8087700499"
        
        host = "http://173.45.76.226"
        user_name = "dialrm"
        user_password = "dialrm"
        recipient = "trans1"
        sender="DIALRM"
        number=mobile_no
        
        http_req = host
        http_req += ":81/send.aspx?username="
        http_req += urllib.quote(user_name)
        http_req += "&pass="
        http_req += urllib.quote(user_password)
        http_req += "&route="
        http_req += urllib.quote(recipient)
        http_req += "&senderid="
        http_req += urllib.quote(sender)
        http_req += "&numbers="
        http_req += urllib.quote(number)
        http_req += "&message="
        http_req += urllib.quote(TEXT)
        get = urllib.urlopen(http_req)
        req = get.read()
        s=req.split('\r')
        status=s[0].split('|')
        print "Status",status[0]
        get.close()
        
        if(status=='1'):
            data =  {'success': 'true', 'message': 'Message has been sent to the user'}
        else:
            data =  {'success': 'false', 'message': 'Message has not been sent to the user'}
    except SMTPException,e:
        print "failed to send mail", e
        data = {'success': 'false'}




