from django.db import models
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

import MySQLdb, sys
import datetime
import time
import pdb
import json
from CorpRoomApp.models import *

#importing product image model
# from models import PropertyImage


PRODUCT_IMAGES_PATH = 'media/property'


# This is temporary for checking images
@csrf_exempt
def imageupload(request):
    print "in the upload image"
    # pdb.set_trace()
    try:
        if request.method == 'POST':
            property_image   =   PropertyImage(image_name   = request.FILES['file'])
            property_image.save()
            data = {'success' : 'true', 'id':property_image.image_id}
        else:
            data = {'success': 'false'}
    except MySQLdb.OperationalError, e:
        data = {'success': 'invalid request'}
    return HttpResponse(json.dumps(data), content_type='application/json')
        
# @csrf_exempt
def remove_image(request):
    print "in the remove image"
    print request.GET
    try:
        image_id=request.GET.get('image_id')
        print 'image id : - >',image_id
        image= PropertyImage.objects.get(image_id=image_id)
        image.delete()
        data = {'success': 'true'}
    except MySQLdb.OperationalError, e:
        data = {'success': 'false'}
    return HttpResponse(json.dumps(data), content_type='application/json')

