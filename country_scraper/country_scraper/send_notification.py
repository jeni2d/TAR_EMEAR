import os
import pandas as pd
import pickle
# Gmail API utils
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
# for encoding/decoding messages in base64
from base64 import urlsafe_b64decode, urlsafe_b64encode
# for dealing with attachement MIME types
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from mimetypes import guess_type as guess_mime_type
from itemadapter import ItemAdapter
from scrapy.pipelines.images import FilesPipeline
from country_scraper.items import CountryScraperItem, CSVItem, RtffilesItem


# Request all access (permission to read/send/receive emails, manage the inbox, and more)
SCOPES = ['https://mail.google.com/']
our_email = 'notification.tar@gmail.com'

# karina.roslykh@here.com
responsibles = {'jaime.florence@here.com': ['Andorra', 'Gibraltar', 'Spain'],
                'stephan.geissler@here.com': ['Austria', 'Liechtenstein', 'Swiss'],
                'gregory.dhondt@here.com': ['Belgium'],
                'svend.storgaard@here.com': ['Denmark', 'Faroe'],
                'markus.gustafsson@here.com': ['Finland'],
                'yannick.room@here.com': ['France', 'Luxembourg', 'Monaco'],
                'christoph.rehberg@here.com': ['Germany'],
                'alison.hurst@here.com': ['Iceland', 'Ireland', 'UK'],
                'laura.minore@here.com': ['Italy', 'Malta', 'San Marino', 'Vatican City'],
                'patricia.van-eijk@here.com': ['Netherlands'],
                'arve.rygg@here.com': ['Norway'],
                'isolina.ribeiro@here.com': ['Portugal'],
                'johanna.forsberg@here.com': ['Sweden'],
                'shkelqim.brahimaj@here.com': ['Albania', 'Kosovo'],
                'evgeniy.denisov@here.com': ['Armenia', 'Azerbaijan', 'Belarus', 'Estonia', 'Georgia', 'Kazakhstan', 'Latvia', 'Lithuania', 'Russia', 'Ukraine', 'Uzbekistan'],
                'sinisa.miklauzic@here.com': ['Bosnia and Herzegovina', 'Croatia', 'Slovenia'],
                'ioannis.vlamidis@here.com': ['Cyprus', 'Greece', 'British Sovereign Base'],
                'radomir.cab@here.com': ['Czech', 'Slovakia'],
                'ervin.lehoczki@here.com': ['Hungary'],
                'omer.barsheshet@here.com': ['Israel'],
                'andrei.antonescu@here.com': ['Moldova', 'Romania'],
                'magdalena.bieniasz@here.com': ['Poland'],
                'khalid.bouhnak@here.com': ['Marocco', 'Egypt', 'Algeria', 'Libya', 'Tunisia'], 
                'muhammed.mahomed@here.com': ['Namibia', 'South Africa', 'Botswana', 'eSwatini', 'Lesotho'],
                'mohammad.abdulraheem@here.com': ['Oman', 'Qatar', 'UAE', 'Saudi Arabia', 'Kuwait'],
                'burak.akpak@here.com': ['Turkey', 'Turkish Republic of Northern Cyprus (Turkish Cypriot Administered area)']
            }



def gmail_authenticate():
    creds = None
    # the file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first time
    if os.path.exists(os.getcwd() + '/' + 'token.pickle'):
        with open(os.getcwd() + '/' 'token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # if there are no (valid) credentials availablle, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(os.getcwd() + '/' + 'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # save the credentials for the next run
        with open(os.getcwd() + '/' 'token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return build('gmail', 'v1', credentials=creds)

# get the Gmail API service
service = gmail_authenticate()

# Adds the attachment with the given filename to the given message
def add_attachment(message, filename):
    content_type, encoding = guess_mime_type(filename)
    if content_type is None or encoding is not None:
        content_type = 'application/octet-stream'
    main_type, sub_type = content_type.split('/', 1)
    if main_type == 'text':
        fp = open(filename, 'rb')
        msg = MIMEText(fp.read().decode(), _subtype=sub_type)
        fp.close()
    elif main_type == 'image':
        fp = open(filename, 'rb')
        msg = MIMEImage(fp.read(), _subtype=sub_type)
        fp.close()
    elif main_type == 'audio':
        fp = open(filename, 'rb')
        msg = MIMEAudio(fp.read(), _subtype=sub_type)
        fp.close()
    else:
        fp = open(filename, 'rb')
        msg = MIMEBase(main_type, sub_type)
        msg.set_payload(fp.read())
        fp.close()
    filename = os.path.basename(filename)
    msg.add_header('Content-Disposition', 'attachment', filename=filename)
    message.attach(msg)
    
def build_message(destination, obj, body, attachments=[]):
    if not attachments: # no attachments given
        message = MIMEText(body)
        message['to'] = destination
        message['from'] = our_email
        message['subject'] = obj
    else:
        message = MIMEMultipart()
        message['to'] = destination
        message['from'] = our_email
        message['subject'] = obj
        message.attach(MIMEText(body))
        for filename in attachments:
            add_attachment(message, filename)
    return {'raw': urlsafe_b64encode(message.as_bytes()).decode()}
    

def send_message(service, destination, obj, body, attachments=[]):
    return service.users().messages().send(
      userId="me",
      body=build_message(destination, obj, body, attachments)
    ).execute()
    


def send_note(item):
    # df = pd.read_csv('docs/tracking.csv', sep=',')


    send_message(service, [i for i, v in responsibles.items() if item['country'] in v][0], item['country'], 
            'Hi There', 
            [os.getcwd() + '/' + f"docs/{item['country']}" + '/' + item['file_name'] + '.csv']
            )

