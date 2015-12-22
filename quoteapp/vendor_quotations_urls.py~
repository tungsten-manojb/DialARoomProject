from django.conf.urls import patterns, include, url
from quoteapp.views import *

vendor_quote_urls = [
    url(r'^request-list/', 'quoteapp.views.vendor_request.request_list_page', name='get_request_list_page'),
    url(r'^get-quote-request-list/', 'quoteapp.views.vendor_request.get_quote_request', name='get_request_list'),
    url(r'^request-details/', 'quoteapp.views.vendor_request.request_quote_details', name='request_quote_details'),
    url(r'^send-quotation/', 'quoteapp.views.vendor_request.send_quotation', name='send_quotation'),

    url(r'^get-locations/', 'quoteapp.views.vendor_quotations.get_all_location', name='get_all_location'),
    url(r'^get-properties/', 'quoteapp.views.vendor_quotations.get_all_properties', name='get_all_properties'),
]
