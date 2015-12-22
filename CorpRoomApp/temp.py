
from CorpRoomApp.models import *
import json
import ast
from django.http import HttpResponse
import csv

from django.core.mail import send_mail
import smtplib
from smtplib import SMTPException
import urllib
from django.core.mail import EmailMessage
from django.core import mail

from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email import encoders
import sendgrid
from DialARoomProject import settings

USER_TYPE = {
    0 : 'ADMIN',
    1:'CORPORATE',
    2:'OWNER',
    3:'RETAIL',
}

def retrieve_log_data():
    user_track = UserTrackingActivity.objects.get(user_tracking_id=8)
    path = user_track.path
    
    track_list = path.split('$')
    track_list = [ast.literal_eval(track) for track in track_list ]
    print track_list


def customer_last_login_data(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="customer_last_login.csv"'
    try:
        writer = csv.writer(response)
        customer_list = Customer.objects.all()
        row = ['customer_id','email_id','User Type','Last Login Date','Last Login TimeStamp']
        writer.writerow(row)
        for customer in customer_list:
            #row = [customer.cust_unique_id, customer.cust_email, USER_TYPE[customer.user_type], customer.last_login.strftime('%d %b %Y') if customer.last_login else '', customer.last_login ]
            row = [customer.cust_unique_id, customer.cust_email, USER_TYPE[customer.user_type], customer.last_login.strftime('%d %b %Y') if customer.last_login else '', customer.last_login.strftime('%d/%m/%Y %H:%M:%S') if customer.last_login else '' ]
            writer.writerow(row)
        return response #render(request,'order-list.html', response)
    except Exception as  e:
        print 'temp.py | customer_last_login_data | Exception ',e
        return response

def send_test_cronjob_mail():
    try:
        sg = sendgrid.SendGridClient(settings.SENDGRID_USER_NAME,settings.SENDGRID_PASSWORD)
        message = sendgrid.Mail()
        message.set_headers({'X-Sent-Using': 'SendGrid-API', 'X-Transport': 'web'})
        #to_mail = ['manoj.bawane@tungstenbigdata.com','bawane.manoj03@gmail.com']
        to_mail = ['manoj.bawane@tungstenbigdata.com','prashant.girbane@gmail.com','nilesh@dial-a-room.com','veenesh.minocha@dial-a-room.com']
        
        message.add_to(to_mail)
        message.set_subject("Dailiy Customer Login Report")
        message_to_send = '<html><style>tr td { border-bottom : 1px solid #ddd; padding : 5px;border-left : 1px solid #ccc; }</style> <body><br>'
        message_to_send+= 'Hi Prashant,<br>Please find below Customer Last Login report<br><br>'
        message_to_send+= '<table style="border : 1px solid #ddd;"><tr><th>Customer ID</th><th> Email ID </th><th> User Type </th><th>Last Login Date</th><th>Last Login TimeStamp</th>'
        
        customer_list = Customer.objects.all()
        for customer in customer_list:
            last_date = customer.last_login.strftime('%d %b %Y') if customer.last_login else ''
            last_timestamp = customer.last_login.strftime('%d/%m/%Y %H:%M:%S') if customer.last_login else ''
            message_to_send+='<tr> <td> '+ str( customer.cust_unique_id )+'</td><td>'+ str( customer.cust_email )+'</td><td>'+ USER_TYPE[customer.user_type] +'</td><td>'+ last_date +'</td><td>'+ last_timestamp +'</td></tr>'
        message_to_send+='</table></body></html>'
        print message_to_send
        
        message.set_html(message_to_send)
        message.set_text('')
        
        message.set_from('ADMIN SERVICE <admin@dial-a-room.com>')
        status, msg = sg.send(message)
        print status
        data = {'success': 'true'}
    except Exception, e:
        print e
        data = {'success': 'false'}
    return HttpResponse(json.dumps(data), content_type='application/json')

