from django.db import models
from django.contrib.auth.models import User
import datetime
# Create your models here.
import pdb

ROOM_IMAGES_PATH            =   "media/rooms"
CAM_IMAGES_PATH             =   "media/cam"
PROPERTY_DOCUMENT_PATH      =   "media/documents"

SERVER_MEDIA_URL = 'http://192.168.0.121:8000'
#SERVER_MEDIA_URL = 'http://ec2-52-4-20-173.compute-1.amazonaws.com'

YES_NO_CHOICES = (
        (0, 'NO'),
        (1, 'YES'),
    )

ACTIVE_DEACTIVE_CHOICES = (
        (1, 'ACTIVE'),
        (0, 'IN-ACTIVE'),
    )

ROOM_TYPE_CHOICES = (
        ('Single Bed','Single Bed'),
        ('Double Bed','Double Bed')
    )

GENDER_CHOICES = (
    ('M','MALE'),
    ('F','FEMALE'),
)

BOOKING_STATUS_CHOICES =(
    (0,'AVAILABLE'),
    (1,'BOOKED'),
    (2,'COMPLETED'),
    (3,'CANCELLED'),
    (4,'OPEN'),
)

INVOICE_CHOICES = (
    ('P','PAID'),
    ('U','UNPAID'),
)



APARTMENT_AVAILABILITY = (
    (True, 'AVAILABLE'),
    (False,'NOT AVAILABLE')
)

PROPERTY_TYPE = (
    (0, 'Service Apartment'),
    (1,'HOTEL')
)

USER_TYPE = (
    (0, 'ADMIN'),
    (1, 'CORPORATE'),
    (2,'OWNER'),
    (3,'RETAIL'),
)

OCCUPANCY_TYPE = (
    (0, 'Single'),
    (1,'Double'),
    (2,'Additional'),
)





BOOKING_ALL         = 0
BOOKING_BOOKED      = 1
BOOKING_COMPLETED   = 2
BOOKING_CANCELLED   = 3
BOOKING_OPEN        = 4


class Customer(User):
    #user_ptr_id                         = models.AutoField(primary_key=True) # No need of this 
    cust_unique_id                      = models.CharField(max_length=20, null=True)
    cust_company_id                     = models.ForeignKey(Company,related_name = 'company', null=True,verbose_name="Company Name")
    cust_first_name                     = models.CharField("First Name ",max_length=50, null=True)
    cust_last_name                      = models.CharField("Last Name ",max_length=50, null=True)
    cust_email                          = models.CharField("Email Id ",max_length=50, null=True)
    cust_contact_no                     = models.CharField("Contact Number ",max_length=50, null=True)
    cust_address_line                   = models.CharField("Address Line ",max_length=150, null=True)
    cust_city                           = models.CharField("City ",max_length=50, null=True)
    cust_gender                         = models.CharField("Gender",max_length=20, null=True, choices= GENDER_CHOICES)
    cust_age                            = models.PositiveIntegerField("Age",null =True)
    cust_pincode                        = models.PositiveIntegerField("Pincode",null =True)
    cust_image                          = models.ImageField("Upload Image", upload_to= CAM_IMAGES_PATH, max_length=255, null=True,blank=True)
    email_alert_on                      = models.IntegerField("Email Alert", default=0, choices= YES_NO_CHOICES)
    sms_alert_on                        = models.IntegerField("SMS Alert", default=0, choices= YES_NO_CHOICES)
    cust_status                         = models.IntegerField("Status", default=1, choices=ACTIVE_DEACTIVE_CHOICES)
    cust_creation_date                  = models.DateTimeField()
    user_type                           = models.IntegerField(choices=USER_TYPE,null=True)
    updated_by                          = models.CharField(max_length=30)       # added by MB
    cust_updated_date                   = models.DateTimeField(default=datetime.datetime.now())
    sign_up_source                      = models.CharField(max_length=15, null=True)
    sign_up_device                      = models.CharField(max_length=20,null=True)
    relationship_manager_id             = models.ForeignKey(RelationShipManager,related_name = 'relationManager', null=True,verbose_name="RelationShipManager")

    def __unicode__(self):
        return self.user_ptr_id

class Property(models.Model):
    property_id                             = models.AutoField(primary_key=True)
    property_unique_id                      = models.CharField("Property Unique_id",max_length=30, null=True)
    property_actual_name                    = models.CharField("Property Actual Name",max_length=30, null=True)
    property_display_name                   = models.CharField("Property Display Name",max_length=30, null=True)
    property_description                    = models.CharField('Property Description',max_length=4000,null=True)
    number_of_rooms                         = models.PositiveIntegerField("Number Of Rooms ", null=True)
    property_address                        = models.CharField("Address Line",max_length=200, null=True)
    location                                = models.CharField("Location",max_length=200, null=True)
    property_pincode                        = models.CharField("Pincode",max_length=10, null=True)
    property_status                         = models.IntegerField("Status", default=0, choices= BOOKING_STATUS_CHOICES,null=True)
    property_creation_date                  = models.DateTimeField()
    property_update_date                    = models.DateTimeField(default=datetime.datetime.now())
    property_availability_status            = models.CharField('Property Availability',max_length=20,choices= APARTMENT_AVAILABILITY)
    property_owner_id                       = models.ForeignKey(Customer,related_name = 'customer_id', null=True,verbose_name="Owner Name")
    distance_from_railway_station           = models.FloatField('Distance From Railway Station', default = 0.0)
    distance_from_airport                   = models.FloatField('Distance From Airport', default = 0.0)
    nearest_railway_station                 = models.CharField("Nearest Railway Station",max_length=30, null=True)
    nearest_bus_stop                        = models.CharField("Nearest Bus Stop",max_length=30, null=True)
    property_images                         = models.ForeignKey(PropertyImage,related_name = 'image_id', null=True)
    property_documents                      = models.ForeignKey(PropertyDocument,related_name = 'document_id', null=True)
    property_facility                       = models.ForeignKey(Facility,related_name = 'facility_id', null=True)
    property_type                           = models.IntegerField('Property Type',max_length=20, default=0,choices= PROPERTY_TYPE,null=True)
    contact_person                          = models.CharField("Contact Person",max_length=30, null=True)
    contact_person_email_id                 = models.CharField("Contact Person Email",max_length=30, null=True)
    contact_person_phone_no                 = models.CharField("Contact Person Phone",max_length=30, null=True)
    existing_occupacy                       = models.CharField("Existing Occupancy Status",max_length=30, null=True)
    remark                                  = models.CharField("Remark",max_length=30, null=True)
    star_category                           = models.IntegerField("Star Category", default=0,null=True)
    latitude                                = models.FloatField('Latitude', default = 0.0)
    longitude                               = models.FloatField('Longitude', default = 0.0)
    no_of_person_allowed_per_room           = models.IntegerField("No Of Person Per Room", default=0,null=True)

    def __unicode__(self):
        return self.property_id


class PropertyRoom(models.Model):
    room_id                     = models.AutoField(primary_key=True)
    property_id                 = models.ForeignKey(Property,related_name = 'room_property_id', null=True,verbose_name="Property Name")
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
    property_id                                      = models.ForeignKey(Property,related_name = 'rate_property_id', null=True,verbose_name="Property Name")
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
    property_id                = models.ForeignKey(Property,related_name = 'image_property_id', null=True,verbose_name="Property Name")

    def __unicode__(self):
        # This should return Image Path prefixed with server url
        return  str(self.image_id)  


class PropertyDocument(models.Model):
    document_id                   = models.AutoField(primary_key=True)
    document_name                 = models.CharField("Document Name",max_length=30, null=True)
    document_description          = models.CharField("Document Description",max_length=30, null=True)
    document_file                 = models.FileField("Upload File", upload_to= PROPERTY_DOCUMENT_PATH, max_length=255, null=True,blank=True)
    property_id                   = models.ForeignKey(Property,related_name = 'document_property_id', null=True,verbose_name="Property Name")

    def __unicode__(self):
        # This should return Document Path prefixed with server url
        return  str(self.document_id)

class Facilities(models.Model):
    facility_id                   = models.AutoField(primary_key=True)
    facility_name                 = models.CharField("Facility",max_length=30, null=True)

    def __unicode__(self):
        return  str(self.facility_id)

class Cuisines(models.Model):
    cuisines_id                   = models.AutoField(primary_key=True)
    cuisines_type                 = models.CharField("Cuisines Type",max_length=30, null=True)

    def __unicode__(self):
        return  str(self.cuisines_id)


class Country(models.Model):
    country_id                     = models.AutoField(primary_key=True)
    country_name                   = models.CharField("Country",max_length=30, null=True)

    def __unicode__(self):
        return  str(self.country_id)

class State(models.Model):
    state_id                     = models.AutoField(primary_key=True)
    state_name                   = models.CharField("State",max_length=30, null=True)
    country_id                   = models.ForeignKey(Country,related_name = 'country_id', null=True,verbose_name="Country Name")

    def __unicode__(self):
        return  str(self.state_id)

class City(models.Model):
    city_id                      = models.AutoField(primary_key=True)
    city_name                    = models.CharField("Loaction",max_length=30, null=True)
    state_id                     = models.ForeignKey(State,related_name = 'state_id', null=True,verbose_name="State Name")
    def __unicode__(self):
        return  str(self.city_id)

class Location(models.Model):
    location_id                   = models.AutoField(primary_key=True)
    location_name                 = models.CharField("Location",max_length=30, null=True)
    city_id                       = models.ForeignKey(City,related_name = 'city_id', null=True,verbose_name="City Name")
    
    def __unicode__(self):
        #return  str(self.location_id)        
        return  self.location_name + ','+ self.city_id.city_name + ','+ self.city_id.state_id.state_name        # MB

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
        return self.guest_id 


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


class PropertyOwnerBankDetails(models.Model):
    property_owner_bank_detail_id              = models.AutoField(primary_key=True)
    prefered_payment_method                    = models.CharField("Payment Method",max_length=40, null=True)
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


class RelationShipManager(models.Model):
    relationship_manager_id                 = models.AutoField(primary_key=True)
    rm_unique_id                            = models.CharField("Payment Method",max_length=50, null=True)
    rm_first_name                           = models.CharField("Payment Method",max_length=40, null=True)
    rm_last_name                            = models.CharField("Payment Method",max_length=40, null=True)
    rm_email                                = models.CharField("Payment Method",max_length=40, null=True)
    rm_contactno                            = models.CharField("Payment Method",max_length=40, null=True)
    rm_status                               = models.CharField("Payment Method",max_length=40, null=True)
    rm_creation_date                        = models.DateTimeField()
    rm_update_date                          = models.DateTimeField(default=datetime.datetime.now())

    def __unicode__(self):
        return self.relationship_manager_id




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

    booking_estimated_checkin_date      = models.DateField("Estimated Check In Date ",null=True,blank=True )
    booking_estimated_checkin_time      = models.TimeField("Estimated Check In Time ",null=True,blank=True )

    booking_estimated_checkout_date     = models.DateField("Estimated Check Out Date ",null=True,blank=True)
    booking_estimated_checkout_time     = models.TimeField("Estimated Check Out Time ",null=True,blank=True)

    booking_actual_checkin_date         = models.DateField("Actual Check In Date ",null=True, blank=True)
    booking_actual_checkin_time         = models.TimeField("Actual Check In Time ",null=True, blank=True)

    booking_actual_checkout_date        = models.DateField("Actual Check Out Date ",null=True, blank=True)
    booking_actual_checkout_time        = models.TimeField("Actual Check Out Time ",null=True, blank=True)


    booking_estimated_no_of_day_stay    = models.PositiveIntegerField("Estimated Days",null =True)
    booking_actual_no_of_day_stay       = models.PositiveIntegerField("Actual Days Stayed",null =True, blank=True)

    booking_check_in_status             = models.BooleanField("Check-In Status", default=False)
    booking_check_out_status            = models.BooleanField("Check-Out Status", default=False)

    booking_estimated_no_of_night_stay  = models.PositiveIntegerField("Estimated Nights",null =True)
    booking_actual_no_of_night_stay     = models.PositiveIntegerField("Actual Nights",null =True, blank=True)

    customer_id                         = models.ForeignKey(Customer, related_name = 'booking_customer_id', null=True,verbose_name="CAM Name")
    guest_id                            = models.ForeignKey(Guest, related_name = 'guest_id', null=True, verbose_name="Guests")
    property_id                         = models.ForeignKey(Property,related_name = 'property_id', null=True,verbose_name="Apartment Name")
    property_room_id                    = models.ForeignKey(PropertyRoom,related_name = 'property_room_id', null=True,verbose_name="Room Number")
    guest_rating                        = models.ForeignKey(GuestRating,related_name = 'guest_ratings', null=True,verbose_name="Guest Rating")

    booking_cancellation_on_datetime    = models.DateTimeField("Booking Cancellation Date",null=True, blank=True)
    booking_favourite                   = models.IntegerField("Favourite?", default=0, choices= YES_NO_CHOICES)
    booking_status                      = models.IntegerField("Status", default=0, choices= BOOKING_STATUS_CHOICES)
    booking_creation_date               = models.DateTimeField(default=datetime.datetime.now())
    booking_remark                      = models.CharField('Booking Remark', max_length=150, null=True)
    payment_status                      = models.IntegerField("Status", default=1, choices=ACTIVE_DEACTIVE_CHOICES)
    payment_method                      = models.CharField('Booking Remark', max_length=150, null=True)
    payment_transaction_id              = models.ForeignKey(PaymentTransaction,related_name = 'payment_transaction_id', null=True,verbose_name="PaymentTransaction")

    def __unicode__(self):
        return str(self.booking_id)


class Promotion_code(models.Model):
    promotion_code_id                = models.AutoField(primary_key=True) 
    promotion_code                   = models.CharField(max_length=40, null=True)
    promo_code_amount                = models.FloatField('Promo Code Amount', default = 0.0)
    promo_start_date                 = models.DateTimeField()
    promo_end_date                   = models.DateTimeField()
    created_date                     = models.DateTimeField()
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
    booking_id            = models.ForeignKey(Booking, related_name = 'booking_id', null=True, verbose_name="CAM Booking Details")
    invoice_datetime      = models.DateField(default=datetime.datetime.now())
    room_charges          = models.FloatField("Room Charges",default = 0.0)
    extra_charges         = models.FloatField("Extra Charges",default = 0.0)
    invoice_total_amount  = models.FloatField("Invoice Total Amount",default = 0.0)
    discount              = models.FloatField("Discount Amount",default = 0.0)
    tax_amount            = models.FloatField('Tax Amount',default=0.0)
    invoice_gross_amount  = models.FloatField("Invoice Gross Amount",default = 0.0)
    invoice_status        = models.CharField("Status",max_length=3, default='U',choices= INVOICE_CHOICES)
    invoice_paid_date     = models.DateTimeField("Paid Date", null=True, blank = True)
    invoice_generated_datetime  = models.DateTimeField("Invoice Generated DateTime", default=datetime.datetime.now())

    def __unicode__(self):
        return self.invoice_id


class PaymentTransaction(models.Model):
    payment_transaction_id              =     models.AutoField(primary_key=True)
    mmp_txn                             =     models.CharField("mmp_txn",max_length=40, null=True,blank=True)
    ipg_txn_id                          =     models.CharField("ipg_txn_id",max_length=40, null=True,blank=True)
    transaction_type                    =     models.CharField("transaction_type",max_length=40, null=True,blank=True)
    property_booking_id                 =     models.CharField("property_booking_id",max_length=40, null=True,blank=True)
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
    udf6                                =     models.CharField("Account No",max_length=40, null=True,blank=True)
    udf9                                =     models.CharField("Account No",max_length=40, null=True,blank=True)
    booking_transaction_create_by       =     models.CharField("Create By",max_length=20, null=True,blank=True)
    booking_transaction_update_by       =     models.CharField("Update By",max_length=20, null=True,blank=True)
    booking_transaction_update_date     =     models.DateTimeField("Update Date",default=datetime.datetime.now())
    
    def __unicode__(self):
            return self.payment_transaction_id
 