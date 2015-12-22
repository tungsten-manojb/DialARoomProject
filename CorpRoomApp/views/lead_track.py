
"""
__author__      = 'ManojB'
__version__     = '0.0.1'
__created_date__ = '28-08-2015'
This module is related lead traking 
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
from LeadTrackingApp.models import *

def lead_tracking_page(request):
    return render_to_response('web/lead_tracking.html')


@csrf_exempt
def save_lead_details(request):
    print "in the save_lead_details"
    try:
        print 'Saving Lead Tracking'
        lead = LeadTracker(
            company_name =  request.POST.get('companyName'),
            company_category= request.POST.get('companyCategory'),
            company_address=request.POST.get('companyAddress'),
            company_city=request.POST.get('cityName'),
            cust_name= request.POST.get('customerName'),
            cust_designation= request.POST.get('designation'),
            cust_mobile_no= request.POST.get('mobileNumber'),
            cust_landline_no= request.POST.get('phoneNumber'),
            cust_email= request.POST.get('emailId'),
            dar_executive= request.POST.get('darExecutive'),
            follow_up_count= request.POST.get('followUpCount'),
            lead_status       =  request.POST.get('leadstatus'),
            meeting_remark    =  request.POST.get('remark'),
            call_to_action    =  request.POST.get('action'),
            lead_dept         = request.POST.get('leaddept'),
            potential_room_nights=request.POST.get('roomnights')
        )
        lead.save()
        if request.POST.get('meetingdate'):
            lead.meeting_date      = datetime.datetime.strptime(request.POST.get('meetingdate'),'%m/%d/%Y').date()
        if request.POST.get('followUpDate'):
            lead.follow_up_date    = datetime.datetime.strptime(request.POST.get('followUpDate'),'%m/%d/%Y').date() 

        lead.save()
        lead.lead_tracking_unique_id = 'LEAD' + datetime.date.today().strftime('%d%m%y') + str(lead.lead_tracking_id).zfill(6)
        lead.save()
    except Exception, e:
        print 'Exception ', e
    
    return redirect('/lead-tracking-form/')