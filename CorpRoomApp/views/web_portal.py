
"""
__author__      = 'ManojB'
__version__     = '0.0.1'
__created_date__ = '10-08-2015'
This module is related to WEB site and all the operations.
"""

from django.shortcuts import render_to_response
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect
from django.db import transaction
import datetime
import smtplib
import json
from django.core.mail import send_mail
from smtplib import SMTPException
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.http import HttpResponse

from django.core.mail import send_mail

from django.db.models import Q

from CorpRoomApp.models import *

SERVER_MEDIA_URL = 'http://192.168.0.121:8000'

#SERVER_MEDIA_URL = 'http://ec2-52-4-20-173.compute-1.amazonaws.com'

# Booking Constants
BOOKING_ALL         = 0
BOOKING_OPEN        = 1
BOOKING_BOOKED      = 2
BOOKING_CANCELLED   = 3
BOOKING_COMPLETED   = 4

GUEST_ACTIVE    = 1
GUEST_INACTIVE  = 0

AVAILABLE_ROOM  = 0

SERVICE_TAX = 14.0
LUXURY_TAX = 4.0

PAID = '1'
UNPAID = '0'

APARTMENT_AVAILABILITY = True

# Accessing the Common Functionality of Property
from CorpRoomApp.common_functionality import PropertyCommonFunctionality
from CorpRoomApp.send_sms import *
# This returns a property list to result page 
def search_properties(request):
    print '==== Searching Properties ===='

    filter_args={}
    pcf = PropertyCommonFunctionality()
    try:
        check_in  = request.GET.get('date_from')
        check_out = request.GET.get('date_to')
    
        additional_data = {
            "city_name" : request.GET.get('city_name'),
            "check_in" : request.GET.get('date_from'),
            "check_out" : request.GET.get('date_to'),
            "no_of_rooms" : request.GET.get('no_of_rooms'),
            "no_of_adults": request.GET.get('no_of_adults'),
        }
        request.session['additional_data']= additional_data # Store all the details in session
        
        room_list = pcf.get_searched_property_details(**additional_data)
        count = len(room_list)
        data = {'success':'true', 'count':count, 'no_of_rooms': int(request.GET.get('no_of_rooms')), 'no_of_adults': int(request.GET.get('no_of_adults')),  'property_list': room_list,  'check_in': check_in, 'check_out': check_out , 'location_list' : pcf.get_all_location_list() }
        #return render(request, 'web/hotel-list-view.html', data)
    except Exception, e:
        print 'Exception ',e
        data = { 'success':'false', 'error_message': 'Server Error - Unable to Process request', 'property_list':[], 'check_in': check_in, 'check_out': check_out, 'no_of_rooms':request.GET.get('no_of_rooms'), 'no_of_adults':request.GET.get('no_of_adults'), 'location_list' : pcf.get_all_location_list() }
    return render(request, 'web/hotel-list-view.html', data)



# This is redirect to booking page where user can see the details of Property
# and Enter the occupant details
def booking_page(request):
    #pdb.set_trace()
    try:
        print 'Booking page Opening'
        property = Property.objects.get(property_id=request.GET.get('prop_id'))
        additional_data = request.session['additional_data']
        print 'Additional Data : ',additional_data
        
        if additional_data['check_in']!='None' or additional_data['check_in']!='' :
            check_in_date = datetime.datetime.strptime(additional_data['check_in'], '%d/%m/%Y')
            check_out_date = datetime.datetime.strptime(additional_data['check_out'], '%d/%m/%Y')
        else :
            check_in_date = datetime.datetime.strptime(request.GET.get('check_in'), '%d/%m/%Y')
            check_out_date = datetime.datetime.strptime(request.GET.get('check_out'), '%d/%m/%Y')

        # fetch Property Rates
        rates = PropertyRate.objects.get(property_id=property)
        single_rate = rates.single_occupancy_display_rate
        double_rate = rates.double_occupancy_display_rate
        additional_rate = rates.additional_occupancy_display_rate
        
        d = check_out_date - check_in_date
        days =0
        if d.days == 0: # this is for single day booking
            days = 1
        else:
            days = d.days
        
        # Room Calculation
        no_of_rooms = additional_data['no_of_rooms']
        no_of_persons = additional_data['no_of_adults']
        
        amount = 0
        if no_of_rooms == no_of_persons: 
            amount = days * int(no_of_rooms) * single_rate
            
        if no_of_persons > no_of_rooms:
            per_rem = int(no_of_persons) % 2
            persons = int(no_of_persons) / 2
            
            room_rem = int(no_of_rooms) % 2
            room_nos = int(no_of_rooms) / 2
            
            amount = persons * double_rate * days
            amount  =  amount + (per_rem * single_rate * days)

        service_tax_amount = ( amount * SERVICE_TAX )/100
        luxury_tax_amount  = ( amount * LUXURY_TAX )/100
    
        tax_amount = service_tax_amount + luxury_tax_amount
        gross_amount = amount + tax_amount
    
        invoice = {
            'single_room_rate' : single_rate,
            'double_room_rate' : double_rate,
            'service_tax_amount' : service_tax_amount,
            'luxury_tax_amount':luxury_tax_amount,
            'amount': amount,
            'days' : days,
            'tax_amount' : tax_amount,
            'gross_amount': gross_amount
        }
        additional_data.update({'room_id' : property.property_id})
        additional_data.update({'invoice' : invoice})
        request.session['additional_data'] = additional_data
        data = { 'property_name' : property.property_display_name, 'property_id': property.property_id , 'property_address' : property.property_address,
            'no_of_nights': str(d.days), 'check_in_date' : check_in_date.strftime('%b %d, %Y'), 'no_of_persons': no_of_persons,
            'check_out_date' : check_out_date.strftime('%b %d, %Y'), 'invoice': invoice, 'no_of_rooms': no_of_rooms,
            'room_image': SERVER_MEDIA_URL + '/static/media/rooms/paris.jpg', 'check_out' : check_out_date.strftime('%d/%m/%Y'),
            'check_in' : check_in_date.strftime('%d/%m/%Y') }
        print data
    except Exception, e:
        print 'WEB PORTAL - Exception :',e
        data = {}
    return render(request,'web/booking-page.html',data)


# Save booking details
@csrf_exempt
@transaction.atomic
def save_booking_with_payment(request):
    print 'Saving Portal Booking'

    try:
        print '======== REQUEST ===============>'
        print request.POST
        print '=======================>'
        v_first_name = request.POST.get('frmGuestFName')
        v_last_name = request.POST.get('frmGuestLName')
        email_id = request.POST.get('frmEmailId')
##        confirm_email = request.POST.get('confirmEmail')
##        country_code = request.POST.get('countryCode')
        phone_number = request.POST.get('frmPhoneNumber')
        
        # Saving Guest Details 
        guest_obj = Guest(
                guest_first_name    = v_first_name +' '+ v_last_name,
                guest_last_name     = v_last_name,
                guest_contactno     = phone_number,
                guest_email         = email_id,
                guest_status        = GUEST_ACTIVE,
                guest_creation_date = datetime.datetime.now()
        )
        guest_obj.save()
        guest_obj.guest_unique_id = 'GST' + str(guest_obj.guest_id).zfill(6)
        guest_obj.save()
        
        # Saving Booking details
        property = Property.objects.get(property_id=request.POST.get('frmPropertyId'))
        
        booking_obj = Booking(
            guest_id    = guest_obj,
            property_id   = property,
            number_of_rooms = request.POST.get('frmNoOfRooms'),
            number_of_person = request.POST.get('frmNoOfPersons'),
            #booking_datetime = datetime.datetime.strptime(request.POST.get('frmBookingDate'), '%m/%d/%Y'),
            

            booking_estimated_checkin_date = datetime.datetime.strptime(request.POST.get('frmCheckIn'), '%d/%m/%Y'),
            booking_estimated_checkout_date = datetime.datetime.strptime(request.POST.get('frmCheckOut'), '%d/%m/%Y'),

            booking_actual_checkin_date = datetime.datetime.strptime(request.POST.get('frmCheckIn'), '%d/%m/%Y'),
            booking_actual_checkout_date = datetime.datetime.strptime(request.POST.get('frmCheckOut'), '%d/%m/%Y'),

            booking_estimated_checkout_time = datetime.datetime.now().time(),
            booking_estimated_checkin_time = datetime.datetime.now().time(),

            booking_status  = BOOKING_OPEN,
            booking_estimated_no_of_day_stay = request.POST.get('frmNoOfNightsStay'),
            booking_actual_no_of_day_stay = request.POST.get('frmNoOfNightsStay'),
            payment_status = 0,
            payment_method = request.POST.get('frmPaymentMethod'),
            booking_amount = request.POST.get('frmGrossBookingAmount')
        )
        booking_obj.save()
        booking_obj.booking_unique_id = 'BK' +  datetime.date.today().strftime('%d%m%y') + 'G' + str(guest_obj.guest_id) + str(booking_obj.booking_id).zfill(6)
        booking_obj.save()
        
        invoice = Invoice(
            booking_id = booking_obj,
            room_charges    = request.POST.get('frmBookingAmount'),
            invoice_total_amount = request.POST.get('frmBookingAmount'),
            tax_amount  = request.POST.get('frmTaxAmount'),
            invoice_gross_amount = request.POST.get('frmGrossBookingAmount'),
            invoice_status = 0,
            #invoice_paid_date = request.POST.get('frmBookingDate'),
        )
        invoice.save()
        invoice.invoice_unique_id = 'INVBK' + str(booking_obj.booking_id) + str(invoice.invoice_id).zfill(6)
        invoice.save()
        # message sending to customer
        #send_booking_submission_sms_to_customer(guest_obj.guest_contactno, booking_obj.booking_unique_id)
        
        data = {'success': 'true', 'booking_unique_id': str(booking_obj.booking_unique_id), 'booking_amount' : invoice.invoice_gross_amount }
    except Exception, e :
        print 'Exception : ',e
        data = {'success': 'false'}
        print data
    return  HttpResponse(json.dumps(data), content_type='application/json')

@csrf_exempt
@transaction.atomic
def save_booking_pay_at_checkout(request):
    print 'Saving Portal Booking'

    try:
        print '======== REQUEST ===============>'
        print request.POST
        print '=======================>'
        v_first_name = request.POST.get('frmGuestFName')
        v_last_name = request.POST.get('frmGuestLName')
        email_id = request.POST.get('frmEmailId')
##        confirm_email = request.POST.get('confirmEmail')
##        country_code = request.POST.get('countryCode')
        phone_number = request.POST.get('frmPhoneNumber')
        
        # Saving Guest Details 
        guest_obj = Guest(
                guest_first_name    = v_first_name +' '+ v_last_name,
                guest_last_name     = v_last_name,
                guest_contactno     = phone_number,
                guest_email         = email_id,
                guest_status        = GUEST_ACTIVE,
                guest_creation_date = datetime.datetime.now()
        )
        guest_obj.save()
        guest_obj.guest_unique_id = 'GST' + str(guest_obj.guest_id).zfill(6)
        guest_obj.save()
        
        # Saving Booking details
        property = Property.objects.get(property_id=request.POST.get('frmPropertyId'))
        
        booking_obj = Booking(
            guest_id    = guest_obj,
            property_id   = property,
            number_of_rooms = request.POST.get('frmNoOfRooms'),
            number_of_person = request.POST.get('frmNoOfPersons'),
            #booking_datetime = datetime.datetime.strptime(request.POST.get('frmBookingDate'), '%m/%d/%Y'),
            

            booking_estimated_checkin_date = datetime.datetime.strptime(request.POST.get('frmCheckIn'), '%d/%m/%Y'),
            booking_estimated_checkout_date = datetime.datetime.strptime(request.POST.get('frmCheckOut'), '%d/%m/%Y'),

            booking_actual_checkin_date = datetime.datetime.strptime(request.POST.get('frmCheckIn'), '%d/%m/%Y'),
            booking_actual_checkout_date = datetime.datetime.strptime(request.POST.get('frmCheckOut'), '%d/%m/%Y'),

            booking_estimated_checkout_time = datetime.datetime.now().time(),
            booking_estimated_checkin_time = datetime.datetime.now().time(),

            booking_status  = BOOKING_OPEN,
            booking_estimated_no_of_day_stay = request.POST.get('frmNoOfNightsStay'),
            booking_actual_no_of_day_stay = request.POST.get('frmNoOfNightsStay'),
            payment_status = 0,
            payment_method = request.POST.get('frmPaymentMethod'),
            booking_amount = request.POST.get('frmGrossBookingAmount')
        )
        booking_obj.save()
        booking_obj.booking_unique_id = 'BK' +  datetime.date.today().strftime('%d%m%y') + 'G' + str(guest_obj.guest_id) + str(booking_obj.booking_id).zfill(6)
        booking_obj.save()
        
        invoice = Invoice(
            booking_id = booking_obj,
            room_charges    = request.POST.get('frmBookingAmount'),
            invoice_total_amount = request.POST.get('frmBookingAmount'),
            tax_amount  = request.POST.get('frmTaxAmount'),
            invoice_gross_amount = request.POST.get('frmGrossBookingAmount'),
            invoice_status = 0,
            #invoice_paid_date = request.POST.get('frmBookingDate'),
        )
        invoice.save()
        invoice.invoice_unique_id = 'INVBK' + str(booking_obj.booking_id) + str(invoice.invoice_id).zfill(6)
        invoice.save()
        # message sending to customer
        send_booking_submission_sms_to_customer(guest_obj.guest_contactno, booking_obj.booking_unique_id)
        
        data = {'success': 'true', 'booking_unique_id': str(booking_obj.booking_unique_id), 'booking_amount' : invoice.invoice_gross_amount }
    except Exception, e :
        print 'Exception : ',e
        data = {'success': 'false'}
        print data
    return  HttpResponse(json.dumps(data), content_type='application/json')

# This function return the booking details to calable
def get_booking_details(booking_number):
    booking_details = Booking.objects.get(booking_unique_id=booking_number)
    invoice = Invoice.objects.get(booking_id=booking_details)
    return {
            'booking_number': booking_details.booking_unique_id,
            'full_name' : booking_details.guest_id.guest_first_name,
            'email_address' : booking_details.guest_id.guest_email,
            'phone_number' : booking_details.guest_id.guest_contactno,
            'address'   : booking_details.property_id.property_address,
            'city'      : booking_details.property_id.location,
            'zipcode'   : booking_details.property_id.property_pincode,
            #'room_rate' : booking_details.cam_booking_rate,
            'check_in'  : booking_details.booking_actual_checkin_date.strftime('%d/%m/%Y'),
            'check_out' : booking_details.booking_actual_checkout_date.strftime('%d/%m/%Y'),
            'nights_stay': booking_details.booking_actual_no_of_day_stay,
            'room_charges' : invoice.room_charges,
            'taxes'     : invoice.tax_amount,
            'gross_amount':invoice.invoice_gross_amount
        }

# This method is for showing the booking details
def show_portal_booking_details(request, *args):
    print 'Booking Number From : ',request.GET.get('booking_number')
    try:
        data =  get_booking_details(request.GET.get('booking_number'))
    except Booking.DoesNotExist, e:
        print 'Invalid Booking ID', e
        data = {'error_message' : 'Invalid booking ID' }
    except Exception, e:
        print 'Invalid Booking ID', e
        data = { 'error_message' : 'Internal Server Error' }
    return render( request, 'web/thank-you.html', data )

# This is for payment bookings
def show_confirmed_booking(request):
    """
    This is for showing payemnts booking. either payment failed status or payment success.
    """
    print 'Booking Number From : ',request.GET.get('booking_number')
    try:
        data = get_booking_details(request.GET.get('booking_number'))
        if request.GET.get('payment_status') == PAID:
            return render(request,'web/payment-success.html', data)
        else:
            return render(request,'web/payment-failed.html', data)
    except Booking.DoesNotExist, e:
        print 'Invalid Booking ID', e
        data = {'error_message' : 'Invalid booking ID' }
    except Exception, e:
        print 'Invalid Booking ID', e
        data = {'error_message' : 'Internal Server Error'}
    return render(request,'web/error-page.html',data )

"""
This method will call by url when customer first time failed online transaction,
and he select option for checkout.
"""
def checkout_after_payment_fail(request):
    try:
        booking_details = Booking.objects.get(booking_unique_id=request.POST.get('booking_number'))
        booking_details.payment_method = request.POST.get('frmPaymentMethod')
        booking_details.payment_status = UNPAID
        booking_details.save()
        data = {'success': 'true'}
        #return redirect('/booking-details/?booking_number='+request.POST.get('booking_number'))
    except Exception as e:
        print 'e'
        data = {'success': 'false'}
    return HttpResponse(json.dumps(data), content_type='application/json')
        #return redirect('/booking-details/?booking_number='+request.POST.get('booking_number'))
        
def just_test(request):
    data = { 'booking_reference_id' : 'BK240915G13000006'}
    return render(request, 'web/just-for-test.html',data)


def terms(request):
    return render(request, 'web/terms.html')
