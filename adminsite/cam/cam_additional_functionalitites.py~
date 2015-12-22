from CorpRoomApp.models import *
from CorpRoomApp.constants import *
import pdb
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from django.shortcuts import render
from django.http import HttpResponse
from CorpRoomApp.common_functionality import store_user_track # for tracking user activity
import json

BOOKING_ALL         = 0
BOOKING_OPEN        = 1
BOOKING_BOOKED      = 2
BOOKING_CANCELLED   = 3
BOOKING_COMPLETED   = 4

SERVICE_TAX = 14.5
LUXURY_TAX  = 4.5



def get_corporate_prefered_property_images(cam_obj):
    try:
        property_image_list = []
        # List of prefered Properties
        properties = CustomerFavoriteProperty.objects.filter(customer_id=cam_obj)
        index = 1
        for property in properties:
            try:
                # retrieving list of prefered property images
                image = PropertyImage.objects.filter(property_id=property.property_id)[0]
                property_image_list.append({ 'index': index,  'property_id': property.property_id.property_id, 'image' : SERVER_URL + image.image_name.url, 'name': property.property_id.property_actual_name })
                index+=1
            except Exception as err:
                print 'No Image for ', property
    except Exception as e:
        print 'cam_additional_functionality.py | PREFERED PROPERTY | EXCEPTION ', e
    return property_image_list


# This method is for Saving Booking From Dashboard Page
# This has ability to store multiple guest w.r.t booking
@csrf_exempt
@transaction.atomic
def new_booking_from_dashboard(request):
    if not request.user.is_authenticated():
        return redirect('/corporate/')
    sid = transaction.savepoint()
    print request.POST
    
    try:
        print 'Request Accepted '
        store_user_track(request, "Customer Doing Booking From Dashboard")   # for tracking user activity
        if request.method == "POST":
            v_cam_id        = request.session['user_id']
            var_property_id = request.POST.get('property_id')
            occupancy_type  = int(request.POST.get('occupancy_type'))
            check_in    = datetime.datetime.strptime(request.POST.get('check_in'), '%d/%m/%Y')
            check_out   = datetime.datetime.strptime(request.POST.get('check_out'), '%d/%m/%Y')
            
            guest_list = request.POST.get('guest_ids')
            guest_list = guest_list.split(',')
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
                customer_id     = cam_obj,
                guest_id        = None,
                property_id     = property_obj,
                booking_estimated_checkin_date  = check_in,
                booking_actual_checkin_date     = check_in,
                booking_estimated_checkout_date = check_out,
                booking_actual_checkout_date    = check_out,
                booking_estimated_checkout_time = datetime.datetime.now().time(),
                booking_estimated_checkin_time  = datetime.datetime.now().time(),
                booking_estimated_no_of_day_stay = days.days,
                booking_actual_no_of_day_stay   = day,
                booking_status  = BOOKING_OPEN, #BOOKING_BOOKED
                booking_rate    = occupancy_rate
            )
            booking_obj.save()
            booking_obj.booking_unique_id = 'BK' +  datetime.date.today().strftime('%d%m%y') + str(booking_obj.booking_id).zfill(6)
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
            
            # guest bookings
            for guest in guest_list:
                guest_in_booking = BookingGuest(
                    guest_id    = Guest.objects.get(guest_id=guest),
                    booking_id  = booking_obj
                )
                guest_in_booking.save()
                
            # Update booking with guest
            booking_obj.guest_id = guest_in_booking.guest_id
            booking_obj.save()
            
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
            data = {'success':'true', 'error_message':'Successfullly Booked'}
            return HttpResponse(json.dumps(data), content_type='application/json')
            #return redirect('/corporate/cam-booking-details/?booking_id='+ str(booking_obj.booking_unique_id))
        else:
            print 'Hello'
            transaction.savepoint_rollback(sid)
            data = {'success':'false', 'error_message':'Invalid Request'}
    except Exception, e:
        print 'cam_additional_functionality.py | new_booking_from_dashboard | EXCEPTION ', e
        transaction.savepoint_rollback(sid)
    data = {'success':'false', 'error_message':'Server Error- Please Try Again'}
    #return render(request,'cam-user/cam-booking-confirmed-page.html', data )
    return HttpResponse(json.dumps(data), content_type='application/json')
