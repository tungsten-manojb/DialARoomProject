import cStringIO as StringIO
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse
from cgi import escape
import pdb
from CorpRoomApp.models import *
from django.views.decorators.csrf import csrf_exempt
from quoteapp.models import *


def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    context = Context(context_dict)
    html  = template.render(context)
    result = StringIO.StringIO()

    pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return HttpResponse('We had some errors<pre>%s</pre>' % escape(html))

def get_invoice_details_for_print(booking_number):
    try:
        print 'Fetching Records for Invoice'
        
        booking_details = Booking.objects.get(booking_unique_id=booking_number)
        invoice = Invoice.objects.get(booking_id=booking_details)
        corporate_name      = ''
        company_address     = ''
        company_state_pin   = ''
        
        if booking_details.customer_id:
            corporate_name = booking_details.customer_id.cust_company_id.company_name
            company_address = booking_details.customer_id.cust_company_id.get_company_address()
            company_state_pin = booking_details.customer_id.cust_company_id.get_company_state_pincode()
    
        if booking_details.is_from_quote:
            quote_res = QuotationResponse.objects.get(quotation_uid=booking_details.quotation_id)
            rack_rate = quote_res.property_rack_rate
        else:
            rack_rate = booking_details.property_id.rack_rate
        
        rack_rate_amt = booking_details.booking_actual_no_of_day_stay * rack_rate
        
        save_rate = rack_rate - booking_details.booking_rate
        save_rate_amt = save_rate * booking_details.booking_actual_no_of_day_stay
        
        
        
        data = {
                'invoice_no' : invoice.invoice_unique_id,
                'invoice_date' : invoice.invoice_generated_datetime.strftime('%d/%m/%Y'),
                'booking_number': booking_details.booking_unique_id,
                'guest_name' : booking_details.guest_id.guest_first_name,
                'nights_stay': booking_details.booking_actual_no_of_day_stay,
                'tariff_rate': booking_details.booking_rate,
                'room_charges' : invoice.room_charges,
                'taxes'     : invoice.tax_amount,
                'rack_rate' :  rack_rate,
                'rack_rate_amt' : rack_rate_amt,
                'save_rate' : save_rate,
                'save_rate_amt': save_rate_amt,
                'corporate_name' : corporate_name,
                'company_address' : company_address,
                'company_state_pin' : company_state_pin,
                'extra_charges' : invoice.extra_charges,
                'email_address' : booking_details.guest_id.guest_email,
                'phone_number' : booking_details.guest_id.guest_contactno,
                'address'   : booking_details.property_id.property_address,
                'city'      : booking_details.property_id.property_location,
                'zipcode'   : booking_details.property_id.property_pincode,
                'check_in'  : booking_details.booking_actual_checkin_date.strftime('%d/%m/%Y'),
                'check_out' : booking_details.booking_actual_checkout_date.strftime('%d/%m/%Y'),
                'tax_amount': invoice.tax_amount,
                'gross_amount':invoice.invoice_gross_amount
            }
        return data
    except Exception as err:
        print 'Error', err
    return {}


def admin_print_corporate_invoice(request):
    print "print here"
    data = get_invoice_details_for_print(request.GET.get('booking_number'))
    return render_to_pdf(
            'web/invoice-print.html',
            {
                'pagesize':'A4',
                'data' : data
            }
        )