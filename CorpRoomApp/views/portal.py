
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
from django.core.mail import send_mail
from smtplib import SMTPException
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from django.core.mail import send_mail

from django.db.models import Q

from CorpRoomApp.models import *

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

SERVICE_TAX = 14.0
LUXURY_TAX = 4.0

CAM_USER_NAME = 'b2c'

OFFER_TARIFF = 499.00

APARTMENT_AVAILABILITY = 'AVAILABLE'

# Accessing the Common Functionality of Property
from CorpRoomApp.common_functionality import PropertyCommonFunctionality

# this function will return all the locations from database
def get_all_locations():
    data = []
    try:
        locations = Location.objects.all()
        data = [location.__unicode__() for location in locations]
    except Exception as e:
        print e
    return data

def index(request):
    #data = {'location_list': get_all_locations()}
    #print data
    return redirect('/corporate/')
    #return render(request,'web/index.html',data)


# This returns a property list to result page 

def search_properties(request):
    print '==== Searching Properties ===='
    filter_args={}
    try:
        print 'Hello'
        if request.GET.get('city_name'):
            filter_args['location__icontains']  =   request.GET.get('city_name')
        filter_args['property_availability_status']  =   APARTMENT_AVAILABILITY

        check_in  = request.GET.get('date_from')
        check_out = request.GET.get('date_to')

        additional_data = {
                "city_name" : request.GET.get('city_name'),
                "check_in" : request.GET.get('date_from'),
                "check_out" : request.GET.get('date_to'),
                "no_of_rooms" : request.GET.get('no_of_rooms'),
                "no_of_adults": request.GET.get('no_of_adults'),
                "no_of_kids" : request.GET.get('no_of_kids')
        }

        request.session['additional_data']= additional_data

        print 'SESSION : ', request.session
        #pdb.set_trace()
        print additional_data
        print '-------'
        print 'no_of_rooms :', request.GET.get('no_of_rooms')
        print 'no_of_adults : ', request.GET.get('no_of_adults')
        room_list = PropertyRoom.objects.filter(Q(apartment_id = Property.objects.filter(**filter_args)))
        count = len(room_list)
        data = {'success':'true', 'count':count, 'no_of_rooms': int(request.GET.get('no_of_rooms')), 'no_of_adults': int(request.GET.get('no_of_adults')),  'property_list': [room.get_apt_room_details_for_admin_booking() for room in room_list],  'check_in': check_in, 'check_out': check_out }
        print 'Searched DAta ',data
        #return render(request, 'web/hotel-list-view.html', data)
    except Exception, e:
        print 'Exception ',e
        data = { 'success':'false', 'error_message': 'Server Error - Unable to Process request', 'property_list':[], 'check_in': check_in, 'check_out': check_out, 'no_of_rooms':request.GET.get('no_of_rooms'), 'no_of_adults':request.GET.get('no_of_adults') }
    return render(request, 'web/hotel-list-view.html', data)


def test_search(request):
    try:
        print 'submitting request======>'
        data = {}
    except Exception, e:
        print 'Exception ',e
        data = { 'success':'false', 'count':count, 'error_message': 'Server Error - Unable to Process request', 'property_list':[], 'check_in': check_in, 'check_out': check_out  }
    return render(request, 'web/hotel-list-view.html', data)



# This is redirect to booking page where user can see the details of Property
# and Enter the occupant details
def booking_page(request):
    try:
        print 'Booking page Opening'
        apartmentroom = PropertyRoom.objects.get(apt_room_id=request.GET.get('prop_id'))
        additional_data = request.session['additional_data']
        print 'Additional Data : ',additional_data
        
        if additional_data['check_in']!='None' or additional_data['check_in']!='' :
            check_in_date = datetime.datetime.strptime(additional_data['check_in'], '%m/%d/%Y')
            check_out_date = datetime.datetime.strptime(additional_data['check_out'], '%m/%d/%Y')
        else :
            check_in_date = datetime.datetime.strptime(request.GET.get('check_in'), '%m/%d/%Y')
            check_out_date = datetime.datetime.strptime(request.GET.get('check_out'), '%m/%d/%Y')

        d = check_out_date - check_in_date
        days =0
        if d.days == 0: # this is for single day booking
            days = 1
            amount = 1 * apartmentroom.room_general_rate
        else:
            days = d.days
            amount = (d.days) * apartmentroom.room_general_rate
    
        service_tax_amount = ( amount * SERVICE_TAX )/100
        luxury_tax_amount  = ( amount * LUXURY_TAX )/100
    
        tax_amount = service_tax_amount + luxury_tax_amount
        gross_amount = amount + tax_amount
    
        invoice = {
            'room_rate' : apartmentroom.room_general_rate,
            'service_tax_amount' : service_tax_amount,
            'luxury_tax_amount':luxury_tax_amount,
            'amount': amount,
            'days' : days,
            'tax_amount' : tax_amount,
            'gross_amount': gross_amount
        }
        additional_data.update({'room_id' : apartmentroom.apt_room_id})
        additional_data.update({'invoice' : invoice})
        request.session['additional_data'] = additional_data
        data = {
            'property_name' : apartmentroom.apartment_id.apt_name, 'property_address' : apartmentroom.apartment_id.get_apartment_address(),
            'no_of_nights': str(d.days), 'check_in_date' : check_in_date.strftime('%b %d, %Y'),
            'check_out_date' : check_out_date.strftime('%b %d, %Y'), 'room_type': apartmentroom.room_type,
            'invoice': invoice , 'room_image': SERVER_MEDIA_URL + apartmentroom.apt_room_images1.url,
            'check_in' : check_in_date.strftime('%m/%d/%Y'), 'check_out' : check_out_date.strftime('%m/%d/%Y'),
        }
        print data
    except Exception, e:
        print 'WEB PORTAL - Exception :',e
        data = {}
    return render(request,'web/booking-page.html',data)


@csrf_exempt
@transaction.atomic
def save_portal_booking(request):
    pdb.set_trace()
    print 'Saving Portal Booking'
    sid = transaction.savepoint()
    try:
        print 'Booking Details'
        v_first_name = request.POST.get('firstName')
        v_last_name = request.POST.get('lastName')
        email_id = request.POST.get('emailId')
        confirm_email = request.POST.get('confirmEmail')
        country_code = request.POST.get('countryCode')
        phone_number = request.POST.get('phoneNumber')
        #country_code = request.POST.get('countryCode')
        additional_data = request.session['additional_data']
        
        cam_obj = CAM.objects.get(username= CAM_USER_NAME)
        guest_obj = Guest(
                guest_first_name    = v_first_name +' '+ v_last_name,
                guest_last_name     = v_last_name,
                guest_contactno     = phone_number,
                guest_email         = email_id,
                guest_status        = GUEST_ACTIVE,
                cam_id              = cam_obj,
                guest_creation_date = datetime.datetime.now()
        )
        
        guest_obj.save()
        guest_obj.guest_unique_id = 'CAMGST' +  str(cam_obj.id) + str(guest_obj.guest_id).zfill(6)
        guest_obj.save()
        
        room_obj = PropertyRoom.objects.get(apt_room_id= additional_data['room_id'])
    
        booking_obj = CAMBooking(
            cam_id = cam_obj,
            guest_id    = guest_obj,
            apartment   = room_obj.apartment_id,
            aptroom_id  = room_obj,
            cam_booking_estimated_checkin_date = datetime.datetime.strptime(request.POST.get('check_in'), '%m/%d/%Y'),
            cam_booking_estimated_checkout_date = datetime.datetime.strptime(request.POST.get('check_out'), '%m/%d/%Y'),

            cam_booking_actual_checkin_date = datetime.datetime.strptime(request.POST.get('check_in'), '%m/%d/%Y'),
            cam_booking_actual_checkout_date = datetime.datetime.strptime(request.POST.get('check_out'), '%m/%d/%Y'),

            cam_booking_estimated_checkout_time = datetime.datetime.now().time(),
            cam_booking_estimated_checkin_time = datetime.datetime.now().time(),

            cam_booking_status  = BOOKING_OPEN,
            cam_booking_estimated_no_of_day_stay = days,
            cam_booking_actual_no_of_day_stay = days
        )
        booking_obj.save()
        booking_obj.booking_unique_id = 'BK' +  datetime.date.today().strftime('%d%m%y') + 'A' + str(room_obj.apartment_id.apt_id) + 'G' + str(guest_obj.guest_id) + str(booking_obj.cam_booking_id).zfill(6)
        # <DDMMYY>A<APTSrNO>G<GuestSrNo>XXXX
        booking_obj.save()
        invoice_details = additional_data['invoice']
        
        invoice = Invoice(
            cam_booking_id = booking_obj,
            room_charges    = invoice_details['amount'],
            invoice_total_amount = invoice_details['amount'],
            tax_amount  = invoice_details['tax_amount'],
            invoice_gross_amount = invoice_details['gross_amount'],
            invoice_status = 'UNPAID'
        )
        invoice.save()

        data = {
            'booking_number': booking_obj.booking_unique_id,
            'full_name' : guest_obj.guest_first_name,
            'email_address' : guest_obj.guest_email,
            'address'   : room_obj.apartment_id.apt_address,
            'city'      : room_obj.apartment_id.apt_city,
            'zipcode'   : room_obj.apartment_id.apt_pincode,
            'country'   : room_obj.apartment_id.apt_country,
        }
        transaction.savepoint_commit(sid)
        request.session['additional_data']=None
        send_booking_notification_mail(booking_obj.cam_booking_id) # To Admin
        send_booking_mail_to_customer(booking_obj.cam_booking_id) # To Customer 
        return redirect('/booking-details/?booking_number='+booking_obj.booking_unique_id)
    except Exception, e :
        print 'Exception : ',e
        data = {'success': 'Not Confirmed'}
        transaction.savepoint_rollback(sid)
        print data
    return render(request,'web/thank-you.html',data )

def show_portal_booking_details(request, *args):
    print 'Booking Number From : ',request.GET.get('booking_number')
    try:
        booking_details = CAMBooking.objects.get(booking_unique_id=request.GET.get('booking_number'))
        invoice = booking_details.cam_bookings.all()[0]
        data = {
            'booking_number': booking_details.booking_unique_id,
            'full_name' : booking_details.guest_id.guest_first_name,
            'email_address' : booking_details.guest_id.guest_email,
            'address'   : booking_details.aptroom_id.apartment_id.apt_address,
            'city'      : booking_details.aptroom_id.apartment_id.apt_city,
            'zipcode'   : booking_details.aptroom_id.apartment_id.apt_pincode,
            'country'   : booking_details.aptroom_id.apartment_id.apt_country,
            'room_rate' : booking_details.cam_booking_rate,
            'check_in'  : booking_details.cam_booking_actual_checkin_date.strftime('%d/%m/%Y'),
            'check_out' : booking_details.cam_booking_actual_checkout_date.strftime('%d/%m/%Y'),
            'nights_stay': booking_details.cam_booking_actual_no_of_day_stay,
            'room_charges' : invoice.room_charges,
            'taxes'     : invoice.tax_amount,
            'gross_amount':invoice.invoice_gross_amount
        }
    except CAMBooking.DoesNotExist, e:
        print 'Invalid Booking ID', e
        data = {'error_message' : 'Invalid booking ID' }
    except Exception, e:
        print 'Invalid Booking ID', e
        data = {'error_message' : 'Internal Server Error' }
    return render(request,'web/offer-thank-you.html',data )

    
def about_us_page(request):
    return render_to_response('web/about-us.html')
    
    
def contact_us_page(request):
    return render_to_response('web/contact-us.html')


def offer_booking_page(request):
    return render_to_response('web/offer-booking-page.html')



@csrf_exempt
@transaction.atomic
def save_august_portal_booking(request):
    #   pdb.set_trace()
    print 'Saving Portal Booking'
    sid = transaction.savepoint()
    try:
        print 'Booking Details'
        v_first_name = request.POST.get('firstName')
        v_last_name = request.POST.get('lastName')
        email_id = request.POST.get('emailId')
        confirm_email = request.POST.get('confirmEmail')
        country_code = request.POST.get('countryCode')
        phone_number = request.POST.get('phoneNumber')
        #country_code = request.POST.get('countryCode')
        
        cam_obj = CAM.objects.get(username= CAM_USER_NAME)
        guest_obj = Guest(
                guest_first_name    = v_first_name +' '+ v_last_name,
                guest_last_name     = v_last_name,
                guest_contactno     = phone_number,
                guest_email         = email_id,
                guest_status        = GUEST_ACTIVE,
                cam_id              = cam_obj,
                guest_creation_date = datetime.datetime.now()
        )
    
        guest_obj.save()
        guest_obj.guest_unique_id = 'CAMGST' +  str(cam_obj.id) + str(guest_obj.guest_id).zfill(6)
        guest_obj.save()
        
        room_obj = PropertyRoom.objects.get(apt_room_id=1)
    
        check_in_date = datetime.datetime.strptime(request.POST.get('checkInDate'), '%m/%d/%Y')
        check_out_date = datetime.datetime.strptime(request.POST.get('checkOutDate'), '%m/%d/%Y')

        d = check_out_date - check_in_date
        days = 1
        if d.days == 0: # this is for single day booking
            days = 1;
            amount = 1 * OFFER_TARIFF #apartmentroom.room_general_rate
        else:
            days = d.days
            amount = (d.days) * OFFER_TARIFF
    

# Creating Booking Objects and saving details
        booking_obj = CAMBooking(
            cam_id = cam_obj,
            guest_id    = guest_obj,
            apartment   = room_obj.apartment_id,
            aptroom_id  = room_obj,
            cam_booking_estimated_checkin_date = datetime.datetime.strptime(request.POST.get('checkInDate'), '%m/%d/%Y'),
            cam_booking_estimated_checkout_date = datetime.datetime.strptime(request.POST.get('checkOutDate'), '%m/%d/%Y'),
            cam_booking_estimated_checkout_time = datetime.datetime.now().time(),
            cam_booking_estimated_checkin_time = datetime.datetime.now().time(),
            cam_booking_actual_checkin_date = datetime.datetime.strptime(request.POST.get('checkInDate'), '%m/%d/%Y'),
            cam_booking_actual_checkout_date = datetime.datetime.strptime(request.POST.get('checkOutDate'), '%m/%d/%Y'),
            cam_booking_status  = BOOKING_OPEN,
            booking_remark = request.POST.get('areaName'),
            cam_booking_rate = OFFER_TARIFF,
            cam_booking_estimated_no_of_day_stay = days,
            cam_booking_actual_no_of_day_stay = days
        )
        booking_obj.save()
        booking_obj.booking_unique_id = 'BK' +  datetime.date.today().strftime('%d%m%y') + 'A' + str(room_obj.apartment_id.apt_id) + 'G' + str(guest_obj.guest_id) + str(booking_obj.cam_booking_id).zfill(6)
        booking_obj.save()

# Calculations for Invoice

        service_tax_amount = ( amount * SERVICE_TAX )/100
        luxury_tax_amount  = ( amount * LUXURY_TAX )/100
    
        v_tax_amount = service_tax_amount + luxury_tax_amount
        gross_amount = amount + v_tax_amount
        
# generating invoice
        invoice = Invoice(
            cam_booking_id = booking_obj,
            room_charges    = amount,
            invoice_total_amount = amount,
            tax_amount  = v_tax_amount,
            invoice_gross_amount = gross_amount,
            invoice_status = 'UNPAID'
        )
        invoice.save()
    
##        data = {
##            'booking_number': booking_obj.booking_unique_id,
##            'full_name' : guest_obj.guest_first_name,
##            'email_address' : guest_obj.guest_email,
##            'address'   : room_obj.apartment_id.apt_address,
##            'city'      : room_obj.apartment_id.apt_city,
##            'zipcode'   : room_obj.apartment_id.apt_pincode,
##            'country'   : room_obj.apartment_id.apt_country,
##            'room_rate' : OFFER_TARIFF,
##            'check_in'  : check_in_date.strftime('%d/%m/%Y'),
##            'check_out' : check_out_date.strftime('%d/%m/%Y'),
##            'nights_stay': days,
##            'taxes'     : v_tax_amount,
##            'gross_amount':gross_amount
##        }
        transaction.savepoint_commit(sid)
        send_booking_mail_to_customer(booking_obj.cam_booking_id)   # Mail to Customer
        send_booking_notification_mail(booking_obj.cam_booking_id)  # Mail to Admin for confirmation
        return redirect('/offer-booking-details/?booking_number='+booking_obj.booking_unique_id)
    except Exception, e :
        print 'Exception : ',e
        data = {'success': 'Not Confirmed'}
    #return redirect('show_booking_details', data )
        transaction.savepoint_rollback(sid)
        print data
    return render(request,'web/offer-thank-you.html',data )

def test_redirect(request):
    return redirect('/offer-booking-details/?booking_number='+'BK210815A2G12000005')


def show_offer_booking_details(request):
    print 'Booking Number From : ',request.GET.get('booking_number')
    try:
        booking_details = CAMBooking.objects.get(booking_unique_id=request.GET.get('booking_number'))
        invoice = booking_details.cam_bookings.all()[0]
        data = {
            'booking_number': booking_details.booking_unique_id,
            'full_name' : booking_details.guest_id.guest_first_name,
            'email_address' : booking_details.guest_id.guest_email,
            'address'   : booking_details.aptroom_id.apartment_id.apt_address,
            'city'      : booking_details.aptroom_id.apartment_id.apt_city,
            'zipcode'   : booking_details.aptroom_id.apartment_id.apt_pincode,
            'country'   : booking_details.aptroom_id.apartment_id.apt_country,
            'room_rate' : booking_details.cam_booking_rate,
            'check_in'  : booking_details.cam_booking_actual_checkin_date.strftime('%d/%m/%Y'),
            'check_out' : booking_details.cam_booking_actual_checkout_date.strftime('%d/%m/%Y'),
            'nights_stay': booking_details.cam_booking_actual_no_of_day_stay,
            'room_charges' : invoice.room_charges,
            'taxes'     : invoice.tax_amount,
            'gross_amount':invoice.invoice_gross_amount
        }
    except CAMBooking.DoesNotExist, e:
        print 'Invalid Booking ID', e
        data = {'error_message' : 'Invalid booking ID'}
    except Exception, e:
        print 'Invalid Booking ID', e
        data = {'error_message' : 'Internal Server Error'}
    return render(request,'web/offer-thank-you.html',data )
    

# This is method for sending mail to DAR Admin
def send_booking_notification_mail(booking_id):
    gmail_user = "info@dial-a-room.com"
    gmail_pwd = "Dial01"
    FROM = 'Dial-A-Room Booking Notification : <info@dial-a-room.com>'

    TO = [] #must be a list
    #mailid = request.GET.get('user_email')
    
    try:
        booking_obj = CAMBooking.objects.get(cam_booking_id=booking_id)
        TO.append('cs@dial-a-room.com')
        #TO.append('manoj.bawane@tungstenbigdata.com')
    except Exception, e:
        print e
    TO.append('vikas.padhy@dial-a-room.com')
    TO.append('info@dial-a-room.com')

    #TO.append('umang@tungstenbigdata.com')
    SUBJECT = "Confirmation of Property Booking"
    try:
        #user_name = request.GET.get('username')
        try:
            TEXT = "HI Team,\n\nNew Booking Has been Submitted to our system."
            TEXT = TEXT + "\nThe Booking Details are :"
            TEXT = TEXT + "\n      Booking ID : "+str(booking_id)
            TEXT = TEXT + "\n      Booking Reference # : "+ booking_obj.booking_unique_id
            TEXT = TEXT + "\n      Guest Name  : " + booking_obj.guest_id.guest_first_name + ' '+ booking_obj.guest_id.guest_first_name
            TEXT = TEXT + "\n      Check In Date : " + booking_obj.cam_booking_estimated_checkin_date.strftime('%d/%m/%Y')
            TEXT = TEXT + "\n      Check Out Date : " + booking_obj.cam_booking_estimated_checkout_date.strftime('%d/%m/%Y')
            TEXT = TEXT + "\n\n Please Make a Booking Confirmation "

            # Prepare actual message
            message = """From: %s\nTo: %s\nSubject: %s\n\n%s """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
            #server = smtplib.SMTP(SERVER)
            server = smtplib.SMTP_SSL() #or port 465 doesn't seem to work!
            server.connect("secure43.webhostinghub.com", 465)
            server.ehlo()
            #server.ssltls()
            server.login(gmail_user, gmail_pwd)
            server.sendmail(FROM, TO, message)
            server.quit()
            print 'successfully sent the mail'
            data =  {'success': 'true', 'message': 'Email has been sent to your email Id'}
        except User.DoesNotExist,e:
            data = {'success': 'false', 'error_message': 'User Name Is Not Registered'}
    except SMTPException,e:
        print "failed to send mail", e
        data = {'success': 'false'}
        


# This is for sending mail to customer who booked a room
def send_booking_mail_to_customer(booking_id):
    gmail_user = "info@dial-a-room.com"
    gmail_pwd = "Dial01"
    FROM = 'Dial-A-Room : <info@dial-a-room.com>'

    TO = [] #must be a list
    #mailid = request.GET.get('user_email')
    
    try:
        booking_obj = CAMBooking.objects.get(cam_booking_id=booking_id)
        TO.append('cs@dial-a-room.com')
        #TO.append('manoj.bawane@tungstenbigdata.com')
        TO.append(booking_obj.guest_id.guest_email)    # guest mail id
        TO.append('info@dial-a-room.com')

        #TO.append('umang@tungstenbigdata.com')
        SUBJECT = "Dial-A-Room Booking Details"
        try:
            #user_name = request.GET.get('username')
            try:
                TEXT = "Dear %s,"%(booking_obj.guest_id.guest_email)
                
                TEXT = TEXT + "\n Thank you for choosing Dial-A-Room! We welcome you to our world of Comfort Convenience!"
                TEXT = TEXT + "\n Kindly note your Booking Details as appended below. We request you to quote the Booking Number given below in your future communication with us."
                
                TEXT = TEXT + "\n\n      BOOKING DETAILS : "
                TEXT = TEXT + "\n      Booking ID : "+ booking_obj.booking_unique_id
                TEXT = TEXT + "\n      Guest Name  : " + booking_obj.guest_id.guest_first_name
                TEXT = TEXT + "\n      Check In Date : " + booking_obj.cam_booking_estimated_checkin_date.strftime('%d/%m/%Y')
                TEXT = TEXT + "\n      Check Out Date : " + booking_obj.cam_booking_estimated_checkout_date.strftime('%d/%m/%Y')
                TEXT = TEXT + "\n      HOTEL DETAILS :" 
                TEXT = TEXT + "\n      HOTEL ADDRESS :" + booking_obj.apartment.get_apartment_address()
                TEXT = TEXT + "\nPlease note that this is not a confirmation of your booking. You will receive a Confirmation Email as soon as your booking is confirmed."
                TEXT = TEXT + "\n\nThank you for choosing Dial-A-Room!"

                # Prepare actual message
                message = """From: %s\nTo: %s\nSubject: %s\n\n%s """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
                #server = smtplib.SMTP(SERVER)
                server = smtplib.SMTP_SSL() #or port 465 doesn't seem to work!
                server.connect("secure43.webhostinghub.com", 465)
                server.ehlo()
                #server.ssltls()
                server.login(gmail_user, gmail_pwd)
                server.sendmail(FROM, TO, message)
                server.quit()
                print 'successfully sent the mail'
                data =  {'success': 'true', 'message': 'Email has been sent to your email Id'}
            except User.DoesNotExist,e:
                data = {'success': 'false', 'error_message': 'User Name Is Not Registered'}
        except SMTPException,e:
            print "failed to send mail", e
            data = {'success': 'false'}
    except Exception, e:
        print e
        
        

def test_method():
    
    today = datetime.datetime.today()

    start_date = date(today.year, today.month, 01)
    print "start_date"
    print start_date

    end_date = date(today.year, today.month-6, 01)
    print end_date

    cam_obj=CAM.objects.get(id='120')

    monthly_bookings=CAMBooking.objects.filter(cam_id=cam_obj,cam_booking_estimated_checkin_date__range=[start_date, end_date] ).extra(select={'month': "EXTRACT(month FROM cam_booking_estimated_checkin_date)"}).values('month').annotate(total=Count('cam_booking_id'))
    print monthly_bookings
