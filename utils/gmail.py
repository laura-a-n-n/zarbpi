import imaplib
import email
import time
import socket
from email.header import decode_header
from itertools import chain
from config.main import settings

VERSION = 0.5

def poll_for_emails():
    print("Venmo thread running")

    imap_ssl_host = 'imap.gmail.com'
    username = settings['email_username']
    password = settings['email_password']

    criteria = {}
    uid_max = 0

    def search_string(uid_max, criteria):
        c = list(map(lambda t: (t[0], '"'+str(t[1])+'"'), criteria.items())) + [('UID', '%d:*' % (uid_max+1))]
        return '(%s)' % ' '.join(chain(*c))

    mail = imaplib.IMAP4_SSL(imap_ssl_host)
    mail.login(username, password)
    #select the folder
    mail.select('inbox')

    result, data = mail.uid('SEARCH', None, search_string(uid_max, criteria))
    uids = [int(s) for s in data[0].split()]
    if uids:
        uid_max = max(uids)
    mail.logout()

    print("Successfully authenticated to gmail")

    def process_message_contents(mail): 
        if "squambo" not in mail:
            if "From: Venmo <venmo@venmo.com>" not in mail:
                return False
            if "paid you $" not in mail:
                return False
        command = ".G"
        client_socket = socket.socket()
        client_socket.connect(("localhost", settings["socket_port"]))
        client_socket.send(bytes(command, encoding="utf8"))
        client_socket.close()

    while 1:
        mail = imaplib.IMAP4_SSL(imap_ssl_host)
        mail.login(username, password)
        mail.select('inbox')
        result, data = mail.uid('search', None, search_string(uid_max, criteria))
        uids = [int(s) for s in data[0].split()]

        for uid in uids:
            # Have to check again because Gmail sometimes does not obey UID criterion.
            if uid > uid_max:
                result, data = mail.uid('fetch', str(uid), '(RFC822)')
                for response_part in data:
                    if isinstance(response_part, tuple):
                        message_contents = email.message_from_bytes(response_part[1])
                        process_message_contents(str(message_contents))
                uid_max = uid
    mail.logout()
    time.sleep(1)

poll_for_emails()
