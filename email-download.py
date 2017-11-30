import csv
import smtplib
from random import randint
from datetime import datetime
from threading import Timer
from string import whitespace
from re import sub

import imaplib
import email
import email.parser
from HTMLParser import HTMLParser
import base64
import binascii

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

def extract_body(payload):
    if isinstance(payload,str):
        return payload
    else:
        return '\n'.join([extract_body(part.get_payload()) for part in payload])
def decode_base64(data):
    missing_padding = 4 - len(data) % 4
    if missing_padding:
        data += b'='* missing_padding
    return base64.decodestring(data)

positivephonenumbers = ['replace with phone numbers']


conn = imaplib.IMAP4_SSL("imap.gmail.com", 993)
conn.login('USERNAME', 'PASSWORD')
conn.select()
typ, data = conn.search(None, 'UNSEEN')
try:
    for num in data[0].split():
        typ, msg_data = conn.fetch(num, '(RFC822)')
        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_string(response_part[1])
                for part in msg.walk():
                    if part.get_content_type() == "text/plain":
                        body = part.get_payload(decode=True)
                        content_charset = msg.get_content_charset('utf8')
                        print body
                        text = body.decode(content_charset)
                subject=msg['subject']
                varFrom = msg['from']
                messagedate = msg['date']
                print(subject)
                payload=msg.get_payload()
                body=extract_body(payload)
                try:
                    body = base64.decodestring(body)
                except binascii.Error:
                    pass
                body3 = strip_tags(body)
                body3.encode("latin-1")
                print(varFrom)
                print(messagedate)
                try:
                    body3.translate(None, whitespace)
                    body4 = sub(r"(\s)+",' ',body3)
                    body4 = body4.replace("Original Message", "")
                    body4 = body4.replace("From", "")
                    body4 = body4.replace("_", "")
                    body4 = body4.replace("-", "")
                    body4 = body4.replace("www.", "")
                    body4 = body4.replace("==", "")
                    body4 = body4.replace("This mobile text message is brought to you by AT", "")
                    body4 = body4.replace("Thank you for using Picture and Video Messaging by U.S. Cellular. See uscellular.com for info.", "")
                    body4 = body4.replace("Subject", "")
                    body4 = body4.replace("Sent from my mobile.", "")
                    print body4
                    if varFrom in positivephonenumbers:
                        group = 'positive'
                    else:
                        group = 'neutral'
                    csvFile = open('data.csv','a')
                    csvWriter=csv.writer(csvFile)
                    for response_part in msg_data:
                        csvWriter.writerow([varFrom,body4,messagedate, group])
                    csvFile.close()
                except:
                    print "No new messages"
                pass
        typ, response = conn.store(num, '+FLAGS', r'(\Seen)')
finally:
    try:
        conn.close()
    except:
        pass
    conn.logout()



