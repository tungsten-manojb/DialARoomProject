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

# this is for constants the 
from constants import ExceptionMessages, ExceptionLabel
from CorpRoomApp.models import *
from datetime import date

from CorpRoomApp.send_mail import  *

SERVER_MEDIA_URL = 'http://192.168.0.121:8000'

#SERVER_MEDIA_URL = 'http://ec2-52-4-20-173.compute-1.amazonaws.com'

# Booking Constants
BOOKING_ALL         = 0
BOOKING_BOOKED      = 1
BOOKING_COMPLETED   = 2
BOOKING_OPEN        = 4

GUEST_ACTIVE    = 1
GUEST_INACTIVE  = 0

AVAILABLE_ROOM  = 0


# The POST request will be shown, This service is for cam login
@csrf_exempt
def cam_login(request):
    #print request.POST
    #pdb.set_trace()
    try:
        if request.method == 'POST':
            json_obj= json.loads(request.body)
            print 'JSON OBJECT : ',json_obj
            user = authenticate(username=json_obj['username'], password= json_obj['password'])
            if user is not None:
                if user.is_active:
                    data= {'success' : 'true', ExceptionLabel.ERROR_MESSAGE:'Successfully Login', 'user_info' : get_cam_profile_info(user.id) }
                    print data
                else:
                    data= {'success' : 'false', ExceptionLabel.ERROR_MESSAGE:'User Is Not Active'}
            else:
                data= {'success' : 'false', ExceptionLabel.ERROR_MESSAGE:'Invalid Username or Password'}
        else:
            data= {'success' : 'false', ExceptionLabel.ERROR_MESSAGE:'Invalid Request'}
    except User.DoesNotExist:
        print 'usr'
        data= {'success' : 'false', ExceptionLabel.ERROR_MESSAGE:'User Not Exist'}
    except MySQLdb.OperationalError, e:
        print e
        data= {'success' : 'false', ExceptionLabel.ERROR_MESSAGE:'Internal Server Error '}
    except Exception, e:
        print e
        data= {'success' : 'false', ExceptionLabel.ERROR_MESSAGE:'Internal Server Error '}
    return HttpResponse(json.dumps(data), content_type='application/json')

# this method returns all the KPI's details of Dashboard
def get_dashboard_kpis(request):
    try:
        cam_id = int(request.GET.get('cam_user_id'))
        cam_object = CAM.objects.get(user_ptr_id=cam_id)
        total_days = cam_object.cam.aggregate(total=Sum('cam_booking_actual_no_of_day_stay'))
        cam_total_days = total_days['total']

        this_month_days = 0
        this_month_amount = 0
        sum =0
        amount_fy   = 0
        days_fy     = 0
        this_month  = datetime.datetime.today().month
        this_year   = datetime.datetime.today().year
        
        if month <= 3:
            str_start_date  = '01-04-' + str((datetime.datetime.today().year - 1))
            str_end_date    = '31-03-' + str((datetime.datetime.today().year))
        else:
            str_start_date  = '01-04-' + str((datetime.datetime.today().year))
            str_end_date    = '31-03-' + str((datetime.datetime.today().year+1))
        
        start_date  = datetime.datetime.strptime(str_start_date, '%d-%m-%Y')
        end_date    = datetime.datetime.strptime(str_end_date, '%d-%m-%Y')
        
        cbs = cam_object.cam.all() 
        for cb in cbs:
            invoice= cb.cam_bookings.all()[0]
            sum=sum+ invoice.invoice_gross_amount
            
            if invoice.invoice_datetime.month == this_month:
                this_month_days = this_month_days + cb.cam_booking_actual_no_of_day_stay
                this_month_amount = this_month_amount + invoice.invoice_gross_amount
            
            temp_date = date(invoice.invoice_datetime.year, invoice.invoice_datetime.month, invoice.invoice_datetime.day)
            
            if s_date < temp_date < e_date:
                days_fy     = days_fy + cb.cam_booking_actual_no_of_day_stay
                amount_fy   = amount_fy + invoice.invoice_gross_amount
                
        # this is for getting the no.of day for this month and amounts
        data = {'success':'true','total_days' : cam_total_days, 'total_amount': '{:,.2f}'.format(sum), 'month_days': this_month_days, 'month_amount': '{:,.2f}'.format(this_month_amount), 'days_fy': days_fy, 'amount_fy': '{:,.2f}'.format(amount_fy) }
    except User.DoesNotExist, e:
        print e
        data = {'success':'true','total_days' : cam_total_days, 'total_amount': '{:,.2f}'.format(sum), 'month_days': this_month_days, 'month_amount': '{:,.2f}'.format(this_month_amount), 'days_fy': days_fy, 'amount_fy': '{:,.2f}'.format(amount_fy) }
    except Exception, e :
        print e
        data = {'total_days': '0','total_amount': '0'}
    return HttpResponse(json.dumps(data), content_type='application/json')

# This added on 26-05-2015
# This is for getting dashboard days
def get_dashboard_days(request):
    #pdb.set_trace()
    try:
        cam_id = int(request.GET.get('cam_user_id'))
        cam_object = CAM.objects.get(user_ptr_id=cam_id)
        total_days = cam_object.cam.aggregate(total=Sum('cam_booking_actual_no_of_day_stay'))
        cam_total_days = total_days['total']
        
        this_month_days     = 0
        this_month_amount   = 0
        sum = 0.00
        amount_fy   = 0
        days_fy     = 0
        this_month  = datetime.datetime.today().month
        this_year   = datetime.datetime.today().year
        
        if this_month <= 3:
            str_start_date  = '01-04-' + str((datetime.datetime.today().year - 1))
            str_end_date    = '31-03-' + str((datetime.datetime.today().year))
        else:
            str_start_date  = '01-04-' + str((datetime.datetime.today().year))
            str_end_date    = '31-03-' + str((datetime.datetime.today().year + 1))
        
        start_date  = datetime.datetime.strptime(str_start_date, '%d-%m-%Y')
        end_date    = datetime.datetime.strptime(str_end_date, '%d-%m-%Y')
        
        s_date = date(start_date.year, start_date.month, start_date.day)
        e_date = date(end_date.year, end_date.month, end_date.day)
        
        print s_date
        print e_date
        
        cbs = cam_object.cam.all()
        try:
            for cb in cbs:
                invoice = cb.cam_bookings.all()[0]
                sum = sum + invoice.invoice_gross_amount
                
                if invoice.invoice_datetime.month == this_month:
                    this_month_days = this_month_days + cb.cam_booking_actual_no_of_day_stay
    #                this_month_amount = this_month_amount + invoice.invoice_gross_amount
                
                temp_date = date(invoice.invoice_datetime.year, invoice.invoice_datetime.month, invoice.invoice_datetime.day)
                
                if s_date < temp_date < e_date:
                    days_fy     = days_fy + cb.cam_booking_actual_no_of_day_stay
    #                amount_fy   = amount_fy + invoice.invoice_gross_amount
        except IndexError, e:
            print e
        # this is for getting the no.of day for this month and amounts
        data = {'success':'true','total_days' : str(cam_total_days), 'month_days': str(this_month_days), 'days_fy': str(days_fy) }
        print data
    except User.DoesNotExist, e:
        print e
        data = {'success':'false','total_days' : '0', 'month_days': '0', 'days_fy': '0'}
    except Exception, e :
        print e
        data = {'success':'false','total_days' : '0', 'month_days': '0', 'days_fy': '0'}
    return HttpResponse(json.dumps(data), content_type='application/json')

# This added on 26-05-2015
# This is for getting dashboard amounts
def get_dashboard_amounts(request):
    try:
        cam_id = int(request.GET.get('cam_user_id'))
        cam_object = CAM.objects.get(user_ptr_id=cam_id)
        total_days = cam_object.cam.aggregate(total=Sum('cam_booking_actual_no_of_day_stay'))
        cam_total_days = total_days['total']

        this_month_days = 0
        this_month_amount = 0
        sum = 0.00
        amount_fy   = 0
        days_fy     = 0
        this_month  = datetime.datetime.today().month
        this_year   = datetime.datetime.today().year
        
        if this_month <= 3:
            str_start_date  = '01-04-' + str((datetime.datetime.today().year - 1))
            str_end_date    = '31-03-' + str((datetime.datetime.today().year))
        else:
            str_start_date  = '01-04-' + str((datetime.datetime.today().year))
            str_end_date    = '31-03-' + str((datetime.datetime.today().year + 1))
        
        start_date  = datetime.datetime.strptime(str_start_date, '%d-%m-%Y')
        print 'Start Date : ',start_date
        end_date    = datetime.datetime.strptime(str_end_date, '%d-%m-%Y')
        print 'End Date : ',end_date
        
        s_date = date(start_date.year, start_date.month, start_date.day)
        e_date = date(end_date.year, end_date.month, end_date.day)
        
        cbs = cam_object.cam.all()
        try:
            for cb in cbs:
                invoice = cb.cam_bookings.all()[0]
                sum=sum + invoice.invoice_gross_amount
                
                if invoice.invoice_datetime.month == this_month:
    #                this_month_days = this_month_days + cb.cam_booking_actual_no_of_day_stay
                    this_month_amount = this_month_amount + invoice.invoice_gross_amount
                
                temp_date = date(invoice.invoice_datetime.year, invoice.invoice_datetime.month, invoice.invoice_datetime.day)
                
                if s_date < temp_date < e_date:
    #                days_fy     = days_fy + cb.cam_booking_actual_no_of_day_stay
                    amount_fy   = amount_fy + invoice.invoice_gross_amount
        except IndexError, e:
            print e
            print 'error'
        # this is for getting the no.of day for this month and amounts
        data = {'success':'true', 'total_amount': '{:,.2f}'.format(sum), 'month_amount': '{:,.2f}'.format(this_month_amount), 'amount_fy': '{:,.2f}'.format(amount_fy) }
        print data
    except User.DoesNotExist, e:
        print e
        data = {'success':'false', 'total_amount': '0', 'month_amount': '0', 'amount_fy': '0'}
    except Exception, e :
        print e
        data = {'success':'false', 'total_amount': '0', 'month_amount': '0', 'amount_fy': '0'}
    return HttpResponse(json.dumps(data), content_type='application/json')



# GET Request for getting all the booking details.
def get_all_booking_of_cam(request):
    try:
        cam_id = int(request.GET.get('cam_user_id'))
        print 'Hellow ',cam_id
        cam_object = CAM.objects.get(user_ptr_id=cam_id)
        #objects = []
        #    # This will fetch all the booking of cam user
        objects = cam_object.cam.all()
        
        #print '----> ',objects
        booking_list=[]
        #print objects
        
        for obj in objects:
            
            temp = {
                'cam_booking_id'    : obj.cam_booking_id,
                'check_in_date'     : obj.cam_booking_estimated_checkin_date.strftime('%a, %d %b'),
                'check_out_date'    : obj.cam_booking_estimated_checkout_date.strftime('%a, %d %b'),
                'guest_name'        : obj.guest_id.guest_first_name,
                'number_of_roooms'  : obj.aptroom_id.apt_room_number,
                'apartment_name'    : obj.apartment.apt_name
            }
            #print temp
            booking_list.append(temp)
        data = { 'data': booking_list }
        
    except CAM.DoesNotExist:
        data = {'data': None, ExceptionLabel.ERROR_MESSAGE:'The User is not Exist'}
    except Exception, e:
        print e
        data = {'data': None, ExceptionLabel.ERROR_MESSAGE:'Server Error - Please Try Again'}
    return HttpResponse(json.dumps(data), content_type='application/json')

# this method will return the current bookings of CAM user
def get_current_booking_of_cam(request):
    #
    try:
        cam_id = request.GET.get('cam_user_id')
        cam_object = CAM.objects.get(user_ptr_id=cam_id)
        #objects = []
        #    # This will fetch all the booking of cam user

        objects = cam_object.cam.filter(cam_booking_status=BOOKING_BOOKED, cam_booking_estimated_checkin_date= datetime.datetime.today() )

        print objects
        booking_list=[]

        for obj in objects:
            temp = {
                'cam_booking_id'    : obj.cam_booking_id,
                'check_in_date'     : obj.cam_booking_estimated_checkin_date.strftime('%a, %d %b'),
                'check_out_date'    : obj.cam_booking_estimated_checkout_date.strftime('%a, %d %b'),
                'guest_name'        : obj.guest_id.guest_first_name,
                'number_of_roooms'  : obj.aptroom_id.apt_room_number,
                'apartment_name'    : obj.apartment.apt_name
            }
            booking_list.append(temp)

        data = { 'data': booking_list }
        print data
    except CAM.DoesNotExist:
        data = {'data': None, ExceptionLabel.ERROR_MESSAGE:'The User is not Exist'}
    except Exception, e:
        print e
        data = {'data': None, ExceptionLabel.ERROR_MESSAGE:'Server Error - Please Try Again'}
    return HttpResponse(json.dumps(data), content_type='application/json')


# this service returns all upcoming bookings
def get_upcoming_booking_of_cam(request):
    try:
        cam_id = request.GET.get('cam_user_id')
        cam_object = CAM.objects.get(user_ptr_id=cam_id)
        #objects = []
        #    # This will fetch all the booking of cam user

        objects = cam_object.cam.filter(cam_booking_status=BOOKING_BOOKED)
        
            
        print objects
        booking_list=[]
        
        for obj in objects:
            temp = {
                'cam_booking_id'    : obj.cam_booking_id,
                'check_in_date'     : obj.cam_booking_estimated_checkin_date.strftime('%a, %d %b'),
                'check_out_date'    : obj.cam_booking_estimated_checkout_date.strftime('%a, %d %b'),
                'guest_name'        : obj.guest_id.guest_first_name,
                'number_of_roooms'  : obj.aptroom_id.apt_room_number,
                'apartment_name'    : obj.apartment.apt_name
            }
            
            booking_list.append(temp)
        data = { 'data': booking_list }
        print data
    except CAM.DoesNotExist:
        data = {'data': None, ExceptionLabel.ERROR_MESSAGE:'The User is not Exist'}
    except Exception, e:
        print e
        data = {'data': None, ExceptionLabel.ERROR_MESSAGE:'Server Error - Please Try Again'}
    return HttpResponse(json.dumps(data), content_type='application/json')


# this will return all completed bookings
def get_completed_booking_of_cam(request):
    try:
        cam_id = request.GET.get('cam_user_id')
        cam_object = CAM.objects.get(id=cam_id)
        
        objects = cam_object.cam.filter(cam_booking_status=BOOKING_COMPLETED)
            
        print objects
        booking_list=[]
        
        for obj in objects:
            temp = {
                'cam_booking_id'    : obj.cam_booking_id,
                'check_in_date'     : obj.cam_booking_estimated_checkin_date.strftime('%a, %d %b'),
                'check_out_date'    : obj.cam_booking_estimated_checkout_date.strftime('%a, %d %b'),
                'guest_name'        : obj.guest_id.guest_first_name,
                'number_of_roooms'  : obj.aptroom_id.apt_room_number,
                'apartment_name'    : obj.apartment.apt_name
            }
            
            booking_list.append(temp)
        data = { 'data': booking_list }
        print data
    except CAM.DoesNotExist:
        data = {'data': None, ExceptionLabel.ERROR_MESSAGE:'The User is not Exist'}
    except Exception, e:
        print e
        data = {'data': None, ExceptionLabel.ERROR_MESSAGE:'Server Error - Please Try Again'}
    return HttpResponse(json.dumps(data), content_type='application/json')


# this method will return specific booking details of cam
# This will returns 
# guest_name, booking_id, address, no of rooms, check in , check out, Total Bill, room image
def get_booking_details(request):
    
    try:
        var_cam_id = request.GET.get('cam_user_id')
        booking_id = request.GET.get('cam_booking_id')
        cam_booking_obj = CAMBooking.objects.get(cam_booking_id=booking_id, cam_id = var_cam_id)
        #cam_booking_obj.guest_id.all()
        total_invoice = 0.00
        paid_bill = ''
        if cam_booking_obj.cam_booking_status == BOOKING_COMPLETED :
            try:
                invoice = cam_booking_obj.cam_bookings.all()[0]
                total_amount = invoice.invoice_gross_amount
            except Exception, e:
                print 'NO Invoice found for Booking ID : ', booking_id
                
        data = {
            'cam_booking_id'    : str(cam_booking_obj.cam_booking_id),
            'apartment_name'    : cam_booking_obj.apartment.apt_name,
            'apartment_address' : cam_booking_obj.apartment.get_apartment_address(),
            'booked_rooms'      : cam_booking_obj.aptroom_id.apt_room_number,
            'room_image'        : SERVER_MEDIA_URL + cam_booking_obj.aptroom_id.apt_room_images1.url,
            'check_in_time'     : cam_booking_obj.cam_booking_estimated_checkin_time.strftime('%I:%M %p'),
            'check_out_time'    : cam_booking_obj.cam_booking_estimated_checkout_time.strftime('%I:%M %p'),
            'check_in_date'     : cam_booking_obj.cam_booking_estimated_checkin_date.strftime('%a, %d %b, %Y'),
            'check_out_date'    : cam_booking_obj.cam_booking_estimated_checkout_date.strftime('%a, %d %b, %Y'),
            'total_bill'        : '{:,.2f}'.format(total_invoice),
            'total_paid'        : '{:,.2f}'.format(total_invoice),
            'booking_status'    : cam_booking_obj.cam_booking_status,
            'room_type'         : cam_booking_obj.aptroom_id.room_type,
            'favourite_status'  : cam_booking_obj.cam_booking_favourite,
            'number_of_days'    : str(cam_booking_obj.cam_booking_actual_no_of_day_stay),
            'guest_name'        : cam_booking_obj.guest_id.guest_first_name #+ ' ' + cam_booking_obj.guest_id.guest_last_name,
        }
    except CAM.DoesNotExist,e:
        print 'exception ',e
        data = {'data': '', ExceptionLabel.ERROR_MESSAGE:'The User is not Exist'}
    except Exception,e:
        print 'Big Exception',e
        data = {'data': '', ExceptionLabel.ERROR_MESSAGE:'Server Error - Please Try Again'}
    return HttpResponse(json.dumps(data), content_type='application/json')


# save the booking info generated from mobile.
@csrf_exempt
@transaction.atomic
def save_booking_info(request):
    #
    try:
        print 'Request Accepted '
        #   print request
        sid = transaction.savepoint()
        if request.method == "POST":
            json_obj=json.loads(request.body)
            print 'JSON OBJECT : ',json_obj
            v_cam_id      = json_obj['user_id']
            guest_name  = json_obj['guest_name']
            guest_phone = json_obj['phone_number']
            v_guest_email = json_obj['email_id']
            room_id     = json_obj['room_id']
            check_in    = datetime.datetime.strptime(json_obj['check_in'], '%d/%m/%Y')
            check_out   = datetime.datetime.strptime(json_obj['check_out'], '%d/%m/%Y')
            promocode   = json_obj['promocode']
            amount      = json_obj['amount']
            taxes       = json_obj['taxes']
            gross_amount= json_obj['gross_amount']
            
            guest_obj = Guest(
                guest_first_name    = guest_name,
                guest_contactno     = guest_phone,
                guest_email         = v_guest_email,
                guest_status        = GUEST_ACTIVE,
                )
            guest_obj.save()
            
            room_obj = ApartmentRoom.objects.get(apt_room_id=room_id)
            
            booking_obj = CAMBooking(
                cam_id      = CAM.objects.get(id=v_cam_id),
                guest_id    = guest_obj,
                apartment   = room_obj.apartment_id,
                aptroom_id  = room_obj,
                cam_booking_estimated_checkin_date = check_in,
                cam_booking_estimated_checkout_date = check_out,
                cam_booking_estimated_checkout_time = datetime.datetime.now().time(),
                cam_booking_estimated_checkin_time = datetime.datetime.now().time(),
                cam_booking_status  = BOOKING_OPEN
                )
            booking_obj.save()
            room_obj.apt_room_status = BOOKING_BOOKED
            room_obj.save()
            
            transaction.savepoint_commit(sid)
            data = {'success':'true'}
        else:
            print 'Hello'
            transaction.savepoint_rollback(sid)
            data = {'success':'false', 'error_message':'Invalid Request'}
    except Exception, e:
        transaction.savepoint_rollback(sid)
        print 'Error ', e
        data = {'success':'false', 'error_message':'Server Error- Please Try Again'}
    return HttpResponse(json.dumps(data), content_type='application/json')


# this method returns complete profile information
def get_cam_profile_info(cam_id):
    #try#:
        #
    print cam_id
        
        #cam_id = request.GET.get('cam_user_id')
    cam_object = CAM.objects.get(id=cam_id)
    if cam_object.cam_image:
        image = SERVER_MEDIA_URL + cam_object.cam_image.url
    else:
        image = ''
    data = {
        'basic': {
            'user_id'    : str(cam_object.id),
            'first_name' : cam_object.cam_first_name,
            'last_name'  : cam_object.cam_last_name,
            'address_line' : cam_object.cam_address_line,
            'city'       : cam_object.cam_city,
            'state'      : cam_object.cam_state,
            'country'    : cam_object.cam_country,
            'gender'     : cam_object.cam_gender,
            'age'        : cam_object.cam_age,
            'image'      : image,
            },
        'contacts': {
            'email_id'   : cam_object.cam_email,
            'contact_number': cam_object.cam_contactno
        },
        'company': {
            'name'      : cam_object.cam_company_id.cam_company_name,
            'address'   : cam_object.cam_company_id.get_address(),
            'contact_number' : cam_object.cam_company_id.cam_company_contactno,
            'email_id'  : cam_object.cam_company_id.cam_company_email,
        },
        'setting': {
            'email_alert' : str(cam_object.cam_isemailalert_on),
            'sms_alert'   : str(cam_object.cam_issmsalert_on)
        }
    }
##    except CAM.DoesNotExist:
##        data = {'data': None, ExceptionLabel.ERROR_MESSAGE:'The User is not Exist' }
##    except Exception,e:
##        data = {'data': None, ExceptionLabel.ERROR_MESSAGE:'Server Error - Please Try Again' }
    return data #HttpResponse(json.dumps(data), content_type='application/json')


'''
-------------------------------------------------------------------------------
The following API's are related with the CAM User Profile information
-------------------------------------------------------------------------------
'''

#This method is update the CAM User Profile.
@csrf_exempt
def update_user_basic_profile(request):
    print 'hello'
    #
    #print request
    try:
        if request.method == 'POST':
            #json_obj=json.loads(request.body)
            cam_object = CAM.objects.get(id=request.POST.get('user_id'))
            cam_object.cam_first_name = request.POST.get('first_name')
            cam_object.cam_last_name = request.POST.get('last_name')
            cam_object.first_name = request.POST.get('first_name')  # This is for User table
            cam_object.last_name = request.POST.get('last_name')    # This is for User table
            cam_object.cam_address_line = request.POST.get('address_line')
            cam_object.cam_city = request.POST.get('city')
            cam_object.cam_state = request.POST.get('state')
            cam_object.cam_age = request.POST.get('age')
            cam_object.cam_country = request.POST.get('country')
            cam_object.save()
            data = {'success':'true'}
        else:
            data = {'success':'false'}
    except CAM.DoesNotExist, e:
        print e
        data = {'success':'false', 'error_message':'Invalid Request'}
    except Exception, e:
        print e
        data = {'success':'false', 'error_message': 'Server Internal Error'}
    return HttpResponse(json.dumps(data), content_type='application/json')

# This web service used for update the CAM company details.
# This service we are not providing currently to CAM User.
# CAM can not edit the company details.
@csrf_exempt
def update_cam_company_details(request):
    try:
        if request.method == 'POST':
            #json_obj=json.loads(request.body)
            cam_object = CAM.objects.get(id=request.POST.get('user_id'))
            company     = cam_object.cam_company_id
            company.cam_company_name        = request.POST.get('company_name')
            company.cam_company_contactno   = request.POST.get('company_contactno')
            company.cam_company_email       = request.POST.get('company_email')
            company.cam_company_address     = request.POST.get('company_address')
            company.cam_company_city        = request.POST.get('company_city')
            company.cam_company_state       = request.POST.get('company_state')
            company.cam_company_country     = request.POST.get('company_country')
            company.cam_company_pincode     = request.POST.get('company_pincode')
            company.save()
            data = {'success':'true'}
        else:
            data = {'success':'false'}
    except CAM.DoesNotExist, e:
        print e
        data = {'success':'false', 'error_message':'Invalid Request'}
    except Exception, e:
        print e
        data = {'success':'false', 'error_message': 'Server Internal Error'}
    return HttpResponse(json.dumps(data), content_type='application/json')

@csrf_exempt
def update_cam_settings_details(request):
    #
    try:
        if request.method == 'POST':
            #json_obj=json.loads(request.body)
            cam_object = CAM.objects.get(id=request.POST.get('user_id'))
            cam_object.cam_isemailalert_on  = request.POST.get('email_alert')
            cam_object.cam_issmsalert_on    = request.POST.get('sms_alert')
            cam_object.save()
            data = {'success':'true'}
        else:
            data = {'success':'false'}
    except CAM.DoesNotExist, e:
        print e
        data = {'success':'false', 'error_message':'Invalid Request'}
    except Exception, e:
        print e
        data = {'success':'false', 'error_message': 'Server Internal Error'}
    return HttpResponse(json.dumps(data), content_type='application/json')
            

@csrf_exempt
def update_cam_contact_details(request):
    try:
        if request.method == 'POST':
            #json_obj    =json.loads(request.body)
            cam_object = CAM.objects.get(id=request.POST.get('user_id'))
            cam_object.cam_email        = request.POST.get('email_id')
            cam_object.email            = request.POST.get('email_id')
            cam_object.cam_contactno    = request.POST.get('contact_number')
            cam_object.save()
            data = {'success':'true'}
        else:
            data = {'success':'false'}
    except CAM.DoesNotExist, e:
        print e
        data = {'success':'false', 'error_message':'Invalid Request'}
    except Exception, e:
        print e
        data = {'success':'false', 'error_message': 'Server Internal Error'}
    return HttpResponse(json.dumps(data), content_type='application/json')


@csrf_exempt
@transaction.atomic
def update_cam_profile_pic(request):
    #
    try:
        data={}
        #
        sid = transaction.savepoint()
        if request.method == 'POST':
            cam_object    = CAM.objects.get(id=request.POST.get('user_id'))
            cam_object.cam_image = request.FILES['filename']
            cam_object.save()
            print "SUCCESS"
            data = { 'success' : 'true', 'image': SERVER_MEDIA_URL + cam_object.cam_image.url }
        else:
            data = {'success': 'false', 'error_message' : 'Failed To Update the profile pic on server'}
    except MySQLdb.OperationalError, e:
        transaction.savepoint_rollback(sid)
        data = {'success': 'false', 'error_message' : 'Failed To Update the profile pic on server'}
    except Exception, e:
        transaction.savepoint_rollback(sid)
        print e
        data = {'success': 'false', 'error_message' : 'Failed To Update the profile pic on server'}
    return HttpResponse(json.dumps(data), content_type='application/json')


@transaction.atomic
def delete_cam_profile_pic(request):
    try:
        data={}
        sid = transaction.savepoint()
        cam_object    = CAM.objects.get(id=request.GET.get('cam_user_id'))
        cam_object.cam_image = None
        cam_object.save()
        print "SUCCESS"
        data = { 'success' : 'true'}
    except MySQLdb.OperationalError, e:
        transaction.savepoint_rollback(sid)
        data = {'success': 'false', 'error_message' : 'Failed To Update the profile pic on server'}
    except Exception, e:
        transaction.savepoint_rollback(sid)
        print e
        data = {'success': 'false', 'error_message' : 'Failed To Update the profile pic on server'}
    return HttpResponse(json.dumps(data), content_type='application/json')


# this service updates the cam booking for favourite
def update_favourite_room(request):
    #
    print 'hello'
    try:
        booking_id = request.GET.get('cam_booking_id')
        status = request.GET.get('status')
        cam_booking_obj = CAMBooking.objects.get(cam_booking_id=booking_id)
        cam_booking_obj.cam_booking_favourite = status
        cam_booking_obj.save()
        data = { 'success' : 'true'}
    except Expetion, e:
        data = { 'success' : 'false'}
    return HttpResponse(json.dumps(data), content_type='application/json')

'''
-------------------------------------------------------------------------------

-------------------------------------------------------------------------------
'''
# This is used for generate the bills 
def generate_invoice(request):
    try:
        var_cam_id = request.GET.get('cam_user_id')
        booking_id = request.GET.get('cam_booking_id')
        cam_booking_obj = CAMBooking.objects.get(cam_booking_id=booking_id, cam_id = var_cam_id )
        # calculations for generate bills
        
        estimate_days = cam_booking_obj.cam_booking_estimated_no_of_day_stay
        room_rate = cam_booking_obj.aptroom_id.apt_room_rate
        total_invoice = estimated_days * room_rate
        
    except CAM.DoesNotExist,e:
        print 'exception ',e
        data = {'data': '', ExceptionLabel.ERROR_MESSAGE:'The User is not Exist'}
    except Exception,e:
        print 'Big Exception',e
        data = {'data': '', ExceptionLabel.ERROR_MESSAGE:'Server Error - Please Try Again'}
    return HttpResponse(json.dumps(data), content_type='application/json')

# this method will update the password from app.
@csrf_exempt
def change_password_from_app(request):
    try:
##        if request.method == 'POST':
        data ={}
        json_obj=json.loads(request.body)
        user_obj = User.objects.get(id=request.GET.get('cam_user_id'))
        user = authenticate(username=user_obj.username, password= request.GET.get('old_password'))
        if user is not None:
            if user.is_active:
                user.set_password(request.GET.get('new_password'))
                user.save()
                print 'succeess'
                data= {'success' : 'true', ExceptionLabel.ERROR_MESSAGE:'Successfully Login'}
            else:
                data= {'success' : 'false', ExceptionLabel.ERROR_MESSAGE:'User Is Not Active'}
        else:
            data= {'success' : 'false', ExceptionLabel.ERROR_MESSAGE:'Invalid Username or Password'}
##        else:
##            data= {'success' : 'false', ExceptionLabel.ERROR_MESSAGE:'Invalid Request'}
    except User.DoesNotExist:
        print 'usr'
        data= {'success' : 'false', ExceptionLabel.ERROR_MESSAGE:'User Not Exit'}
    except MySQLdb.OperationalError, e:
        print e
        data= {'success' : 'false', ExceptionLabel.ERROR_MESSAGE:'Internal Server Error '}
    except Exception, e:
        print e
        data= {'success' : 'false', ExceptionLabel.ERROR_MESSAGE:'Internal Server Error '}
    return HttpResponse(json.dumps(data), content_type='application/json')
    

'''
-------------------------------------------------------------------------------
    These API's are related with Apartments for mobile
-------------------------------------------------------------------------------
'''


def get_available_apartment_rooms(request):
    filter_args={}
    try:
        print 'Hello'
        if request.GET.get('city_name'):
            filter_args['apt_city__icontains']=request.GET.get('city_name')
        room_list = ApartmentRoom.objects.filter(Q(apt_room_status=AVAILABLE_ROOM) & Q (apartment_id = Apartment.objects.filter(**filter_args)))
        data = {'success':'true','data': [room.get_apartment_room_details() for room in room_list]}
    except Exception, e:
        print 'Exception ',e
        data = { 'success':'false', 'error_message': 'Server Error - Unable to Process request' }
    return HttpResponse(json.dumps(data), content_type='application/json')

# This API return specific room and apartment details.
def get_specific_room_details(request):
    try:
        print 'Hello '
        room_details = ApartmentRoom.objects.get(apt_room_id=request.GET.get('room_id'))
        room_images = [SERVER_MEDIA_URL+room_details.apt_room_images1.url, SERVER_MEDIA_URL+room_details.apt_room_images2.url, SERVER_MEDIA_URL+room_details.apt_room_images3.url, SERVER_MEDIA_URL+room_details.apt_room_images4.url, SERVER_MEDIA_URL+room_details.apt_room_images5.url]
        data = {'success':'true', 'room_id': str(room_details.apt_room_id), 'apartment_name':room_details.apartment_id.apt_name, 'apartment_address' : room_details.apartment_id.get_apartment_address(), 'apartment_singlebed_price': room_details.apt_room_rate , 'room_type':room_details.room_type, 'apartment_description' : room_details.apartment_id.apt_description, 'room_images':room_images , 'apartment_features': room_details.apartment_id.get_apartment_features() }
    except Exception, e:
        print 'Error : ',e
        data = {'success': 'false', 'error_message':'Server Error - Unable to Proceed request, Please Try again'}
    return HttpResponse(json.dumps(data), content_type='application/json')
    
    
    
    
