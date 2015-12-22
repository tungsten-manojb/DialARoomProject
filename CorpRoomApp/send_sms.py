import smtplib
from smtplib import SMTPException
import urllib
from DialARoomProject import settings
from CorpRoomApp import bitly 
from CorpRoomApp.models import RelationShipManager

#SERVER_URL = 'http://192.168.0.121:8000'
SERVER_URL = 'http://dial-a-room.com'
VENDOR_REQUEST_URL = '/vendor/quote/request-details/?request_uid='
VENDOR_BOOKING_DETAIL_URL = '/vendor/display-booking-details/?booking_id='

CORPORATE_REQUEST_DETAIL_URL = '/corporate/quote/request-details/?request_uid='

def send_generalised_sms(mobile_no,message):
    '''
    This method will take number and message as an argument to send sms
    '''
    try:
        host = "http://173.45.76.226"
        user_name = "dialrm"
        user_password = "dialrm"
        recipient = "trans1"
        sender="DIALRM"
        number=mobile_no+ ',9579513850' # TEST Purpose
        #number=mobile_no+ ',7722071007,7769868067' # for live added prashant, nilesh
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
        http_req += urllib.quote(message)
        
        print http_req 
        
        get = urllib.urlopen(http_req)
        req = get.read()
        s=req.split('\r')
        status=s[0].split('|')
        print "Status",status[0]
        get.close()
        
        if(status=='1'):
            data =  {'success': 'true', 'message': 'Message has been sent to the user'}
            print 'message sent to DAR ADMIN'
        else:
            data =  {'success': 'false', 'message': 'Message has not been sent to the user'}
            print 'message sent to DAR ADMIN'
    except SMTPException,e:
        print "failed to send mail", e
        data = {'success': 'false'}



# This is for sending booking submission SMS to CORPORATE CUSTOMER
def send_booking_submission_sms_to_customer(mobile_no, cust_name, booking_reference_no):
    try:
        
        TEXT ="Hi "+ cust_name +"\nYour Booking has been Submitted"
        TEXT= TEXT + "\nBooking ID: " + booking_reference_no
        TEXT= TEXT+"\nConfirmation msg will be sent to your phone and email"
        TEXT = TEXT + "\nFor any query,Pls Call us on 8087700499"
        
        send_generalised_sms(mobile_no, TEXT)
        print 'Booking Submission Message Sent to '+mobile_no
    except SMTPException,e:
        print 'Booking Submission Message Not Sent to '+mobile_no
        print 'Error : ',e
        data = {'success': 'false'}

# This is for sending booking submission SMS to VENDOR
def send_booking_submission_sms_to_vendor(mobile_no, vendor_name, booking_reference_no, property_name, book_id ):
    try:
        
        TEXT ="Hi "+ vendor_name +"\nNew booking "+ booking_reference_no
        TEXT= TEXT + "\nSubmitted for your property "+property_name
        TEXT= TEXT+"\nPlz Check and accept booking"
        TEXT = TEXT + "\nFor any query, Call us on 8087700499"
        
        URL = SERVER_URL + VENDOR_BOOKING_DETAIL_URL + book_id
        print 'URL : ',URL
        a=bitly.Api(login=settings.BITLY_USER_NAME,apikey=settings.BITLY_API_KEY)
        print a
        shortURL =a.shorten(URL)
        TEXT = TEXT + shortURL
        send_generalised_sms(mobile_no, TEXT)
        print 'Booking Submission Message Sent to '+mobile_no
    except SMTPException,e:
        print 'Booking Submission Message Not Sent to '+mobile_no
        print 'Error : ',e
        data = {'success': 'false'}



# This is for sending booking Confirmation SMS to the customer
def send_booking_confirmation_sms_to_customer(cust_mobile_no, booking_reference_no, check_in,check_out, property_name):
    try:
        TEXT ="Your Booking from "+check_in + " to "+check_out +" has been Confirmed at "
        TEXT = TEXT+ property_name #+ '\n'+ property_name
        TEXT = TEXT + "\nFor any queries, Pls call us on 8087700499 or write to us at cs@dial-a-room.com"
        send_generalised_sms(cust_mobile_no,TEXT)
    except SMTPException,e:
        print "failed to send mail", e
        data = {'success': 'false'}


# This method will send SMS to Property Owner
def send_sms_to_property_owner(mobile_no):
    try:
        TEXT ="TEST SMS from Dial-A-Room"
        TEXT= TEXT + "\n THIS IS TEST"
        
        TEXT= TEXT + "\nContact: 8087700499"
        
        host = "http://173.45.76.226"
        user_name = "dialrm"
        user_password = "dialrm"
        recipient = "trans1"
        sender="DIALRM"
        number=cust_mobile_no
        
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



# This method will send SMS to DAR admin
def new_request_sms_to_admin(mobile_no):
    try:
        TEXT ="Hi, You Have Received a New request in a System"
        TEXT= TEXT + "\n Please Check and Respond"
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
        
        print http_req 
        
        get = urllib.urlopen(http_req)
        req = get.read()
        s=req.split('\r')
        status=s[0].split('|')
        print "Status",status[0]
        get.close()
        
        if(status=='1'):
            data =  {'success': 'true', 'message': 'Message has been sent to the user'}
            print 'message sent to DAR ADMIN'
        else:
            data =  {'success': 'false', 'message': 'Message has not been sent to the user'}
            print 'message sent to DAR ADMIN'
    except SMTPException,e:
        print "failed to send mail", e
        data = {'success': 'false'}

# New Request Message to Property Owners.
def send_new_request_sms_to_property_owners(owner_name,mobile_no, property_name,req_id, frm_date, to_date):
    '''
    This function is use to send SMS to property owner it takes argumnet as in sequence
    owner_name, owner_contact_number, property name, request_id, start date, end date
    In SMS it sends quote requests date
    '''
    try:
        TEXT ="Hi "+ owner_name +",\nYou have a quotation request for "
        TEXT = TEXT + property_name
        TEXT = TEXT + ' from ' + frm_date.strftime('%d-%b') + ' to ' + to_date.strftime('%d-%b')  # DAte Range
        TEXT= TEXT + "\nPlease Respond\n"
        URL = SERVER_URL + VENDOR_REQUEST_URL + req_id
        print 'URL : ',URL
        a=bitly.Api(login=settings.BITLY_USER_NAME,apikey=settings.BITLY_API_KEY)
        print a
        shortURL =a.shorten(URL)
        TEXT = TEXT + shortURL
        print 'FINAL TEXT : ',TEXT
        return send_generalised_sms(mobile_no, TEXT)
    except Exception as err:
        print 'MSG NOT SENT TO Vendor : ', mobile_no
        print 'Exception : ',err
        return 0

# Request SMS to Relationship Managers
def send_new_request_sms_to_relationship_managers(req_uid, frm_date, to_date, location):
    '''
    This function is use to send SMS to Relationship Managers it takes argumnet as in sequence
    owner_name, owner_contact_number, property name, request_id, start date, end date
    In SMS it sends quote requests date
    '''
    try:
        print 'In SMS to Relationship Manager'
        relation_managers = RelationShipManager.objects.all().values('rm_first_name','rm_contactno')
        for rm in relation_managers:
            if rm['rm_contactno']:
                TEXT ="Hi "+ rm['rm_first_name'] +",\nWe get new request : " + req_uid
                TEXT = TEXT + ' from ' + frm_date + ' to ' + to_date  # Date Range
                TEXT = TEXT + '\nLocation '+ location
                TEXT= TEXT + "\nPlz Respond"
                return send_generalised_sms(rm['rm_contactno'], TEXT)
    except Exception as err :
        print 'MSG NOT SENT TO Relationship Manager'
        print 'Exception : ',err
    return 0


# Quotation response SMS to corporate user.
def send_new_quotation_sms_to_corporate_user(mobile_no, req_no, quote_lcoation, frm_property, to_corporate):
    try:
        TEXT ="Hi "+to_corporate +",\nYou have received new quotation from "+ frm_property 
        TEXT = TEXT +" against your request for "+ quote_lcoation
        TEXT= TEXT + "\nPls click to consider/accept"
        URL = SERVER_URL + CORPORATE_REQUEST_DETAIL_URL + req_no
        a=bitly.Api(login=settings.BITLY_USER_NAME,apikey=settings.BITLY_API_KEY)
        shortURL =a.shorten(URL)
        TEXT = TEXT + shortURL
        send_generalised_sms(mobile_no, TEXT)
        print 'New Quotation sent to '+mobile_no 
    except SMTPException,e:
        print "failed to send SMS", e
        data = {'success': 'false'}

