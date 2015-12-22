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

from CorpRoomApp.common_functionality import PropertyCommonFunctionality

AVAILABLE          = 0
NOT_AVAILABLE      = 1

SERVER_URL = "http://192.168.0.121:8000"
#SERVER_URL = 'http://dial-a-room.com'


pcf = PropertyCommonFunctionality() # to access the city and state list


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def apartment_list_page(request):
    if not request.user.is_authenticated():
        return redirect('/')
    return render(request,'apartments.html')

def get_all_locations():
    data = []
    try:
        locations = Location.objects.all()
        data = [location.__unicode__() for location in locations]
    except Exception as e:
        print e
    return data

def get_apartment_owner_list():
    """
    This function returns the available owner_list.
    This function called by new-apartment-page. for showing the owner list in owner section.
    """
    try:
        print 'Apartment Owner List'
        owner_list=[]
        apartment_owner_list = Customer.objects.filter(user_type='2')
        if apartment_owner_list:
            for owner in apartment_owner_list:
                owner_list.append({'owner_id':owner.user_ptr_id,'owner_first_name':owner.cust_first_name,
                    'owner_last_name':owner.cust_last_name})
            return owner_list
    except Exception, e:
        print 'Exception : ',e
        owner_list = []
    return owner_list
  


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def new_apartment_page(request):
    # pdb.set_trace()
    if not request.user.is_authenticated():
        return redirect('/')
    try:
        data = { 'owner_list': get_apartment_owner_list, 'state_list' : pcf.get_all_state_name(), 'city_list': pcf.get_all_city_name() }

    except Exception, e:
        data = {}
    return render(request,'new-apartment-add.html',data, context_instance=RequestContext(request))

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def apartment_confirm(request):
    if not request.user.is_authenticated():
        return redirect('/')
    return render_to_response('apartment_confirm.html')


@csrf_exempt
@transaction.atomic
def save_apartment_information(request):
    print "in the save_apartment_information"
    sid = transaction.savepoint()
    try:
        if request.method == "POST":
            print 'Request Accepted '
            print request.POST
            room_ids = request.POST.get('room_id_list')
            room_ids = room_ids.strip(' ')
            room_ids = room_ids.split(' ')
            room_ids = [x for x in room_ids if x]
            no_of_rooms = len(room_ids)
           
            apt_obj = Property(
                property_display_name                   = request.POST.get('property_display_name'),
                property_actual_name                    = request.POST.get('property_actual_name'),
                property_owner_id                       = Customer.objects.get(user_ptr_id=request.POST.get('property_owner_name')),
                property_description                    = request.POST.get('property_description'),
                property_creation_date                  = datetime.datetime.now(),
                property_address                        = request.POST.get('address_line'),
                property_location                       = request.POST.get('location'),  #request.POST.get('address_line')+','+request.POST.get('location')+','+request.POST.get('city')+','+request.POST.get('state')+','+request.POST.get('country') ,
                property_city                           = request.POST.get('city'),
                property_state                          = request.POST.get('state'),
                property_country                        = request.POST.get('country'),
                latitude                                = request.POST.get('lattitude') or 0.0,
                longitude                               = request.POST.get('longitude') or 0.0,
                distance_from_railway_station           = request.POST.get('dist_from_railway_station') or 0.0,
                distance_from_airport                   = request.POST.get('dist_from_airport_station') or 0.0,
                nearest_railway_station                 = request.POST.get('nearest_railway_station') ,
                nearest_bus_stop                        = request.POST.get('nearest_bus_stop'),
                remark                                  = request.POST.get('remark'),
                rack_rate                               = request.POST.get('rack_rate'),
                contact_person                          = request.POST.get('contact_person'),
                contact_person_email_id                 = request.POST.get('contact_person_email'),
                contact_person_phone_no                 = request.POST.get('contact_person_phno'),
                property_availability_status            = 0,
                property_status                         = 0
            )
            
            apt_obj.save()

            if request.POST.get('no_of_person_per_rooms'):
                apt_obj.no_of_person_allowed_per_room                   =int(request.POST.get('no_of_person_per_rooms'))
            if request.POST.get('no_of_rooms'):
                apt_obj.number_of_rooms                         = int(request.POST.get('no_of_rooms'))
            if request.POST.get('pincode'):
                apt_obj.property_pincode                        = int(request.POST.get('pincode'))
            if request.POST.get('star'):
                apt_obj.star_category                           =int(request.POST.get('star'))
            if request.POST.get('facilities_list'):
                apt_obj.property_facility                       =str(request.POST.get('facilities_list'))
            apt_obj.save()

            apt_obj.property_unique_id='PRO'+ datetime.date.today().strftime('%d%m%y') + str(apt_obj.property_id).zfill(6)
            apt_obj.save()

            print "done"

            save_property_rate(request,apt_obj) # To save property rates
            save_property_images(request,apt_obj) # To save property images
            if no_of_rooms > 0:
                for roomid in room_ids:
                    room = PropertyRoom.objects.get(room_id=roomid)
                    room.property_id = apt_obj
                    room.save()

            transaction.savepoint_commit(sid)
            
            return redirect('/business/property-info/?property_token='+str(apt_obj.property_id)+'&update=new')
        else:
            print 'Invalid Request'
            transaction.savepoint_rollback(sid)
            data = { 'sucess': 'false' , ExceptionLabel.ERROR_MESSAGE :'Invalid Request' }
    except Exception, e:
        transaction.savepoint_rollback(sid)
        print 'error', e
        data = { 'sucess': 'false', ExceptionLabel.ERROR_MESSAGE :'Server Error' }
    return render(request,'new-apartment-add.html',data, context_instance=RequestContext(request))
    #return HttpResponse(json.dumps(data), content_type='application/json')

def property_info(request):
    print "innthe property_info"
    print request
    try:
        apt_obj = Property.objects.get(property_id=request.GET.get('property_token'))
        data = { 'success': 'true',
                 'apartment': apt_obj,
                 'room_list': apt_obj.property_rooms.all(),
                 'facilities' : get_facility(apt_obj),
                'update' : request.GET.get('update')
            }
    except Exception, e:
        print 'error', e
        data = { 'sucess': 'false', ExceptionLabel.ERROR_MESSAGE :'Server Error' }
    return render(request,'apartment_confirm.html',data, context_instance=RequestContext(request))


def get_facility(apt_obj):
    print "room_list"
    try:
        facilities=''
        fac_list=[]
        f=[]
        facilities = str(apt_obj.property_facility)
        print "property_room_obj"
        fac_list = facilities.split(',')
        print fac_list
        for facility in fac_list[1:]:
            f.append(facility)
        return f
    except Exception, e:
        print 'error', e
        return ''


def save_property_rate(request,apt_obj):
    print "in the save_property_rate"
    try:
        if apt_obj:
            property_rate_obj = PropertyRate(
                property_agreed_rate                             = float(request.POST.get('agreed_rate')),
                property_display_rate                            = float(request.POST.get('display_rate')),
                property_discount_rate                           = float(request.POST.get('discount_rate')),
                single_occupancy_display_rate                    = float(request.POST.get('single_occ_display_rate')),
                single_occupancy_agreed_rate                     = float(request.POST.get('single_occ_agreed_rate')) ,
                double_occupancy_display_rate                    = float(request.POST.get('double_occ_display_rate'))  if request.POST.get('double_occ_display_rate') else 0.0,
                double_occupancy_agreed_rate                     = float(request.POST.get('double_occ_agreed_rate')) if request.POST.get('double_occ_agreed_rate') else 0.0,
                additional_occupancy_display_rate                = float(request.POST.get('additional_occ_display_rate')) if request.POST.get('additional_occ_display_rate') else 0.0 ,
                additional_occupancy_agreed_rate                 = float(request.POST.get('additional_occ_agreed_rate')) if request.POST.get('additional_occ_agreed_rate') else 0.0,
                property_id=apt_obj
            )
            property_rate_obj.save()
        return ""
    except Exception, e:
        print 'Property Rate Failed To Add', apt_obj ,e
        return False

def save_property_images(request,apt_obj):
    print "in the save images"
    try:
        image_ids=''
        if request.POST.get('image_count'):
            print request.POST.get('image_count')    
            image_ids= str(request.POST.get('image_count'))
            image_id_list = image_ids.split(",")
            for image_id in image_id_list:
                image= PropertyImage.objects.get(image_id=image_id)
                image.property_id=apt_obj
                image.save()
            print "done"
        return ""
    except Exception, e:
        print e
        return False


def get_apartment_list(request):
    data = {'data' : "none"}
    try:
        print 'Property List'
        property_list=[]
        apartment_list = Property.objects.all()
        for apartment in apartment_list:
            property_list.append(get_apartment_info(apartment))

        data = { 'data':property_list,'success':'true'}
    except Exception, e:
        print 'Error ',e
        data = {'data' : "none"}
    return HttpResponse(json.dumps(data), content_type='application/json')

def get_apartment_info(property_obj):
        status = ''
        more = ''
        owner_name = ''
        if property_obj.property_availability_status == AVAILABLE:
            status  = '<a marked="1" href="/business/get-apartment-details/?apartment_id='+ str(property_obj.property_id)+'"><span class="label label-info">Available</span></a>'
        if property_obj.property_availability_status == NOT_AVAILABLE:
            status  = '<a marked="1" href="/business/get-apartment-details/?apartment_id='+ str(property_obj.property_id)+'"><span class="label label-success">Not Available</span></a>'
        # if property_obj.property_status == BOOKING_COMPLETED:
        #     status  = '<a marked="1" href="/business/get-apartment-details/?apartment_id='+ str(property_obj.property_id)+'"><span class="label label-warning">Completed</span></a>'
        # if property_obj.property_status == BOOKING_CANCELLED:
        #     status = '<a marked="1" href="/business/get-apartment-details/?apartment_id='+ str(property_obj.property_id)+'"><span class="label label-danger">Cancelled</span></a>'

        more = '<a marked="1" href="/business/get-apartment-details/?apartment_id='+ str(property_obj.property_id)+'"><i class="fa-2x pe-7s-more text-primary2"></i></a>'
        # print property_obj.property_id
        if property_obj.property_owner_id:
            owner_name=property_obj.property_owner_id.cust_first_name

        # print property_obj.property_owner_id.cust_first_name
        return {
                'apt_id': property_obj.property_id,
                'city':property_obj.property_location,
                'apartment_name': property_obj.property_actual_name,
                'owner':owner_name or "",
                'no_of_rooms' : property_obj.number_of_rooms,
                'status' : status,'more':more
            }


# # This is used for getting specific details of specific apartment
# def get_apartment_details(request):
    
#     try:
#         apt_obj = Apartment.objects.get(apt_id=request.GET.get('apartment_id'))
#         data = { 'success': 'true',
#          'apartment': apt_obj ,
#          'room_list': apt_obj.property_id.all()
#          # 'facilities' : apt_obj.get_apartment_features() 
#          }
#     except Exception, e:
#         print 'error' ,e
#         data = { 'sucess': 'false', ExceptionLabel.ERROR_MESSAGE :'Server Error' }
#     return render(request,'apartment_details.html',data, context_instance=RequestContext(request))

def get_apartment_details(request):
    print "innthe property_info"
    print request
    try:
        apt_obj = Property.objects.get(property_id=request.GET.get('apartment_id'))
        data = { 'success': 'true',
                 'apartment': apt_obj,
                 'room_list': apt_obj.property_rooms.all(),
                 'facilities' : get_facility(apt_obj)
                }
        print data

    except Exception, e:
        # transaction.savepoint_rollback(sid)
        print 'error', e
        data = { 'sucess': 'false', ExceptionLabel.ERROR_MESSAGE :'Server Error' }
    return render(request,'apartment_details.html',data, context_instance=RequestContext(request))
  
'''
-------------------------------------------------------------------------------
THESE API's RELATED WITH THE ROOM SERVICES
-------------------------------------------------------------------------------
'''

@csrf_exempt
@transaction.atomic
def save_room_information(request):
    sid = transaction.savepoint()
    try:
        print 'Hello'
        # pdb.set_trace()
        if request.method == "POST":
            print 'Request Accepted ',request
            apt_room_obj = PropertyRoom(
                room_number                 = request.POST.get('room_number'),
                room_type                   = request.POST.get('room_type'),
                # no_of_occupant_allowed      = request.POST.get('no_of_occupants'),
                room_status                 = 0,
                room_active_status          = 1,
                room_creation_date          =datetime.datetime.now(),
            )

            apt_room_obj.save()
            print "done"
            transaction.savepoint_commit(sid)
            data = {'success': 'true', 'update':'false', 'room_id':apt_room_obj.room_id, 'room_number': apt_room_obj.room_number, 'room_type': apt_room_obj.room_type
             # 'occupant_cnt' : apt_room_obj.no_of_occupant_allowed 
             }
        else:
            print 'Invalid Request'
            # transaction.savepoint_rollback(sid)
            data = {'sucess': 'false' , ExceptionLabel.ERROR_MESSAGE :'Invalid Request'}
    except Exception, e:
        print 'error',e
        transaction.savepoint_rollback(sid)
        data = {'sucess': 'false', ExceptionLabel.ERROR_MESSAGE :'Server Error'}
    return HttpResponse(json.dumps(data), content_type='application/json')

def edit_apartment_room(request):
    try:

        print 'Hello'
        if request.method == "POST":
            #roomForm= ApartmentRoomForm(request.POST,request.FILES)
            print 'Request Accepted '
            print request
            print request.FILES
            apt_room_obj = PropertyRoom.objects.get(room_id=request.POST.get('edit_apt_room_id'))
            apt_room_obj.room_number = request.POST.get('edit_room_number')
            apt_room_obj.room_type       = request.POST.get('edit_room_type')
            apt_room_obj.room_active_status = request.POST.get('edit_room_active_status')
            apt_room_obj.save()
            data = {'success': 'true',
             'room_id':apt_room_obj.room_id,
             'room_number': apt_room_obj.room_number,
             'room_type': apt_room_obj.room_type
             # 'room_rate' : apt_room_obj.apt_room_rate
            }
        else:
            print 'Invalid Request'
            data = {'sucess': 'false' , ExceptionLabel.ERROR_MESSAGE :'Invalid Request'}
    except Exception, e:
        print 'error',e
        data = {'sucess': 'false', ExceptionLabel.ERROR_MESSAGE :'Server Error'}
    return HttpResponse(json.dumps(data), content_type='application/json')



'''
-------------------------------------------------------------------------------
THESE API's RELATED WITH THE OWNER  
-------------------------------------------------------------------------------
'''
@csrf_exempt
@transaction.atomic
def save_owner_information(request):
    print "in the saVEsave_owner_information "
    sid = transaction.savepoint()
    try:
        if request.method == "POST":
            print 'Request Accepted '
            apt_owner_obj = Customer(
                cust_first_name       = request.POST.get('owner_first_name'),
                cust_last_name        = request.POST.get('owner_last_name'),
                cust_email            = request.POST.get('owner_email'),
                email                 = request.POST.get('owner_email'),
                cust_contact_no       = request.POST.get('owner_contact'),
                cust_address_line     = request.POST.get('owner_address'),
                username              = request.POST.get('owner_email'), # User Name ByDefault email id for owner
                cust_city             = request.POST.get('city'),
                cust_state            = request.POST.get('state'),
                cust_country          = request.POST.get('country'),
                cust_pincode          = request.POST.get('pincode'),
                cust_gender           = request.POST.get('gender'),
                cust_age              = request.POST.get('owner_age'),
                email_alert_on        = request.POST.get('email_alert'),
                sms_alert_on          = request.POST.get('sms_alert'),
                cust_creation_date    = datetime.datetime.now(),
                user_type             = 2
                )
            apt_owner_obj.save()
            apt_owner_obj.cust_unique_id = 'PRO'+ datetime.date.today().strftime('%d%m%y') + str(apt_owner_obj.user_ptr_id).zfill(6)
            apt_owner_obj.save()
            transaction.savepoint_commit(sid)
            data = {'success': 'true', 'owner_id':apt_owner_obj.cust_unique_id, 'owner_name': apt_owner_obj.cust_first_name }
        else:
            print 'Invalid Request'
            transaction.savepoint_rollback(sid)
            data = {'success': 'false' , ExceptionLabel.ERROR_MESSAGE :'Invalid Request'}
    except Exception, e:
        transaction.savepoint_rollback(sid)
        print 'error',e
        print(traceback.format_exc())
        data = {'sucess': 'false', ExceptionLabel.ERROR_MESSAGE :'Server Error'}
    return HttpResponse(json.dumps(data), content_type='application/json')


# This is for opening edit the apartment page.
def edit_apartment_page(request):
    try:
        apt_obj = Property.objects.get(property_id=request.GET.get('apartment_id'))
        try:
            rates = apt_obj.property_rates.get()
        except Exception as err:
            rates = None
        data = { 'success': 'true', 'apartment': apt_obj , 'room_list': apt_obj.property_rooms.all(),
        'property_rate': rates,'image_list':get_image_list(apt_obj),
        'owner_list': get_apartment_owner_list(),'image_ids':get_image_list(apt_obj),
        'state_list' : pcf.get_all_state_name() }
    except Exception, e:
        print 'error', e
        data = { 'sucess': 'false', ExceptionLabel.ERROR_MESSAGE :'Server Error' }
    return render(request,'edit-apartment.html',data, context_instance=RequestContext(request))


def get_image_list(apt_obj):
    #property_image_list={"id":"","url":""}
    property_image_ids = []
    property_image_urls = []
    property_image= apt_obj.PropertyImages.all()
    for image in property_image:
#       property_image_list['id']=image.image_id
#       property_image_list['url']=SERVER_URL + image.image_name.url
       property_image_ids.append(str(image.image_id))
       property_image_urls.append(SERVER_URL + image.image_name.url)

    if property_image_ids:
        return property_image_ids, property_image_urls
    else:
        return [],[]


@csrf_exempt
def update_apartment_info(request):
    try:
        # pdb.set_trace()
        print request.POST
        if request.method == "POST":
            print 'Request Accepted '
            print request.POST.get('facilities_list')
            room_ids = request.POST.get('room_id_list')
            room_ids = room_ids.strip(' ')
            room_ids = room_ids.split(' ')
            room_ids = [x for x in room_ids if x]
            no_of_rooms = len(room_ids)
            print 'property_owner_name'
            print request.POST.get('property_owner_name')

            apt_obj = Property.objects.get(property_id=request.POST.get('property_id'))
            apt_obj.property_display_name                   = request.POST.get('property_display_name')
            apt_obj.property_actual_name                    = request.POST.get('property_actual_name')
            apt_obj.property_owner_id                       = Customer.objects.get(user_ptr_id=request.POST.get('property_owner_name'))
            apt_obj.property_description                    = request.POST.get('property_description')
            #apt_obj.property_creation_date                  = datetime.datetime.now()
            apt_obj.property_address                        = request.POST.get('address_line')
            apt_obj.property_location                       = request.POST.get('location') #request.POST.get('address_line')+','+request.POST.get('location')+','+request.POST.get('city')+','+request.POST.get('state')+','+request.POST.get('country') 
            apt_obj.property_city                           = request.POST.get('city')  
            apt_obj.property_state                          = request.POST.get('state')  
            apt_obj.property_country                        = request.POST.get('country')
            apt_obj.latitude                                = request.POST.get('lattitude') or 0.0
            apt_obj.longitude                               = request.POST.get('longitude') or 0.0
            apt_obj.distance_from_railway_station           = request.POST.get('dist_from_railway_station') or 0.0
            apt_obj.distance_from_airport                   = request.POST.get('dist_from_airport_station') or 0.0
            apt_obj.nearest_railway_station                 = request.POST.get('nearest_railway_station') 
            apt_obj.nearest_bus_stop                        = request.POST.get('nearest_bus_stop')
            apt_obj.remark                                  = request.POST.get('remark')
            apt_obj.rack_rate                               = request.POST.get('rack_rate')
            apt_obj.contact_person                          = request.POST.get('contact_person')
            apt_obj.contact_person_email_id                 = request.POST.get('contact_person_email')
            apt_obj.contact_person_phone_no                 = request.POST.get('contact_person_phno')
            apt_obj.property_availability_status            = 0
            apt_obj.property_status                         = 0
            apt_obj.save()
            if request.POST.get('no_of_person_per_rooms'):
                apt_obj.no_of_person_allowed_per_room           =int(request.POST.get('no_of_person_per_rooms'))
            if request.POST.get('no_of_rooms'):
                apt_obj.number_of_rooms                         = int(request.POST.get('no_of_rooms'))
            if request.POST.get('pincode'):
                apt_obj.property_pincode                        = int(request.POST.get('pincode'))
            if request.POST.get('star'):
                print "----------------"
                apt_obj.star_category                           =int(request.POST.get('star'))
            else:
                print "else"
                apt_obj.star_category                           =3
            if request.POST.get('facilities_list'):
                apt_obj.property_facility                       =str(request.POST.get('facilities_list'))
            apt_obj.save()
            edit_property_rate(request,apt_obj)
            apt_obj.save()
            # save_property_images(request,apt_obj)
            if no_of_rooms > 0:
                for roomid in room_ids:
                    room = PropertyRoom.objects.get(room_id=roomid)
                    room.property_id = apt_obj
                    room.save()
            
            # transaction.savepoint_commit(sid)
            return redirect('/business/property-info/?property_token='+str(apt_obj.property_id) +'&update=update' )
        else:
            print 'Invalid Request'
            # transaction.savepoint_rollback(sid)
            data = { 'sucess': 'true' , ExceptionLabel.ERROR_MESSAGE :'Invalid Request' }
    except Exception, e:
        # transaction.savepoint_rollback(sid)
        print 'error', e
        data = { 'sucess': 'false', ExceptionLabel.ERROR_MESSAGE :'Server Error' }


def edit_property_rate(request,apt_obj):
    print "in the edit_property_rate"
    try:
        if apt_obj:
            property_rate_obj = PropertyRate.objects.get(property_id=apt_obj)
            property_rate_obj.property_agreed_rate                             = request.POST.get('agreed_rate') or '0.0'
            property_rate_obj.property_display_rate                            = request.POST.get('display_rate') 
            property_rate_obj.property_discount_rate                           = request.POST.get('discount_rate') or '0.0'
            property_rate_obj.single_occupancy_display_rate                    = request.POST.get('single_occ_display_rate') or '0.0'
            property_rate_obj.single_occupancy_agreed_rate                     = request.POST.get('single_occ_agreed_rate') or '0.0'
            property_rate_obj.double_occupancy_display_rate                    = request.POST.get('double_occ_display_rate') or '0.0'
            property_rate_obj.double_occupancy_agreed_rate                     = request.POST.get('double_occ_agreed_rate') or '0.0'
            property_rate_obj.additional_occupancy_display_rate                = request.POST.get('additional_occ_display_rate') or '0.0'
            property_rate_obj.additional_occupancy_agreed_rate                 = request.POST.get('additional_occ_agreed_rate') or '0.0'
            property_rate_obj.save()
        return ""
    except Exception, e:
        print e
        return False



