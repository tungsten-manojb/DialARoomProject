from django.db import models
from django.contrib.auth.models import User
import datetime
# Create your models here.
import pdb

ROOM_IMAGES_PATH    =   "media/rooms"
CAM_IMAGES_PATH      =   "media/cam"

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
PROPERTY_TYPE = (
    ('SA','Service Apartment'),
    ('HO','HOTEL'),
)


APARTMENT_AVAILABILITY = (
    ('AVAILABLE', 'AVAILABLE'),
    ('NOTAVAILABLE','NOT AVAILABLE')
)


BOOKING_ALL         = 0
BOOKING_BOOKED      = 1
BOOKING_COMPLETED   = 2
BOOKING_CANCELLED   = 3
BOOKING_OPEN        = 4



class Property(models.Model):
    property_id                               = models.AutoField(primary_key=True)
    property_unique_id                        = models.CharField("Apartment Unique_id",max_length=30, null=True)
    property_actual_name                      = models.CharField("Apartment Name",max_length=50, null=True)
    property_display_name                     = models.CharField("Apartment Display Name",max_length=50,null=True)
    property_description                      = models.CharField('Apartment Description',max_length=4000,null=True)
    number_of_rooms                           = models.PositiveIntegerField("Number Of Rooms ", null=True)
    property_address                          = models.CharField("Address Line",max_length=150, null=True)
    location                                  = models.CharField("Location",max_length=150, null=True)
    property_pincode                          = models.CharField("Pincode",max_length=20, null=True)
    property_status                           = models.IntegerField("Status", default=0, choices= BOOKING_STATUS_CHOICES,null=True)
    property_creation_date                    = models.DateTimeField()
    property_update_date                      = models.DateTimeField(default=datetime.datetime.now())
    property_availability_status              = models.CharField('Apartment Availability',max_length=20,choices= APARTMENT_AVAILABILITY)
    property_owner                            = models.ForeignKey(Customer,related_name = 'customer_id', null=True,verbose_name="Customer Name")
    distance_from_railway_station             = models.FloatField("Distance From Railway Station",null=True)
    distance_from_airport                     = models.FloatField("Distance From Railway Station",null=True)
    nearest_railway_station                   = models.CharField("Nearest Railway Station",max_length=100, null=True)
    nearest_bus_stop                          = models.CharField("Nearest Bus Stop",max_length=100, null=True)
    property_images                           = models.CharField("Image Path",max_length=100, null=True)
    property_documents                        = models.CharField("Document Path",max_length=100, null=True)
    property_facility                         = models.CharField("Facility Ids",max_length=100, null=True)
    property_type                             = models.CharField("Property Type",max_length=100,choices=PROPERTY_TYPE, null=True)
    contact_person                            = models.CharField("Facility Ids",max_length=100, null=True)
    contact_person_email_id                   = models.CharField("Contact Person Email Id",max_length=100, null=True)
    contact_person_phone_no                   = models.CharField("Contact Person Phone Number",max_length=100, null=True)
    existing_occupacy                         = models.CharField("Existing Occupancy",max_length=40, null=True)
    remark                                    = models.CharField("Remark",max_length=100, null=True)
    star_category                             = models.IntegerField("Star", default=0,null=True)
    latitude                                  = models.CharField("Latitude",max_length=100, null=True)
    longitude                                 = models.CharField("Longitude",max_length=100, null=True)
    no_of_person_allowed_per_room             = models.IntegerField("No Of Person Per Room", default=0,null=True)

    def __unicode__(self):
        return self.property_id
    
  
class PropertyRoom(models.Model):
    room_id                          = models.AutoField(primary_key=True)        
    room_number                      = models.IntegerField("Room Number ", null=True)
    room_type                        = models.CharField("Room Type",max_length=12, default=0, choices= ROOM_TYPE_CHOICES)
    property_room_status             = models.IntegerField("Status", default=0, choices= BOOKING_STATUS_CHOICES)
    room_active_status              = models.IntegerField('Room Active Status', default=1, choices=ACTIVE_DEACTIVE_CHOICES)
    room_creation_date              = models.DateTimeField()
    room_update_date                = models.DateTimeField(default=datetime.datetime.now())
    property_id                     = models.ForeignKey(Property,related_name = 'property_id', null=True,verbose_name="Property Name")
    
    def __unicode__(self):
        return  str(self.room_id)
        

class PropertyImage(models.Model):
    image_id                         = models.AutoField(primary_key=True)
    images_name                      = models.ImageField("Room Image 1", upload_to= ROOM_IMAGES_PATH, max_length=255, default=None, null=True,blank=True)
    property_id                      = models.ForeignKey(Property,related_name = 'property_id', null=True,verbose_name="Property Name")

      
    def __unicode__(self):
        return  str(self.room_id)




class Company(models.Model):
    cam_company_id            = models.AutoField(primary_key=True)
    company_unique_id         = models.CharField("Company Unique ID",max_length=30, null=True)
    cam_company_name          = models.CharField("Company Name",max_length=50, null=True)
    cam_company_email         = models.CharField("Company Email",max_length=50, null=True)
    cam_company_site          = models.CharField("Company Website",max_length=50, null=True)
    cam_company_contactno     = models.CharField("Company Contact No.",max_length=50, null=True)
    cam_company_address       = models.CharField("Company Address",max_length=350, null=True)
    cam_company_city          = models.CharField("City",max_length=50, null=True)
    cam_company_state         = models.CharField("State",max_length=50, null=True)
    cam_company_country       = models.CharField("Country",max_length=50, null=True)
    cam_company_pincode       = models.CharField("Pincode",max_length=50, null=True)
    cam_company_status        = models.IntegerField("Company Status", default=1,choices=ACTIVE_DEACTIVE_CHOICES)
    cam_company_creation_date = models.DateTimeField()
    cam_company_update_date   = models.DateTimeField(default=datetime.datetime.now())
    
    def __unicode__(self):
        return self.cam_company_name

    def get_company_info(self):
        return { 'company_id': self.cam_company_id ,'company_name' : self.cam_company_name }

    def get_address(self):
        return self.cam_company_address +' '+ self.cam_company_city + ' '+ self.cam_company_state + ' ' +self.cam_company_country +' ' +self.cam_company_pincode


class CAM(User):
    cam_unique_id           = models.CharField(max_length=20, null=True)
    cam_company_id          = models.ForeignKey(CAMCompany,related_name = 'company', null=True,verbose_name="Company Name")
    cam_first_name          = models.CharField("First Name ",max_length=50, null=True)
    cam_last_name           = models.CharField("Last Name ",max_length=50, null=True)
    cam_email               = models.CharField("Email Id ",max_length=50, null=True)
    cam_contactno           = models.CharField("Contact Number ",max_length=50, null=True)
    cam_address_line        = models.CharField("Address Line ",max_length=150, null=True)
    cam_city                = models.CharField("City ",max_length=50, null=True)
    cam_state               = models.CharField("State ",max_length=50, null=True)
    cam_country             = models.CharField("Country ",max_length=50, null=True)
    cam_gender              = models.CharField("Gender",max_length=20, null=True, choices= GENDER_CHOICES)
    cam_age                 = models.PositiveIntegerField("Age",null =True)
    cam_pincode             = models.PositiveIntegerField("Pincode",null =True)
    cam_image               = models.ImageField("Upload Image", upload_to= CAM_IMAGES_PATH, max_length=255, null=True,blank=True)
    cam_isemailalert_on     = models.IntegerField("Email Alert", default=0, choices= YES_NO_CHOICES)
    cam_issmsalert_on       = models.IntegerField("SMS Alert", default=0, choices= YES_NO_CHOICES)
    cam_status              = models.IntegerField("Status", default=1, choices=ACTIVE_DEACTIVE_CHOICES)
    cam_creation_date       = models.DateTimeField()
    cam_single_room_rate    = models.FloatField('Single Room Rate',default = 0.0)
    cam_double_room_rate    = models.FloatField('Double Room Rate', default = 0.0)
    cam_half_room_rate      = models.FloatField('Half Day Room Rate', default = 0.0)
    is_cam_user             = models.BooleanField('Is CAM User', default=False)
    cam_update_date         = models.DateTimeField(default=datetime.datetime.now())
    
    def get_cam_user(self):
        return { 'cam_id': self.id , 'cam_user': self.cam_first_name +' , '+ str(self.cam_company_id) }

    def __unicode__(self):
        return self.cam_first_name +','+ str(self.cam_company_id)

    def get_cam_user_info(self):
        more = '<a marked="1" href="/crm/customer-detail-display/?customer_id='+ str(self.id)+'"><i class="fa-2x pe-7s-more text-primary2"></i></a>'
        company_name = ''
        if self.is_cam_user:
            company_name = self.cam_company_id.cam_company_name
        return {
            'cust_id' : str(self.id), 'customer_name': self.cam_first_name ,
            'company_name': company_name, 'city': self.cam_city,
            'email_id':self.cam_email,'contact_number': self.cam_contactno, 
            'more':more
        }


class Guest(models.Model):
    guest_id                = models.AutoField(primary_key=True)
    guest_unique_id         = models.CharField('Guest Unique Id', max_length=30, null=True)
    guest_first_name        = models.CharField("First Name ",max_length=50, null=True)
    guest_last_name         = models.CharField("Last Name ",max_length=50, null=True)
    guest_email             = models.CharField("Guest Email Id ",max_length=50, null=True)
    guest_contactno         = models.CharField("Contact Number ",max_length=15, null=True)
    cam_id                  = models.ForeignKey(CAM,related_name = 'cam_guest', null=True,verbose_name="CAM Name")
    guest_status            = models.IntegerField("Status", null=True, choices=ACTIVE_DEACTIVE_CHOICES)
    guest_creation_date     = models.DateTimeField()
    guest_update_date       = models.DateTimeField(default=datetime.datetime.now())
    
    def __unicode__(self):
        return self.guest_first_name #+' '+ self.guest_last_name 
    
    def get_guest_info(self):
        if self.guest_status:
            status = '<span class="label label-success ">Active</span>'
        else:
            status = '<span class="label label-danger">In-Active</span>' 
        return {
        'guest_id' : self.guest_id, 'activate_status': self.guest_status,
        'guest_name': self.guest_first_name , 'guest_email':  self.guest_email,
        'guest_contact':self.guest_contactno, 'status': status, 
        'edit': "<div class='btn btn-primary2 btn-xs' onclick='getRowValues(this,"+ str(self.guest_id) +" )' ><i class='fa fa-pencil'></i></div>"
        }

class GuestRating(models.Model):
    guest_rating_id         = models.AutoField(primary_key=True)
    guest_id                = models.ForeignKey(Guest,related_name = 'guest', null=True,verbose_name="Guest Name")
    guest_rating_number     = models.PositiveIntegerField("Guest Rating(0 to 5)",null =True)
    is_favorite             = models.IntegerField("Favorite?", default=0, choices= YES_NO_CHOICES)
    guest_issues_details    = models.CharField("Guest Issues(If Any) ",max_length=1000, null=True)
    guest_feedback          = models.CharField("Guest Feedback ",max_length=1000, null=True)
    guest_rating_date       = models.DateTimeField(default=datetime.datetime.now())

    def __unicode__(self):
        return str(self.guest_rating_number)

class Booking(models.Model):
    cam_booking_id                          = models.AutoField(primary_key=True)
    cam_id                                  = models.ForeignKey(CAM, related_name = 'cam', null=True,verbose_name="CAM Name")
    guest_id                                = models.ForeignKey(Guest, related_name = 'guest_name', null=True, verbose_name="Guests")
    apartment                               = models.ForeignKey(Apartment,related_name = 'apartment', null=True,verbose_name="Apartment Name")
    aptroom_id                              = models.ForeignKey(ApartmentRoom,related_name = 'apartmentrooms', null=True,verbose_name="Room Number")
    guest_rating                            = models.ForeignKey(GuestRating,related_name = 'guest_ratings', null=True,verbose_name="Guest Rating")

    booking_unique_id                       = models.CharField('Booking Unique ID', max_length=25,null=True )

    number_of_person                        = models.PositiveIntegerField('Number Of Person', null=True, blank=True)
    number_of_adults                        = models.PositiveIntegerField('Number Of Adults', null=True, blank=True)
    number_of_kids                          = models.PositiveIntegerField('Number Of kids', null=True, blank=True)


    promotion_code                          = models.CharField('Promotion Code',max_length=20,  null=True , blank=True )
    cam_booking_datetime                    = models.DateTimeField(default=datetime.datetime.now())

    # CAM booking rate for differentiate room rate for different CAM's
    cam_booking_rate                        = models.FloatField('Booking Room Rate', default = 0.0)

    cam_booking_estimated_checkin_date      = models.DateField("Estimated Check In Date ",null=True,blank=True )
    cam_booking_estimated_checkin_time      = models.TimeField("Estimated Check In Time ",null=True,blank=True )

    cam_booking_estimated_checkout_date     = models.DateField("Estimated Check Out Date ",null=True,blank=True)
    cam_booking_estimated_checkout_time     = models.TimeField("Estimated Check Out Time ",null=True,blank=True)

    cam_booking_actual_checkin_date         = models.DateField("Actual Check In Date ",null=True, blank=True)
    cam_booking_actual_checkin_time         = models.TimeField("Actual Check In Time ",null=True, blank=True)

    cam_booking_actual_checkout_date        = models.DateField("Actual Check Out Date ",null=True, blank=True)
    cam_booking_actual_checkout_time        = models.TimeField("Actual Check Out Time ",null=True, blank=True)

    cam_booking_estimated_no_of_day_stay    = models.PositiveIntegerField("Estimated Days",null =True)
    cam_booking_actual_no_of_day_stay       = models.PositiveIntegerField("Actual Days Stayed",null =True, blank=True)

    cam_booking_check_in_status             = models.BooleanField("Check-In Status", default=False)
    cam_booking_check_out_status            = models.BooleanField("Check-Out Status", default=False)
    
    cam_booking_cancellation_on_datetime    = models.DateTimeField("Booking Cancellation Date",null=True, blank=True)
    cam_booking_favourite                   = models.IntegerField("Favourite?", default=0, choices= YES_NO_CHOICES)
    cam_booking_status                      = models.IntegerField("Status", default=0, choices= BOOKING_STATUS_CHOICES)
    cam_booking_creation_date               = models.DateTimeField(default=datetime.datetime.now())
    booking_remark                          = models.CharField('Booking Remark', max_length=150, null=True)

    def __unicode__(self):
        #return str(self.cam_booking_id)
        return str(self.cam_booking_id) + ', ' + self.cam_id.cam_first_name +' , '+ str(self.cam_id.cam_company_id) +' ' +self.guest_id.guest_first_name
    
    def get_booking_info(self):
        """
        This is for getting the specific booking information
        """
        status = ''
        more = ''
        if self.cam_booking_status == BOOKING_OPEN:
            status  = '<a marked="1" href="/crm/booking-confirm/?booking_id='+ str(self.cam_booking_id)+'"><span class="label label-info">Open</span></a>'
            more    = '<a marked="1" href="/crm/booking-confirm/?booking_id='+ str(self.cam_booking_id)+'"><i class="fa-2x pe-7s-more text-primary2"></i></a>'
        if self.cam_booking_status == BOOKING_BOOKED:
            status  = '<a marked="1" href="/crm/booking-detail-display/?booking_id='+ str(self.cam_booking_id)+'"><span class="label label-success">Booked</span></a>'
            more    = '<a marked="1" href="/crm/booking-detail-display/?booking_id='+ str(self.cam_booking_id)+'"><i class="fa-2x pe-7s-more text-primary2"></i></a>'
        if self.cam_booking_status == BOOKING_COMPLETED:
            status  = '<a marked="1" href="/crm/booking-detail-display/?booking_id='+ str(self.cam_booking_id)+'"><span class="label label-warning">Completed</span></a>'
            more    = '<a marked="1" href="/crm/booking-detail-display/?booking_id='+ str(self.cam_booking_id)+'"><i class="fa-2x pe-7s-more text-primary2"></i></a>'
        if self.cam_booking_status == BOOKING_CANCELLED:
            status = '<a marked="1" href="/crm/booking-detail-display/?booking_id='+ str(self.cam_booking_id)+'"><span class="label label-danger">Cancelled</span></a>'
            more = '<a marked="1" href="/crm/booking-detail-display/?booking_id='+ str(self.cam_booking_id)+'"><i class="fa-2x pe-7s-more text-primary2"></i></a>'
        if self.apartment:
            apt_name = self.apartment.apt_name
            apt_city = self.apartment.apt_city
        else :
            apt_name = 'Hillview Residency'
            apt_city = 'Pune'
        return  {
                    'apartment_name': apt_name, 'apt_location': apt_city ,
                    'guest_name'    : self.guest_id.guest_first_name, 'check_in': self.cam_booking_estimated_checkin_date.strftime('%d %b %Y'),
                    'check_out'     : self.cam_booking_estimated_checkout_date.strftime('%d %b %Y'),
                    'status'        : status, 'promotion_code': self.promotion_code, 'more' : more
                }
    
    def get_cam_booking_info(self):
        """
        This is for getting the specific booking information
        """
        status = ''
        more = ''
        if self.cam_booking_status == BOOKING_OPEN:
            status  = '<a marked="1" href="../cam-booking-details/?booking_id='+ str(self.cam_booking_id)+'"><span class="label label-info">Open</span></a>'
            more    = '<a marked="1" href="../cam-booking-details/?booking_id='+ str(self.cam_booking_id)+'"><i class="fa-2x pe-7s-more text-primary2"></i></a>'
        if self.cam_booking_status == BOOKING_BOOKED:
            status  = '<a marked="1" href="../cam-booking-details/?booking_id='+ str(self.cam_booking_id)+'"><span class="label label-success">Booked</span></a>'
            more    = '<a marked="1" href="../cam-booking-details/?booking_id='+ str(self.cam_booking_id)+'"><i class="fa-2x pe-7s-more text-primary2"></i></a>'
        if self.cam_booking_status == BOOKING_COMPLETED:
            status  = '<a marked="1" href="../cam-booking-details/?booking_id='+ str(self.cam_booking_id)+'"><span class="label label-warning">Completed</span></a>'
            more    = '<a marked="1" href="../cam-booking-details/?booking_id='+ str(self.cam_booking_id)+'"><i class="fa-2x pe-7s-more text-primary2"></i></a>'
        if self.cam_booking_status == BOOKING_CANCELLED:
            status = '<a marked="1" href="../cam-booking-details/?booking_id='+ str(self.cam_booking_id)+'"><span class="label label-danger">Cancelled</span></a>'
            more = '<a marked="1" href="../cam-booking-details/?booking_id='+ str(self.cam_booking_id)+'"><i class="fa-2x pe-7s-more text-primary2"></i></a>'

        if self.apartment:
            apt_name = self.apartment.apt_name
            apt_city = self.apartment.apt_city
        else :
            apt_name = 'Hillview Residency'
            apt_city = 'Pune'
            
        return  {
                    'apartment_name': apt_name, 'apt_location': apt_city ,
                    'guest_name'    : self.guest_id.guest_first_name, 'check_in': self.cam_booking_estimated_checkin_date.strftime('%d %b %Y'),
                    'check_out'     : self.cam_booking_estimated_checkout_date.strftime('%d %b %Y'),
                    'status'        : status, 'promotion_code': self.promotion_code, 'more' : more
                }

    # Apartment Owner Related
    def get_apartment_booking_info(self):
        """
        This is for getting the specific booking information for Apaertment
        Owner.
        """
        status = ''
        more = ''
        check_in_status = ''
        if self.cam_booking_check_in_status:
            check_in_status = '<i class="fa fa-check-square-o text-success" style="font-size: 20px;"></i>'
        
        if self.cam_booking_status == BOOKING_OPEN:
            status  = '<a marked="1" href="../apt-open-booking-details/?booking_id='+ str(self.cam_booking_id)+'"><span class="label label-info">Open</span></a>'
            more    = '<a marked="1" href="../apt-open-booking-details/?booking_id='+ str(self.cam_booking_id)+'"><i class="fa-2x pe-7s-more text-primary2"></i></a>'
        if self.cam_booking_status == BOOKING_BOOKED:
            status  = '<a marked="1" href="../apt-booked-booking-details/?booking_id='+ str(self.cam_booking_id)+'"><span class="label label-success">Booked</span></a>'
            more    = '<a marked="1" href="../apt-booked-booking-details/?booking_id='+ str(self.cam_booking_id)+'"><i class="fa-2x pe-7s-more text-primary2"></i></a>'
        if self.cam_booking_status == BOOKING_COMPLETED:
            status  = '<a marked="1" href="../apt-completed-booking-details/?booking_id='+ str(self.cam_booking_id)+'"><span class="label label-warning">Completed</span></a>'
            more    = '<a marked="1" href="../apt-completed-booking-details/?booking_id='+ str(self.cam_booking_id)+'"><i class="fa-2x pe-7s-more text-primary2"></i></a>'
        if self.cam_booking_status == BOOKING_CANCELLED:
            status = '<a marked="1" href="../apt-cancelled-booking-details/?booking_id='+ str(self.cam_booking_id)+'"><span class="label label-danger">Cancelled</span></a>'
            more = '<a marked="1" href="../apt-cancelled-booking-details/?booking_id='+ str(self.cam_booking_id)+'"><i class="fa-2x pe-7s-more text-primary2"></i></a>'
        
        if self.apartment:
            apt_name = self.apartment.apt_name
            apt_city = self.apartment.apt_city
        else :
            apt_name = 'Hillview Residency'
            apt_city = 'Pune'
        
        return  {
                    'apartment_name': apt_name, 'check_in_status': check_in_status ,
                    'guest_name'    : self.guest_id.guest_first_name, 'check_in': self.cam_booking_estimated_checkin_date.strftime('%d %b %Y'),
                    'check_out'     : self.cam_booking_estimated_checkout_date.strftime('%d %b %Y'),
                    'status'        : status, 'promotion_code': self.promotion_code, 'more' : more
                }


class CRM(User):
    #crm_id              = models.AutoField(unique=True)
    crm_contactno       = models.CharField("Phone Number",max_length=15, null = True)
    crm_city            = models.CharField("City",max_length=30, null = True)
    crm_state           = models.CharField("State",max_length=30, null = True)
    crm_country         = models.CharField("Country",max_length=30, null = True)
    crm_gender          = models.CharField("Gender",max_length=10, null=True, choices= GENDER_CHOICES)
    crm_age             = models.PositiveIntegerField("Age",null =True)
    crm_isemailalert_on = models.IntegerField("Email Alerts?", default=0, choices= YES_NO_CHOICES)
    crm_issmsalert_on   = models.IntegerField("SMS Alerts?", default=0, choices= YES_NO_CHOICES)
    crm_status          = models.IntegerField("Status", default=1, choices=ACTIVE_DEACTIVE_CHOICES)
    crm_creation_date   = models.DateTimeField(default=datetime.datetime.now())

    def __unicode__(self):
        return self.first_name +' '+ self.last_name


class Invoice(models.Model):
    invoice_id            = models.AutoField(primary_key=True)
    invoice_unique_id     = models.CharField('Invoice Unique ID',max_length=30, null=True)
    cam_booking_id        = models.ForeignKey(CAMBooking, related_name = 'cam_bookings', null=True, verbose_name="CAM Booking Details")
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
        return self.cam_booking_id.cam_id.cam_first_name + ' ' + self.cam_booking_id.cam_id.cam_company_id.cam_company_name + ' ' + '{:,.2f}'.format(self.invoice_gross_amount)

    def days_stayed(self):
        return str(self.cam_booking_id.cam_booking_actual_no_of_day_stay)

