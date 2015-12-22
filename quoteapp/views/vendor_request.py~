from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect

from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect
from django.contrib import auth
from propertyvendor.views import sign_out_vendor
from quoteapp.models import *
from django.http import HttpResponse
from quoteapp.quote_constants import QuoteConstant
from CorpRoomApp.models import *
from CorpRoomApp.forms import *
import pdb
import json
from admin_service import send_quotation_email
from django.db.models import Q



# Accessing the Common Functionality of Property
from CorpRoomApp.common_functionality import PropertyCommonFunctionality
from CorpRoomApp.send_sms import send_new_quotation_sms_to_corporate_user
from CorpRoomApp.common_functionality import store_user_track # for tracking user activity

pcf = PropertyCommonFunctionality()

SERVICE_TAX = 14.5
LUXURY_TAX  = 4.5

QUOTE = 'QUOTE'
REQUOTE = 'REQUOTE'

def request_list_page(request):
    print 'Quote Request List Page'
    data="";
    try:
        request.session['vendor_name']
    except:
        sign_out_vendor(request)
        return redirect('/vendor/')

    if not request.user.is_authenticated():
        return redirect('/vendor/')
    try:
        # store user activities
        store_user_track(request,'Vendor Opening Request List Page' )
        
        vendor = Customer.objects.get(id=request.session['apt_vendor_id'])
        data = { 'vendor' : vendor }
    except Customer.DoesNotExist,e:
        print 'FAILED TO retrieve Customer information'
    except Exception,e:
        print 'Exception ',e
    return render(request,'property-vendor/quote-request/vendor-request-list.html', data)
    

def get_request_list(request):
    data = {}
    try:
         request.session['vendor_name']
    except:
         sign_out_vendor(request)
         return redirect('/vendor/')
    try:
        quotes = QuoteRequest.objects.all()
        data = { 'data' :  [ q.get_quote_info() for q in quotes ]}
    except Exception as err:
        print 'err', err
        data = {'data' : 'none'}
    return HttpResponse(json.dumps(data), content_type='application/json')

def get_request_info(request_no):
  
    try:
        print 'Quotation Request Details'
        quote_req = QuoteRequest.objects.get(quote_request_uid=request_no)
        locations = quote_req.quote_location.split('$')
        property_type = 'HOTEL'
        if quote_req.quote_property_type == 0:
            property_type = 'Service Apartment'
        data = {'quote' : quote_req, 'error_message': 'success', 
            'property_type':property_type,  'success': 'true', 'location_list':locations }
    except Exception as err:
        print 'Error : ',err
        data = {}
    return data

def request_quote_details(request):
    #pdb.set_trace()
    try:
         request.session['vendor_name']
    except:
         sign_out_vendor(request)
         return redirect('/vendor/')
    data = {}
    try:
        # store user activities
        store_user_track(request,'Vendor Views Request Details '+request.GET.get('request_uid') )
        # Request Objects
        quote_req = QuoteRequest.objects.get(quote_request_uid=request.GET.get('request_uid'))
        locations = quote_req.quote_location.split('$')
        
        quote_requote = REQUOTE # By Default Requote
        days = quote_req.quote_end_date - quote_req.quote_start_date
        
        owner = Customer.objects.get(id=request.session['apt_vendor_id'])
        
        if days.days == 0:
            no_of_days = 1
        else:
            no_of_days = days.days
        
        my_status = 0
        
        # GET APARTMENT LIST OF OWENR
        apartment_list = Property.objects.filter(property_owner_id=owner)
        property_list = []
        try:
            requestProperty = RequestedProperty.objects.filter(quote_request_id=quote_req, property_owner_id=owner, property_id__in= apartment_list, quoted_status=False )
            if requestProperty: 
                for req_prop in requestProperty:
                    if req_prop.property_id.property_type == 0:
                        prop_type='Service Apartment'
                    if req_prop.property_id.property_type == 1:
                        prop_type='Hotel'
                    if req_prop.property_id.property_status ==1:
                        status='NOT AVAILABLE'
                    if req_prop.property_id.property_status ==0:
                        status='AVAILABLE'
                    
                    quote_requote = QUOTE #if not req_prop.quoted_status else REQUOTE
                    
                    rate = get_property_rate(req_prop.property_id)
                    amount = rate * no_of_days * quote_req.quote_no_of_guest
                    tax_amount = amount * (SERVICE_TAX + LUXURY_TAX) / 100
                    total = amount + tax_amount
                
                    property_list.append({ 'property_id': req_prop.property_id.property_id,
                    'property_location':req_prop.property_id.property_location,
                    'property_name': req_prop.property_id.property_actual_name, 'tax' : '{:.2f}'.format(tax_amount),
                    'property_rack_rate' : req_prop.property_id.rack_rate, 'quote_status' : req_prop.quoted_status, 
                    'property_rate' : '{:.2f}'.format(rate), 'amount' : '{:.2f}'.format(amount), 
                    'total_amt': '{:.2f}'.format(total),'property_type' : prop_type, 'status' :status })
            else:
                property_list = get_quoted_property(quote_req,owner)
        except Exception as err:
            print 'vendor_request.py | request_quote_details | Exception ', err
            mystatus = 0

        data = { 'quote' : quote_req,   'error_message': 'success',
           'no_of_days':no_of_days,     'success': 'true', 'quote_requote': quote_requote,
           'my_status' : my_status,     'property_list': property_list,
           'location_list': locations,  'city_list': pcf.get_all_city_name(),
           #'quoted_property_list':get_quoted_property(quote_req,owner) 
        }
    except Exception as err:
        print 'vendor_request.py | request_quote_details | Exception ', err
        data = {}
    return render(request,'property-vendor/quote-request/request-details.html',data)


def get_property_rate(property_obj):
    property_rate=0.0
    try:
        property_rate =property_obj.property_rates.get().property_display_rate
    except Exception as err:
        print 'err', err
    return property_rate


# This will give already quoted list
def get_quoted_property(quote_req,owner):
    data = {}
    print 'Retrieving Quoted Property'
    try:
        quoted_property_list=[]
        property_list = Property.objects.filter(property_owner_id=owner)
        
        quotations = QuotationResponse.objects.filter(request_id=quote_req, property_id__in = property_list)
        
        print quotations
        
        for quote in quotations:
            if quote.property_id.property_type == 0:
                prop_type='Service Apartment'
            if quote.property_id.property_type == 1:
                prop_type='Hotel'
            quoted_property_list.append({ 'property_id': quote.property_id.property_id,
                'property_location':quote.property_id.property_location,
                'property_name': quote.property_id.property_actual_name,
                'property_rack_rate': quote.property_rack_rate,
                'property_rate' : quote.rate, 'amount' : quote.amount,
                'tax' : quote.tax_amount, 'total_amt' : quote.total_quote_amt,
                'property_type' :prop_type, 'quote_id' : quote.quotation_id
                })
        print quoted_property_list
        
        return quoted_property_list
    except Exception as err:
        print 'err', err
        data = {'data' : 'none'}
        return quoted_property_list


# This will return a list of properties already quoted against the request
def get_properties_for_quote(request):
    try:
        print 'Property List'
        owner = Customer.objects.get(id=request.session['apt_vendor_id'])
        property_list=[]
        prop_list=[]
        prop_type=''
        status=''
        property_rate=0.0
        quote_req = QuoteRequest.objects.get(quote_request_uid=request.GET.get('request_uid'))
        locations = quote_req.quote_location.split('$')

        properties_list=CustomerFavoriteProperty.objects.filter(customer_id=Customer.objects.get(user_ptr_id=quote_req.customer_id))
        
        for prop in properties_list:
            prop_list.append(prop.property_id.property_id)
        
        apartment_list = Property.objects.filter(property_owner_id=owner)
        apartment_list = RequestedProperty.objects.filter(property_id__in = apartment_list, quote_request_id= quote_req)
        
        for apartment in apartment_list:
            if apartment.property_id.property_type == 0:
                prop_type='Service Apartment'
            if apartment.property_id.property_type == 1:
                prop_type='Hotel'
            if apartment.property_id.property_status ==1:
                status='NOT AVAILABLE'
            if apartment.property_id.property_status ==0:
                status='AVAILABLE'
            property_list.append({ 'property_id': apartment.property_id.property_id,
                'property_location':apartment.property_id.property_location,
                'property_name': apartment.property_id.property_actual_name,
                'property_rack_rate' : '{:,.2f}'.format(apartment.property_id.rack_rate),
                'property_rate' : '{:,.2f}'.format(get_property_rate(apartment.property_id)),
                'property_type' : prop_type,
                'status' :status
                })
    except Exception, e:
        print 'Error ',e
    return property_list


def get_quote_request(request):
    """
    This returns a list of quotes
    """
    propList=[]
    requested=[]
    data = {}
    try:
         request.session['vendor_name']
    except:
         sign_out_vendor(request)
         return redirect('/vendor/')
    try:
        properties=Property.objects.filter(property_owner_id=Customer.objects.get(user_ptr_id=request.GET.get('vendor_id')))
        for prop in properties:
            propList.append(prop.property_id)

        requestedProperty= RequestedProperty.objects.filter(property_id__in=propList)
        #print requestedProperty
        for obj in requestedProperty:
            requested.append(obj.quote_request_id.get_vendor_quote_info())

        #quotes = QuoteRequest.objects.filter(customer_id=Customer.objects.get(id=request.session['apt_vendor_id']))
        data = { 'data' : requested }
    except Exception as err:
        print 'err', err
        data = {'data' : []}
    return HttpResponse(json.dumps(data), content_type='application/json')


# This function call from send_quotation function only
def send_mail_and_sms_for_quotation(quote_req,quotation):
    location = quote_req.quote_location.split('$')[0]
    # Sending Mail to corporate use regarding quotation against request
    send_quotation_email(quotation,quote_req)

    # Sending SMS to corporate user for each property quotation alert.
    #send_new_quotation_sms_to_corporate_user(quote_req.customer_id.cust_contact_no,quote_req.quote_request_uid,quotation.quotation_uid, quotation.property_id.property_owner_id.cust_first_name)
    send_new_quotation_sms_to_corporate_user(quote_req.customer_id.cust_contact_no, quote_req.quote_request_uid,
     location , quotation.property_id.property_actual_name,quote_req.customer_id.cust_first_name )


@csrf_exempt
def send_quotation(request):
    print 'send_quotation'
    property_ids = request.POST.getlist('property_ids')
    rate      = request.POST.getlist('rate')
    amount    = request.POST.getlist('amt')
    tax       = request.POST.getlist('tax')
    total_amt = request.POST.getlist('total_amt')

    # newly added on 14 Dec 2015
    rack_rate = request.POST.getlist('rack_rate')

    try:
        # store user activities
        store_user_track(request,'Vendor Sending Quotation against '+request.POST.get('request_id'))
        quote_req = QuoteRequest.objects.get(quote_request_id=request.POST.get('request_id'))
        
        if request.POST.get('quote_requote') == QUOTE:
        # If Already Quoted 
        #for prop in property_details:
            index=0
            for prop_id in property_ids:
                property= Property.objects.get(property_id=prop_id)
                property.rack_rate = rack_rate[index]
                property.save()
                    
                quotation = QuotationResponse(
                    request_id              = quote_req,
                    property_id             = Property.objects.get(property_id=prop_id),
                    rate                    = rate[index],
                    amount                  = amount[index],
                    tax_amount              = tax[index],
                    total_quote_amt         = total_amt[index],
                    property_rack_rate      = property.rack_rate,   # rack rate
                    quote_date              = datetime.datetime.today() ,
                    created_date            = datetime.datetime.today(),
                    created_by              = 'Admin',
                    is_new                  = True,
                    quotation_status        = 'QUOTED',
                    viewed_by_customer      = False
                )
                index += 1
                quotation.save()
                quotation.quotation_uid='QT'+str(quotation.quotation_id).zfill(6)
                quotation.save()
                try:
                    requestedProperty = RequestedProperty.objects.get(property_id=quotation.property_id,quote_request_id=quotation.request_id,property_owner_id =quotation.property_id.property_owner_id)
                    requestedProperty.quoted_status = True
                    requestedProperty.save()
                except Exception as err:
                    print 'Error '
                # Send SMS and EMAIL
                send_mail_and_sms_for_quotation(quote_req,quotation)
            print 'Quotation Successfully Saved'
        else:
            # Else Update the previous quote
            index = 0
            quotations = request.POST.getlist('quotations')
            for quote_id in quotations:
                try:
                    quotation = QuotationResponse.objects.get(quotation_id=quote_id)
                    quotation.request_id = quote_req
                    quotation.property_id = Property.objects.get(property_id=property_ids[index])
                    quotation.rate          = rate[index]
                    quotation.amount        = amount[index]
                    quotation.tax_amount    = tax[index]
                    quotation.total_quote_amt       = total_amt[index]
                    quotation.property_rack_rate    = rack_rate[index]
                    quotation.quote_date    = datetime.datetime.today()
                    quotation.created_by    = request.session['vendor_name']
                    quotation.save()
                    index+=1
                    # Send SMS and EMAIL
                    send_mail_and_sms_for_quotation(quote_req,quotation)
                except Exception as err:
                    print 'vendor_request.py | send_quotation | Update Quote | Exception ', err
            print 'Update Successfully '
    except Exception, e:
        print 'Exception : ',e
        data = { 'sucess': 'false' }
    return redirect('../request-list/')
    #return render(request,'admin/quote-request/admin-quotation-list.html')
    # return render(request,'quote-request/quotation.html',data, context_instance=RequestContext(request))

