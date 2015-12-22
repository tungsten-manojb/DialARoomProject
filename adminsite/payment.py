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



@csrf_exempt
@transaction.atomic
def save_payment_information(request):
	print "save_payment_information"
	# pdb.set_trace()
	# print request
	print request.POST.get('payment_amt')
	sid = transaction.savepoint()
	try:
		if request.method == "POST":
			corporate_obj = CorporateTransaction(
		    	corporate_id             = Customer.objects.get(user_ptr_id=request.POST.get('cam_name')),
		        transaction_amount       = float(request.POST.get('payment_amt')),
		        transaction_type         = int(request.POST.get('payment_type')),
		        transaction_method       = request.POST.get('payment_method'),
		        cheque_number            = request.POST.get('cheque_no'),
		        cheque_bank_branch       = request.POST.get('bank_details'),
		        transaction_date         = datetime.datetime.now()
		        )
			corporate_obj.save()
			print "done"
		transaction.savepoint_commit(sid)
		data = {'success': 'true'
		 # 'company_id':company_obj.company_id,
		 #  'company_name':company_obj.company_name
		   }

	except Exception, e:
	# 	# transaction.savepoint_rollback(sid)
		print 'error',e
		data = {'success': 'false', ExceptionLabel.ERROR_MESSAGE :'Server Error'}
	return HttpResponse(json.dumps(data), content_type='application/json')




def get_payment_list(request):
    try:
        print 'get_payment_list List'
        payment_list=[]
        transaction_list = CorporateTransaction.objects.all()
        for transaction in transaction_list:
            payment_list.append(transaction.get_payment_info())
        data = {'success':'true', 'data': payment_list }
    except Exception, e:
        print 'Exception : ',e
        data = {'success':'false', 'data' : ''}
    return HttpResponse(json.dumps(data), content_type='application/json')	


