from django.db import models

from CorpRoomApp.models import Property
from CorpRoomApp.models import Customer


import datetime
# Create your models here.

QUOTE_STATUS = (
    ('OPEN','OPEN'),
    ('CLOSE','CLOSE'),
)

CUSTOMER_QUOTE_STATUS = (
    ('VIEWED','VIEWED'),
    ('QUOTED','QUOTED'),
    ('EXPIRED','EXPIRED'),
    ('INPROGRESS','INPROGRESS'),
    ('SUBMITTED','SUBMITTED'),
    ('REJECTED','REJECTED'),
    ('ACCEPTED','ACCEPTED'),
    ('CANCELLED','CANCELLED'),
    ('BOOKED','BOOKED')
)

class QuoteRequest(models.Model):
    quote_request_id        = models.AutoField(primary_key=True)
    quote_request_uid       = models.CharField("Quote Unique ID",max_length=30, null=True,blank=True)
    quote_category          = models.CharField("Quote Category",max_length=30, null=True,blank=True)
    quote_sub_category      = models.CharField("Quote Category",max_length=30, null=True,blank=True)
    quote_property_type     = models.CharField("Property Type",max_length=30, null=True,blank=True)
    property_rating         = models.IntegerField("Property Rating",default=1,null=True,blank=True)
    quote_start_date        = models.DateField('Start Date', null=True,blank=True)
    quote_end_date          = models.DateField('Start Date', null=True,blank=True)
    quote_city              = models.CharField("Target City",max_length=30, null=True,blank=True)
    quote_location          = models.CharField("Quote Category",max_length=70, null=True,blank=True)
    quote_lowest_price      = models.FloatField("Range Min Price", default=0.0,null=True,blank=True)
    quote_highest_price     = models.FloatField("Range Min Price", default=0.0,null=True,blank=True)
    quote_no_of_guest       = models.IntegerField("Number Of Guest",default=0,blank=True)
    quote_no_of_room        = models.IntegerField("Number Of Guest",default=0,blank=True)
    quote_request_creation_date = models.DateTimeField('Created Date', null=True,blank=True)
    quote_request_update_date   = models.DateTimeField('Update Date',default=datetime.datetime.now() ,null=True,blank=True)
    quote_remark            = models.CharField("Quote Remark",max_length=250, null=True,blank=True)
    quote_request_status    = models.CharField("Quote Status",max_length=10, choices=QUOTE_STATUS, null=True,blank=True)
    quote_admin_status      = models.CharField("Quote ADMIN Status",max_length=20, choices=CUSTOMER_QUOTE_STATUS, null=True,blank=True)
    quote_customer_status   = models.CharField("Quote Customer Status",max_length=20, choices=CUSTOMER_QUOTE_STATUS, null=True,blank=True)
    customer_id             = models.ForeignKey(Customer,related_name='customer_request')
    
    def __unicode__(self):
        return self.quote_request_uid
    
    def get_quote_info(self):
        info = '<a href="../request-details/?request_uid='+self.quote_request_uid +'"><i class="fa-2x pe-7s-more text-info"></i></a>'
        return { 'quote_request_uid' : self.quote_request_uid, 'quote_category':self.quote_category, 'city': self.quote_city,
        'quote_sub_category': self.quote_sub_category, 'quote_admin_status': self.quote_admin_status, 'date': self.quote_request_creation_date.strftime('%d/%m/%Y'), 'info':info }

    def get_vendor_quote_info(self):
        info = '<a class="btn btn-info btn-circle" href="../request-details/?request_uid='+self.quote_request_uid +'"><i class="fa fa-check"></i></a>'
        return { 'quote_request_uid' : self.quote_request_uid,'quote_user':self.customer_id.cust_first_name, 'quote_category':self.quote_category, 'city': self.quote_city,
        'quote_sub_category': self.quote_sub_category, 'quote_admin_status': self.quote_admin_status, 'date': self.quote_request_creation_date.strftime('%d/%m/%Y'), 'info':info }
    

class QuotationResponse(models.Model):
    quotation_id            = models.AutoField(primary_key=True)
    quotation_uid           = models.CharField("Quotation UID",max_length=20, null=True,blank=True)
    request_id              = models.ForeignKey(QuoteRequest,related_name='qoatation_response')
    property_id             = models.ForeignKey(Property,related_name='requested_property')
    property_rack_rate      = models.FloatField("Rack Rate Per Night", default=0.0,null=True,blank=True)
    rate                    = models.FloatField("Rate Per Night", default=0.0,null=True,blank=True)
    amount                  = models.FloatField("Total Amount", default=0.0,null=True,blank=True)
    tax_amount              = models.FloatField("Tax Amount", default=0.0,null=True,blank=True)
    total_quote_amt         = models.FloatField("Total Quotation Amount", default=0.0,null=True,blank=True)
    quote_date              = models.DateField('Quatation Date', null=True,blank=True)
    created_date            = models.DateTimeField('Created Date', null=True,blank=True)
    updated_date            = models.DateTimeField('Update Date',default=datetime.datetime.now() ,null=True,blank=True)
    created_by              = models.CharField("Created By",max_length=70, null=True,blank=True)
    is_new                  = models.BooleanField("Is New Quotation", default=True)
    quotation_status        = models.CharField("Quatation Status",max_length=20, choices = CUSTOMER_QUOTE_STATUS,null=True)
    viewed_by_customer      = models.BooleanField("Viewed By Customer", default=False)
    action                  = models.CharField("Action", max_length=100, blank=True)

    def __unicode__(self):
        return str(self.quotation_uid)

    def get_quotation_info(self):
        info = '<a href="../quotation-details/?quotation_uid='+self.quotation_uid +'&quote_request_uid='+ self.request_id.quote_request_uid +'"><i class="fa-2x pe-7s-more text-info"></i></a>'
        return { 'quote_request_uid' : self.request_id.quote_request_uid ,
                 'quotation_uid': self.quotation_uid,
                 'property_name' : self.property_id.property_actual_name,
                 'rate' : self.rate, 'status' : self.quotation_status,
                 'location' : self.property_id.property_location,
                 'date' : self.created_date.strftime('%d/%m/%Y'),
                 'info':info }

class RequestedProperty(models.Model):
    requested_property_id   = models.AutoField(primary_key=True)
    quote_request_id        = models.ForeignKey(QuoteRequest,related_name='requested_property', null=False) 
    property_id             = models.ForeignKey(Property, related_name='r_property', null=False)
    property_owner_id       = models.ForeignKey(Customer, related_name='owner_req_property', null=True)
    quoted_status           = models.BooleanField('Quotation Status',default=False)
    created_date            = models.DateTimeField('Created Date', null=True,blank=True)
    updated_date            = models.DateTimeField('Update Date',default=datetime.datetime.now() ,null=True,blank=True)
    created_by              = models.CharField("Created By",max_length=70, null=True,blank=True)

    def __unicode__(self):
        return str(self.requested_property_id)

# This is added on 11 Dec 2015
class UserRequestStatisticTrack(models.Model):
    user_request_statistic_track_id = models.AutoField(primary_key=True)
    user_id             = models.ForeignKey(Customer,null=True,verbose_name="Customer Name", blank=True)
    request_path        = models.CharField('Booking Path',max_length=100)
    count               = models.PositiveIntegerField(default=1)
    current_timestamp   = models.DateTimeField('Current Time Stamp',default=datetime.datetime.now())
    request_date        = models.DateField()
    request_id          = models.ForeignKey(QuoteRequest,verbose_name="Quotation Request", null =True)
    
    def __unicode__(self):
        return 'Request From ' + str(self.user_id.username) + ' on ' + self.request_date.strftime('%d/%m/%Y')

