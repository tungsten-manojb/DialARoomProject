
import smtplib
import smtplib
from smtplib import SMTPException
import urllib


def send_sms(message, mobile_no):
    try:
        host = "http://173.45.76.226"
        user_name = "dialrm"
        user_password = "dialrm"
        recipient = "trans1"
        sender="DIALRM"
        number=mobile_no
        
        http_req = host
        http_req += ":81/send.aspx?username="
        http_req += urllib.quote(user_name)
        http_req += "&pass="
        http_req += urllib.quote(user_password)
        http_req += "&route="
        http_req += urllib.quote(recipient)
        http_req += "&senderid="
        http_req += urllib.quote(sender)
        http_req += "&numbers="
        http_req += urllib.quote(number)
        http_req += "&message="
        http_req += urllib.quote(message)
        get = urllib.urlopen(http_req)
        req = get.read()
        s=req.split('\r')
        status=s[0].split('|')
        print "Status",status[0]
        get.close()

        if(status=='1'):
            data =  {'success': 'true', 'message': 'Message has been sent to the user'}
        else:
            data =  {'success': 'false', 'message': 'Message has not been sent to the user'}
    except SMTPException,e:
        print "failed to send mail", e
        data = {'success': 'false'}


