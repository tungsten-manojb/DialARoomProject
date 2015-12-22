
from __future__ import unicode_literals
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.views.decorators.cache import cache_control

import traceback # This is for exception stack-trace

import MySQLdb, sys
import datetime
import time
import smtplib
from django.db.models import Count, Sum
from django.db.models import Max
import pdb
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_exempt
from django.utils.datastructures import MultiValueDictKeyError
import json
from django.contrib import auth
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
import random


# for sending emails
from django.core.mail import send_mail
from smtplib import SMTPException
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from django.core.mail import send_mail
import sendgrid
from DialARoomProject import settings

from CorpRoomApp.models import *
# Booking Constants
BOOKING_ALL         = '0'
BOOKING_BOOKED      = 1
BOOKING_COMPLETED   = 2

ADMIN = 0
CORPORATE = 1
OWNER = 2
RETAIL = 3


SERVER_MEDIA_URL = 'http://192.168.0.121:8000'
#SERVER_MEDIA_URL = 'http://dial-a-room.com'
#   SERVER_MEDIA_URL = 'http://ec2-52-4-20-173.compute-1.amazonaws.com'

gmail_user = "training.tungsten@gmail.com"
gmail_pwd = "Tungsten74"
FROM = 'Dial-A-Room App Admin'

def send_booking_confirmation_email(booking_id):

    TO = [] #must be a list
    #mailid = request.GET.get('user_email')
    
    try:
        booking_obj = CAMBooking.objects.get(cam_booking_id=booking_id)
        TO.append(booking_obj.customer_id.cam_email)
        TO.append(booking_obj.guest_id.guest_email)
    except Exception, e:
        print e
    TO.append('manoj.bawane@tungstenbigdata.com')
    #TO.append('prashant.girbane@gmail.com')
    #TO.append('umang@tungstenbigdata.com')
    SUBJECT = "Confirmation of Apartment Booking"
    try:
        #user_name = request.GET.get('username')
        try:
            TEXT = "HI Your Apartment is Booked.\n\n Your Apartment Booking Id is :"+ str(booking_id) 
            TEXT = TEXT + "\n\n Thank You "
            # Prepare actual message
            message = """From: %s\nTo: %s\nSubject: %s\n\n%s """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
            #server = smtplib.SMTP(SERVER)
            server = smtplib.SMTP("smtp.gmail.com", 587) #or port 465 doesn't seem to work!
            server.ehlo()
            server.starttls()
            server.login(gmail_user, gmail_pwd)
            server.sendmail(FROM, TO, message)
            server.close()
            print 'successfully sent the mail'
            data =  {'success': 'true', 'message': 'Email has been sent to your email Id'}
        except User.DoesNotExist,e:
            data = {'success': 'false', 'error_message': 'User Name Is Not Registered'}
    except SMTPException,e:
        print "failed to send mail", e
        data = {'success': 'false'}
        
    #return HttpResponse(json.dumps(data), content_type='application/json')
    
# This is testing purpose    
def sending_mail():
    try:
        TO.append('manoj.bawane@tungstenbigdata.com')
        msg = MIMEMultipart('alternative')
        msg['Subject'] = "TEST MAIL"
        msg['From'] = FROM
        msg['To'] = TO
        TEXT = "HI Your Apartment is Booked.\n\n Your Apartment Booking Id is :"
        html ="""<html><table>
                <tr>
                    <td>Chekc In Date</td>
                    <td>:</td>
                    <td>"""+ '12-12' + """</td>
                </tr>
                <tr>
                    <td>Check Out Date</td>
                    <td>:</td>
                    <td>"""+ '13-12' + """</td>
                </tr>
                <tr>
                    <td>Number Of Days Stayed </td>
                    <td>:</td>
                    <td>"""+ '1'+"""</td>
                </tr>
                <tr>
                    <td>Room Charges</td>
                    <td>:</td>
                    <td>"""+ '10' +"""</td>
                </tr>
                <tr>
                    <td>Total Amount</td>
                    <td>:</td>
                    <td> """+ '10' +"""</td>
                </tr>
                <tr align='center'>
                    <td colspan='3'> Thank you</td>
                </tr>
            </table>
            </html>"""
        
        part1 = MIMEText(TEXT, 'plain')
        part2 = MIMEText(html, 'html')
        
        msg.attach(part1)
        msg.attach(part2)
        
        server = smtplib.SMTP("smtp.gmail.com", 587) #or port 465 doesn't seem to work!
        server.ehlo()
        server.starttls()
        server.login(gmail_user, gmail_pwd)
        TEXT ="""
                ========== INVOICE DETAILS ============ 
                
                CHECK IN DATE   : """+ '12-12-2014' +"""

                CHECK OUT DATE  : """+ '12-12-2014' +"""

                NUMBER OF DAYS  : """+ '12-12-2014' +"""

                CHECK OUT DATE  : """+ '12-12-2014' +"""
                

                             THANK YOU
                ======================================= 
                """
        #message = """From: %s\nTo: %s\nSubject: %s\n\n%s """ % (FROM, ", ".join(TO), msg['Subject'], msg)
        server.sendmail(FROM, TO, msg)
        server.close()
        print 'successfully sent the mail'
        #send_mail('Hello, Test', email_text, 'Drifter App Developer', ['bawane.manoj03@gmail.com','manoj.bawane@tungstenbigdata.com'], fail_silently=False)
        print 'sent'
        data = {'success': 'true'}
    except Exception, e:
        print 'failed', e
        data ={'success': 'false', 'hello': 'failed'}
    return HttpResponse(json.dumps(data), content_type='application/json')
    

# This method for sending mail on CAM's email id, when the user request to send invoice on his mail
#def send_invoice_mail(booking_id,var_customer_id):
def send_invoice_mail(request):
    var_cam_id = request.GET.get('cam_user_id')
    booking_id = request.GET.get('cam_booking_id')
    TO = [] #['prashant.girbane@gmail.com']
    TO.append('manoj.bawane@tungstenbigdata.com')
    try:
        cam_booking_obj = CAMBooking.objects.get(cam_booking_id=booking_id, cam_id = var_cam_id)
        invoices = cam_booking_obj.cam_bookings.all()
        invoice = invoices[0]
        if cam_booking_obj.cam_booking_status == BOOKING_COMPLETED :
            print invoice
            days = cam_booking_obj.cam_booking_actual_no_of_day_stay
            rate = cam_booking_obj.aptroom_id.apt_room_rate
            total = days * rate
            total_invoice_amt = invoice.invoice_gross_amount
            TEXT ="""
            Hi """+ str(cam_booking_obj.cam_id )+"""
            Your Guest """ + str(cam_booking_obj.guest_id) + """ stayed at """+ str(cam_booking_obj.apartment) + """
                    
            The Invoice against the booking as Follows:
            
                    ========== INVOICE DETAILS ============ 

                    CHECK IN DATE-TIME   : """+ cam_booking_obj.cam_booking_actual_checkin_datetime.strftime('%a, %d %b %Y,  %I:%M %p') +"""

                    CHECK OUT DATE-TIME  : """+ cam_booking_obj.cam_booking_actual_checkout_datetime.strftime('%a, %d %b %Y,  %I:%M %p') +"""

                    NUMBER OF DAYS STAY  : """+ str(days) +"""

                    ROOM CHARGES         : """+ '{:,.2f}'.format(rate) +"""

                    TOTAL CHARGES        : """+ '{:,.2f}'.format(total_invoice_amt) +"""

                                    THANK YOU
                    ======================================= 
            
            
            This mail is system generated.
                    """
            SUBJECT = "Apartment Booking Invoice"
            server = smtplib.SMTP("smtp.gmail.com", 587) #or port 465 doesn't seem to work!
            server.ehlo()
            server.starttls()
            server.login(gmail_user, gmail_pwd)
            message = """From: %s\nTo: %s\nSubject: %s\n\n%s """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
            server.sendmail(FROM, TO, message)
            server.close()
            data = {'success' : 'true'}
        else:
            print 'error'
            data = {'success': 'false', 'error_message': 'The Booking Is not completed yet' }
    except Exception, e:
        print 'Exception : ', e
        data = {'success': 'false'}
    return HttpResponse(json.dumps(data), content_type='application/json')
    
# This is with the sendgrid template
def send_invoice_mail_with_template(request):
    #pdb.set_trace()
    sg = sendgrid.SendGridClient(settings.SENDGRID_USER_NAME,settings.SENDGRID_PASSWORD)

    # this is code for fetching the information of CAM user and its Booking with invoice
    var_cam_id = request.GET.get('cam_user_id')
    booking_id = request.GET.get('cam_booking_id')
    try:
        cam_booking_obj = CAMBooking.objects.get(cam_booking_id=booking_id, cam_id = var_cam_id)
        # Apartment details
        apartment_name          = cam_booking_obj.apartment.apt_name
        apartment_address       = cam_booking_obj.apartment.apt_address +', ' + cam_booking_obj.apartment.apt_city + ', '+ cam_booking_obj.apartment.apt_state + ', ' + cam_booking_obj.apartment.apt_country + '-' + cam_booking_obj.apartment.apt_pincode
        apartment_owner_name    = str(cam_booking_obj.apartment.apt_owner_id)
        
        # Room Details  cam_booking_obj.
        room_rate               = cam_booking_obj.aptroom_id.apt_room_rate
        room_number             = cam_booking_obj.aptroom_id.apt_room_number
        room_type               = 'Single Bed'  #cam_booking_obj.aptroom_id
        room_image_url          = SERVER_MEDIA_URL+ cam_booking_obj.aptroom_id.apt_room_images1.url
        
        # CAM details
        cam_user_name           = cam_booking_obj.cam_id.cam_first_name
        
        # Guest Details
        guest_name              = str(cam_booking_obj.guest_id)
        guest_rating            = str(cam_booking_obj.guest_rating)
        
        # Booking related details
        check_in_date           = cam_booking_obj.cam_booking_actual_checkin_date.strftime('%d-%b-%Y')
        check_out_date          = cam_booking_obj.cam_booking_actual_checkout_date.strftime('%d-%b-%Y')
        number_of_days_stayed   = cam_booking_obj.cam_booking_actual_no_of_day_stay
        
        # Invoice details
        invoices = cam_booking_obj.cam_bookings.all()
        invoice = invoices[0]
        
        invoice_date            = invoice.invoice_datetime.strftime('%d-%b-%Y')
        invoice_amount          = '{:,.2f}'.format(invoice.invoice_gross_amount)
        sub_total               = '{:,.2f}'.format(invoice.room_charges)
        
        # This is for sending mail 
        subject_line = 'Your Dial-A-Room Invoice for Booking ID :'+ str(cam_booking_obj.cam_booking_id)
        
        message = sendgrid.Mail()
        message.set_headers({'X-Sent-Using': 'SendGrid-API', 'X-Transport': 'web'})
##        to_mail = ['manoj.bawane@tungstenbigdata.com', 'prashant.girbane@gmail.com']
##        message.add_to(to_mail)
        message.set_tos(["prashant.girbane@gmail.com","vikas.padhy@tungstenbigdata.com", "manoj.bawane@tungstenbigdata.com"])
        message.set_subject(subject_line)
        message.set_html('Body')
        message.set_text('Body')
        message.set_from('Dial-a-Room Admin<admin@dial-a-room.com>')

        # This next section is all to do with Template Engine
        
        # change url append with the customer id and random query parameter
        
        # You pass substitutions to your template like this
        message.add_substitution('%apartment_name%', apartment_name)
        message.add_substitution('%apartment_address%', apartment_address)
        message.add_substitution('%apartment_owner_name%', apartment_owner_name)
        message.add_substitution('%room_rate%', room_rate)
        message.add_substitution('%room_number%', room_number)
        message.add_substitution('%room_type%', room_type)
        message.add_substitution('%room_image_url%', room_image_url)
        message.add_substitution('%cam_user_name%', cam_user_name)
        message.add_substitution('%guest_name%', guest_name)
        message.add_substitution('%guest_rating%', guest_rating)
        message.add_substitution('%check_in_date%', check_in_date)
        message.add_substitution('%check_out_date%', check_out_date)
        message.add_substitution('%number_of_days_stayed%', number_of_days_stayed)
        message.add_substitution('%invoice_date%', invoice_date)
        message.add_substitution('%invoice_amount%', invoice_amount)
        message.add_substitution('%sub_total%', sub_total)
        
        message.add_substitution('%body%', 'Thank you ')

        # Turn on the template option
        message.add_filter('templates', 'enable', '1')

        # Tell SendGrid which template to use
        message.add_filter('templates', 'template_id', '78b40323-bc5c-43b9-bcce-99146ba2fb0a')

        # Get back a response and status
        status, msg = sg.send(message)
            
        print 'successfully sent'
        data = {'success': 'true'}
    except Exception, e:
        print 'Exception : ', e
        data = {'success': 'false'}
    return HttpResponse(json.dumps(data), content_type='application/json')
    

# This web service is use to send the issue raised by the CAM from Contact us page.
@csrf_exempt
def send_issue_mail(request):
#def send_issue_mail():
    print 'Hello'
    try:
        #issue = request.POST.get('message')
        #print issue
        json_obj=json.loads(request.body)
        print json_obj['message']
        issue = json_obj['message']

        user_name = json_obj['username']
        user_id = json_obj['cam_user_id']

        print request
        sg = sendgrid.SendGridClient(settings.SENDGRID_USER_NAME,settings.SENDGRID_PASSWORD)
        message = sendgrid.Mail()
        message.set_headers({'X-Sent-Using': 'SendGrid-API', 'X-Transport': 'web'})
        to_mail = ['manoj.bawane@tungstenbigdata.com','prashant.girbane@gmail.com']
        message.add_to(to_mail)
        message.set_subject("TEST MAIL FOR CONTACT US")
        message_to_send = '<html><body> <br> User ID :'+ str(user_id)+'<br> User Name : '+ str(user_name)+ '<br> Issue : '+ str(issue) +'</body></html>'
        print message_to_send
        message.set_html(message_to_send)
        message.set_text('Hello Your Complaint')
        
        message.set_from('Dial-A-Room Admin<admin@dial-a-room.com>')
        status, msg = sg.send(message)
        print status
        data = {'success': 'true'}
    except Exception, e:
        print e
        data = {'success': 'false'}
    return HttpResponse(json.dumps(data), content_type='application/json')


# BOOKING CONFIRMATION 
# This function will send the booking confimation mail with Sendgrid template
def send_booking_confirmation_mail_with_template(booking_id):
    print "iNSIDE CONFIRMATION MAIL "
    TO = [] #must be a list
    SUBJECT = "Confirmation of Booking"
    try:
        sg = sendgrid.SendGridClient(settings.SENDGRID_USER_NAME,settings.SENDGRID_PASSWORD)
        message = sendgrid.Mail()
        message.set_headers({'X-Sent-Using': 'SendGrid-API', 'X-Transport': 'web'})
        message.set_subject(SUBJECT)
        message.set_html('Body')
        message.set_text('Body')
        message.set_from('Dial-a-Room Admin<admin@dial-a-room.com>')
        
        try:
            booking_obj = Booking.objects.get(booking_id=booking_id)
            TO.append(booking_obj.customer_id.cust_email)     # cam email
            TO.append(booking_obj.property_id.property_owner_id.cust_email) # apartment owner email
            message.add_to(TO)
            message.bcc = ['manoj@bynry.com','bawane.manoj03@gmail.com']
            #message.bcc = ['prashant.girbane@gmail.com','nilesh@dial-a-room.com','yashpal@dial-a-room.com','cs@dial-a-room.com' ]
            
            booking_ref_no = booking_obj.booking_unique_id
            customer_name = booking_obj.customer_id.cust_first_name
            guest_name  = booking_obj.guest_id.guest_first_name
            guest_email_id = booking_obj.guest_id.guest_email
            contact_number = booking_obj.guest_id.guest_contactno
            property_name = booking_obj.property_id.property_actual_name
            check_in_date = booking_obj.booking_actual_checkin_date.strftime('%d-%b-%Y')
            check_out_date = booking_obj.booking_actual_checkout_date.strftime('%d-%b-%Y')
            property_address = booking_obj.property_id.property_location
            
            data = {
                "%booking_ref_no%": [booking_ref_no,booking_ref_no,booking_ref_no,booking_ref_no,booking_ref_no,booking_ref_no],
                "%customer_name%": [customer_name,customer_name,customer_name,customer_name,customer_name,customer_name],
                "%guest_name%": [guest_name,guest_name,guest_name,guest_name,guest_name,guest_name],
                '%guest_email_id%': [guest_email_id,guest_email_id,guest_email_id,guest_email_id,guest_email_id,guest_email_id],
                '%guest_contact_number%': [contact_number,contact_number,contact_number,contact_number,contact_number,contact_number],
                '%property_name%': [property_name,property_name,property_name,property_name,property_name,property_name],
                '%check_in_date%': [check_in_date,check_in_date,check_in_date,check_in_date,check_in_date,check_in_date],
                '%check_out_date%': [check_out_date,check_out_date,check_out_date,check_out_date,check_out_date,check_out_date],
                '%property_address%' : [property_address,property_address,property_address,property_address,property_address,property_address]
            }
            message.set_substitutions(data)
            message.add_filter('templates', 'enable', '1')
            # Tell SendGrid which template to use
            message.add_filter('templates', 'template_id', '1e5e0c81-9cec-4f31-b62f-18a90ea0b5cf')
            # Get back a response and status
            status, msg = sg.send(message)
            print 'Booking Confirmation email successfully sent to customer ',status, msg
        except Exception, e:
            print 'Booking Confirmation email Not successfully sent to customer',e
        data = {'success': 'true'}
    except Exception, e:
        print 'Exception : ', e
        data = {'success': 'false'}
    return HttpResponse(json.dumps(data), content_type='application/json')


def send_cancellation_mail(booking_obj):
    #pdb.set_trace()
    TO = [] #must be a list
    #mailid = request.GET.get('user_email')
    
    #if mailid == 'test.rockstars2014@gmail.com':
    #TO.append('manoj.bawane@tungstenbigdata.com')
    #TO.append('prashant.girbane@gmail.com')
    #TO.append('umang@tungstenbigdata.com')
    SUBJECT = "Cancellation of Booking"
    try:
        sg = sendgrid.SendGridClient(settings.SENDGRID_USER_NAME,settings.SENDGRID_PASSWORD)
        message = sendgrid.Mail()
        message.set_headers({'X-Sent-Using': 'SendGrid-API', 'X-Transport': 'web'})
#       to_mail = ['manoj.bawane@tungstenbigdata.com', 'prashant.girbane@gmail.com']

#        message.set_tos(TO)
        message.set_subject(SUBJECT)
        message.set_html('Body')
        message.set_text('Body')
        message.set_from('Dial-a-Room Admin<admin@dial-a-room.com>')
        
        try:
            #TO.append('prashant.girbane@gmail.com')
            #booking_obj = CAMBooking.objects.get(cam_booking_id=booking_id)
            TO.append(booking_obj.cam_id.cam_email)     # cam email
            TO.append(booking_obj.guest_id.guest_email) # guest email
            TO.append(booking_obj.apartment.apt_owner_id.apt_owner_email) # apartment owner email
            #To.append()    # dial-a-room admin email
##            TO.append('vikas.padhy@tungstenbigdata.com')
            message.add_to(TO)
            #message.add_cc(TO)
            
            data = {
                "%cam_user_name%": [booking_obj.customer_id.cust_first_name,booking_obj.customer_id.cust_first_name,booking_obj.customer_id.cust_first_name],
                "%guest_name%": [booking_obj.guest_id.guest_first_name, booking_obj.guest_id.guest_first_name, booking_obj.guest_id.guest_first_name],
                '%guest_email_id%': [booking_obj.guest_id.guest_email,booking_obj.guest_id.guest_email,booking_obj.guest_id.guest_email],
                '%guest_contact_number%': [booking_obj.guest_id.guest_contactno,booking_obj.guest_id.guest_contactno,booking_obj.guest_id.guest_contactno],
#                    '%room_number%': [booking_obj.aptroom_id.apt_room_number,booking_obj.aptroom_id.apt_room_number,booking_obj.aptroom_id.apt_room_number],
                '%apartment_name%': [ booking_obj.property_id.property_display_name,booking_obj.property_id.property_display_name,booking_obj.property_id.property_display_name],
                '%check_in_date%': [booking_obj.booking_actual_checkin_date.strftime('%d-%b-%Y'),booking_obj.booking_actual_checkin_date.strftime('%d-%b-%Y'),booking_obj.booking_actual_checkin_date.strftime('%d-%b-%Y')],
                '%check_out_date%': [booking_obj.booking_actual_checkout_date.strftime('%d-%b-%Y'),booking_obj.booking_actual_checkout_date.strftime('%d-%b-%Y'),booking_obj.booking_actual_checkout_date.strftime('%d-%b-%Y')],
                '%apartment_address%' : [booking_obj.apartment.get_apartment_address(),booking_obj.apartment.get_apartment_address(),booking_obj.apartment.get_apartment_address()]
            }
            message.set_substitutions(data)
            message.add_filter('templates', 'enable', '1')
            # Tell SendGrid which template to use
            message.add_filter('templates', 'template_id', '7db51932-392e-4edb-ba42-e5e6269643d2')

            # Get back a response and status
            status, msg = sg.send(message)
        except Exception, e:
            print e
        # You pass substitutions to your template like this
        # Turn on the template option
        
        print 'successfully sent',status, msg
        data = {'success': 'true'}
    except Exception, e:
        print 'Exception : ', e
        data = {'success': 'false'}
    return HttpResponse(json.dumps(data), content_type='application/json')


# This function will send the booking confimation mail with Sendgrid template
def send_booking_submission_mail_with_template(booking_id):
    TO = [] #must be a list
    SUBJECT = "Dial-A-Room Booking Submission"
    try:
        sg = sendgrid.SendGridClient(settings.SENDGRID_USER_NAME,settings.SENDGRID_PASSWORD)
        message = sendgrid.Mail()
        message.set_headers({'X-Sent-Using': 'SendGrid-API', 'X-Transport': 'web'})
        message.set_subject(SUBJECT)
        message.set_html('Body')
        message.set_text('Body')
        message.set_from('Dial-a-Room Admin<admin@dial-a-room.com>')
        
        try:
            booking_obj = Booking.objects.get(booking_id=booking_id)
            TO.append(booking_obj.customer_id.cust_email)     # cam email
            TO.append(booking_obj.property_id.property_owner_id.cust_email) # apartment owner email
            message.add_to(TO)
            message.bcc = ['manoj@bynry.com','bawane.manoj03@gmail.com']
            #message.bcc = ['prashant.girbane@gmail.com','nilesh@dial-a-room.com','yashpal@dial-a-room.com','cs@dial-a-room.com' ]
            
            booking_ref_no = booking_obj.booking_unique_id
            customer_name = booking_obj.customer_id.cust_first_name
            guest_name  = booking_obj.guest_id.guest_first_name
            guest_email_id = booking_obj.guest_id.guest_email
            contact_number = booking_obj.guest_id.guest_contactno
            property_name = booking_obj.property_id.property_actual_name
            check_in_date = booking_obj.booking_actual_checkin_date.strftime('%d-%b-%Y')
            check_out_date = booking_obj.booking_actual_checkin_date.strftime('%d-%b-%Y')
            property_address = booking_obj.property_id.property_location
            
            data = {
                "%booking_ref_no%": [booking_ref_no,booking_ref_no,booking_ref_no,booking_ref_no,booking_ref_no,booking_ref_no],
                "%customer_name%": [customer_name,customer_name,customer_name,customer_name,customer_name,customer_name],
                "%guest_name%": [guest_name,guest_name,guest_name,guest_name,guest_name,guest_name],
                '%guest_email_id%': [guest_email_id,guest_email_id,guest_email_id,guest_email_id,guest_email_id,guest_email_id],
                '%guest_contact_number%': [contact_number,contact_number,contact_number,contact_number,contact_number,contact_number],
                '%property_name%': [property_name,property_name,property_name,property_name,property_name,property_name],
                '%check_in_date%': [check_in_date,check_in_date,check_in_date,check_in_date,check_in_date,check_in_date],
                '%check_out_date%': [check_out_date,check_out_date,check_out_date,check_out_date,check_out_date,check_out_date],
                '%property_address%' : [property_address,property_address,property_address,property_address,property_address,property_address]
            }
            message.set_substitutions(data)
            message.add_filter('templates', 'enable', '1')
            # Tell SendGrid which template to use
            message.add_filter('templates', 'template_id', '3bd98166-7a22-4d44-bab0-7e3f9e4e4a58')
            status, msg = sg.send(message)
            print 'successfully sent',status, msg
        except Exception, e:
            print e
        data = {'success': 'true'}
    except Exception, e:
        print 'Exception : ', e
        data = {'success': 'false'}
    return HttpResponse(json.dumps(data), content_type='application/json')
    
