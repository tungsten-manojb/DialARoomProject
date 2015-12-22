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
from CorpRoomApp.constants import ExceptionMessages, ExceptionLabel
# import OperationalError

from CorpRoomApp.send_mail import  *


import cStringIO as StringIO
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse
from cgi import escape

SERVER_MEDIA_URL = 'http://192.168.0.121:8080'
SERVER_MEDIA_URL = 'http://dial-a-room.com'

#SERVER_MEDIA_URL = 'http://ec2-52-4-20-173.compute-1.amazonaws.com'

AVAILABLE_ROOM  = 0
BOOKING_OPEN        = 1
BOOKING_BOOKED      = 2
BOOKING_CANCELLED   = 3
BOOKING_COMPLETED   = 4


SERVICE_TAX = 14.4
LUXURY_TAX = 4.5



GUEST_ACTIVE    = 1
GUEST_INACTIVE  = 0

'''
-------------------------------------------------------------------------------
THESE API's RELATED WITH THE BOOKINGS
-------------------------------------------------------------------------------
'''

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def booking_list_page(request):
    if not request.user.is_authenticated():
        return redirect('/')
    return render(request,'booking-list.html')
    #return render_to_response('booking-list.html')
    
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def booking_search_page(request):
    if not request.user.is_authenticated():
        return redirect('/')
    return render(request,'booking-search.html')


# This is for new booking details page, will added by CRM admin
def new_booking_page(request):
    #pdb.set_trace()
    try:
        print 'New booking Page '
        cam_list=[]
        var_room_id = request.GET.get('apartment_room_id')
        var_check_in = request.GET.get('check_in')
        var_check_out = request.GET.get('check_out')
        print "var_check_in"
        print var_check_in
        check_in_date=datetime.datetime.strptime(var_check_in, '%d/%m/%Y')
        check_out_date=datetime.datetime.strptime(var_check_out, '%d/%m/%Y')
        d = check_out_date - check_in_date

        cam_user_list= Customer.objects.filter(user_type=1)

        for cam_user in cam_user_list:
            cam_list.append(get_cam_user(cam_user))


        property_obj = Property.objects.get(property_id=var_room_id)
        # print "here"

        data = { 'success':'true',
                #'room': get_apartment_room_details(property_obj,str(d.days)),
                'no_of_days': str(d.days),
                'check_in':check_in_date.strftime('%d/%m/%Y'),
                'check_out':check_out_date.strftime('%d/%m/%Y'),
                'cam_user_list': cam_list
                 } 
    except Exception, e:
        print 'Exception ',e
        data = { 'success': 'false' }
    return render(request,'booking-confirm.html', data)


def get_cam_user(cam_user):
        return { 'cam_id': cam_user.id , 'cam_user': cam_user.cust_first_name+' '+cam_user.cust_last_name  }

def get_apartment_room_details(property_obj,days):
    #print room.property_rates.get()
    return {
        'city_name':room.property_id.property_city,
        'room_id': room.room_id,
        'apartment_name': room.property_id.property_display_name,
        'apartment_address':room.property_id.property_address+ ', ' + room.property_id.property_city + ', ' + room.property_id.property_state + ', ' + room.property_id.property_country + '- ' +room.property_id.property_pincode,
        'room_type':room.room_type,
        'room_number':room.room_number
    }


def get_booking_details(booking_id):
    print "in the get_booking_details"
    """
        This function is used for getting specific booking details,
        This function called by booking_detail_display()
    """
    try:
        cam_booking_obj = Booking.objects.get(booking_id=booking_id)
        total_amount = 0.00
        paid_bill = ''
        invoice = ''
        #if cam_booking_obj.booking_status == BOOKING_COMPLETED:
        try:
            invoice = Invoice.objects.get(booking_id=cam_booking_obj)
            print "invoice"
            print invoice
            total_amount =invoice.invoice_gross_amount
            print "total_amount"
            print total_amount
            # total_amount = '20
        except Exception, e:
            print 'Exception ', e
        data = {
            'cam_booking_id'    : str(cam_booking_obj.booking_id),
            'booking_number' : cam_booking_obj.booking_unique_id,
            'apartment_name'    : cam_booking_obj.property_id.property_actual_name,
            'apartment_address' : cam_booking_obj.property_id.property_address,
            'booked_rooms'      : cam_booking_obj.property_id.number_of_rooms,
            'room_rate'         : cam_booking_obj.booking_rate,
            #'room_image'        : SERVER_MEDIA_URL + cam_booking_obj.aptroom_id.apt_room_images1.url,
            'check_in_time'     : cam_booking_obj.booking_estimated_checkin_time.strftime('%I:%M %p'),
            'check_out_time'    : cam_booking_obj.booking_estimated_checkout_time.strftime('%I:%M %p'),
            'check_in_date'     : cam_booking_obj.booking_estimated_checkin_date.strftime('%a, %d %b, %Y'),
            'check_out_date'    : cam_booking_obj.booking_estimated_checkout_date.strftime('%a, %d %b, %Y'),
            'total_bill'        : '{:,.2f}'.format(total_amount),
            'total_paid'        : '{:,.2f}'.format(total_amount),
            'booking_status'    : cam_booking_obj.booking_status,
            # 'room_type'         : cam_booking_obj.aptroom_id.room_type,
            # 'favourite_status'  : cam_booking_obj.cam_booking_favourite,
            'number_of_days'    : str(cam_booking_obj.booking_actual_no_of_day_stay),
            'guest_name'        : cam_booking_obj.guest_id.guest_first_name if cam_booking_obj.guest_id else '' , #+ ' ' + cam_booking_obj.guest_id.guest_last_name,
            'guest_email'       : cam_booking_obj.guest_id.guest_email if cam_booking_obj.guest_id else '',
            'guest_contact_no'  : cam_booking_obj.guest_id.guest_contactno if cam_booking_obj.guest_id else ''
        }
        return data
    except Booking.DoesNotExist, e:
        data = {'success' : 'false', 'error_message':'Failed To Fetch Booking Details' }
        return data
    

def booking_detail_display(request):
    #pdb.set_trace()
    if not request.user.is_authenticated():
        return redirect('/')
    try:
        if request.GET.get('booking_id'):
            booking_id = request.GET.get('booking_id')
            return render(request,'admin/booking-completed-cancelled-booked.html', get_booking_details(booking_id))
        else:
            print 'Hello'
            data = { 'success': 'false'}
    except Exception, e:
        print 'Exception : ', e
        data = { 'success': 'false'}
    return render(request,'booking-confirm.html', data)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def booking_confirm_page(request):
    """
    This request method will redirect to booking details page,
    where user can view/add guest Detail and confirms the booking details.
    Also This is used for to confirm the booking details which is registered from
    Mobile app.
    """
    # pdb.set_trace()
    if not request.user.is_authenticated():
        return redirect('/')
    try:
        if request.GET.get('booking_id'):
            booking_id = request.GET.get('booking_id')
            return render(request,'admin/booking-confirm.html', get_booking_details(booking_id))
        else:
            print 'Hello'
            data = { 'success': 'false'}
    except Exception, e:
        print 'Exception : ', e
        data = {'success': 'false'}
    return render(request,'booking-confirm.html', data)
    #return render_to_response('booking-confirm.html')


# save the booking info by CRM admin
@csrf_exempt
@transaction.atomic
def save_booking_details(request):
    print "in the save_booking_details"
    if not request.user.is_authenticated():
        return redirect('/')
    #pdb.set_trace()
    sid = transaction.savepoint()
    try:
        print request
        print 'Request Accepted '
        
        if request.method == "POST":
            print "selected_guest_name"
            print request.POST.get('selected_guest_name')
            v_cam_id      = request.POST.get('cam_user_id')
            guest_name  = request.POST.get('selected_guest_name')
            guest_phone = request.POST.get('phone_number')
            v_guest_email = request.POST.get('email_id')
            room_id     = request.POST.get('room_id')
            check_in    = datetime.datetime.strptime(request.POST.get('check_in'), '%m/%d/%Y')
            check_out   = datetime.datetime.strptime(request.POST.get('check_out'), '%m/%d/%Y')
            promocode   = request.POST.get('promocode')
            #amount      = request.POST.get('amount')
            #taxes       = request.POST.get('taxes')
            gross_amount= request.POST.get('gross_amount')
            
            guest_obj = Guest.objects.get(guest_id= guest_name)
            # guest_obj.save()
            
            room_obj = PropertyRoom.objects.get(room_id=room_id)
            
            booking_obj = Booking(
                customer_id      = Customer.objects.get(id=v_cam_id),
                guest_id    = guest_obj,
                property_id   = room_obj.property_id,
                property_room_id  = room_obj,
                booking_estimated_checkin_date = check_in,
                booking_estimated_checkout_date = check_out,
                booking_estimated_checkin_time = datetime.datetime.now().time(),
                booking_estimated_checkout_time = datetime.datetime.now().time(),
                booking_status  = BOOKING_BOOKED
                )
            booking_obj.save()
            room_obj.apt_room_status = BOOKING_BOOKED
            room_obj.save()
            # transaction.savepoint_commit(sid)
            send_booking_confirmation_mail_with_template(booking_obj.booking_id)
            transaction.savepoint_commit(sid)
            data = {'success':'true', 'booking':booking_obj, 'room_obj': room_obj }
        else:
            print 'Hello'
            transaction.savepoint_rollback(sid)
            data = {'success':'false', 'error_message':'Invalid Request'}
    except MySQLdb.OperationalError, e:
        transaction.savepoint_rollback(sid)
        print 'Operational Error : ',e
        data = {'success':'false', 'error_message':'Internal Server Error'}
    except Exception, e:
        print 'Error ', e
        data = {'success':'false', 'error_message':'Server Error- Please Try Again'}
    return render(request,'booking-confirmed-page.html', data )


# this provides a list of bookings for booking list table in booking list page
def get_booking_list(request):
    """
    This method returns all the bookings booked by customer.
    """
    data = {'data' : "none"}
    try:
        print 'Hello'
        booking_list=[]
        bookings = Booking.objects.all()
        for booking in bookings:
            booking_list.append(get_booking_info(booking))
        data = { 'data':booking_list}
    except Exception, e:
        print 'Error ',e
        data = {'data' : "none"}
    return HttpResponse(json.dumps(data), content_type='application/json')



def get_booking_info(booking):
    status = ''
    more = ''
    if booking.booking_status == BOOKING_OPEN:
        status  = '<a marked="1" href="/business/booking-confirm/?booking_id='+ str(booking.booking_id)+'"><span class="label label-info">Open</span></a>'
        more    = '<a marked="1" href="/business/booking-confirm/?booking_id='+ str(booking.booking_id)+'"><i class="fa-2x pe-7s-more text-primary2"></i></a>'
    if  booking.booking_status == BOOKING_BOOKED:
        status  = '<a marked="1" href="/business/booking-detail-display/?booking_id='+ str(booking.booking_id)+'"><span class="label label-success">Booked</span></a>'
        more    = '<a marked="1" href="/business/booking-detail-display/?booking_id='+ str(booking.booking_id)+'"><i class="fa-2x pe-7s-more text-primary2"></i></a>'
    if  booking.booking_status == BOOKING_COMPLETED:
        status  = '<a marked="1" href="/business/booking-detail-display/?booking_id='+ str(booking.booking_id)+'"><span class="label label-warning">Completed</span></a>'
        more    = '<a marked="1" href="/business/booking-detail-display/?booking_id='+ str(booking.booking_id)+'"><i class="fa-2x pe-7s-more text-primary2"></i></a>'
    if  booking.booking_status == BOOKING_CANCELLED:
        status = '<a marked="1" href="/business/booking-detail-display/?booking_id='+ str(booking.booking_id)+'"><span class="label label-danger">Cancelled</span></a>'
        more = '<a marked="1" href="/business/booking-detail-display/?booking_id='+ str(booking.booking_id)+'"><i class="fa-2x pe-7s-more text-primary2"></i></a>'
    if booking.property_id:
        apt_name = booking.property_id.property_actual_name
        apt_city = booking.property_id.property_location
    else :
        apt_name = 'Hillview Residency'
        apt_city = 'Pune'
    return  {
                'booking_number' : booking.booking_unique_id,
                'apartment_name': apt_name,
                'apt_location': apt_city ,
                'guest_name'    : booking.guest_id.guest_first_name if booking.guest_id else '',
                'check_in': booking.booking_estimated_checkin_date.strftime('%d %b %Y'),
                'check_out'     : booking.booking_estimated_checkout_date.strftime('%d %b %Y'),
                'status'        : status,
                'promotion_code': booking.promotion_code,
                'more' : more
            }


# This API provides the confirmation facility to admin 
@csrf_exempt
def make_admin_booking_confirm(request):
    print "make_admin_booking_confirm"
    print request
    try:
        print 'Hello', request.POST.get('booking_id'), request.POST.get('promotion_code')
        cam_booking_obj = Booking.objects.get(booking_id=request.POST.get('booking_id'))
        cam_booking_obj.booking_status = BOOKING_BOOKED
        cam_booking_obj.save()
        data = get_booking_details(cam_booking_obj.booking_id)
        
        send_booking_confirmation_mail_with_template(cam_booking_obj.booking_id)
        #return render(request,'admin/cam-booking-confirmation.html', data)
    except Exception, e:
        print 'Error ',e
        data = { 'data' : "none" }
    return render(request,'admin/cam-booking-confirmation.html', data )


def get_available_rooms_for_booking(request):
    filter_args={}
    try:
        print 'Hello'
        available_room_list=[]
        if request.GET.get('city_name'):
            filter_args['property_city__icontains']  =   request.GET.get('city_name')
        room_list = PropertyRoom.objects.filter(Q(room_status=AVAILABLE_ROOM) & Q (property_id = Property.objects.filter(**filter_args)))
        print "room_list"
        print room_list
        for room in room_list:
            available_room_list.append(get_apt_room_details_for_admin_booking(room))

        data = {'success':'true', 'data': available_room_list }
    except Exception, e:
        print 'Exception ',e

        data = { 'success':'false', 'error_message': 'Server Error - Unable to Process request' }
    return HttpResponse(json.dumps(data), content_type='application/json')



def get_apt_room_details_for_admin_booking(room):
    print room.property_id.property_rates
    return {
            'city_name':room.property_id.property_city,
            'room_id': room.room_id,
            'apartment_name': room.property_id.property_display_name,
            'room_type': room.room_type,
            'apartment_address':room.property_id.property_address+ ', ' + room.property_id.property_city + ', ' + room.property_id.property_state + ', ' + room.property_id.property_country + '- ' +room.property_id.property_pincode,
            'location': room.property_id.property_location,
            'room_rate':'', 
            'room_image':  "",
            'info' : '<a marked="1" onClick="showDetails(this)"><i class="fa-2x pe-7s-info text-info"></i></a>',
            'book' : '<a onClick="goForBooking('+ str(room.room_id) +')" marked="1"><i class="fa-2x pe-7s-angle-right-circle text-success"></i></a>',
            'book_now_id' : str(room.room_id),
            # 'general_room_rate' : room.room_general_rate or "", 
            'desc' : room.property_id.property_description
        }









def make_admin_booking_cancel(request):
    try:
        print 'Hello', request.GET.get('cam_booking_id') #request.POST.get('promotion_code')
        cam_booking_obj = Booking.objects.get(booking_id=request.GET.get('cam_booking_id'))
        cam_booking_obj.cam_booking_status = BOOKING_CANCELLED
        cam_booking_obj.save()
        data = get_booking_details(cam_booking_obj.booking_id)
        #send_booking_confirmation_email(cam_booking_obj.cam_booking_id)
        #return render(request,'admin/cam-booking-confirmation.html', data)
    except Exception, e:
        print 'Error ',e
        data = { 'data' : "none" }
    return render( request,'admin/cam-booking-cancellation.html', data )


def create_transaction_entry(booking_obj,gross_amount):
    print "in the create_transaction_entry"
    try:
        transaction_obj=CorporateTransaction(
            invoice_id                 =booking_obj.invoicebooking.get().invoice_unique_id,
            corporate_id               =booking_obj.customer_id,
            transaction_date           =datetime.datetime.now(),
            transaction_amount         =gross_amount,
            transaction_type           =0
            )
        transaction_obj.save()
        print "entry done"
        return True
    except Exception, e:
        print 'Error ',e
        return False


@csrf_exempt
def add_extra_charges(request):
    print request.POST.get('check_out_date')
    check_out_dt = request.POST.get('check_out_date')
    try:
        gross_amount=''
        amount=''

        cam_booking_obj = Booking.objects.get(booking_id=request.POST.get('booking_id'))
        if cam_booking_obj :

            check_in_date=cam_booking_obj.booking_actual_checkin_date
            check_out_date=datetime.datetime.strptime(check_out_dt, '%d-%m-%Y')
            final_date=check_out_date.date() - check_in_date

            amount =cam_booking_obj.booking_rate * final_date.days
            service_tax_amount = ( amount * SERVICE_TAX )/100
            luxury_tax_amount  = ( amount * LUXURY_TAX )/100
        
            tax_amount = service_tax_amount + luxury_tax_amount
            gross_amount = amount + tax_amount

            # cam_booking_obj.booking_amount=cam_booking_obj.invoicebooking.get().invoice_gross_amount+float(request.POST.get('charges'))
            cam_booking_obj.booking_amount=gross_amount+float(request.POST.get('charges'))
            # cam_booking_obj.booking_actual_checkout_date=check_out_date.date()
            cam_booking_obj.booking_status = 4
            cam_booking_obj.booking_check_out_status=True
            cam_booking_obj.save()

            invoice_obj=cam_booking_obj.invoicebooking.get()
            invoice_obj.invoice_gross_amount=gross_amount+float(request.POST.get('charges'))
            invoice_obj.extra_charges = request.POST.get('charges')
            invoice_obj.extra_charge_details = request.POST.get('description')
            invoice_obj.save()

            if cam_booking_obj.customer_id:
                if cam_booking_obj.customer_id.user_type==1:
                    create_transaction_entry(cam_booking_obj,gross_amount)
            print "done"
        data = { 'success':'true', 'booking_number':cam_booking_obj.booking_unique_id }
    except Exception, e:
        print 'Error ',e
        data = { 'data' : 'None','success':'false'}
    return HttpResponse(json.dumps(data), content_type='application/json')



def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    context = Context(context_dict)
    html  = template.render(context)
    result = StringIO.StringIO()

    pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        print "here"
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return HttpResponse('We had some errors<pre>%s</pre>' % escape(html))


# @csrf_exempt
def myview(request):
    print "print here"
    results = Booking.objects.all()[0:2]
    print results
    return render_to_pdf(
            'web/invoice-print.html',
            {
                'pagesize':'A4',
                'mylist': results,
            }
        )



# @csrf_exempt
# @transaction.atomic
def save_guest_information(request):
    print "save_guest_information"
    sid = transaction.savepoint()
    try:
        #pdb.set_trace()
        print 'Hello'
        if request.method == "POST":
            cam_id= request.session['user_id']
            cam_obj=Customer.objects.get(id=cam_id)
            guest_obj = Guest(
                guest_first_name = request.POST.get('guest_name'),
                guest_email = request.POST.get('guest_email'),
                guest_contactno = request.POST.get('phone_number'),
                customer_id = cam_obj,
                guest_status = 1,
                guest_creation_date = datetime.datetime.now()
            )
            guest_obj.save()
            guest_obj.guest_unique_id = 'CAMGST' +  str(cam_obj.id) + str(guest_obj.guest_id).zfill(6)
            guest_obj.save()
            transaction.savepoint_commit(sid)

            data = {'success': 'true', 'guest_id':guest_obj.guest_id , 'guest_name' : guest_obj.guest_first_name, 'email_id':guest_obj.guest_email, 'phone_no':guest_obj.guest_contactno }
        else:
            transaction.savepoint_rollback(sid)
            print 'Invalid Request'
            data = {'success': 'false' , ExceptionLabel.ERROR_MESSAGE :'Invalid Request'}
    except Exception, e:
        print 'error',e
        data = {'success': 'false', ExceptionLabel.ERROR_MESSAGE :'Server Error'}
    return HttpResponse(json.dumps(data), content_type='application/json')

