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
import operator
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

from CorpRoomApp.constants import ExceptionMessages, ExceptionLabel
from CorpRoomApp.views.web_portal import get_booking_details
from CorpRoomApp.send_sms import send_booking_submission_sms_to_customer
UNPAID = 0
PAID = 1

BOOKING_ALL         = 0
BOOKING_OPEN        = 1
BOOKING_BOOKED      = 2
BOOKING_CANCELLED   = 3
BOOKING_COMPLETED   = 4

OK = 'Ok'

@csrf_exempt
def save_payment_gateway_response(request):
    print "save_payment_details"
    try:
        print request.POST
        link=''
        if request.method == 'POST':
            print request.POST.get('mmp_txn')
            payment_obj = PaymentTransaction(
                mmp_txn                            =    request.POST.get('mmp_txn'),
                ipg_txn_id                         =    request.POST.get('ipg_txn_id'),
                transaction_type                   =    request.POST.get('transaction_type'),
                property_booking_id                =    request.POST.get('udf4'),
                discriminator                      =    request.POST.get('discriminator'),
                srcharge                           =    request.POST.get('surcharge'),
                customer_name                      =    request.POST.get('udf1'),
                mer_txn                            =    request.POST.get('mer_txn'),
                card_number                        =    request.POST.get('CardNumber'),
                ath_code                           =    request.POST.get('auth_code'),
                prod                               =    request.POST.get('prod'),
                bank_name                          =    request.POST.get('bank_name'),
                date                               =    request.POST.get('date'),
                merchant_id                        =    request.POST.get('merchant_id'),
                amount                             =    request.POST.get('amt'),
                error_description                  =    request.POST.get('desc'),
                bank_txn                           =    request.POST.get('bank_txn'),
                f_code                             =    request.POST.get('f_code'),
                clientcode                         =    request.POST.get('clientcode'),
                mobile_no                          =    request.POST.get('udf3'),
                email_id                           =    request.POST.get('udf2'),
                udf5                               =    request.POST.get('udf5'),
                billing_address                    =    request.POST.get('udf4'),
                udf6                               =    request.POST.get('udf6'),
                booking_transaction_create_by      =    request.POST.get('udf1'),
                booking_transaction_update_by      =    request.POST.get('udf1')
            )
            payment_obj.save()
            print "done"
                
            data = {
                'success': 'true',
                'cust_email':payment_obj.email_id,
                'error_message': payment_obj.error_description,
                'merchant_id':payment_obj.merchant_id,
                'mer_txn':payment_obj.mer_txn,
                'amt':payment_obj.amount,
                'date':payment_obj.date,
            }
            if payment_obj.f_code == OK :
                # booking_obj = Booking.objects.earliest('-booking_id')
#                booking_obj = Booking.objects.earliest('-booking_unique_id')
                booking_obj = Booking.objects.get(booking_unique_id=request.POST.get('udf4'))
                booking_obj.booking_status = BOOKING_OPEN
                booking_obj.payment_status = PAID
                booking_obj.save()
                send_booking_submission_sms_to_customer(booking_obj.guest_id.guest_contactno, booking_obj.booking_unique_id)
                data = { 'booking_reference_id': booking_obj.booking_unique_id , 'payment_status': booking_obj.payment_status }
                return render(request,'web/just-for-test.html', data)
#                return redirect('/booking-confirmation/?booking_number='+payment_obj.booking_unique_id+'&payment_status='+PAID)
            else:
                booking_obj = Booking.objects.get(booking_unique_id=request.POST.get('udf4'))
                booking_obj.booking_status = BOOKING_OPEN
                booking_obj.payment_status = UNPAID
                booking_obj.save()
                data = { 'booking_reference_id': booking_obj.booking_unique_id , 'payment_status': booking_obj.payment_status }
                return render(request,'web/just-for-test.html', data)
                #return redirect('/booking-confirmation/?booking_number='+ payment_obj.booking_unique_id+'&payment_status='+UNPAID)
    except Exception,e:
        print e
        data = {'error_message': 'Oops something went wrong...'}
        return render( request, 'web/error-page.html', data )
    # return HttpResponse(json.dumps(data), content_type='application/json')
    # return render(request, 'mobile-success.html', data )



