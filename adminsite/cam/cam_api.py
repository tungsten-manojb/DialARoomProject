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
from CorpRoomApp.constants import ExceptionMessages, ExceptionLabel
from CorpRoomApp.models import *
from quoteapp.models import QuotationResponse
from datetime import date

from CorpRoomApp.send_mail import  *
from adminsite.customers import get_favorite_list
from CorpRoomApp.common_functionality import authenticate_system_user
from CorpRoomApp.common_functionality import store_user_track # for tracking user activity

from CorpRoomApp.send_sms import send_booking_submission_sms_to_customer
from CorpRoomApp.send_sms import send_booking_submission_sms_to_vendor

# Accessing the Common Functionality of Property
from CorpRoomApp.common_functionality import PropertyCommonFunctionality

from cam_additional_functionalitites import get_corporate_prefered_property_images

#SERVER_MEDIA_URL = 'http://192.168.0.121:8000'
SERVER_MEDIA_URL = 'http://dial-a-room.com'

#SERVER_MEDIA_URL = 'http://www.dial-a-room.com'

# Booking Constants
BOOKING_ALL         = 0
BOOKING_OPEN        = 1
BOOKING_BOOKED      = 2
BOOKING_CANCELLED   = 3
BOOKING_COMPLETED   = 4

GUEST_ACTIVE    = 1
GUEST_INACTIVE  = 0

AVAILABLE_ROOM  = 0

SERVICE_TAX = 14.4
LUXURY_TAX = 4.5

pcf = PropertyCommonFunctionality()

def cam_index(request):
    #store_user_track(request, 'Customer Dashboard')   # for tracking user activity
    return authenticate_system_user(request)
    #return redirect('/corporate/dashboard/')
    #print 'Hello'
    #return render(request,'cam-user/index.html')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def cam_dashboard(request):
    store_user_track(request,'Customer Dashboard')   # for tracking user activity
    print 'CAM Dashboard'
    print 'REQUEST : ', dir(request)
    #pdb.set_trace()
    try:
        cam_id = int(request.session['user_id'])
        cam_object = Customer.objects.get(user_ptr_id=cam_id)
        total_days = cam_object.customerbooking.aggregate(total=Sum('booking_actual_no_of_day_stay'))
        cam_total_days = total_days['total']

        # Number of guest count
        no_of_guests = Guest.objects.filter(customer_id= cam_object).count()
        print 'Number Of Guest : ', no_of_guests

        this_month_days = 0
        this_month_amount = 0
        sum =0
        amount_fy   = 0
        days_fy     = 0
        this_month  = datetime.datetime.today().month
        this_year   = datetime.datetime.today().year

        if this_month <= 3:
            str_start_date  = '01-04-' + str((datetime.datetime.today().year - 1))
            str_end_date    = '31-03-' + str((datetime.datetime.today().year))
        else:
            str_start_date  = '01-04-' + str((datetime.datetime.today().year))
            str_end_date    = '31-03-' + str((datetime.datetime.today().year+1))

        start_date  = datetime.datetime.strptime(str_start_date, '%d-%m-%Y')
        end_date    = datetime.datetime.strptime(str_end_date, '%d-%m-%Y')
        
        s_date = date(start_date.year, start_date.month, start_date.day)
        e_date = date(end_date.year, end_date.month, end_date.day)        
        
        no_of_bookings = 0
        cbs = cam_object.customerbooking.all() 
        for cb in cbs:
            no_of_bookings = no_of_bookings +1
            try:
                invoice = Invoice.objects.get(booking_id=cb)
                sum = sum + invoice.invoice_gross_amount
                if cb.booking_estimated_checkin_date.month == this_month:
                    this_month_days = this_month_days + cb.booking_actual_no_of_day_stay
                    this_month_amount = this_month_amount + invoice.invoice_gross_amount
                
                temp_date = date(cb.booking_estimated_checkin_date.year, cb.booking_estimated_checkin_date.month, cb.booking_estimated_checkin_date.day)
                
                if s_date < temp_date < e_date:
                    days_fy     = days_fy + cb.booking_actual_no_of_day_stay
                    amount_fy   = amount_fy + invoice.invoice_gross_amount
            except Exception, e:
                print 'Exception ',e
                
        # this is for getting the no.of day for this month and amounts
        monthly_bookings = Booking.objects.filter(booking_estimated_checkin_date__range=(start_date, end_date)).extra(select={'month': "EXTRACT(month FROM booking_estimated_checkin_date)"}).values('month').annotate(total=Count('booking_id'))

        # guest List 
        guests = Guest.objects.filter(customer_id=cam_object)

        #orderList=OrderInfo.objects.filter(Q(**filter_args) &  (Q(ProductID = ProductInfo.objects.filter(Q(**product_filter_args) & Q(VendorID = VendorInfo.objects.filter(**vendor_filter_args)))) & Q(ShipmentAddressID = ShipmentAddressInfo.objects.filter(**ship_filter_args )))).order_by('-OrderDate')
        invoice_amount = Invoice.objects.filter(Q(booking_id = Booking.objects.filter(customer_id=cam_object))).aggregate(total_amount=Sum('invoice_gross_amount'))

        if invoice_amount['total_amount'] == None:
            tot_amount = 0
        else:
            tot_amount = invoice_amount['total_amount']

        request.session['total_amount'] = invoice_amount['total_amount']
        data = {'success':'true','total_days' : cam_total_days, 'total_amount': tot_amount, 'month_days': this_month_days, 'month_amount': this_month_amount,
            'days_fy': days_fy, 'amount_fy': amount_fy, 'no_of_guests':no_of_guests, 'no_of_bookings': no_of_bookings, 'state_list' : pcf.get_all_state_name(),
            'image_carousal' : get_corporate_prefered_property_images(cam_object), 'guest_list' :guests  }
        print data
#        data = {'success':'true','total_days' : cam_total_days, 'total_amount': '{:,.2f}'.format(invoice_amount['total_amount']),        'month_days': this_month_days, 'month_amount': '{:,.2f}'.format(this_month_amount),
#            'days_fy': days_fy, 'amount_fy': '{:,.2f}'.format(amount_fy), 'no_of_guests':no_of_guests, 'no_of_bookings': no_of_bookings }
    except Exception, e:
        print 'Exception ',e
        data = {'data': 'Hello'}
    return render(request,'cam-user/cam-home-page.html',data, context_instance=RequestContext(request))



def get_property_info(property,corporate_user):
    """ This function returns a specific property information for search proprties """
    print '----------------->'

    print property
    print corporate_user
    property_rate_list = {}
    property_rates = CAMPropertyRate.objects.filter(property_id=property, cust_id=corporate_user)
    for rate in property_rates:
        if rate.occupancy_type == 0:
            property_rate_list.update({ 'single' : rate.agreed_rate })
        if rate.occupancy_type == 1:
            property_rate_list.update({ 'double' : rate.agreed_rate })
        if rate.occupancy_type == 2:
            property_rate_list.update({ 'additional' : rate.agreed_rate })
    
    return {
                'city_name':property.property_city, 'room_id': property.property_id,
                'apartment_name': property.property_actual_name, 'apartment_address': property.property_location,
                'location': property.property_location, 'corporate_rates': property_rate_list,
                'room_image': SERVER_MEDIA_URL + '/static/media/rooms/paris.jpg',
                'info' : '<a marked="1" onClick="showDetails(this)"><i class="fa-2x pe-7s-info text-info"></i></a>',
                'book' : '<a onClick="goForBooking('+ str(property.property_id) +')" marked="1"><i class="fa-2x pe-7s-angle-right-circle text-success"></i></a>'
        }



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def booking_list_page(request):
    store_user_track(request, 'Customer Booking List')   # for tracking user activity
    if not request.user.is_authenticated():
        return redirect('/corporate/')
    #return render(request,'booking-list.html', data)
    return render(request,'cam-user/cam-booking-list.html')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def booking_search_page(request):
    store_user_track(request, "Customer New Booking Search" )   # for tracking user activity
    if not request.user.is_authenticated():
        return redirect('/corporate/?next='+request.path)
    data = {}

    try:
        corporate_user = Customer.objects.get(id=request.session['user_id'])
        prefered_properties = CustomerFavoriteProperty.objects.filter(customer_id=corporate_user)
        data = {'prefered_properties': [ get_property_info(property.property_id,corporate_user) for property in prefered_properties ] }
    except Exception as err:
        print 'Exception : ',err
        data = {'prefered_properties': [] }
    return render(request,'cam-user/booking-search.html',data)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def cam_my_profile(request):
    store_user_track(request, "Customer Profile Page")   # for tracking user activity
    if not request.user.is_authenticated():
        return redirect('/?next='+request.path)
    try:
        if request.session['user_id']:
            cam = Customer.objects.get(id=request.session['user_id'])
        else:
            cam = Customer.objects.get(cust_unique_id=request.GET.get('profile'))
        
        data = { 'cam' : cam , 'fav_properties' : get_favorite_list(cam) }
    except Customer.DoesNotExist,e:
        print 'FAILED TO retrieve Customer information'
    except Exception,e:
        print 'Exception ',e
    return render(request,'cam-user/cam-profile.html',data)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def edit_cam_profile_page(request):
    store_user_track(request,"Customer Edit Profile" )   # for tracking user activity
    if not request.user.is_authenticated():
        return redirect('/corporate/')
    try:
        cam = Customer.objects.get(id=request.session['user_id'])
        data = { 'cam' : cam }
    except Customer.DoesNotExist,e:
        print 'FAILED TO retrieve Customer information'
    except Exception,e:
        print 'Exception ',e
        data = {'error_message': 'Oops Something Went Wrong..!'}
    return render(request,'cam-user/edit-cam-profile.html',data)

# This guest list
def cam_guest_list(request):
    store_user_track(request,"Customer Guest List")   # for tracking user activity
    if not request.user.is_authenticated():
        return redirect('/coporate/')
    return render(request,'cam-user/cam-guest-list.html')

#
def get_booking_details(p_booking_id):
    """
        This function is used for getting specific booking details,
        This function called by booking_detail_display()
    """
    try:
        cam_booking_obj = Booking.objects.get(booking_unique_id=p_booking_id)
        total_amount = 0.00
        paid_bill = ''
        invoice = Invoice.objects.get(booking_id=cam_booking_obj)
        total_amount = invoice.invoice_gross_amount
        
        data = {
            'cam_booking_id'    : str(cam_booking_obj.booking_unique_id),
            'apartment_name'    : cam_booking_obj.property_id.property_actual_name,
            'apartment_address' : cam_booking_obj.property_id.property_location,
            #'booked_rooms'      : cam_booking_obj.aptroom_id.apt_room_number,
#            'room_rate'         : cam_booking_obj.aptroom_id.apt_room_rate,
            'room_rate'         : cam_booking_obj.booking_rate,
            #'room_image'        : SERVER_MEDIA_URL + cam_booking_obj.property_id..url,
            'check_in_time'     : cam_booking_obj.booking_estimated_checkin_time.strftime('%I:%M %p'),
            'check_out_time'    : cam_booking_obj.booking_estimated_checkout_time.strftime('%I:%M %p'),
            'check_in_date'     : cam_booking_obj.booking_estimated_checkin_date.strftime('%a, %d %b, %Y'),
            'check_out_date'    : cam_booking_obj.booking_estimated_checkout_date.strftime('%a, %d %b, %Y'),
            'total_amount'        : '{:,.2f}'.format(invoice.invoice_total_amount),
            'gross_amount'        : '{:,.2f}'.format(total_amount),
            'tax_amount'        : '{:,.2f}'.format(invoice.tax_amount),
            'booking_status'    : cam_booking_obj.booking_status,
            #'room_type'         : cam_booking_obj.aptroom_id.room_type,
            'favourite_status'  : cam_booking_obj.booking_favourite,
            'number_of_days'    : str(cam_booking_obj.booking_actual_no_of_day_stay),
            'guest_name'        : cam_booking_obj.guest_id.guest_first_name if cam_booking_obj.guest_id else '', #+ ' ' + cam_booking_obj.guest_id.guest_last_name,
            'guest_email'       : cam_booking_obj.guest_id.guest_email if cam_booking_obj.guest_id else '',
            'guest_contact_no'  : cam_booking_obj.guest_id.guest_contactno if cam_booking_obj.guest_id else '',
            'cam'               : cam_booking_obj.customer_id.get_customer_info()
        }
        
        if cam_booking_obj.is_from_quote:
            qr = QuotationResponse.objects.get(quotation_uid=cam_booking_obj.quotation_id)
        return data
    except Booking.DoesNotExist, e:
        data = { 'success' : 'false', 'error_message':'Failed To Fetch Booking Details' }
        return data


# This is for getting all cam bookings 
def get_cam_booking_list(request):
    """
    This method returns all the bookings booked by customer.
    """
    data = { 'data' : "none" }
    data_list = []
    #pdb.set_trace()
    try:
        print 'Hello'
        cam_user_id = request.session['user_id']
        bookings = Booking.objects.filter(customer_id=Customer.objects.get(id=cam_user_id))
        for booking in bookings:
            """
            This is for getting the specific booking information
            """
            status = ''
            more = ''
            if booking.booking_status == BOOKING_OPEN:
                status  = '<a marked="1" href="../cam-booking-details/?booking_id='+ str(booking.booking_unique_id)+'"><span class="label label-info">Open</span></a>'
                more    = '<a marked="1" href="../cam-booking-details/?booking_id='+ str(booking.booking_unique_id)+'"><i class="fa-2x pe-7s-more text-primary2"></i></a>'
            if booking.booking_status == BOOKING_BOOKED:
                status  = '<a marked="1" href="../cam-booking-details/?booking_id='+ str(booking.booking_unique_id)+'"><span class="label label-success">Booked</span></a>'
                more    = '<a marked="1" href="../cam-booking-details/?booking_id='+ str(booking.booking_unique_id)+'"><i class="fa-2x pe-7s-more text-primary2"></i></a>'
            if booking.booking_status == BOOKING_COMPLETED:
                status  = '<a marked="1" href="../cam-booking-details/?booking_id='+ str(booking.booking_unique_id)+'"><span class="label label-warning">Completed</span></a>'
                more    = '<a marked="1" href="../cam-booking-details/?booking_id='+ str(booking.booking_unique_id)+'"><i class="fa-2x pe-7s-more text-primary2"></i></a>'
            if booking.booking_status == BOOKING_CANCELLED:
                status = '<a marked="1" href="../cam-booking-details/?booking_id='+ str(booking.booking_unique_id)+'"><span class="label label-danger">Cancelled</span></a>'
                more = '<a marked="1" href="../cam-booking-details/?booking_id='+ str(booking.booking_unique_id)+'"><i class="fa-2x pe-7s-more text-primary2"></i></a>'
            
            bill_invoice = '<a marked="1" target="_blank" href="/business/invoice-page/?booking_number='+ str(booking.booking_unique_id)+'"><i class="fa-2x pe-7s-print text-primary2"></i></a>'
            apt_name = booking.property_id.property_actual_name
            apt_city = booking.property_id.property_location
            
            temp =  { 'apartment_name': apt_name, 'apt_location': apt_city,'guest_name' : booking.guest_id.guest_first_name if booking.guest_id else '',
                'check_in' : booking.booking_actual_checkin_date.strftime('%d %b %Y'), 'status' : status, 'more' : more,
                'check_out' : booking.booking_actual_checkout_date.strftime('%d %b %Y'),'invoice' :bill_invoice }
            data_list.append(temp)
        
        data = { 'data': data_list }
    except Exception, e:
        print 'Error ',e
        data = { 'data': data_list }
    return HttpResponse(json.dumps(data), content_type='application/json')

# New Booking Search for Corporate
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def cam_new_booking_search(request):
    store_user_track(request, "Customer New Booking Search")   # for tracking user activity
    if not request.user.is_authenticated():
        return redirect('/corporate/?next='+request.path)
    try:
        corporate_user = Customer.objects.get(id=request.session['user_id'])
        prefered_properties = CustomerFavoriteProperty.objects.filter(customer_id=corporate_user)
        data = {'prefered_properties': [ get_property_info(pre_property.property_id,corporate_user) for pre_property in prefered_properties ] }
        print data
    except Exception as err:
        print 'Exception : ',err
        data = {'prefered_properties': []}
    return render(request,'cam-user/cam-booking-search.html',data)

# @deprecated
def edit_profile_page(request):
    try:
        print 'Edit Profile Page'
        cam = Customer.objects.get(id=request.session['user_id'])
    except Exception as e:
        print 'Exception :',e


# This is for new booking details page, will added by CRM admin
def cam_new_booking_page(request):
    """
    This web service open a new page for adding booking by Customer.
    Check In Date, CheckOut Date and City
    """
    store_user_track(request, "Customer New Booking Page")   # for tracking user activity
    try:
        print '--|  New booking Page  |--'
        var_property_id = request.GET.get('apartment_room_id')
        var_check_in = request.GET.get('check_in')
        var_check_out = request.GET.get('check_out')
##        if request.GET.get('check_in'):
##            check_in_date=datetime.datetime.strptime(var_check_in, '%d/%m/%Y')
##            check_out_date=datetime.datetime.strptime(var_check_out, '%d/%m/%Y')
##            d = check_out_date - check_in_date
##        else:
        check_in_date = datetime.date.today()
        check_out_date = datetime.date.today()
        d = check_out_date - check_in_date
        # getting list of Customer users

        print request.session['user_id']
        cam_user= Customer.objects.get(id=request.session['user_id'])

        guests = Guest.objects.filter(customer_id=cam_user)
        property_obj = Property.objects.get(property_id=var_property_id)

        pro_images = PropertyImage.objects.filter(property_id=property_obj)
        images = ''
        if pro_images:
            images = [image.image_name.url for image in pro_images]
            images = '$'.join(images)
        
        data = { 'success':'true','property': property_obj, 'no_of_days': str(d.days), 'image_list': images,
         'check_in':check_in_date.strftime('%d/%m/%Y'), 'check_out':check_out_date.strftime('%d/%m/%Y'),
         'guest_list':guests, 'facility_list' : [f for f in property_obj.property_facility.split(',') if f ] }
        print data
        #data = { 'success':'true', 'guest_list':guests }
    except Exception, e:
        print 'Exception ',e
        data = { 'success': 'false' }
    return render(request,'cam-user/cam-new-booking.html', data)


def cam_booking_detail_display(request):
    if not request.user.is_authenticated():
        return redirect('/corporate/?next='+request.path)
    store_user_track(request,"Customer Booking Details Page")   # for tracking user activity
    try:
        if request.GET.get('booking_id'):
            v_booking_id = request.GET.get('booking_id')
            cam_booking_obj = Booking.objects.get(booking_unique_id=v_booking_id)
            if cam_booking_obj.booking_status == BOOKING_OPEN:
                return render(request,'cam-user/cam-booking-details.html', get_booking_details(v_booking_id))
            else:
                return render(request,'cam-user/booking-completed-cancelled-booked.html', get_booking_details(v_booking_id))
        else:
            print 'Hello'
            data = {'success': 'false'}
    except Exception, e:
        print 'Exception : ', e
        data = { 'success': 'false','error_message': 'Internal Server Error' }
    return render(request,'cam-user/cam-error-page.html', data)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def cam_booking_confirm_page(request):
    """
    This request method will redirect to booking details page,
    where user can view/add guest Detail and confirms the booking details.
    Also This is used for to confirm the booking details which is registered from
    Mobile app.
    """
    store_user_track(request,"Customer Booking Confirm Page")   # for tracking user activity

    if not request.user.is_authenticated():
        return redirect('/corporate/')
    try:
        if request.GET.get('booking_id'):
            booking_id = request.GET.get('booking_id')
            return render(request,'cam-user/cam-new-booking.html', get_booking_details(booking_id) )
            #return render(request,'cam-user/cam-booking-confirmed-page.html', get_booking_details(booking_id) )
        else:
            print 'Hello'
            data = { 'success': 'false'}
    except Exception, e:
        print 'Exception : ', e
        data = { 'success': 'false'}
    return render(request,'cam-user/cam-new-booking.html', data)


def get_available_rooms_for_cam_booking(request):
    filter_args={}
    try:
        print 'Hello'
        if request.GET.get('city_name'):
            filter_args['property_location__icontains']  =   request.GET.get('city_name')
        filter_args['property_availability_status']=True
        
        property_list = Property.objects.filter(**filter_args)
        
        # This code added on 04 Aug 2014 on demand of Prashant G, room rate according to Customer Rate.
        available_room_list = []
        
        cam_user= Customer.objects.get(id=request.session['user_id']) # Customer obj for rates
        property_rate =  999.00
        
        for property in property_list:
            property_rate_list = {}
            property_rates = CAMPropertyRate.objects.filter(property_id=property, cust_id=cam_user)
            for rate in property_rates:
                if rate.occupancy_type == 0:
                    property_rate_list.update({ 'single' : rate.agreed_rate })
                if rate.occupancy_type == 1:
                    property_rate_list.update({ 'double' : rate.agreed_rate })
                if rate.occupancy_type == 2:
                    property_rate_list.update({ 'additional' : rate.agreed_rate })
            
            #room_detail = get_property_info(property)   # This will prepare the property info
            room_detail =  {
                'city_name':property.property_city, 'room_id': property.property_id,
                'apartment_name': property.property_actual_name, 'apartment_address': property.property_location,
                'location': property.property_location, 'corporate_rates': property_rate_list,
                'room_image': SERVER_MEDIA_URL + '/static/media/rooms/paris.jpg',
                'info' : '<a marked="1" onClick="showDetails(this)"><i class="fa-2x pe-7s-info text-info"></i></a>',
                'book' : '<a onClick="goForBooking('+ str(property.property_id) +')" marked="1"><i class="fa-2x pe-7s-angle-right-circle text-success"></i></a>'
            }
            available_room_list.append(room_detail)
            
        data = {'success':'true', 'data': available_room_list }
        print data
        # data = {'success':'true', 'data': [room.get_apt_room_details_for_cam_booking() for room in room_list] }
    except Exception, e:
        print 'Exception ',e
        data = { 'success':'false', 'error_message': 'Server Error - Unable to Process request' }
    return HttpResponse(json.dumps(data), content_type='application/json')


@csrf_exempt
@transaction.atomic
def cam_save_booking_details(request):
    if not request.user.is_authenticated():
        return redirect('/corporate/')
    sid = transaction.savepoint()
    #pdb.set_trace()
    try:
        print 'Request Accepted '
        store_user_track(request, "Customer Saving Booking details")   # for tracking user activity
        if request.method == "POST":
            v_cam_id        = request.session['user_id']
            guest_name      = request.POST.get('guest_name')
            guest_phone     = request.POST.get('phone_number')
            v_guest_email   = request.POST.get('email_id')
            var_property_id = request.POST.get('property_id')
            occupancy_type  = int(request.POST.get('occupancy_type'))
            check_in    = datetime.datetime.strptime(request.POST.get('check_in'), '%d/%m/%Y')
            check_out   = datetime.datetime.strptime(request.POST.get('check_out'), '%d/%m/%Y')
            promocode   = request.POST.get('promocode')
            #amount      = request.POST.get('amount')
            #taxes       = request.POST.get('taxes')
            gross_amount= request.POST.get('gross_amount')
            
            guest_obj = Guest.objects.get(guest_id=guest_name)
            guest_obj.guest_contactno     = guest_phone
            guest_obj.guest_email         = v_guest_email
            guest_obj.save()
            
            # Getting Property Object
            property_obj = Property.objects.get(property_id=var_property_id)
            
            # Default Property Rate if it is not decided for CAM.
            default_rate = PropertyRate.objects.get(property_id=property_obj)
            occupancy_rate =0
        
            # Customer Object
            cam_obj= Customer.objects.get(id=v_cam_id)
            # This is for fetching property rates and applying rates according to occupancy type
            property_rates = CAMPropertyRate.objects.filter(property_id=property_obj, cust_id=cam_obj)
            if property_rates:
                for rate in property_rates:
                    if int(rate.occupancy_type) == int(occupancy_type):
                        occupancy_rate = rate.agreed_rate
            else:
                if occupancy_type == 0:
                    occupancy_rate = default_rate.single_occupancy_display_rate
                else:
                    occupancy_rate = default_rate.double_occupancy_display_rate
            
            days = check_out - check_in
            if days.days == 0:
                day = 1
            else:
                day = days.days
                
            booking_obj = Booking(
                customer_id      = cam_obj,
                guest_id    = guest_obj,
                property_id   = property_obj,
                booking_estimated_checkin_date = check_in,
                booking_actual_checkin_date = check_in,
                booking_estimated_checkout_date = check_out,
                booking_actual_checkout_date = check_out,
                booking_estimated_checkout_time = datetime.datetime.now().time(),
                booking_estimated_checkin_time = datetime.datetime.now().time(),
                booking_estimated_no_of_day_stay = days.days,
                booking_actual_no_of_day_stay = day,
                booking_status  = BOOKING_OPEN, #BOOKING_BOOKED
                booking_rate    = occupancy_rate
            )
            booking_obj.save()
            booking_obj.booking_unique_id = 'BK' +  datetime.date.today().strftime('%d%m%y') + 'G' + str(guest_obj.guest_id) + str(booking_obj.booking_id).zfill(6)
            booking_obj.save()
            
            # Generating Invoice
            
            amount = occupancy_rate * day
            service_tax_amount = ( amount * SERVICE_TAX )/100
            luxury_tax_amount  = ( amount * LUXURY_TAX )/100
        
            tax_amount = service_tax_amount + luxury_tax_amount
            gross_amount = amount + tax_amount
            invoice = Invoice(
                booking_id = booking_obj,
                room_charges = amount,
                invoice_total_amount = amount,
                tax_amount  = tax_amount,
                invoice_gross_amount = gross_amount,
                invoice_status = 0,
            )
            invoice.save()
            invoice.invoice_unique_id = 'INVBK' + str(booking_obj.booking_id) + str(invoice.invoice_id).zfill(6)
            invoice.save()
            
            corporate_transaction = CorporateTransaction(
                invoice_id      = invoice.invoice_unique_id,
                corporate_id    = cam_obj,
                transaction_amount= invoice.invoice_gross_amount,
                transaction_type = 1
            )
            corporate_transaction.save()
            
            # This is for Booking Statistics added on 11 Dec 2015
            booking_stat = UserBookingStatisticTrack(
                user_id = cam_obj,
                booking_path = request.path,
                booking_date = datetime.date.today(),
                booking_id = booking_obj
            )
            booking_stat.save()
            transaction.savepoint_commit(sid)
            try:
                # Sending SMS to vendot regarding booking submission
                send_booking_submission_sms_to_vendor(property_obj.property_owner_id.cust_contact_no, property_obj.property_owner_id.cust_first_name,
                    booking_obj.booking_unique_id, property_obj.property_actual_name,  booking_obj.booking_id)
                # Sending Booking Submission SMS to Corporate User
                send_booking_submission_sms_to_customer(cam_obj.cust_contact_no, cam_obj.cust_first_name, booking_obj.booking_unique_id)
                # Sending Booking Submission Email to Corporate User
                send_booking_submission_mail_with_template(booking_obj.booking_id)
            except Exception as err:
                print 'SMS/ Email not sent to vendor/ customer / '
            return redirect('/corporate/cam-booking-details/?booking_id='+ str(booking_obj.booking_unique_id))
        else:
            print 'Hello'
            transaction.savepoint_rollback(sid)
            data = {'success':'false', 'error_message':'Invalid Request'}
    except Exception, e:
        print 'Error ', e
        transaction.savepoint_rollback(sid)
        data = {'success':'false', 'error_message':'Server Error- Please Try Again'}
    #return render(request,'cam-user/cam-booking-confirmed-page.html', data )
    return render(request,'cam-user/cam-error-page.html', data )


# This returns a list of guest of respe
def get_corporate_guest_list(cam_id):
    guest_list = []

    try:
        print 'Guest List '
        #bookings = Booking.objects.filter(cam_id=Customer.objects.get(id=4))
        guests = Guest.objects.filter(customer_id=Customer.objects.get(id=cam_id))
        for guest in guests:
            guest_list.append(guest.get_guest_info())
        data = { 'success':'true', 'data': guest_list }
    except Exception, e:
        print 'Exception ',e
        data = { 'data': guest_list }
    return data

# This function returns a guest list of Customer @deprecated
def get_cam_guest_list(request):
    cam_id = request.session['user_id']
    data = get_corporate_guest_list(cam_id)
    return HttpResponse(json.dumps(data), content_type='application/json')
    

@csrf_exempt
@transaction.atomic
def save_guest_information(request):
    print "save_guest_information"
    sid = transaction.savepoint()
    try:
        store_user_track(request, "Customer Adding new Guest")   # for tracking user activity
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


@csrf_exempt
def update_guest_information(request):
    
    try:
        store_user_track(request, "Customer Updating Guest Details")   # for tracking user activity
        if request.method == "POST":
            var_guest_id = request.POST.get('edit_guest_id')
            guest_obj = Guest.objects.get(guest_id = var_guest_id)
            guest_obj.guest_first_name = request.POST.get('edit_guest_name')
            guest_obj.guest_email = request.POST.get('edit_guest_email')
            guest_obj.guest_contactno = request.POST.get('edit_phone_number')
            guest_obj.guest_status = request.POST.get('edit_guest_active_status')
            guest_obj.save()
            data = {'success': 'true'}
        else:
            print 'Invalid Request'
            data = {'sucess': 'false' , ExceptionLabel.ERROR_MESSAGE :'Invalid Request'}
    except Exception, e:
        print 'error',e
        data = {'sucess': 'false', ExceptionLabel.ERROR_MESSAGE :'Server Error'}
    return HttpResponse(json.dumps(data), content_type='application/json')

# This is for getting guest details 
def get_guest_details(request):
    print "get_guest_details"
    print request
    try:
        print 'Guest Details'
        guest = Guest.objects.get(guest_id=request.GET.get('request_guest_id'))
        data = {'success':'true', 'email_id': guest.guest_email, 'phone_no': guest.guest_contactno, 'guest_name': guest.guest_first_name  }
    except Guest.DoesNotExist,e :
        print 'Exception : ',e
        data = { 'success': 'false', 'error_message': ''}
    return HttpResponse(json.dumps(data), content_type='application/json')
    

@csrf_exempt
def update_cam_profile_info(request):
    """
    This is for updating the cam Information
    """
    store_user_track(request, "Customer Updating Profile")   # for tracking user activity
    try:
        if request.method == "POST":
            print 'Request Accepted '
            cam_obj = Customer.objects.get(id= request.POST.get('cam_user_id'))

##            cam_obj.username = request.POST.get('user_name')
##            cam_obj.password = request.POST.get('passwd')
            cam_obj.cust_first_name = request.POST.get('first_name')
            cam_obj.cust_last_name = request.POST.get('last_name')
            cam_obj.cust_company_id = Company.objects.get(company_id=request.POST.get('company_name'))
            cam_obj.cust_email       = request.POST.get('cam_email')
            cam_obj.cust_contact_no  = request.POST.get('contact_number')
            cam_obj.cust_address_line   = request.POST.get('address_line')
            cam_obj.cust_city   = request.POST.get('city')
            #cam_obj.cam_state   = request.POST.get('state')
            #cam_obj.cam_country   = request.POST.get('country')
            cam_obj.cust_pincode   = request.POST.get('pincode')
            cam_obj.cust_gender   = request.POST.get('gender')
            cam_obj.cust_age   = request.POST.get('cam_age')
            cam_obj.email_alert_on   = request.POST.get('email_alert')
            cam_obj.sms_alert_on   = request.POST.get('sms_alert')

            cam_obj.save()
##            cam_obj.set_password(request.POST.get('passwd'))
##            cam_obj.save()
            data = {'success': 'true','cam':cam_obj, 'mode':'show' }
        else:
            print 'Invalid Request'
            data = {'sucess': 'false' , ExceptionLabel.ERROR_MESSAGE :'Invalid Request'}
        return redirect('../cam-my-profile/?profile='+cam_obj.cust_unique_id)
    except Exception, e:
        print 'error',e
        data = {'sucess': 'false', ExceptionLabel.ERROR_MESSAGE :'Server Error'}
    #return HttpResponseRedirect('')
    return render(request,'cam-user/cam-error-page.html',data, context_instance=RequestContext(request))


# This added on  Jul 16, 2015
@csrf_exempt
def cam_password_change(request):
    store_user_track(request, "Customer Password Change")   # for tracking user activity
    #pdb.set_trace()
    try:
        if request.method == 'POST':
            data ={}
            #json_obj=json.loads(request.body)
            # if new password and confirm password are mis-matched..!
            if request.POST.get('new_password') != request.POST.get('new_password'):
                data = { 'success' : 'false', ExceptionLabel.ERROR_MESSAGE:'New Password and Confirm Password Mis-matched!'} 
                return HttpResponse(json.dumps(data), content_type='application/json')
            
            user_obj = User.objects.get(id= request.session['user_id'])
            user = authenticate(username=user_obj.username, password= request.POST.get('current_password'))
            if user is not None:
                if user.is_active:
                    user.set_password(request.POST.get('new_password'))
                    user.save()
                    print 'succeess'
                    data= {'success' : 'true', ExceptionLabel.ERROR_MESSAGE:'Successfully Login'}
                else:
                    data= {'success' : 'false', ExceptionLabel.ERROR_MESSAGE:'User Is Not Active'}
            else:
                data= {'success' : 'false', ExceptionLabel.ERROR_MESSAGE:'Invalid Username or Password'}
        else:
            data= {'success' : 'false', ExceptionLabel.ERROR_MESSAGE:'Invalid Request'}
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
    


def get_specific_property_info(request):
    """ This is getting specific property information at the time of Booking search page """
    store_user_track(request, "Customer Views Property Information For Booking")   # for tracking user activity
    try:
        property_obj = Property.objects.get(property_id = request.GET.get('property_id'))
        
        pro_images = PropertyImage.objects.filter(property_id=property_obj)
        images = ''
        if pro_images:
            images = [image.image_name.url for image in pro_images]
        data = { 'success':'true', 'property_name': property_obj.property_actual_name, 'property_location' : property_obj.property_location,
         'images':images, 'facility_list' : [q for q in property_obj.property_facility.split(',') if q]}
    except Exception as e:
        print 'Exception '
        data = {}
    return HttpResponse(json.dumps(data), content_type='application/json')
