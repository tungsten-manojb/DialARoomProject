from django.conf.urls import patterns, include, url
from quoteapp.views import *

corporate_quote_urls = [
    url(r'^request-list/', 'quoteapp.views.corporate_request.request_list_page', name='get_request_list_page'),
    url(r'^get-quote-request-list/', 'quoteapp.views.corporate_request.get_quote_request', name='get_request_list'),
    url(r'^request-new-quote/','quoteapp.views.corporate_request.request_new_quote',name='request_new_quote'),
    url(r'^submit-quote-request/', 'quoteapp.views.corporate_request.submit_quote_request', name='submit_quote_request'),
    url(r'^request-details/', 'quoteapp.views.corporate_request.request_quote_details', name='request_quote_details'),
    url(r'^request-quote-details/', 'quoteapp.views.corporate_request.get_requested_quotation_detail', name='get_requested_quotation_detail'),
    

    url(r'^quotation-list/', 'quoteapp.views.corporate_quotations.quotation_list_page', name='quotation_list_page'),
    url(r'^get-quotation-list/', 'quoteapp.views.corporate_quotations.get_quotation_list', name='get_quotation_list'),
    url(r'^quotation-details/', 'quoteapp.views.corporate_quotations.quotation_details', name='quotation_detail'),
    url(r'^accept-quotation/', 'quoteapp.views.corporate_quotations.accept_quotation', name='accept_quotation'),
    url(r'^reject-quotation/', 'quoteapp.views.corporate_quotations.reject_quotation', name='reject_quotation'),

    url(r'^create-quotation-booking/', 'quoteapp.views.corporate_quote_bookings.corporate_quote_booking_page', name='make_corporate_quote_booking_page'),
    url(r'^confirm-quote-booking/', 'quoteapp.views.corporate_quote_bookings.save_quote_booking', name='save_quote_booking'),
    
    #url(r'^check-for-new-quotation/', 'quoteapp.views.corporate_quotations.check_for_new_quotation', name='check_for_new_quotation'),

    url(r'^get-city-locations/', 'quoteapp.views.corporate_request.get_city_wise_locations', name='get_city_wise_locations'),
    url(r'^get-state-cities/', 'quoteapp.views.corporate_request.get_state_wise_cities', name='get_state_wise_cities'),
]
