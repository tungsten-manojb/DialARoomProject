from django.db import models
from django.contrib.auth.models import User
import datetime
#from quoteapp.models import QuoteResponse
# Create your models here.
import pdb

ROOM_IMAGES_PATH            =   "media/rooms"
CAM_IMAGES_PATH             =   "media/cam"
PROPERTY_DOCUMENT_PATH      =   "media/documents"

SERVER_MEDIA_URL = 'http://192.168.0.121:8000'
#SERVER_MEDIA_URL = 'http://dial-a-room.com'

YES_NO_CHOICES = (
        (0, 'NO'),
        (1, 'YES'),
    )

ACTIVE_DEACTIVE_CHOICES = (
        (1, 'ACTIVE'),
        (0, 'IN-ACTIVE'),
    )

ROOM_TYPE_CHOICES = (
        ('Single','Single Bed'),
        ('Double','Double Bed')
    )

GENDER_CHOICES = (
    ('M','MALE'),
    ('F','FEMALE'),
)

BOOKING_STATUS_CHOICES =(
    (0,'AVAILABLE'),
    (1,'OPEN'),
    (2,'BOOKED'),
    (3,'CANCELLED'),
    (4,'COMPLETED'),
)

PAYMENT_STATUS_CHOICES = (
    ('1','PAID'),
    ('0','UNPAID'),
)

PAYMENT_METHOD = (
    ('ONLINE','ON-LINE'),
    ('ONCHECKOUT','ON-CHECK-OUT')
)

PROPERTY_AVAILABILITY = (
    (True, 'AVAILABLE'),
    (False,'NOT AVAILABLE')
)

PROPERTY_TYPE = (
    (0, 'Service Apartment'),
    (1,'HOTEL')
)

USER_TYPE = (
    (0,'ADMIN'),
    (1,'CORPORATE'),
    (2,'OWNER'),
    (3,'RETAIL'),
)

OCCUPANCY_TYPE = (
    (0,'Single'),
    (1,'Double'),
    (2,'Additional'),
)

TRANSACTION_TYPE = (
    (0,'DEPOSIT'),
    (1,'INVOICE'),
)

TRANSACTION_METHOD = (
    ('CASH','CASH'),
    ('CHEQUE','CHEQUE'),
)


class Company(models.Model):
    company_id                  = models.AutoField(primary_key=True)
    company_unique_id           = models.CharField("Company Unique ID",max_length=30, null=True)
    company_name                = models.CharField("Company Name",max_length=50, null=True)
    company_email               = models.CharField("Company Email",max_length=50, null=True)
    company_site                = models.CharField("Company Website",max_length=50, null=True)
    company_phone_no            = models.CharField("Company Contact No.",max_length=50, null=True)
    company_address             = models.CharField("Company Address",max_length=350, null=True)
    company_city                = models.CharField("City",max_length=50, null=True)
    company_state               = models.CharField("State",max_length=50, null=True)
    company_country             = models.CharField("Country",max_length=50, null=True)
    company_pincode             = models.CharField("Pincode",max_length=50, null=True)
    company_status              = models.IntegerField("Company Status", default=1,choices=ACTIVE_DEACTIVE_CHOICES)
    company_creation_date       = models.DateTimeField()
    company_update_date         = models.DateTimeField(default=datetime.datetime.now())

    def __unicode__(self):
        return self.company_name

    def get_company_address(self):
        return self.company_address+ ', '+ self.company_city 

    def get_company_state_pincode(self):
        return self.company_state + ' - '+ self.company_pincode

class RelationShipManager(models.Model):
    relationship_manager_id                 = models.AutoField(primary_key=True)
    rm_unique_id                            = models.CharField("Manager Id",max_length=50, null=True)
    rm_first_name                           = models.CharField("First Name",max_length=40, null=True)
    rm_last_name                            = models.CharField("Last Name",max_length=40, null=True)
    rm_email                                = models.CharField("Email Id",max_length=40, null=True)
    rm_contactno                            = models.CharField("Contact  No",max_length=40, null=True)
    rm_status                               = models.IntegerField("Company Status", default=1,choices=ACTIVE_DEACTIVE_CHOICES)
    rm_creation_date                        = models.DateTimeField()
    rm_update_date                          = models.DateTimeField(default=datetime.datetime.now())

    def __unicode__(self):
        return str(self.relationship_manager_id)

class Customer(User):
    #user_ptr_id                         = models.AutoField(primary_key=True) # No need of this 
    cust_unique_id                      = models.CharField(max_length=20, null=True)
    cust_company_id                     = models.ForeignKey(Company,related_name = 'customerCompany', null=True,verbose_name="Company Name",blank=True)
    cust_first_name                     = models.CharField("First Name ",max_length=50, default='')
    cust_last_name                      = models.CharField("Last Name ",max_length=50,  default='')
    cust_email                          = models.CharField("Email Id ",max_length=50, default='')
    cust_contact_no                     = models.CharField("Contact Number",max_length=50, default='')
    cust_address_line                   = models.CharField("Address Line ",max_length=250, default='')
    cust_city                           = models.CharField("City ",max_length=50, default='')
    cust_state                          = models.CharField("State ",max_length=50, default='')
    cust_country                        = models.CharField("Country ",max_length=50, default='')
    cust_gender                         = models.CharField("Gender",max_length=20, default='M', choices= GENDER_CHOICES)
    cust_age                            = models.PositiveIntegerField("Age", default=0)
    cust_pincode                        = models.PositiveIntegerField("Pincode", default=0)
    cust_image                          = models.ImageField("Upload Image", upload_to= CAM_IMAGES_PATH, max_length=255, null=True,blank=True)
    email_alert_on                      = models.IntegerField("Email Alert", default=0, choices= YES_NO_CHOICES)
    sms_alert_on                        = models.IntegerField("SMS Alert", default=0, choices= YES_NO_CHOICES)
    cust_status                         = models.IntegerField("Status", default=1, choices=ACTIVE_DEACTIVE_CHOICES)
    cust_creation_date                  = models.DateTimeField()
    user_type                           = models.IntegerField(choices=USER_TYPE,null=True)
    updated_by                          = models.CharField(max_length=30)       # added by MB
    cust_updated_date                   = models.DateTimeField(default=datetime.datetime.now())
    sign_up_source                      = models.CharField(max_length=15, default='')
    sign_up_device                      = models.CharField(max_length=20, default='')
    relationship_manager_id             = models.ForeignKey(RelationShipManager,related_name = 'relationManager', null=True,verbose_name="RelationShipManager", blank=True)

    def __unicode__(self):
        return str(self.cust_first_name) + ' ' + str(self.cust_last_name)
    
    def get_customer_info(self):
        return { 'cam_id': self.id , 'cam_user': self.cust_first_name +' , '+ str(self.cust_company_id) }
    
    def get_vendor_info(self):
        return { 'vendor_id' : self.cust_unique_id, 'vendor_name' : self.__unicode__(), 'vendor_email': self.cust_email,
        'vendor_contact_no' : self.cust_contact_no, 'vendor_city': self.cust_city }


class Property(models.Model):
    property_id                             = models.AutoField(primary_key=True)
    property_unique_id                      = models.CharField("Property Unique_id",max_length=30, null=True)
    property_actual_name                    = models.CharField("Property Actual Name",max_length=50, null=True)
    property_display_name                   = models.CharField("Property Display Name",max_length=50, null=True)
    property_description                    = models.TextField('Property Description',default = '')
    number_of_rooms                         = models.PositiveIntegerField("Number Of Rooms ", default = 0)
    property_address                        = models.CharField("Address Line",max_length=200, default = '')
    property_location                       = models.CharField("Location",max_length=100, default = '')
    property_city                           = models.CharField("City",max_length=50, default = '')
    property_state                          = models.CharField("State",max_length=50,  default = '')
    property_country                        = models.CharField("Country",max_length=50,  default = '')
    property_pincode                        = models.CharField("Pincode",max_length=10,  default = '')
    property_status                         = models.IntegerField("Status", default=0, choices= BOOKING_STATUS_CHOICES,null=True)
    property_availability_status            = models.BooleanField('Property Availability',choices= PROPERTY_AVAILABILITY)
    property_owner_id                       = models.ForeignKey(Customer,null=True,verbose_name="Owner Name", blank=True)
    distance_from_railway_station           = models.FloatField('Distance From Railway Station', default = 0.0)
    distance_from_airport                   = models.FloatField('Distance From Airport', default = 0.0)
    nearest_railway_station                 = models.CharField("Nearest Railway Station",max_length=30, null=True)
    nearest_bus_stop                        = models.CharField("Nearest Bus Stop",max_length=30, null=True)
    rack_rate                               = models.FloatField('Rack Rate', default =0.0, blank=True)
    property_images                         = models.TextField(default = '')
    property_documents                      = models.TextField(default = '')
    property_facility                       = models.TextField(default = '')
    property_type                           = models.IntegerField('Property Type',max_length=20, default=0,choices= PROPERTY_TYPE,null=True)
    contact_person                          = models.CharField("Contact Person",max_length=30, null=True)
    contact_person_email_id                 = models.CharField("Contact Person Email",max_length=50, null=True)
    contact_person_phone_no                 = models.CharField("Contact Person Phone",max_length=15, null=True)
    existing_occupacy                       = models.CharField("Existing Occupancy",max_length=30, null=True)
    remark                                  = models.TextField("Remark",null=True)
    star_category                           = models.IntegerField("Star Category", default=0)
    latitude                                = models.FloatField('Latitude', default =0.0,max_length=20)
    longitude                               = models.FloatField('Longitude', default =0.0,max_length=20)
    no_of_person_allowed_per_room           = models.IntegerField('No Of Person Per Room', default=2)
    property_creation_date                  = models.DateTimeField()
    property_update_date                    = models.DateTimeField(default=datetime.datetime.now())
    created_by                              = models.CharField(max_length=40,default = '')
    updated_by                              = models.CharField(max_length=40,default = '')

    def __unicode__(self):
        return str(self.property_unique_id)
    


class PropertyRoom(models.Model):
    room_id                     = models.AutoField(primary_key=True)
    property_id                 = models.ForeignKey(Property,related_name = 'property_rooms', null=True,verbose_name="Property Name")
    room_number                 = models.IntegerField("Room Number ", null=True)
    no_of_occupant_allowed      = models.IntegerField("Status", default=0, choices= BOOKING_STATUS_CHOICES)
    room_type                   = models.CharField("Room Type",max_length=12, default=0, choices= ROOM_TYPE_CHOICES)
    room_status                 = models.IntegerField("Status", default=0, choices= BOOKING_STATUS_CHOICES)
    room_creation_date          = models.DateTimeField()
    room_active_status          = models.IntegerField('Room Active Status', default=1, choices=ACTIVE_DEACTIVE_CHOICES)
    room_update_date            = models.DateTimeField(default=datetime.datetime.now())

    def __unicode__(self):
        return  str(self.room_id)


class PropertyRate(models.Model):
    rate_id                                          = models.AutoField(primary_key=True)
    property_id                                      = models.ForeignKey(Property,related_name = 'property_rates', null=True,verbose_name="Property Name")
    property_agreed_rate                             = models.FloatField('Property Agreed Rate', default = 0.0)
    property_display_rate                            = models.FloatField('Property Display Rate', default = 0.0)
    property_discount_rate                           = models.FloatField('Property Discount Rate', default = 0.0)
    single_occupancy_agreed_rate                     = models.FloatField('Single Occupancy Agreed Rate', default = 0.0)
    single_occupancy_display_rate                    = models.FloatField('Single Occupancy Display Rate', default = 0.0)
    double_occupancy_agreed_rate                     = models.FloatField('Double Occupancy Agreed Rate', default = 0.0)
    double_occupancy_display_rate                    = models.FloatField('Double Occupancy Display Rate', default = 0.0)
    additional_occupancy_agreed_rate                 = models.FloatField('Additional Occupancy Agreed Rate', default = 0.0)
    additional_occupancy_display_rate                = models.FloatField('Additional Occupancy Display Rate', default = 0.0)

    def __unicode__(self):
        return  str(self.rate_id)


class PropertyImage(models.Model):
    image_id                   = models.AutoField(primary_key=True)
    image_name                 = models.ImageField("Upload Image", upload_to= ROOM_IMAGES_PATH, max_length=255, null=True,blank=True)
    property_id                = models.ForeignKey(Property,related_name = 'PropertyImages', null=True,verbose_name="Property Name")

    def __unicode__(self):
        # This should return Image Path prefixed with server url
        return  str(self.image_name)  


class PropertyDocument(models.Model):
    document_id                   = models.AutoField(primary_key=True)
    document_name                 = models.CharField("Document Name",max_length=30, null=True)
    document_description          = models.CharField("Document Description",max_length=30, null=True)
    document_file                 = models.FileField("Upload File", upload_to= PROPERTY_DOCUMENT_PATH, max_length=255, null=True,blank=True)
    property_id                   = models.ForeignKey(Property,related_name = 'PropertDocuments', null=True,verbose_name="Property Name")

    def __unicode__(self):
        # This should return Document Path prefixed with server url
        return  str(self.document_name)

class Facilities(models.Model):
    facility_id                   = models.AutoField(primary_key=True)
    facility_name                 = models.CharField("Facility",max_length=30, null=True)

    def __unicode__(self):
        return  str(self.facility_name)

class Cuisines(models.Model):
    cuisines_id                   = models.AutoField(primary_key=True)
    cuisines_type                 = models.CharField("Cuisines Type",max_length=30, null=True)

    def __unicode__(self):
        return  str(self.cuisines_name)


class Country(models.Model):
    country_id                     = models.AutoField(primary_key=True)
    country_name                   = models.CharField("Country",max_length=30, null=True)

    def __unicode__(self):
        return  str(self.country_name)

class State(models.Model):
    state_id                     = models.AutoField(primary_key=True)
    state_name                   = models.CharField("State",max_length=30, null=True)
    country_id                   = models.ForeignKey(Country,related_name = 'country', null=True,verbose_name="Country Name")

    def __unicode__(self):
        return  str(self.state_name)

    def get_state_info(self):
        return {'state_id' : self.state_id, 'state_name':self.state_name }

class City(models.Model):
    city_id                      = models.AutoField(primary_key=True)
    city_name                    = models.CharField("Location",max_length=30, null=True)
    state_id                     = models.ForeignKey(State,related_name = 'state', null=True,verbose_name="State Name")
    def __unicode__(self):
        return  str(self.city_name)
    
    def get_city_info(self):
        return {'city_id' : self.city_id, 'city_name':self.city_name }

class Location(models.Model):
    location_id                   = models.AutoField(primary_key=True)
    location_name                 = models.CharField("Location",max_length=150, null=True)
    city_id                       = models.ForeignKey(City,related_name = 'city', null=True,verbose_name="City Name")
    
    def __unicode__(self):
        #return  str(self.location_id)        
        return  self.location_name + ', '+ self.city_id.city_name + ', '+ self.city_id.state_id.state_name #+', '+ self.city_id.state_id.country_id.country_name         # MB
    
    def get_location_info(self):
        return {'location_id' : self.location_id, 'location_name': self.location_name }


class Guest(models.Model):
    guest_id                = models.AutoField(primary_key=True)
    guest_unique_id         = models.CharField('Guest Unique Id', max_length=30, null=True)
    guest_first_name        = models.CharField("First Name ",max_length=50, null=True)
    guest_last_name         = models.CharField("Last Name ",max_length=50, null=True)
    guest_email             = models.CharField("Guest Email Id ",max_length=50, null=True)
    guest_contactno         = models.CharField("Contact Number ",max_length=15, null=True)
    customer_id             = models.ForeignKey(Customer,related_name = 'customer_guest_id', null=True,verbose_name="Customer Name")
    guest_status            = models.IntegerField("Status", null=True, choices=ACTIVE_DEACTIVE_CHOICES)
    guest_creation_date     = models.DateTimeField()
    guest_update_date       = models.DateTimeField(default=datetime.datetime.now())

    def __unicode__(self):
        return self.guest_first_name
    
    def get_guest_info(self):
        if self.guest_status==1:
            status = '<span class="label label-success ">Active</span>'
        else:
            status = '<span class="label label-danger">In-Active</span>' 
        return {
        'guest_id' : self.guest_id, 'activate_status': self.guest_status,
        'guest_name': self.guest_first_name , 'guest_email':  self.guest_email,
        'guest_contact':self.guest_contactno, 'status': status, 
        'edit': "<div class='btn btn-primary2 btn-xs' onclick='getRowValues(this,"+ str(self.guest_id) +" )' ><i class='fa fa-pencil'></i></div>"
        }

class PropertyOwnerBankDetails(models.Model):
    property_owner_bank_detail_id              = models.AutoField(primary_key=True)
    prefered_payment_method                    = models.CharField("Payment Method",max_length=40, null=True)
    owner_id                                   = models.ForeignKey(Customer, related_name='bank_details', null=True )
    bank_name                                  = models.CharField("Bank Name",max_length=50, null=True)
    bank_branch                                = models.CharField("Bank Branch",max_length=50, null=True)
    account_type                               = models.CharField("Account Type",max_length=50, null=True)
    account_number                             = models.CharField("Account Number",max_length=100, null=True)
    account_name                               = models.CharField("Account Name",max_length=50, null=True)
    account_address                            = models.CharField("Account Address",max_length=100, null=True)
    email_id                                   = models.CharField("Email ID",max_length=100, null=True)
    others                                     = models.CharField("Others",max_length=100, null=True)

    def __unicode__(self):
        return self.property_owner_bank_detail_id


class PaymentTransaction(models.Model):
    payment_transaction_id              =     models.AutoField(primary_key=True)
    mmp_txn                             =     models.CharField("mmp_txn",max_length=40, null=True,blank=True)
    ipg_txn_id                          =     models.CharField("ipg_txn_id",max_length=40, null=True,blank=True)
    transaction_type                    =     models.CharField("transaction_type",max_length=40, null=True,blank=True)
    property_booking_id                 =     models.CharField("property_booking_id",max_length=250, null=True,blank=True)
    discriminator                       =     models.CharField("discriminator",max_length=40, null=True,blank=True)
    srcharge                            =     models.FloatField("srcharge",null=True,blank=True)
    customer_name                       =     models.CharField("udf1",max_length=40, null=True,blank=True)
    mer_txn                             =     models.CharField("mer_txn",max_length=40, null=True,blank=True)
    card_number                         =     models.CharField("CardNmber",max_length=40, null=True,blank=True)
    ath_code                            =     models.CharField("ath_code",max_length=40, null=True,blank=True)
    bank_name                           =     models.CharField("bank_name",max_length=40, null=True,blank=True)
    date                                =     models.CharField("Payment Date",max_length=40,null=True,blank=True)
    merchant_id                         =     models.CharField("merchant_id",max_length=40, null=True,blank=True)
    amount                              =     models.FloatField("PaymentAmount",null=True,blank=True)
    prod                                =     models.CharField("ipg_txn_id",max_length=40, null=True,blank=True)
    error_description                   =     models.CharField("description",max_length=40, null=True,blank=True)
    bank_txn                            =     models.CharField("bank_txn",max_length=40, null=True,blank=True)
    f_code                              =     models.CharField("f_code",max_length=40, null=True,blank=True)
    clientcode                          =     models.CharField("clientcode",max_length=40, null=True,blank=True)
    mobile_no                           =     models.CharField("udf3",max_length=40, null=True,blank=True)
    email_id                            =     models.CharField("udf2",max_length=40, null=True,blank=True)
    udf5                                =     models.CharField("Account No",max_length=40, null=True,blank=True)
    billing_address                     =     models.CharField("udf4",max_length=40, null=True,blank=True)
    udf6                                =     models.CharField("Invoices",max_length=250, null=True,blank=True)
    udf9                                =     models.CharField("Account No",max_length=40, null=True,blank=True)
    booking_transaction_create_by       =     models.CharField("Create By",max_length=20, null=True,blank=True)
    booking_transaction_update_by       =     models.CharField("Update By",max_length=20, null=True,blank=True)
    booking_transaction_update_date     =     models.DateTimeField("Update Date",default=datetime.datetime.now())
    
    def __unicode__(self):
            return str(self.payment_transaction_id)


class Booking(models.Model):
    booking_id                              = models.AutoField(primary_key=True)
    booking_unique_id                       = models.CharField('Booking Unique ID', max_length=25,null=True )
    number_of_rooms                         = models.PositiveIntegerField('Number Of Rooms', null=True, blank=True)
    number_of_person                        = models.PositiveIntegerField('Number Of Person', null=True, blank=True)
    number_of_adults                        = models.PositiveIntegerField('Number Of Adults', null=True, blank=True)
    number_of_kids                          = models.PositiveIntegerField('Number Of kids', null=True, blank=True)
    promotion_code                          = models.CharField('Promotion Code',max_length=20,  null=True , blank=True )

    booking_datetime                        = models.DateTimeField(default=datetime.datetime.now())
    booking_rate                            = models.FloatField('Booking Room Rate', default = 0.0)

    booking_estimated_checkin_date          = models.DateField("Estimated Check In Date ",null=True,blank=True )
    booking_estimated_checkin_time          = models.TimeField("Estimated Check In Time ",null=True,blank=True )

    booking_estimated_checkout_date         = models.DateField("Estimated Check Out Date ",null=True,blank=True)
    booking_estimated_checkout_time         = models.TimeField("Estimated Check Out Time ",null=True,blank=True)

    booking_actual_checkin_date             = models.DateField("Actual Check In Date ",null=True, blank=True)
    booking_actual_checkin_time             = models.TimeField("Actual Check In Time ",null=True, blank=True)

    booking_actual_checkout_date            = models.DateField("Actual Check Out Date ",null=True, blank=True)
    booking_actual_checkout_time            = models.TimeField("Actual Check Out Time ",null=True, blank=True)

    booking_estimated_no_of_day_stay        = models.PositiveIntegerField("Estimated Days",null =True)
    booking_actual_no_of_day_stay           = models.PositiveIntegerField("Actual Days Stayed",null =True, blank=True)

    booking_check_in_status                 = models.BooleanField("Check-In Status", default=False)
    booking_check_out_status                = models.BooleanField("Check-Out Status", default=False)

    booking_estimated_no_of_night_stay      = models.PositiveIntegerField("Estimated Nights",null =True,blank=True)
    booking_actual_no_of_night_stay         = models.PositiveIntegerField("Actual Nights",null =True, blank=True)

    customer_id                             = models.ForeignKey(Customer,related_name = 'customerbooking', null=True,verbose_name="CAM Name")
    guest_id                                = models.ForeignKey(Guest, related_name = 'guestbooking', null=True, verbose_name="Guests")
    property_id                             = models.ForeignKey(Property,related_name = 'propertybooking', null=True,verbose_name="PROPERTY Name")
    property_room_id                        = models.ForeignKey(PropertyRoom,related_name = 'roombooking', null=True,verbose_name="Room Number")
    #guest_rating                        = models.ForeignKey(GuestRating,related_name = 'guest_ratings', null=True,verbose_name="Guest Rating")

    is_from_quote                           = models.BooleanField("Is From Quote",default=False)
    quotation_id                            = models.CharField('quote_booking',max_length=20,null=False,blank=True)

    booking_cancellation_on_datetime        = models.DateTimeField("Booking Cancellation Date",null=True, blank=True)
    booking_favourite                       = models.IntegerField("Favourite?", default=0, choices= YES_NO_CHOICES)
    booking_status                          = models.IntegerField("Status", default=0, choices= BOOKING_STATUS_CHOICES)
    booking_creation_date                   = models.DateTimeField(default=datetime.datetime.now())
    booking_remark                          = models.CharField('Booking Remark', max_length=150, null=True)
    payment_status                          = models.CharField('Payment Status', max_length=1 ,default='0', choices=PAYMENT_STATUS_CHOICES)
    payment_method                          = models.CharField('Payment Method', max_length=150, null=True, choices=PAYMENT_METHOD)
    payment_transaction_id                  = models.ForeignKey(PaymentTransaction,related_name = 'BookingPayment',verbose_name="PaymentTransaction",null=True,blank=True)
    booking_amount                          = models.FloatField(default=0.0)

    def __unicode__(self):
        return str(self.booking_unique_id)

# This added on 16-Dec-2015, This is for tracking multiple guest in single booking
class BookingGuest(models.Model):
    guest_booking_id    = models.AutoField(primary_key=True)
    guest_id            = models.ForeignKey(Guest, related_name='booked_guest', blank=True)
    booking_id          = models.ForeignKey(Booking, related_name='all_guest',blank=True)
    created_date        = models.DateTimeField(default=datetime.datetime.now())

    def __unicode__(self):
        return self.booking_id.booking_unique_id+' '+self.guest_id.guest_first_name 

class Promotion_code(models.Model):
    promotion_code_id                = models.AutoField(primary_key=True) 
    promotion_code                   = models.CharField(max_length=40, null=True)
    promo_code_amount                = models.FloatField('Promo Code Amount', default = 0.0)
    promo_start_date                 = models.DateTimeField()
    promo_end_date                   = models.DateTimeField()
    created_date                     = models.DateTimeField(default=datetime.datetime.now())
    promocode_usage_limit            = models.FloatField('Promo Code Usage Limit', default = 0.0)

    def __unicode__(self):
        return str(self.promotion_code_id)


class BookedRoom(models.Model):
    booked_room_id                  = models.AutoField(primary_key=True) 
    booking_id                      = models.ForeignKey(Booking,related_name = 'booked_room_id', null=True)
    room_id                         = models.ForeignKey(PropertyRoom,related_name = 'property_room_id', null=True)

    def __unicode__(self):
        return str(self.booked_room_id)

class CAMPropertyRate(models.Model):
    cam_property_rate_id             = models.AutoField(primary_key=True)
    property_id                      = models.ForeignKey(Property,related_name = 'cam_property_id', null=True)
    cust_id                          = models.ForeignKey(Customer,related_name = 'customer_rate_id', null=True)
    agreed_rate                      = models.FloatField("Agreed Rate",default = 0.0)
    created_date                     = models.DateTimeField()
    created_by                       = models.CharField(max_length=40, null=True)
    occupancy_type                   = models.IntegerField("Occupancy Type", default=1, choices=OCCUPANCY_TYPE)

    def __unicode__(self):
        return str(self.cam_property_rate_id)


class Invoice(models.Model):
    invoice_id            = models.AutoField(primary_key=True)
    invoice_unique_id     = models.CharField('Invoice Unique ID',max_length=30, null=True)
    booking_id            = models.ForeignKey(Booking, related_name = 'invoicebooking', null=True, verbose_name="Booking ID")
    invoice_datetime      = models.DateField(default=datetime.datetime.now())
    room_charges          = models.FloatField("Room Charges",default = 0.0)
    extra_charges         = models.FloatField("Extra Charges",default = 0.0)
    extra_charge_details  = models.CharField("Extra Charge Details", max_length=100, default = '')
    invoice_total_amount  = models.FloatField("Invoice Total Amount",default = 0.0)
    discount              = models.FloatField("Discount Amount",default = 0.0)
    tax_amount            = models.FloatField('Tax Amount',default=0.0)
    invoice_gross_amount  = models.FloatField("Invoice Gross Amount",default = 0.0)
    invoice_status        = models.CharField("Status",max_length=1, default='0',choices= PAYMENT_STATUS_CHOICES)
    invoice_paid_date     = models.DateTimeField("Paid Date", null=True, blank = True)
    invoice_generated_datetime  = models.DateTimeField("Invoice Generated DateTime", default=datetime.datetime.now())

    def __unicode__(self):
        return str(self.invoice_id)


class CorporateTransaction(models.Model):
    transaction_id              = models.AutoField(primary_key=True)
    invoice_id                  = models.CharField("Invoice",max_length=50,null=True,blank=True)
    corporate_id                = models.ForeignKey(Customer, related_name = 'corporate_id', null=True, verbose_name="Corporate Details")
    transaction_date            = models.DateField(default=datetime.datetime.now())
    transaction_amount          = models.FloatField("Transaction Amount",default = 0.0,null=True)
    transaction_type            = models.IntegerField("Transaction Type", choices= TRANSACTION_TYPE,null=True)
    transaction_method          = models.CharField("Method", max_length=10,null=True, choices= TRANSACTION_METHOD)
    transaction_desc            = models.CharField("Description", max_length=100,null=True)
    cheque_number               = models.CharField("Cheque Number", max_length=15,blank=True,null=True)
    cheque_bank_branch          = models.CharField("Bank Name & Branch", max_length=50,blank=True,null=True)

    def __unicode__(self):
        return str(self.transaction_id)

    def get_payment_info(self):
        t_type = 'DEPOSIT'
        if self.transaction_type == 1:
            t_type = 'INVOICE'

        return { 'tid' : str(self.transaction_id), 'customer_name': self.corporate_id.cust_first_name ,
        'transaction_date':self.transaction_date.strftime('%d/%m/%Y') ,
        'transaction_amount': self.transaction_amount , 'transaction_type': t_type }

class MailingList(models.Model):
    mailing_list_id = models.AutoField(primary_key=True)
    mail_id         = models.CharField("Mail ID",max_length=50,null=True,blank=True)
    updated_date    = models.DateTimeField("Requested Date Time", default=datetime.datetime.now())

    def __unicode__(self):
        return self.mail_id


# Corporate Prefered Property
class CustomerFavoriteProperty(models.Model):
    favourite_id         = models.AutoField(primary_key=True)
    customer_id          = models.ForeignKey(Customer,null=True,verbose_name="Customer Name", blank=True)
    property_id          = models.ForeignKey(Property,related_name = 'customer_property', null=True,verbose_name="Property Name")

    def __unicode__(self):
        return str(self.favourite_id)


class UserTrackingActivity(models.Model):
    user_tracking_id    = models.AutoField(primary_key=True)
    user_id             = models.IntegerField('User ID',null=False)
    path                = models.TextField('Path Flow',default='')
    session_in_time     = models.DateTimeField('Session In Time')
    session_out_time    = models.DateTimeField('Session Out Time',default=datetime.datetime.now())
    session_id          = models.CharField('Session ID',max_length=100)
    aggregate_time      = models.FloatField('Time Spend In hours',default=0.0)

    def __unicode__(self):
        return str(self.user_tracking_id) + ' ' +  str(self.user_id) + ' '+ self.session_in_time.strftime('%d-%m-%Y') 

# This is added on 11 Dec 2015
class UserBookingStatisticTrack(models.Model):
    user_booking_statistic_track_id = models.AutoField(primary_key=True)
    user_id             = models.ForeignKey(Customer,null=True,verbose_name="Customer Name", blank=True)
    booking_path        = models.CharField('Booking Path',max_length=100)
    count               = models.PositiveIntegerField(default=1)
    current_timestamp   = models.DateTimeField('Current Time Stamp',default=datetime.datetime.now())
    booking_date        = models.DateField()
    booking_id          = models.ForeignKey(Booking,verbose_name="Customer Booking", null =True)
    
    def __unicode__(self):
        return 'Booking By ' + str(self.user_id.username) + ' on ' + self.booking_date.strftime('%d/%m/%Y')


