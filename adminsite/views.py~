from django.shortcuts import render

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
from CorpRoomApp.forms import *
from CorpRoomApp.constants import ExceptionMessages, ExceptionLabel
from CorpRoomApp.common_functionality import authenticate_system_user
from CorpRoomApp.common_functionality import store_user_track # for tracking user activity
from CorpRoomApp.common_functionality import user_track_sign_out # for tracking user activity

AVAILABLE_ROOM  = 0
BOOKING_BOOKED      = 1

ADMIN = 0
CORPORATE = 1
OWNER = 2
RETAIL = 3

#SERVER_MEDIA_URL = 'http://192.168.0.121:8000'
SERVER_MEDIA_URL = 'http://dial-a-room.com'
USER_PLACEHOLDER = '/media/media/placeholders/placeholder-person.jpg'
#SERVER_MEDIA_URL = 'http://ec2-52-4-20-173.compute-1.amazonaws.com'

MONTH_LIST = {
    '1' : 'Jan',
    '2' : 'Feb',
    '3' : 'Mar',
    '4' : 'Apr',
    '5' : 'May',
    '6' : 'Jun',
    '7' : 'Jul',
    '8' : 'Aug',
    '9' : 'Sep',
    '10': 'Oct',
    '11': 'Nov',
    '12': 'Dec'
}

FY_MONTH_LIST = [4,5,6,7,8,9,10,11,12,1,2,3]
FY_MONTH_NAME_LIST = ['Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec','Jan','Feb','Mar']
GEN_MONTH_LIST = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']


def home(request):
    return authenticate_system_user(request)
    #return redirect('/business/')
    #return render_to_response('login.html')
    
@csrf_exempt
def admin_login(request):
    print 'request accepted'
    try:
        if request.method == 'POST':
            user = authenticate(username=request.POST.get('username'), password= request.POST.get('password'))
            if user is not None:
                if user.is_active:
                    login(request,user)
                    request.session['login_user']=user.username
                    request.session['login_status']=True
                    request.session['user_id']= user.id
                    if user.is_superuser :
                        store_user_track(request,'Admin Login')   # for tracking user activity
                        return redirect('/business/dashboard/')
                    else:
                        customer = Customer.objects.get(id=user.id)
                        if customer.user_type == CORPORATE:
                            if customer.cust_image:
                                request.session['user_profile_image'] = SERVER_MEDIA_URL + customer.cust_image.url
                            else:
                                request.session['user_profile_image'] = SERVER_MEDIA_URL + USER_PLACEHOLDER
                        request.session['user_full_name'] = customer.cust_first_name + ' '+ customer.cust_last_name
                        store_user_track(request,'Customer Login')   # for tracking user activity
                        if request.POST.get('next'):
                            return HttpResponseRedirect(request.POST.get('next'))
                        else:
                            return HttpResponseRedirect('/corporate/')
                        #return render(request,'/cam/',context_instance=RequestContext(request))
                else:
                    print 'User Not Active'
                    data= {'success' : 'false', ExceptionLabel.ERROR_MESSAGE:'User Is Not Active'}
            else:
                print 'User Not Available'
                data= {'success' : 'false', ExceptionLabel.ERROR_MESSAGE:'Invalid Username or Password'}
        else:
            print 'Invalid Request'
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
    return render_to_response('login.html', {'errors':data})

# This is for Admin Dashaboard
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def show_dashboard(request):
#    return authenticate_system_user(request)
    store_user_track(request, "Admin Dashboard")
    try:
        print 'Dashboard'
        today = date.today()
        if today.month <=3:
            start_date = date(today.year-1, 04, 01)  # (yy,mm,dd)
            end_date = date(today.year, 03, 31)  # (yy,mm,dd)
        else:
            start_date = date(today.year, 04, 01)  # (yy,mm,dd)
            end_date = date(today.year+1, 03, 31)  # (yy,mm,dd)
            
        # This is for getting the list of Bookings against month
        #monthly_bookings = CAMBooking.objects.filter(cam_booking_estimated_checkin_date__range=(start_date, end_date)).extra(select={'month': "EXTRACT(month FROM cam_booking_estimated_checkin_date)"}).values('month').annotate(total=Count('cam_booking_id'))
        #monthly_bookings = CAMBooking.objects.filter(cam_booking_estimated_checkin_date__range=(start_date, end_date)).extra(select={'month': "EXTRACT(month FROM cam_booking_estimated_checkin_date)"}).values('month','cam_booking_estimated_no_of_day_stay').annotate(total=Count('cam_booking_id'))
        monthly_bookings = Booking.objects.filter(booking_estimated_checkin_date__range=(start_date, end_date)).extra(select={'month': "EXTRACT(month FROM booking_estimated_checkin_date)"}).values('month').annotate(total=Sum('booking_estimated_no_of_day_stay'))
        list = {}
        # Convert a month value and total value into single dictionary as 
        # Month is Key and Total as Value,so that it can sorted in ascending order 
        for book in monthly_bookings:   
            list[book['month']]=book['total']
        monthly_booking_count =[]
        
        try:
            for m in FY_MONTH_LIST:
                monthly_booking_count.append(list[m])
        except KeyError,e:
            print monthly_booking_count
            
        print monthly_booking_count
        
        month_amt, total_amt = get_month_and_total_amount()
        request.session['ADMIN_total_income'] = total_amt
        data = {
            'cam_count': get_cam_count(),
            'guest_count':get_guest_count(),
            'available_rooms': get_no_of_available_rooms(),
            'month_amount': month_amt,
            'total_amount': total_amt,
            'booked_rooms':get_no_of_booked_rooms(),
            'graph_data_list' : monthly_booking_count,
            'start_date': start_date.strftime('%b %Y'),
            'end_date':end_date.strftime('%b %Y')
        }
        print data
    except Exception, e:
        print 'Exception : ',e
        data = {}
    #return render_to_response('home.html')
    return render(request,'home.html', data)


def get_guest_count():
    try:
        print 'Guest Count'
        guest_count = Guest.objects.values('guest_email').distinct().count()
        return guest_count
    except Exception, e:
        print 'Exception : ',e
        return 0

def get_cam_count():
    try:
        print 'CAM Count'
        guest_count = Customer.objects.filter(user_type=1).values('cust_email').distinct().count()
        return guest_count
    except Exception, e:
        print 'Exception : ',e
        return 0

def get_no_of_available_rooms():
    print 'Available Rooms'
    apt_room_count = PropertyRoom.objects.filter(Q(room_status=AVAILABLE_ROOM)).count()
    return apt_room_count

def get_no_of_booked_rooms():
    print 'Booked Rooms'
    apt_room_count = PropertyRoom.objects.filter(Q(room_status=BOOKING_BOOKED)).count()
    return apt_room_count


def get_month_and_total_amount():
    """
    This method returns two values : this month amount and total amount
    """
    print 'Total Amount'
    try:
        print 'CAM Count'
        this_month  = datetime.datetime.today().month
        invoices = Invoice.objects.all()
        this_month_amount = 0
        total_amount    = 0
        for invoice in invoices:
            if invoice.invoice_datetime.month == this_month:
                this_month_amount = this_month_amount + invoice.invoice_gross_amount
            total_amount = total_amount + invoice.invoice_gross_amount
        return '{:,.2f}'.format(this_month_amount), '{:,.2f}'.format(total_amount)
    except Exception, e:
        print 'Exception : ',e
        return 0.00, 0.00
    

# log out the user
def signOutAdmin(request):
    request.session['login_user']=None
    request.session['login_status']=False
    request.session['user_id']= None
    user_track_sign_out(request)
    logout(request)
    return redirect('/business/')
