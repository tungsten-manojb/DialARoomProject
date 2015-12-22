
from CorpRoomApp.models import *
from quoteapp.models import *

from django.shortcuts import render
from django.contrib.auth.models import User
from django.template import RequestContext



def display_customer_statistics(request):
    
    
    data = {}
    customer_stats = UserBookingStatisticTrack.objects.all()
    return render(request,'customer-statistics.html',data, context_instance=RequestContext(request))
    


def display_customer_trace(request):
    pass
    