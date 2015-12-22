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

APARTMENT_AVAILABILITY = (
    ('AVAILABLE', 'AVAILABLE'),
    ('NOTAVAILABLE','NOT AVAILABLE')
)


BOOKING_ALL         = 0
BOOKING_BOOKED      = 1
BOOKING_COMPLETED   = 2
BOOKING_CANCELLED   = 3
BOOKING_OPEN        = 4

class ApartmentOwner(models.Model):
    apt_owner_id              = models.AutoField(primary_key=True)
    owner_unique_id           = models.CharField('Owner Unique ID', max_length=30,null=True )
    apt_owner_name            = models.CharField('Owner Name', max_length=50,  null=True)
    apt_owner_username        = models.CharField('owner_username',max_length=50,null=False,unique=True)
    apt_owner_password        = models.CharField('owner_password',max_length=50,null=True)
    apt_owner_email           = models.CharField("Email ID", max_length=50, null=True)
    apt_owner_contactno       = models.CharField("Contact Number", max_length=15, null=True)
    apt_owner_address         = models.CharField("Address Line",max_length=150,null=True)
    apt_owner_city            = models.CharField("City",max_length=20, null=True)
    apt_owner_state           = models.CharField("State",max_length=20, null=True)
    apt_owner_country         = models.CharField("Country",max_length=20, null=True)
    apt_owner_pincode         = models.CharField("Pincode",max_length=12, null=True)
    apt_owner_gender          = models.CharField("Gender",max_length=20, null=True, choices= GENDER_CHOICES)
    apt_owner_age             = models.CharField("Age",max_length=20, null=True)
    apt_owner_isemailalert_on = models.IntegerField("Email Alert", default=0, choices= YES_NO_CHOICES)
    apt_owner_issmsalert_on   = models.IntegerField("SMS Alert", default=0, choices= YES_NO_CHOICES)
    apt_owner_status          = models.IntegerField("Status", default=1, choices=ACTIVE_DEACTIVE_CHOICES)
    apt_owner_creation_date   = models.DateTimeField()
    apt_owner_update_date     = models.DateTimeField(default=datetime.datetime.now())
    
    
    def __unicode__(self):
        return str(self.apt_owner_name)
    
    def get_apartment_owner(self):
        return { 'owner_id': self.apt_owner_id, 'owner_name': self.apt_owner_name }


class Apartment(models.Model):
    apt_id                   = models.AutoField(primary_key=True)
    apartment_unique_id      = models.CharField("Apartment Unique_id",max_length=30, null=True)
    apt_owner_id             = models.ForeignKey(ApartmentOwner,related_name = 'owner', null=True, verbose_name="Owner Name")
    apt_name                 = models.CharField("Apartment Name",max_length=50, null=True)
    apt_description          = models.CharField('Apartment Description',max_length=4000,null=True)
    number_of_rooms          = models.PositiveIntegerField("Number Of Rooms ", null=True)
    apt_address              = models.CharField("Address Line",max_length=150, null=True)
    location                 = models.CharField("Location",max_length=150, null=True)
    apt_city                 = models.CharField("City",max_length=20, null=True)
    apt_state                = models.CharField("State",max_length=20, null=True)
    apt_country              = models.CharField("Country",max_length=20, null=True)
    apt_pincode              = models.CharField("Pincode",max_length=20, null=True)
    is_apt_AC_NONAC          = models.IntegerField("AC",default=0, choices= YES_NO_CHOICES,null=True)
    is_apt_cook              = models.IntegerField("Cook", default=0, choices= YES_NO_CHOICES,null=True)
    is_apt_internet          = models.IntegerField("Internet/Wifi", default=0, choices= YES_NO_CHOICES,null=True)
    is_apt_hotcoldwater      = models.IntegerField("Hot/Cold Water", default=0, choices= YES_NO_CHOICES,null=True)
    is_apt_foodbeverage      = models.IntegerField("Food Beverage",default=0, choices= YES_NO_CHOICES,null=True)
    is_apt_roomfresheners    = models.IntegerField("Room Freshners", default=0, choices= YES_NO_CHOICES,null=True)
    is_apt_newspaper         = models.IntegerField("News Paper", default=0, choices= YES_NO_CHOICES,null=True)
    is_apt_security          = models.IntegerField("Security",default=0, choices= YES_NO_CHOICES,null=True)
    is_apt_laundry           = models.IntegerField("Laundary Services", default=0, choices= YES_NO_CHOICES,null=True)
    is_apt_breakfast         = models.IntegerField("Breakfast", default=0, choices= YES_NO_CHOICES,null=True)
    is_apt_lunch             = models.IntegerField("Lunch", default=0, choices= YES_NO_CHOICES,null=True)
    is_apt_dinner            = models.IntegerField("Dinner", default=0, choices= YES_NO_CHOICES,null=True)
    is_apt_housekeeping      = models.IntegerField("House Keeping", default=0, choices= YES_NO_CHOICES,null=True)
    is_apt_fireexit          = models.IntegerField("Fire Exit ", default=0, choices= YES_NO_CHOICES,null=True)
    is_apt_tv                = models.IntegerField("TV", default=0, choices= YES_NO_CHOICES,null=True)
    apt_status               = models.IntegerField("Status", default=0, choices= BOOKING_STATUS_CHOICES,null=True)
    apt_creation_date        = models.DateTimeField()
    apt_update_date          = models.DateTimeField(default=datetime.datetime.now())
    apartment_availability   = models.CharField('Apartment Availability',max_length=20,choices= APARTMENT_AVAILABILITY)
    
    def __unicode__(self):
        return self.apt_name
    
    def get_apartment_address(self):
        return self.apt_address+ ', ' + self.apt_city + ', ' + self.apt_state + ', ' + self.apt_country + '- ' +self.apt_pincode
    
    def get_apartment_features(self):
        
        feature_list = []
        if self.is_apt_AC_NONAC ==1:
            feature_list.append('AC')
        if self.is_apt_cook == 1:
            feature_list.append('Cook Available')
        if self.is_apt_internet == 1:
            feature_list.append('Wifi/Internet Available')
        if self.is_apt_hotcoldwater == 1:
            feature_list.append('Hot-Cold Water')
        if self.is_apt_foodbeverage ==1:
            feature_list.append('Food Beverage')
        if self.is_apt_roomfresheners ==1:
            feature_list.append('Room Freshners')
        if self.is_apt_newspaper ==1:
            feature_list.append('News Paper')
        if self.is_apt_security ==1:
            feature_list.append('Security')
        if self.is_apt_laundry ==1:
            feature_list.append('Laundary')
        if self.is_apt_breakfast ==1:
            feature_list.append('Break Fast')
        if self.is_apt_lunch ==1:
            feature_list.append('Lunch')
        if self.is_apt_dinner ==1:
            feature_list.append('Dinner')
        if self.is_apt_housekeeping ==1:
            feature_list.append('House Keeping')
        if self.is_apt_fireexit ==1:
            feature_list.append('Fire Exit')
        if self.is_apt_tv ==1:
            feature_list.append('TV')
        print 'Feature List', feature_list
        return feature_list
    
    def get_apartment_info(self):
        status = ''
        more = ''
        if self.apt_status == BOOKING_OPEN:
            status  = '<a marked="1" href="/crm/get-apartment-details/?apartment_id='+ str(self.apt_id)+'"><span class="label label-info">Open</span></a>'
        if self.apt_status == BOOKING_BOOKED:
            status  = '<a marked="1" href="/crm/get-apartment-details/?apartment_id='+ str(self.apt_id)+'"><span class="label label-success">Booked</span></a>'
        if self.apt_status == BOOKING_COMPLETED:
            status  = '<a marked="1" href="/crm/get-apartment-details/?apartment_id='+ str(self.apt_id)+'"><span class="label label-warning">Completed</span></a>'
        if self.apt_status == BOOKING_CANCELLED:
            status = '<a marked="1" href="/crm/get-apartment-details/?apartment_id='+ str(self.apt_id)+'"><span class="label label-danger">Cancelled</span></a>'

        more = '<a marked="1" href="/crm/get-apartment-details/?apartment_id='+ str(self.apt_id)+'"><i class="fa-2x pe-7s-more text-primary2"></i></a>'
        
        return {
                'apt_id': self.apt_id, 'city':self.apt_city,
                'apartment_name': self.apt_name,
                'owner':self.apt_owner_id.apt_owner_name,'no_of_rooms' : self.apartment_id.count(),
                'status' : status,'more':more
            }

class ApartmentRoom(models.Model):
    apt_room_id             = models.AutoField(primary_key=True)
    apartment_id            = models.ForeignKey(Apartment,related_name = 'apartment_id', null=True,verbose_name="Apartment Name")
    apt_room_number         = models.IntegerField("Room Number ", null=True)
    apt_room_rate           = models.FloatField("Room Rate",null=True) # Rate to show customers
    room_general_rate       = models.FloatField("General Rate",null=True)   # General Rates
    room_agreed_rate        = models.FloatField("Agreement Rate",null=True) # Agreement Rate
    room_discount_rate      = models.FloatField("Discout Rate",null=True)   # Discounted Rate
    apt_room_images1        = models.ImageField("Room Image 1", upload_to= ROOM_IMAGES_PATH, max_length=255, default=None, null=True,blank=True)
    apt_room_images2        = models.ImageField("Room Image 2", upload_to= ROOM_IMAGES_PATH, max_length=255, default=None, null=True, blank=True)
    apt_room_images3        = models.ImageField("Room Image 3", upload_to= ROOM_IMAGES_PATH, max_length=255, default=None, null=True, blank=True)
    apt_room_images4        = models.ImageField("Room Image 4", upload_to= ROOM_IMAGES_PATH, max_length=255, default=None, null=True, blank=True)
    apt_room_images5        = models.ImageField("Room Image 5", upload_to= ROOM_IMAGES_PATH, max_length=255, default=None, null=True, blank=True)
    room_type               = models.CharField("Room Type",max_length=12, default=0, choices= ROOM_TYPE_CHOICES)
    apt_room_status         = models.IntegerField("Status", default=0, choices= BOOKING_STATUS_CHOICES)
    apt_room_creation_date  = models.DateTimeField()
    room_active_status      = models.IntegerField('Room Active Status', default=1, choices=ACTIVE_DEACTIVE_CHOICES)
    room_update_date        = models.DateTimeField(default=datetime.datetime.now())
    
    def __unicode__(self):
        return  str(self.apt_room_number)

    def get_apartment_room_details(self):
        return {
            'city_name':self.apartment_id.apt_city, 'room_id': self.apt_room_id,
            'apartment_name': self.apartment_id.apt_name,
            'apartment_address':self.apartment_id.get_apartment_address(),
            'room_rate': self.apt_room_rate, 
            'room_image': SERVER_MEDIA_URL + self.apt_room_images1.url ,
            # 'room_image': 'SERVER_MEDIA_URL + self.apt_room_images1.url or ''',
            'room_type': self.room_type,
            'room_number':self.apt_room_number
            }

    def get_apt_room_details_for_admin_booking(self):
        
        return {
                'city_name':self.apartment_id.apt_city, 'room_id': self.apt_room_id,
                'apartment_name': self.apartment_id.apt_name, 'room_type': self.room_type,
                'apartment_address':self.apartment_id.get_apartment_address(), 'location': self.apartment_id.location,
                'room_rate': self.apt_room_rate, 'room_image': SERVER_MEDIA_URL + self.apt_room_images1.url,
                'info' : '<a marked="1" onClick="showDetails(this)"><i class="fa-2x pe-7s-info text-info"></i></a>',
                'book' : '<a onClick="goForBooking('+ str(self.apt_room_id) +')" marked="1"><i class="fa-2x pe-7s-angle-right-circle text-success"></i></a>',
                'book_now_id' : str(self.apt_room_id),
                'general_room_rate' : self.room_general_rate, 
                'desc' : self.apartment_id.apt_description
            }

    def get_apt_room_details_for_cam_booking(self):
        
        return {
                'city_name':self.apartment_id.apt_city, 'room_id': self.apt_room_id,
                'apartment_name': self.apartment_id.apt_name, 'room_type': self.room_type,
                'apartment_address':self.apartment_id.get_apartment_address(), 'location': self.apartment_id.location,
                'room_rate': self.apt_room_rate, 'room_image': SERVER_MEDIA_URL + self.apt_room_images1.url,
                'info' : '<a marked="1" onClick="showDetails(this)"><i class="fa-2x pe-7s-info text-info"></i></a>',
                'book' : '<a onClick="goForBooking('+ str(self.apt_room_id) +')" marked="1"><i class="fa-2x pe-7s-angle-right-circle text-success"></i></a>'
            }

class CAMCompany(models.Model):
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

class CAMBooking(models.Model):
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

