import os , sys , cgi , re, hmac, hashlib, smtplib, requests, datetime
import logging, dateutil, sqlite3, urllib, httplib2, json, psycopg2
import random, string


def sendMSG(email, subject, msg):
    # Set Headers

    FROM = "status@travellrs.com"
    TO = [email] # must be a list
    SUBJECT = subject
    TEXT = msg

    # Prepare actual message

    message = """\
    From: %s
    To: %s
    Subject: %s

    %s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)

    try:
        server = smtplib.SMTP('mail.travellrs.com:25')
        server.starttls()
        server.login('status@travellrs.com', 'RMW@nasa2015')
        server.sendmail(FROM, TO, message)
        server.quit()

        return 'successful'

    except Exception:
        return 'unsuccessful'

# ---

def newUserAlert():
    # Set Headers

    FROM = "status@travellrs.com"
    TO = ["ryanwaite28@gmail.com"] # must be a list
    SUBJECT = 'New User!'
    TEXT = 'New User Joined!!!'

    # Prepare actual message

    message = """\
    From: %s
    To: %s
    Subject: %s

    %s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)


    server = smtplib.SMTP('mail.travellrs.com:25')
    server.starttls()
    server.login('status@travellrs.com', 'RMW@nasa2015')
    server.sendmail(FROM, TO, message)
    server.quit()

# ---

def errorAlert(msg):

    if not msg:
        msg = ''

    # Set Headers

    FROM = "status@travellrs.com"
    TO = ["ryanwaite28@gmail.com"] # must be a list
    SUBJECT = 'Error Alert.'
    TEXT = msg

    # Prepare actual message

    message = """\
    From: %s
    To: %s
    Subject: %s

    %s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)


    server = smtplib.SMTP('mail.travellrs.com:25')
    server.starttls()
    server.login('status@travellrs.com', 'RMW@nasa2015')
    server.sendmail(FROM, TO, message)
    server.quit()

# ---

current_dir = os.path.dirname(os.path.abspath(__file__))

def uniqueValue():
    value = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in xrange(50))
    return value.lower()
# ---

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif', 'mp4', 'avi', 'mov'])
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
