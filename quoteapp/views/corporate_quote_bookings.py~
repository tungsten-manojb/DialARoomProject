
from django.shortcuts import render
from django.http import HttpResponse

from quoteapp.models import QuotationResponse
from CorpRoomApp.models import UserBookingStatisticTrack
from CorpRoomApp.models import Booking
from CorpRoomApp.models import Invoice
from CorpRoomApp.models import CorporateTransaction

from adminsite.cam.cam_api import get_corporate_guest_list
from django.views.decorators.cache import cache_control
from django.views.decorators.csrf import csrf_exempt
from CorpRoomApp.models import Guest
from django.db import transaction
import datetime
import json
import pdb
from CorpRoomApp.send_sms import send_booking_submission_sms_to_customer
from CorpRoomApp.send_sms import send_booking_submission_sms_to_vendor

from CorpRoomApp.send_mail import send_booking_submission_mail_with_template
from CorpRoomApp.common_functionality import store_user_track # for tracking user activity


BOOKING_ALL         = 0
BOOKING_OPEN        = 1
BOOKING_BOOKED      = 2
BOOKING_CANCELLED   = 3
BOOKING_COMPLETED   = 4

# This method redirects customer to booking page against the quotation
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def corporate_quote_booking_page(request):
    
    data = {}
    try:
        store_user_track(request, 'Customer moved to Booking By Accepting Quotation') # for tracking user activity
        
        qt = QuotationResponse.objects.get(quotation_uid=request.GET.get('qtuid'))
        guest_list = guests = Guest.objects.filter(customer_id= qt.request_id.customer_id)
        data = { 'quotation' : qt, 'quote_request':qt.request_id, 'guest_list': guest_list }
    except Exception as err:
        print 'exception : ',err
        data = { 'quotation': '', 'quote_request':'','error_message': 'Oops Something Wrong..!' }
    return render(request,'cam-user/quote-request/quote-booking.html',data)


@csrf_exempt
@transaction.atomic
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def save_quote_booking(request):
    #pdb.set_trace()
    print 'Hello'
    sid = transaction.savepoint()
    try:
        store_user_track(request, 'Customer Doing Booking By Accepting Quotation') # for tracking user activit

        quotation = QuotationResponse.objects.get(quotation_uid=request.POST.get('quote_uid'))
        
        guest_list = request.POST.get('guest_list')
        guest_list = guest_list.split(',')
        print guest_list
        guest_list = [x for x in guest_list if x] # This removes blank values or empty elements
        
        if len(guest_list)>=1:
            guest_obj = Guest.objects.get(guest_id=guest_list[0])
        else:
            guest_obj = None
        
        days = quotation.request_id.quote_end_date - quotation.request_id.quote_start_date
        booking_obj = Booking(
            customer_id      = quotation.request_id.customer_id,
            guest_id    = guest_obj,
            property_id   = quotation.property_id,
            booking_estimated_checkin_date  = quotation.request_id.quote_start_date,
            booking_actual_checkin_date     = quotation.request_id.quote_start_date,
            booking_estimated_checkout_date = quotation.request_id.quote_end_date,
            booking_actual_checkout_date    = quotation.request_id.quote_end_date,
            booking_estimated_checkout_time = datetime.datetime.now().time(),
            booking_estimated_checkin_time  = datetime.datetime.now().time(),
            booking_estimated_no_of_day_stay = days.days,
            booking_actual_no_of_day_stay   = days.days,
            number_of_person = quotation.request_id.quote_no_of_guest,
            booking_status   = BOOKING_OPEN, #BOOKING_BOOKED
            booking_rate    = quotation.rate,
            booking_amount  = quotation.total_quote_amt,
            is_from_quote   = True,
            quotation_id    = quotation.quotation_uid
        )
        booking_obj.save()
        booking_obj.booking_unique_id = 'BK' +  datetime.date.today().strftime('%d%m%y') + 'Q' + str(quotation.quotation_id) + str(booking_obj.booking_id).zfill(6)
        booking_obj.remark = 'Guest List : ' + ','.join(guest_list)
        booking_obj.save()
        
        # Generating Invoice
        invoice = Invoice(
            booking_id = booking_obj,
            room_charges = quotation.amount,
            invoice_total_amount =  quotation.amount,
            tax_amount  = quotation.tax_amount,
            invoice_gross_amount = quotation.total_quote_amt,
            invoice_status = 0,
        )
        invoice.save()
        invoice.invoice_unique_id = 'INVBK' + str(booking_obj.booking_id) + str(invoice.invoice_id).zfill(6)
        invoice.save()

        corporate_transaction = CorporateTransaction(
            invoice_id      = invoice.invoice_unique_id,
            corporate_id    = quotation.request_id.customer_id,
            transaction_amount= invoice.invoice_gross_amount,
            transaction_type = 1
        )
        corporate_transaction.save()
        
        # This is for Booking Statistics added on 11 Dec 2015
        booking_stat = UserBookingStatisticTrack(
            user_id = quotation.request_id.customer_id,
            booking_path = request.path,
            booking_date = datetime.date.today(),
            booking_id = booking_obj
        )
        booking_stat.save()
        quotation.quotation_status = 'BOOKED'
        quotation.save()
        transaction.savepoint_commit(sid)

        try:
            # Sending Booking Submission SMS to Corporate User
            send_booking_submission_sms_to_customer(quotation.request_id.customer_id.cust_contact_no, quotation.request_id.customer_id.cust_first_name, booking_obj.booking_unique_id)
            
            store_user_track(request, 'Booking Submission SMS Sent To Customer') # for tracking user activity
            # SMS to VENDOR
            send_booking_submission_sms_to_vendor(quotation.property_id.property_owner_id.cust_contact_no,
                quotation.property_id.property_owner_id.cust_first_name, booking_obj.booking_unique_id, quotation.property_id.property_actual_name,  booking_obj.booking_id)
            
            store_user_track(request, 'Booking Submission SMS Sent To Vendor') # for tracking user activity
            # Sending Booking Submission Email to Corporate User
            send_booking_submission_mail_with_template(booking_obj.booking_id)
            
            data = { 'success':'true', 'booking_uid': booking_obj.booking_unique_id }
        except Exception as err:
            store_user_track(request, 'Booking Submission SMS or Email Not Sent To Vendor and Corporate') # for tracking user activity
            print 'Sending SMS or Email not Sent to Corporate Customer : ',err
            data = { 'success':'true', 'booking_uid': booking_obj.booking_unique_id }
    except Exception as err:
        print 'Exception : ',err
        transaction.savepoint_rollback(sid)
        data = {'success':'false', 'error_message':'Server Error- Please Try Again'}
    return HttpResponse(json.dumps(data), content_type='application/json')