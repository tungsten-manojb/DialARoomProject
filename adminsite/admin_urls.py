from django.conf.urls import patterns, include, url
from adminsite.views import *
from adminsite.apartments import *
from adminsite import cam

from quoteapp.admin_quote_urls import quote_url_patterns    # Mobile web services redirects here
from quoteapp.corporate_quote_urls import corporate_quote_urls  # Corporate Quote URLS



cam_patterns = [
    url(r'^$', 'adminsite.cam.cam_api.cam_index', name='cam_index'),
    url(r'^dashboard/', 'adminsite.cam.cam_api.cam_dashboard', name='cam_dashbaord'),
    url(r'^cam-booking-list-page/', 'adminsite.cam.cam_api.booking_list_page', name='cam_booking_list_page'),
    url(r'^cam-guest-list/', 'adminsite.cam.cam_api.cam_guest_list', name='cam_guest_list'),
    url(r'^cam-my-profile/', 'adminsite.cam.cam_api.cam_my_profile', name='my_profile'),
    url(r'^cam-add-new-booking/', 'adminsite.cam.cam_api.cam_new_booking_page', name='cam_new_booking_page'),
    url(r'^get-cam-booking-list/', 'adminsite.cam.cam_api.get_cam_booking_list', name='get_cam_booking_list'),
    #url(r'^cam-new-booking-search/', 'adminsite.cam.cam_api.cam_new_booking_page', name='cam_new_booking_search'),

    url(r'^get-available-rooms-for-cam-booking/','adminsite.cam.cam_api.get_available_rooms_for_cam_booking', name='get_available_rooms_for_cam_booking'),

    url(r'^cam-new-booking-search/', 'adminsite.cam.cam_api.cam_new_booking_search', name='cam_new_booking_search'),

    url(r'^cam-booking-details/', 'adminsite.cam.cam_api.cam_booking_detail_display', name='cam_booking_detail_display'),
    url(r'^cam-booking-confirm/', 'adminsite.cam.cam_api.cam_booking_confirm_page', name='cam_booking_confirm_page'),
    url(r'^cam-save-booking-details/', 'adminsite.cam.cam_api.cam_save_booking_details', name='cam_save_booking_details'),
    url(r'^show-property-info/','adminsite.cam.cam_api.get_specific_property_info',name='get_specific_property_info'),

    url(r'^get-cam-guest-list/', 'adminsite.cam.cam_api.get_cam_guest_list', name='get_cam_guest_list'),
    url(r'^save-guest-information/', 'adminsite.cam.cam_api.save_guest_information', name='save_guest_information'),
    url(r'^update-guest-information/', 'adminsite.cam.cam_api.update_guest_information', name='update_guest_information'),
    url(r'^get-guest-details/', 'adminsite.cam.cam_api.get_guest_details', name='get_guest_details'),
    url(r'^edit-cam-profile/', 'adminsite.cam.cam_api.edit_cam_profile_page', name='edit_cam_profile_page'),
    url(r'^update-cam-profile-info/', 'adminsite.cam.cam_api.update_cam_profile_info', name='update_cam_profile_info'),
    url(r'^cam-password-change/', 'adminsite.cam.cam_api.cam_password_change', name='update_cam_password'),
    url(r'^account-ledger/','adminsite.cam.cam_ledger.cam_ledger_page',name='cam_ledger_page'),
    url(r'^get-cam-transaction-ledger/','adminsite.cam.cam_ledger.get_cam_ledger_transactions',name='get_cam_ledger_transactions'),

    url(r'^payment-page/','adminsite.cam.cam_payments.open_payment_page',name='open_payment_page'),
    url(r'^confirm-payable-amount/','adminsite.cam.cam_payments.get_calculate_payments',name='get_calculate_payments'),

    url(r'^payment-gateway-response/','adminsite.cam.cam_payments.save_payment_gateway_response',name='gateway_response'),
    url(r'^payment-detail/','adminsite.cam.cam_payments.payment_details',name='payment_details'),

    url(r'^print-ledger/','adminsite.cam.cam_ledger.print_cam_ledger_transactions',name='print_cam_ledger_transactions'),
    url(r'^sign-out-ADMIN/', 'adminsite.views.signOutAdmin', name='sign_out'),

    url(r'^dashboard-booking/','adminsite.cam.cam_additional_functionalitites.new_booking_from_dashboard',name='booking_dashboard'),

    
    
    url(r'^quote/', include(corporate_quote_urls)), 
]


admin_url_patterns = [
    url(r'^$', 'adminsite.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    
    # Web Urls for admin Panel login and everything
    url(r'^admin-login/', 'adminsite.views.admin_login', name='admin_login'),
    url(r'^dashboard/', 'adminsite.views.show_dashboard', name='show_dashboard'),
    url(r'^sign-out-ADMIN/', 'adminsite.views.signOutAdmin', name='signOut'),

# Apartment related API's and Web services are here admin panel
    url(r'^apartment-list/', 'adminsite.apartments.apartment_list_page', name='apartment_list'),
    url(r'^add-new-apartment/', 'adminsite.apartments.new_apartment_page', name='new_apartment'),

    url(r'^save-apartment-info/', 'adminsite.apartments.save_apartment_information', name='save_apartment_information'),

    
    url(r'^save-room-information/', 'adminsite.apartments.save_room_information', name='save_room_information'),
    url(r'^save-owner-information/', 'adminsite.apartments.save_owner_information', name='save_owner_information'),
    url(r'^apartment-confirm/', 'adminsite.apartments.apartment_confirm', name='apartment_confirm'),
    url(r'^get-apartment-list/', 'adminsite.apartments.get_apartment_list', name='get_apartment_list'),
    #url(r'^get-owner-list/', 'adminsite.apartments.get_owner_list', name='get_owner_list'),
    url(r'^get-apartment-details/', 'adminsite.apartments.get_apartment_details', name='get_apartment_details'),
    url(r'^edit-apartment-details/', 'adminsite.apartments.edit_apartment_page', name='edit_apartment_page'),
    url(r'^update-apartment-details/', 'adminsite.apartments.update_apartment_info', name='update_apartment_info'),
    url(r'^update-room-details/', 'adminsite.apartments.edit_apartment_room', name='edit_apartment_room'),
    url(r'^property-info/', 'adminsite.apartments.property_info', name='property-info'),

    url(r'^save-payment-information/', 'adminsite.payment.save_payment_information', name='save_payment_information'),
    url(r'^get-payment-list/', 'adminsite.payment.get_payment_list', name='get_payment_list'),

#invoice print test url
    url(r'^invoice-page/', 'adminsite.print_invoice_pdf.admin_print_corporate_invoice', name='show_invoice_page'),

# Customer (CAM) Related API's Web Services
    url(r'^customer-list/', 'adminsite.customers.customer_list_page', name='customer_list_page'),
    url(r'^payment-list/', 'adminsite.customers.payment_list_page', name='payment_list_page'),

    url(r'^add-new-customer/', 'adminsite.customers.add_customer_page', name='add_customer_page'),
    url(r'^save-company-information/', 'adminsite.customers.save_company_information', name='save_company_information'),
    url(r'^save-manager-information/', 'adminsite.customers.save_manager_information', name='save_manager_information'),
    url(r'^save-cam-info/', 'adminsite.customers.save_cam_information', name='save_cam_information'),
    url(r'^customer-confirm/', 'adminsite.customers.customer_confirm', name='customer_confirm'),
    
    url(r'^get-customer-guest-list/', 'adminsite.customers.get_customer_guest_list', name='get_customer_guest_list'),
    url(r'^get-customer-list/', 'adminsite.customers.get_cam_customer_list', name='get_cam_customer_list'),
    url(r'^customer-detail-display/', 'adminsite.customers.customer_detail_display', name='customer_detail_display'),
    url(r'^edit-customer-details/', 'adminsite.customers.edit_customer_details', name='edit_customer_details'),
    url(r'^update-cam-info/', 'adminsite.customers.update_customer_info', name='update_customer_info'),
    url(r'^delete-fav-property/','adminsite.customers.delete_fav_property', name='delete_fav_property'),
    url(r'^add-fav-property/','adminsite.customers.add_fav_property', name='add_fav_property'),

# Booking related URL's for admin panel
    url(r'^booking-list/', 'adminsite.admin_bookings.booking_list_page', name='booking_list'),
    url(r'^new-booking-search/', 'adminsite.admin_bookings.booking_search_page', name='booking_search_page'),
    url(r'^booking-confirm/', 'adminsite.admin_bookings.booking_confirm_page', name='booking_confirm_page'),
    # This is used for adding new booking from backend admin

    url(r'^admin-add-new-booking/', 'adminsite.admin_bookings.new_booking_page', name='new_booking_page'),
    
    url(r'^admin-save-booking/', 'adminsite.admin_bookings.save_booking_details', name='save_booking_details'),
    url(r'^get-booking-list/','adminsite.admin_bookings.get_booking_list', name='get_booking_list'),
    url(r'^booking-detail-display/','adminsite.admin_bookings.booking_detail_display', name='booking_detail_display'),
    
    url(r'^admin-booking-confirm/','adminsite.admin_bookings.make_admin_booking_confirm', name='make_admin_booking_confirm'),
    
    url(r'^admin-cancel-booking/','adminsite.admin_bookings.make_admin_booking_cancel', name='make_admin_booking_cancel'),
    # this url used for check availability of of apartments on admin panel side.
    url(r'^get-available-rooms-for-booking/','adminsite.admin_bookings.get_available_rooms_for_booking', name='get_available_rooms_for_booking'),
    url(r'^image-upload/', 'adminsite.image_upload.imageupload', name='imageupload'),
    url(r'^remove-image/', 'adminsite.image_upload.remove_image', name='remove_image'),
    url(r'^add-extra-charges/', 'adminsite.admin_bookings.add_extra_charges', name='add-extra-charges'),
    url(r'^print-invoice/', 'adminsite.admin_bookings.myview', name='print-invoice'),

    url(r'^quote/', include(quote_url_patterns)), #These API's are for handling the cam user dashboard
    
    # VENDOR RELATED URLS
    url(r'^vendor-list/', 'adminsite.vendors.vendor_list_page', name='vendor_list_page'),
    url(r'^get-vendor-info/', 'adminsite.vendors.show_vendor_details', name='show_vendor_info'),
    url(r'^update-vendor-info/', 'adminsite.vendors.update_vendor_details', name='update_vendor_info'),
    url(r'^reset-vendor-password/', 'adminsite.vendors.reset_vendor_password', name='reset_vendor_password'),
    
    # url(r'^request-list/', 'adminsite.service_request.request_list_page', name='get_request_list'),
    url(r'^customer-stats/', 'adminsite.user_statistics.display_customer_statistics', name='reset_vendor_password'),
    url(r'^customer-trace/', 'adminsite.user_statistics.display_customer_trace', name='reset_vendor_password'),
    

# TEST FOR LAST LOGIN LIST
    url(r'^customer-last-login-data/', 'CorpRoomApp.temp.customer_last_login_data', name='customer_last_login_data'),

]






