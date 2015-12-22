
from django.shortcuts import render
from CorpRoomApp.models import *
from django.http import HttpResponse
import json
from django.db import connection
from adminsite.print_invoice_pdf import render_to_pdf
from django.shortcuts import redirect
import datetime
from CorpRoomApp.common_functionality import store_user_track # for tracking user activity


def cam_ledger_page(request):
    if not request.user.is_authenticated():
        return redirect('/business/')
    store_user_track(request,'Customer Ledger List')   # for tracking user activity
    cam_user_id = request.session['user_id']
    
    print 'Opening Ledger Page'
    data = {}
    return render(request,'cam-user/cam-ledger-list.html',data)


def get_cam_ledger_transactions(request):
    print 'transactions'
    cam_user_id = request.session['user_id']
    balance_amount = 0.0
    data ={}
    var_transaction_list =[]
    desc = ''
    try:
        store_user_track(request,'Customer check for ledger ')   # for tracking user activity
        print 'GET REQUEST : ',  request.GET
        i=0
        if request.GET.get('startDate'):
            startDate = datetime.datetime.strptime(request.GET.get('startDate'), '%d/%m/%Y')
            endDate = datetime.datetime.strptime(request.GET.get('endDate'), '%d/%m/%Y')
            transactions = CorporateTransaction.objects.filter(corporate_id=Customer.objects.get(id=cam_user_id), transaction_date__range=[startDate, endDate] )
            
        else:
            print 'I am in Else'
            transactions = CorporateTransaction.objects.filter(corporate_id=Customer.objects.get(id=cam_user_id))
            
        for transaction in transactions :
            i = i+1
            if transaction.transaction_type == 1:
                balance_amount = balance_amount + transaction.transaction_amount
                amt = transaction.transaction_amount
                desc = 'Invoice :' + str(transaction.invoice_id)
            else:
                balance_amount = balance_amount - transaction.transaction_amount
                amt = -transaction.transaction_amount
                desc = 'Deposit'
            var_transaction_list.append({ 'sr_no':i,  'date' : transaction.transaction_date.strftime('%d/%m/%Y'), 'desc': desc, 'amount' : '{:,.2f}'.format(amt), 'balance' : '{:,.2f}'.format(balance_amount) })
        data = { 'data' : var_transaction_list }
    except Exception as err:
        print 'Error',err
        data = { 'data' : 'None' }
    return HttpResponse(json.dumps(data), content_type='application/json')


def print_cam_ledger_transactions(request):
    print 'transactions'
    cam_user_id = request.session['user_id']
    balance_amount = 0.0
    data = {}
    var_transaction_list = []
    desc = ''
    store_user_track(request,'Customer Printing Ledger Report')   # for tracking user activity
    try:
        customer_obj=Customer.objects.get(id=cam_user_id)
        corporate_name = customer_obj.cust_company_id.company_name
        company_address = customer_obj.cust_company_id.get_company_address()
        company_state_pin = customer_obj.cust_company_id.get_company_state_pincode()
        i=0
        transactions = CorporateTransaction.objects.filter(corporate_id=customer_obj)
        for transaction in transactions :
            i = i+1
            if transaction.transaction_type == 1:
                balance_amount = balance_amount + transaction.transaction_amount
                amt = transaction.transaction_amount
                desc = 'Invoice : ' + str(transaction.invoice_id)
            else:
                balance_amount = balance_amount - transaction.transaction_amount
                amt = -transaction.transaction_amount
                desc = 'Deposit'
            var_transaction_list.append({ 'sr_no':i,  'date' : transaction.transaction_date.strftime('%d/%m/%Y'), 'desc': desc, 'amount' : '{:,.2f}'.format(amt), 'balance' : '{:,.2f}'.format(balance_amount) })
        data = { 'transaction_list' : var_transaction_list, 'corporate_name': corporate_name, 'company_address':company_address,'company_state_pin':company_state_pin, 'final_balance' : '{:,.2f}'.format(balance_amount) }
        
    except Exception as err:
        print 'Error',err
        data = { 'data' : 'None' }
        
    return render_to_pdf(
            'cam-user/cam-ledger-print.html',
            {
                'pagesize':'A4',
                'data' : data
            }
        )

