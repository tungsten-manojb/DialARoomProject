from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect

from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import cache_control
from django.shortcuts import redirect

from django.contrib import auth
from quoteapp.models import *
from django.http import HttpResponse
from quoteapp.quote_constants import QuoteConstant
from CorpRoomApp.models import PropertyImage
import pdb
import json

# Accessing the Common Functionality of Property
from CorpRoomApp.common_functionality import PropertyCommonFunctionality
from CorpRoomApp.send_sms import new_request_sms_to_admin
from CorpRoomApp.send_sms import send_new_request_sms_to_relationship_managers
from find_locations import nearby_properties
from CorpRoomApp.common_functionality import store_user_track # for tracking user activity

pcf = PropertyCommonFunctionality()

def request_list_page(request):
    print 'Quote Request List Page'
    store_user_track(request, "Customer Request List") # for tracking user activity
    data = {'status' : request.GET.get('success') }
    return render(request,'cam-user/quote-request/cam-request-list.html',data)
    

def request_new_quote(request):
    print 'Request New Quotation'
    store_user_track(request, 'Customer Requesting New Quotation') # for tracking user activity
    data = { 'state_list' : pcf.get_all_state_name(), 'city_list': pcf.get_all_city_name() }
    return render(request,'cam-user/quote-request/request-new-quote.html',data)


@csrf_exempt
def submit_quote_request(request):
    a = ()
    try:
        store_user_track(request, 'Customer Submitting New Request for quotation') # for tracking user activity
        
        location_list = request.POST.getlist('location')
        location = '$'.join(location_list)
        
        cust = Customer.objects.get(id=request.session['user_id'])
        
        quote_request = QuoteRequest(
            quote_category = request.POST.get('category'),
            quote_sub_category = request.POST.get('subcategory'),
            quote_start_date = datetime.datetime.strptime(request.POST.get('start'), '%d/%m/%Y'),
            quote_end_date = datetime.datetime.strptime(request.POST.get('end'), '%d/%m/%Y'),
            quote_city = request.POST.get('city'),
            quote_location = location,
            quote_property_type = request.POST.get('property_type'),
            property_rating = request.POST.get('property_rating'),
            quote_lowest_price = float(request.POST.get('minPrice')),
            quote_highest_price = float(request.POST.get('maxPrice')),
            quote_no_of_guest = request.POST.get('no_of_guest'),
            quote_no_of_room= request.POST.get('no_of_rooms'),
            quote_request_creation_date = datetime.datetime.now(),
            quote_remark = request.POST.get('remark'),
            customer_id = cust,
    
            quote_request_status = QuoteConstant.QUOTE_STATUS_OPEN,
            quote_customer_status = QuoteConstant.REQUEST_SUBMITTED
        )
        a = quote_request
        quote_request.save()
        quote_request.quote_request_uid = 'QR'+ str(quote_request.quote_request_id).zfill(6)
        quote_request.save()
        try:
            # SMS to All Relationship Manager
            #send_new_request_sms_to_relationship_managers(quote_request.quote_request_uid,request.POST.get('start'), request.POST.get('end'), location_list[0] )
            # Message To DAR CUSTOMER CARE
            new_request_sms_to_admin('8928513850') # test purpose
            # new_request_sms_to_admin('8087700499,7722071007,9175103645,9423567224')
        except Exception as err:
            print 'Unable to send msg to Dial-A-Room Team'
        # This will search nearby properties and send email and sms to them
        nearby_properties(location, quote_request.quote_request_id)
        
        # This is added on 11 Dec 2015 for request statistics
        request_stat = UserRequestStatisticTrack(
            user_id = cust,
            request_path = request.path,
            request_date = datetime.datetime.today(),
            request_id = quote_request
        )
        request_stat.save()
        
        data = { 'quote': quote_request }
        return HttpResponseRedirect('/corporate/quote/request-list/?success=1')
    except Exception as err:
        print 'Exception : ',err
        data = {'quote' : a ,'status': 1, 'error_message': 'Could not submit the request'}
    return render(request,'cam-user/quote-request/request-new-quote.html',data)

# This function returns a Quotation Request Details of the specific Request Details
def get_request_info(request_no):
    try:
        print 'Quotation Request Details'
        quote_req = QuoteRequest.objects.get(quote_request_uid=request_no)
        locations = quote_req.quote_location.split('$')
        property_type = 'HOTEL'
        if quote_req.quote_property_type == 0:
            property_type = 'Service Apartment'

        quotation_list = QuotationResponse.objects.filter(request_id=quote_req)
        data = {'quote' : quote_req, 'error_message': 'success', 'property_type':property_type, 'success': 'true', 'location_list':locations, 'quotation_list': quotation_list }
    except Exception as err:
        print 'Error : ',err
        data = {}
    return data


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def request_quote_details(request):
    if not request.user.is_authenticated():
        return redirect('/business/')
    print 'Detail Page'
    store_user_track(request, 'Customer Requesting Details') # for tracking user activity
    data = get_request_info(request.GET.get('request_uid'))
    return render(request,'cam-user/quote-request/request-details.html',data)


def get_quote_request(request):
    """
    This returns a list of quotes
    """
    print ''
    data = {}
    try:
        quotes = QuoteRequest.objects.filter(customer_id=Customer.objects.get(id=request.session['user_id']))
        data = { 'data' : [ q.get_quote_info() for q in quotes ] }
    except Exception as err:
        print 'err', err
        data = {'data' : []}
    return HttpResponse(json.dumps(data), content_type='application/json')

def get_state_wise_cities(request):
    """ This request will return cities of requested state  """
    
    print 'Retrieving the list of locations'
    data = {}
    try:
        state_name= request.GET.get('state_name')
        data = { 'success' : 'true', 'city_list': pcf.get_all_cities_based_on_state(state_name) }
    except Exception as err:
        print 'Error ',err
        data = {'success' : 'false'}
    return HttpResponse(json.dumps(data), content_type='application/json')


def get_city_wise_locations(request):
    """ This request will return locations of requested city  """
    print 'Retrieving the list of locations'
    data = {}
    try:
        city_name= request.GET.get('city_name')
        data = { 'success' : 'true', 'location_list': pcf.get_all_location_based_on_city(city_name) }
    except Exception as err:
        print 'Error ',err
        data = {'success' : 'false'}
    return HttpResponse(json.dumps(data), content_type='application/json')


def get_requested_quotation_detail(request):
    """ This method returns a specific quotation details against the request in request details Page """
    try:
        store_user_track(request, 'Customer Viewed Quotation'+request.GET.get('quote_uid')) # for tracking user activity
        
        quote_id = request.GET.get('quote_uid')
        quotation = QuotationResponse.objects.get(quotation_uid=request.GET.get('quote_uid'))
        pro_images = PropertyImage.objects.filter(property_id=quotation.property_id)
        images = ''
        if pro_images:
            images = [image.image_name.url for image in pro_images]
        data = { 'success' : 'true', 'quote_uid' :quotation.quotation_uid, 'quote_date' : quotation.quote_date.strftime('%d/%m/%Y'),
        'rate':quotation.rate, 'amount': quotation.amount, 'tax_amount': quotation.tax_amount , 'images': images, 'rack_rate' : quotation.property_rack_rate,
        'total_amount' : quotation.total_quote_amt, 'action_text': quotation.action, 'property_name': quotation.property_id.property_actual_name,
        'property_location' : quotation.property_id.property_location, 'facility_list' : [q for q in quotation.property_id.property_facility.split(',') if q] }
        print data
    except Exception as e:
        print 'Exception : ',e
        data = {'success' : 'false' }
    return HttpResponse(json.dumps(data), content_type='application/json')