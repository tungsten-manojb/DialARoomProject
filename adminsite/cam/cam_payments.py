from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect

from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt

from django.contrib import auth
from quoteapp.models import *
from django.shortcuts import redirect
from django.http import HttpResponse
from quoteapp.quote_constants import QuoteConstant
from CorpRoomApp.models import Booking
from CorpRoomApp.models import Invoice
from CorpRoomApp.models import PaymentTransaction
from django.db.models import Count, Sum
import pdb
import json
import datetime
from CorpRoomApp.common_functionality import store_user_track # for tracking user activity

UNPAID = 0
PAID = 1

OK = 'Ok'

def open_payment_page(request):
    try:
        store_user_track(request, "Customer Payment")   # for tracking user activity
        
        customer = Customer.objects.get(id=request.session['user_id'])
        bookings = Booking.objects.filter(customer_id=customer)
        invoices = Invoice.objects.filter(booking_id__in=bookings)
        #booking_list = [booking.booking_unique_id for booking in bookings]
        data = { 'invoices' : invoices, 'fullName' : customer.cust_first_name + ' ' +  customer.cust_last_name,
            'email' : customer.cust_email, 'phoneNumber' : customer.cust_contact_no }
    except Exception as err:
        print 'error : ',err
        data = { 'invoices' : [] }
    return render(request,'cam-user/cam-payment-page.html',data)

@csrf_exempt
def get_calculate_payments(request):
    print request.POST
    req_invoices = request.POST.get('inv_list')
    print 'Invoice List ', req_invoices

    total_amount = Invoice.objects.filter(invoice_unique_id__in=req_invoices.split(',')).aggregate(total=Sum('invoice_gross_amount'))
    print 'Total Amount : ', total_amount
    data = { 'success': 'true', 'total_amount' : total_amount['total'] }
    return HttpResponse(json.dumps(data), content_type='application/json')

@csrf_exempt
def save_payment_gateway_response(request):
    print "save_payment_details"
    try:
        print request.POST
        link=''
        if request.method == 'POST':
            store_user_track(request,"Customer Online Payment Gateway Response")   # for tracking user activity
            print 'Online Payment Status', request.POST.get('mmp_txn')
            payment_obj = PaymentTransaction(
                mmp_txn                            =    request.POST.get('mmp_txn'),
                ipg_txn_id                         =    request.POST.get('ipg_txn_id'),
                transaction_type                   =    request.POST.get('transaction_type'),
                property_booking_id                =    request.POST.get('udf4'),
                discriminator                      =    request.POST.get('discriminator'),
                srcharge                           =    request.POST.get('surcharge'),
                customer_name                      =    request.POST.get('udf1'),
                mer_txn                            =    request.POST.get('mer_txn'),
                card_number                        =    request.POST.get('CardNumber'),
                ath_code                           =    request.POST.get('auth_code'),
                prod                               =    request.POST.get('prod'),
                bank_name                          =    request.POST.get('bank_name'),
                date                               =    request.POST.get('date'),
                merchant_id                        =    request.POST.get('merchant_id'),
                amount                             =    request.POST.get('amt'),
                error_description                  =    request.POST.get('desc'),
                bank_txn                           =    request.POST.get('bank_txn'),
                f_code                             =    request.POST.get('f_code'),
                clientcode                         =    request.POST.get('clientcode'),
                mobile_no                          =    request.POST.get('udf3'),
                email_id                           =    request.POST.get('udf2'),
                udf5                               =    request.POST.get('udf5'),
                billing_address                    =    request.POST.get('udf4'),
                udf6                               =    request.POST.get('udf6'),
                booking_transaction_create_by      =    request.POST.get('udf1'),
                booking_transaction_update_by      =    request.POST.get('udf1')
            )
            payment_obj.save()

            data = {
                'success': 'true',
                'cust_email':payment_obj.email_id,
                'error_message': payment_obj.error_description,
                'merchant_id':payment_obj.merchant_id,
                'mer_txn':payment_obj.mer_txn,
                'amt':payment_obj.amount,
                'date':payment_obj.date,
            }

            if payment_obj.f_code == OK :
                invoices = payment_obj.udf6.split(',') # Getting invoice list for confirming the paid status and paid date
                for inv_no in invoices:
                    invoice = Invoice.objects.get(invoice_unique_id=inv_no)
                    invoice.invoice_status = PAID
                    invoice.booking_id.payment_status = PAID
                    invoice.invoice_paid_date = datetime.datetime.now()
                    invoice.save()

                data.update({ 'invoice_list' : invoices })
                
                return redirect('/corporate/payment-detail/?response_code='+str( payment_obj.payment_transaction_id)+'&response_status=true')
            else:
                return redirect('/corporate/payment-detail/?response_code='+str( payment_obj.payment_transaction_id)+'&response_status=false')
    except Exception as e:
        print e
    return redirect('/corporate/payment-detail/?response_code=null&response_status=false')


def payment_details(request):
    try:
        store_user_track(request,'Customer Online Payment Result ')   # for tracking user activity
        response_code = request.GET.get('response_code')
        response_status = request.GET.get('response_status')
        if response_code!='null':
            payment_obj = PaymentTransaction.objects.get(payment_transaction_id=response_code)
            if response_status== 'true' and payment_obj.f_code == OK :
                data = {'success' : 1, 'error_message': payment_obj.error_description }
            else:
                data = {'success' : 2, 'error_message': payment_obj.error_description }
        else:
            data = {'success' : 2, 'error_message': 'Oops something went wrong...'}
    except Exception as err:
        print err
        data = {'success' : 2, 'error_message': 'Oops something went wrong...'}
    return render(request,'cam-user/cam-payment-success.html', data)

