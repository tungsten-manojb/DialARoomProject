from django.conf.urls import patterns, include, url
from adminsite.views import *
from adminsite.apartments import *
from adminsite import cam
from quoteapp.views import *


quote_url_patterns = [

    # url(r'^$', 'adminsite.cam.cam_api.cam_dashboard', name='cam_dashbaord'),
    url(r'^request-list/', 'quoteapp.views.admin_service.request_list_page', name='get_request_list'),
    # url(r'^get-quotation-list/', 'quoteapp.views.admin_service.quotation_list_page', name='get_quotation_list'),
    url(r'^get-quotation-page/', 'quoteapp.views.admin_service.quotation_list_page', name='get_quotation_list'),
    url(r'^get-quotation-list/', 'quoteapp.views.admin_service.get_quotation_list', name='get_quotation_list'),
    url(r'^get-request-list/', 'quoteapp.views.admin_service.get_request_list', name='get-request-list'),
    url(r'^request-details/', 'quoteapp.views.admin_service.request_quote_details', name='request_quote_details'),
    url(r'^send-quotation/', 'quoteapp.views.admin_service.send_quotation', name='send-quotation'),
    url(r'^quotation-details/', 'quoteapp.views.admin_service.quotation_details', name='quotation_detail'),
    url(r'^get-locations/', 'quoteapp.views.admin_service.get_all_location', name='quotation_detail'),
    url(r'^get-properties/', 'quoteapp.views.admin_service.get_all_properties', name='get_properties'),
    url(r'^get-properties-details/', 'quoteapp.views.admin_service.get_properties_details', name='get_properties_details'),
    url(r'^send-quotation/', 'quoteapp.views.admin_service.send_quotation', name='send_quotation'),



    #url(r'^five-properties/', 'quoteapp.views.find_locations.nearby_five_poperties', name='find_properties'),






    

 
]
