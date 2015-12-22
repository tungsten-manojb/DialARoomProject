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


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def customer_list_page(request):
    if not request.user.is_authenticated():
        return redirect('/')
    return render(request,'customer-list.html')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def payment_list_page(request):
    try:
        data = { 'cam_list': get_cam_list()}
    except Exception, e:
        print 'Exception :',e
    return render(request,'payment-list.html',data, context_instance=RequestContext(request))

def get_cam_list():
    try:
        cam_user_list=[]
        cam_list = Customer.objects.filter(user_type='1')
        for cam in cam_list:
            cam_user_list.append(get_cam_info(cam))
        return cam_user_list
    except Exception, e:
        print 'Exception :',e
    return cam_user_list
    
def get_cam_info(cam):
    return { 'cam_id': cam.user_ptr_id ,'cam_name' : cam.cust_first_name+' '+cam.cust_last_name }

# This will give the all company list for adding the 
def get_cam_company_list():
    try:
        cam_company_list=[]
        company_list = Company.objects.all()
        for company in company_list:
            cam_company_list.append(get_company_info(company))
        return cam_company_list
    except Exception, e:
        print 'Exception :',e
    return cam_company_list

def get_company_info(company):
    return { 'company_id': company.company_id ,'company_name' : company.company_name }


def get_company_info(company):
    return { 'company_id': company.company_id ,'company_name' : company.company_name }

def get_rmmanager_list():
    try:
        get_rmmanager_list=[]
        rm_list = RelationShipManager.objects.all()
        for rm in rm_list:
            get_rmmanager_list.append(get_rm_info(rm))
        return get_rmmanager_list
    except Exception, e:
        print 'Exception :',e
    return cam_company_list



def get_rm_info(rm):
    return { 'manager_id': rm.relationship_manager_id ,'manager_name' : rm.rm_first_name + " "+ rm.rm_last_name }
    
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def add_customer_page(request):
    if not request.user.is_authenticated():
        return redirect('/')
    data = { 'cam_company_list': get_cam_company_list() , 'get_rmmanager_list': get_rmmanager_list(),'get_property_list': get_property_list() }
    #return render_to_response('add-cam-customer.html')
    return render(request,'add-cam-customer.html',data, context_instance=RequestContext(request))

# This will give the all company list for adding the 
def get_property_list():
    try:
        apt_list=[]
        property_list = Property.objects.all()
        for apt in property_list:
            apt_list.append({'property_id':apt.property_id,
                            'property_name':apt.property_actual_name,
                            'property_location':apt.property_location})
        return apt_list
    except Exception, e:
        print 'Exception :',
    return apt_list



def customer_confirm(request):
    if not request.user.is_authenticated():
        return redirect('/')
    return render_to_response('customer-confirm.html')

# This is for getting the list of CAM customers
def get_cam_customer_list(request):
    try:
        print 'Apartment List'
        customer_list=[]
        cam_list = Customer.objects.filter(user_type='1')
        for cam in cam_list:
            customer_list.append(get_cam_user_info(cam))
        data = {'success':'true', 'data': customer_list }
    except Exception, e:
        print 'Exception : ',e
        data = {'success':'true'}
    return HttpResponse(json.dumps(data), content_type='application/json')
        
def get_cam_user_info(cam):
    more = '<a marked="1" href="/business/customer-detail-display/?customer_id='+ str(cam.user_ptr_id)+'"><i class="fa-2x pe-7s-more text-primary2"></i></a>'
    company_name = ''
    if cam.user_type==1:
        if cam.cust_company_id:
            company_name = cam.cust_company_id.company_name
    return {
        'cust_id' : str(cam.id), 'customer_name': cam.cust_first_name +' '+cam.cust_last_name ,
        'company_name': company_name, 'city': cam.cust_city,
        'email_id':cam.cust_email,'contact_number': cam.cust_contact_no, 
        'more':more
    }


@csrf_exempt
@transaction.atomic
def save_company_information(request):
    # pdb.set_trace()
    sid = transaction.savepoint()
    try:
        if request.method == "POST":
            company_obj = Company(
                company_name = request.POST.get('company_name'),
                company_email       = request.POST.get('company_email'),
                company_phone_no   = request.POST.get('contact_number'),
                company_address   = request.POST.get('address_line'),
                company_city   = request.POST.get('city'),
                company_state   = request.POST.get('state'),
                company_country   = request.POST.get('country'),
                company_pincode   = request.POST.get('pincode'),
                company_creation_date=datetime.datetime.now()
                )
            company_obj.save()
            print "done"
            company_obj.company_unique_id=str('CO'+ datetime.date.today().strftime('%d%m%y') + str(company_obj.company_id).zfill(4))
            company_obj.save()
            transaction.savepoint_commit(sid)
            data = {'success': 'true', 'company_id':company_obj.company_id, 'company_name':company_obj.company_name }
        else:
            print 'Invalid Request'
            transaction.savepoint_rollback(sid)
            data = {'sucess': 'false' , ExceptionLabel.ERROR_MESSAGE :'Invalid Request'}
    except Exception, e:
        transaction.savepoint_rollback(sid)
        print 'error',e
        data = {'sucess': 'false', ExceptionLabel.ERROR_MESSAGE :'Server Error'}
    return HttpResponse(json.dumps(data), content_type='application/json')

@csrf_exempt
@transaction.atomic
def save_manager_information(request):
    sid = transaction.savepoint()
    try:
        if request.method == "POST":
            rm_obj = RelationShipManager(
                rm_first_name = request.POST.get('first_name'),
                rm_last_name       = request.POST.get('last_name'),
                rm_email   = request.POST.get('manager_email'),
                rm_contactno   = request.POST.get('manager_number'),
                rm_status   = 1,
                rm_creation_date=datetime.datetime.now()
                )
            rm_obj.save()
            print "done"
            rm_obj.rm_unique_id=str('RM'+ datetime.date.today().strftime('%d%m%y') + str(rm_obj.relationship_manager_id).zfill(4))
            rm_obj.save()
            transaction.savepoint_commit(sid)
            data = {'success': 'true', 'manager_id':rm_obj.relationship_manager_id, 'manager_name':rm_obj.rm_first_name +" "+ rm_obj.rm_last_name  }
        else:
            print 'Invalid Request'
            data = {'sucess': 'false' , ExceptionLabel.ERROR_MESSAGE :'Invalid Request'}
    except Exception, e:
        transaction.savepoint_rollback(sid)
        print 'error',e
        data = {'sucess': 'false', ExceptionLabel.ERROR_MESSAGE :'Server Error'}
    return HttpResponse(json.dumps(data), content_type='application/json')

@csrf_exempt
def save_cam_information(request):
    # pdb.set_trace()
    sid = transaction.savepoint()
    fav_obj={}
    try:
        if request.method == "POST":
            cam_obj = Customer(
                username = request.POST.get('user_name'),
                password = request.POST.get('passwd'),
                cust_first_name = request.POST.get('first_name'),
                cust_last_name = request.POST.get('last_name'),
                cust_company_id = Company.objects.get(company_id=request.POST.get('company_name')),
                cust_email       = request.POST.get('cam_email'),
                cust_contact_no  = request.POST.get('contact_number'),
                cust_address_line   = request.POST.get('address_line'),
                cust_city   = request.POST.get('city'),
                cust_state   = request.POST.get('state'),
                cust_country   = request.POST.get('country'),
                cust_pincode   = request.POST.get('pincode'),
                cust_gender   = request.POST.get('gender'),
                cust_age   = request.POST.get('cam_age'),
                email_alert_on   = request.POST.get('email_alert'),
                sms_alert_on   = request.POST.get('sms_alert'),
                cust_creation_date   = datetime.datetime.now(),
                user_type        = 1,
                relationship_manager_id=RelationShipManager.objects.get(relationship_manager_id=request.POST.get('rm_name')),
                cust_status=1
            )
            cam_obj.save()
            cam_obj.cust_unique_id = 'CAM'+ datetime.date.today().strftime('%d%m%y') + str(cam_obj.id).zfill(6)
            cam_obj.set_password(request.POST.get('passwd'))
            cam_obj.save()
            property_ids=request.POST.get('property_ids')
            # print "property_ids"
            # print property_ids
            if property_ids:
                id_list=property_ids.split(',')
                for ids in id_list:
                    if ids!='':
                        fav_obj = CustomerFavoriteProperty(
                        customer_id=cam_obj,
                        property_id=Property.objects.get(property_id=ids))
                        fav_obj.save()
            transaction.savepoint_commit(sid)
#            data = {'success': 'true','cam':cam_obj, 'mode':'show','fav_obj':get_favorite_list(cam_obj)}
#            print "'fav_obj"
            return redirect('../customer-detail-display/?customer_id='+str(cam_obj.id))
#            print get_favorite_list(cam_obj)
        else:
            transaction.savepoint_rollback(sid)
            print 'Invalid Request'
            data = {'sucess': 'false' , ExceptionLabel.ERROR_MESSAGE :'Invalid Request'}
    except Exception, e:
        transaction.savepoint_rollback(sid)
        print 'error',e
        data = {'sucess': 'false', ExceptionLabel.ERROR_MESSAGE :'Server Error'}
    return render(request,'customer-confirm.html',data, context_instance=RequestContext(request))


def get_favorite_list(cam_obj):
    fav_list=[]
    try:
        fav_obj = CustomerFavoriteProperty.objects.filter(customer_id=cam_obj)
        if fav_obj:
            for fav in fav_obj:
                fav_list.append({'property_id':fav.property_id})
                print fav_list
    except Exception, e:
        print 'Exception :',e
    return fav_list



@csrf_exempt
def delete_fav_property(request):
    # print "delete_fav_property"
    try:
        fav_obj = CustomerFavoriteProperty.objects.get(
            customer_id=Customer.objects.get(user_ptr_id=request.POST.get('cam_id')),
            property_id=Property.objects.get(property_id=request.POST.get('property_id')))
        fav_obj.delete()
    except Exception, e:
        print 'Exception :',e
    return HttpResponse(json.dumps(data), content_type='application/json')
   
      
@csrf_exempt
def add_fav_property(request):
    # print "add_fav_property"
    status=''
    try:
        if check_exist(request)=='exist':
            status='exist'
        else:
            fav_obj = CustomerFavoriteProperty(
                customer_id=Customer.objects.get(user_ptr_id=request.POST.get('cam_id')),
                property_id=Property.objects.get(property_id=request.POST.get('property_id')))
            fav_obj.save()
            status='true'
        data = {'success': status , ExceptionLabel.ERROR_MESSAGE :'Invalid Request'}
    except Exception, e:
        print 'Exception :',e
        data = {'success': 'false' , ExceptionLabel.ERROR_MESSAGE :'Invalid Request'}
    return HttpResponse(json.dumps(data), content_type='application/json')
   

def check_exist(request):
    try:
        fav_obj = CustomerFavoriteProperty.objects.get(
                    customer_id=Customer.objects.get(user_ptr_id=request.POST.get('cam_id')),
                    property_id=Property.objects.get(property_id=request.POST.get('property_id')))
        if fav_obj:
            return 'exist'
    except Exception, e:
        print 'Exception :',e
        return ''        



def customer_detail_display(request):
    """
    This request method is use for showing the customer details.
    it takes customer_id as parameter and
    redirect page to the customer-confirm.html to show the information.
    """
    try:
        print 'Customer Detail Display'
        fav_list=[]
        cam_obj = Customer.objects.get(user_ptr_id=request.GET.get('customer_id'))
        fav_obj = CustomerFavoriteProperty.objects.filter(customer_id=cam_obj)
        if fav_obj:
            for fav in fav_obj:
                print fav
                fav_list.append({'property_id':fav.property_id})
        data = {'success': 'true', 'cam':cam_obj,  'fav_obj':fav_list, 'mode': 'show'}
    except CAM.DoesNotExist, e:
        print 'CAM User Doesnt Exist',e
        data = {'success':'false','error_message':'User Does not Exist'}
    except Exception, e:
        print 'Exception :',e
        data = { 'success':'false','error_message':'Invalid Request' }
    return render(request,'customer-confirm.html',data, context_instance=RequestContext(request))


def edit_customer_details(request):
    #pdb.set_trace()
    try:
        fullname=''
        cam_obj = Customer.objects.get(user_ptr_id=request.GET.get('customer_id'))
        if cam_obj.relationship_manager_id:
            fullname+=cam_obj.relationship_manager_id.rm_first_name
        if cam_obj.relationship_manager_id:
            fullname+=" "+cam_obj.relationship_manager_id.rm_last_name


        
        # fullname=cam_obj.relationship_manager_id.rm_first_name+" "+cam_obj.relationship_manager_id.rm_last_name
        data = {'success': 'true', 'cam':cam_obj, 'rm':fullname,'fav_obj':get_favorite_list(cam_obj),'get_property_list': get_property_list(),'mode': 'edit'}
        print "'fav_obj"
        print get_favorite_list(cam_obj)
    except Customer.DoesNotExist, e:
        print 'CAM User Doesnt Exist',e
        data = {'success':'false','error_message':'User Does not Exist'}
    except Exception, e:
        print 'Exception :',e
        data = { 'success':'false','error_message':'Invalid Request' }
    return render(request,'edit-cam-customer.html',data, context_instance=RequestContext(request))
    
@csrf_exempt
def update_customer_info(request):
    """
    This is for updating the cam Information
    """
    # pdb.set_trace()
    try:
        if request.method == "POST":
            print 'Request Accepted '
            cam_obj = Customer.objects.get(user_ptr_id= request.POST.get('cam_user_id'))
            cam_obj.cust_first_name = request.POST.get('first_name')
            cam_obj.cust_last_name = request.POST.get('last_name')
            # cam_obj.cust_company_id = Company.objects.get(company_id=request.POST.get('company_name'))
            cam_obj.cust_email       = request.POST.get('cam_email')
            cam_obj.cust_contact_no  = request.POST.get('contact_number')
            cam_obj.cust_address_line   = request.POST.get('address_line')
            cam_obj.cust_city   = request.POST.get('city')
            cam_obj.cust_state   = request.POST.get('state')
            cam_obj.cust_country   = request.POST.get('country')
            cam_obj.cust_pincode   = request.POST.get('pincode')
            cam_obj.cust_gender   = request.POST.get('gender')
            cam_obj.cust_age   = request.POST.get('cam_age')
            cam_obj.email_alert_on   = request.POST.get('email_alert')
            cam_obj.sms_alert_on   = request.POST.get('sms_alert')
            # cam_obj.relationship_manager_id=RelationShipManager.objects.get(relationship_manager_id=request.POST.get('rm_name'))

            cam_obj.save()
            data = {'success': 'true','cam':cam_obj,'fav_obj':get_favorite_list(cam_obj), 'mode':'show' }
        else:
            print 'Invalid Request'
            data = {'sucess': 'false' , ExceptionLabel.ERROR_MESSAGE :'Invalid Request'}
    except Exception, e:
        print 'error',e
        data = {'sucess': 'false', ExceptionLabel.ERROR_MESSAGE :'Server Error'}
    return render(request,'customer-updated.html',data, context_instance=RequestContext(request))


def get_customer_guest_list(request):
    guest_list = []
    try:
        cam_id = request.GET.get('cam_user_id')
        #bookings = CAMBooking.objects.filter(cam_id=CAM.objects.get(id=4))
        guests = Guest.objects.filter(customer_id=Customer.objects.get(id=cam_id))
        for guest in guests:
            guest_list.append(get_guest_info(guest))
        print "guest_list"
        print guest_list
        data = { 'success': 'true', 'data': guest_list }
    except Exception, e:
        print 'Exception ',e
        data = { 'success': 'false', 'data': guest_list }
    return HttpResponse(json.dumps(data), content_type='application/json')


def get_guest_info(guest):
    if guest.guest_status:
        status = '<span class="label label-success ">Active</span>'
    else:
        status = '<span class="label label-danger">In-Active</span>' 
    return {
    'guest_id' : guest.guest_id,
    'activate_status': guest.guest_status,
    'guest_name': guest.guest_first_name ,
    'guest_email':  guest.guest_email,
    'guest_contact':guest.guest_contactno,
    # 'status': status, 
    'edit': "<div class='btn btn-primary2 btn-xs' onclick='getRowValues(this,"+ str(guest.guest_id) +" )' ><i class='fa fa-pencil'></i></div>"
    }
    
    