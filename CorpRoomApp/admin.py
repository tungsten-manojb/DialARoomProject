from django.contrib import admin
from CorpRoomApp.models import *
# Register your models here.

from CorpRoomApp.send_mail import *


class PropertyOwnerAdmin(admin.ModelAdmin):
    list_display = ['apt_owner_id', 'apt_owner_name', 'apt_owner_email', 'apt_owner_contactno','apt_owner_city']


class PropertyAdmin(admin.ModelAdmin):
    list_display = ['property_id', 'apt_name', 'apt_city','is_apt_AC_NONAC', 'apt_owner_id','number_of_rooms','apartment_availability']

def send_mail_for_booking(modeladmin, request, queryset):
    #print request
    print 'POST : ',request.POST.get('_selected_action')
    booking_id = request.POST.get('_selected_action')
    send_booking_confirmation_email(booking_id)
send_mail_for_booking.short_description = "Send Booking Confirmation Mail"

class BookingAdmin(admin.ModelAdmin):
    list_display = ['booking_id','property_id','guest_id', 'customer_id',  'booking_estimated_checkin_date','booking_estimated_checkout_date','booking_amount']
    ordering = ['booking_id']
    #actions = [send_mail_for_booking]

class InvoiceAdmin(admin.ModelAdmin):
    list_display = ['invoice_id','booking_id', 'invoice_datetime','extra_charges','invoice_gross_amount'] 
    ordering = ['invoice_id']

class ApartmentRoomAdmin(admin.ModelAdmin):
    list_display = ['apt_room_id','property_id','apt_room_number','apt_room_images1','apt_room_rate','apt_room_status']
    ordering = ['apt_room_id']

class CustomerAdmin(admin.ModelAdmin):
    list_display = ['id','cust_unique_id', 'cust_first_name', 'cust_last_name','user_type']

class GuestAdmin(admin.ModelAdmin):
    list_display = ['guest_id','guest_unique_id','guest_first_name','customer_id']

admin.site.register(Booking, BookingAdmin)
admin.site.register(Invoice, InvoiceAdmin)
admin.site.register(Company)
admin.site.register(RelationShipManager)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Property)
admin.site.register(PropertyRoom)
admin.site.register(PropertyRate)
admin.site.register(PropertyImage)
admin.site.register(PropertyDocument)
admin.site.register(Facilities)
admin.site.register(Cuisines)
admin.site.register(Country)
admin.site.register(State)
admin.site.register(City)
admin.site.register(Location)
admin.site.register(Guest, GuestAdmin)
admin.site.register(PropertyOwnerBankDetails)
admin.site.register(PaymentTransaction)
admin.site.register(Promotion_code)
admin.site.register(BookedRoom)
admin.site.register(CAMPropertyRate)
admin.site.register(CorporateTransaction)
admin.site.register(CustomerFavoriteProperty)
admin.site.register(UserTrackingActivity)
admin.site.register(UserBookingStatisticTrack)