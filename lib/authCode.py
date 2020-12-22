import smtplib
import imaplib
import time
import email
import re
from .config import Config

config = Config()

class Getmail:
    def __init__(self):
        time.sleep(60)
        self.FROM_EMAIL  = config['gmail']['email']
        self.FROM_PWD    = config['gmail']['app_password']
        self.SMTP_SERVER = "imap.gmail.com"
        self.SMTP_PORT   = 993
        self.COND = [ 
                        ['"Facebook" <security@facebookmail.com>', 'Your Facebook Security Code'],
                        ['Microsoft account team <account-security-noreply@accountprotection.microsoft.com>', 'Microsoft account security code']
                    ]

    def send_mails(self):
        pass

    def get_mails(self, s):
        try:
            mail = imaplib.IMAP4_SSL(self.SMTP_SERVER)
            mail.login(self.FROM_EMAIL,self.FROM_PWD)
            mail.select('inbox')

            type, data = mail.search(None, 'ALL')
            mail_ids = data[0]

            id_list = mail_ids.split()   
            first_email_id = int(id_list[0])
            latest_email_id = int(id_list[-1])

    
            for i in range(latest_email_id,first_email_id, -1):
                typ, data = mail.fetch(str(i), "(RFC822)" )

                for response_part in data:
                    if isinstance(response_part, tuple):
                        msg = email.message_from_bytes(response_part[1])
                        if msg['From'] == self.COND[s][0] and msg['subject'] == self.COND[s][1]:
                            if msg.is_multipart():
                                for part in msg.walk():
                                    try:
                                        if part.get_content_type() == "text/html":
                                            hmsg = part.get_payload(decode=True).decode()
                                    except Exception as error:
                                        print(error)
                                
                                email_subject = msg['subject']
                                email_from = msg['from']
                        
                                print('From : ' + email_from + '\n')
                                print('Subject : ' + email_subject + '\n')
                                return str(re.findall(r">\d+<", hmsg)[0].strip("><"))

        except Exception as e:
            print(str(e))

    def get_code(self, meth):
        if meth == "facebook":
            code = self.get_mails(0)
        elif meth == "xbox":
            code = self.get_mails(1)

        return str(code)

