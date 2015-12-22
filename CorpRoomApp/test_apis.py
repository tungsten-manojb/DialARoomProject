
from django.shortcuts import render
from django.contrib.auth.models import User

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

# this is for constants the 
from constants import ExceptionMessages, ExceptionLabel
from CorpRoomApp.models import *
from datetime import date


@csrf_exempt
def mobile_login(request):
    print 'request accepted'
    print request
    #pdb.set_trace()
    try:
        if request.method == 'POST':
            #json_obj=json.loads(request.body)
            #print 'JSON OBJECT : ',json_obj
            user = authenticate(username=request.POST.get('username'), password= request.POST.get('password'))
            if user is not None:
                if user.is_active:
                    data= {'success' : 'true', ExceptionLabel.ERROR_MESSAGE:'Successfully Login' }
                    print data
                else:
                    data= {'success' : 'false', ExceptionLabel.ERROR_MESSAGE:'User Is Not Active'}
            else:
                data= {'success' : 'false', ExceptionLabel.ERROR_MESSAGE:'Invalid Username or Password'}
        else:
            data= {'success' : 'false', ExceptionLabel.ERROR_MESSAGE:'Invalid Request'}
    except User.DoesNotExist:
        print 'usr'
        data= {'success' : 'false', ExceptionLabel.ERROR_MESSAGE:'User Not Exist'}
    except MySQLdb.OperationalError, e:
        print e
        data= {'success' : 'false', ExceptionLabel.ERROR_MESSAGE:'Internal Server Error '}
    except Exception, e:
        print e
        data= {'success' : 'false', ExceptionLabel.ERROR_MESSAGE:'Internal Server Error '}
    return HttpResponse(json.dumps(data), content_type='application/json')


def invoice_page(request):
    data = {'invoice_no' : 'INV123456' }
    return render( request, 'web/invoice-print.html', data )