# Expects a list of tuples of
# (sendas,sendat,to,cc,bcc,subject,text,attachments)
# sendat can be either datetime or string in emaildatefmt
# attachments are Path objects
# Each field can be a scalar or a list

from email.message import EmailMessage
import smtplib
import magic

emaildatefmt = '%a, %d %b %Y %H:%M:%S %z'
def uemail(msgs):
    for (sendas,sendat,to,cc,bcc,subject,msgtext,attachments) in msgs:

        msg = EmailMessage()
        msg['From'] = sendas
        if sendat: msg['Date'] = sendat if isinstance(sendat,str) else sendat.strftime(emaildatefmt)
        if to: msg['To'] = to
        if cc: msg['Cc'] = cc
        if bcc: msg['Bcc'] = bcc
        if subject: msg['Subject'] = subject

        #  unsure about this line, this was introduced when for a feed it was failing
        msg.set_content(msgtext.encode('utf-8','ignore'),maintype='text',subtype='plain')
        for a in attachments if isinstance(attachments,list) else [attachments]:
            maintype,subtype = magic.from_file(str(a),mime=True).split('/')
            with a.open('rb') as fp:
                msg.add_attachment(fp.read(),
                    maintype=maintype,
                    subtype=subtype,
                    filename=a.name)

        # Not sure whether keeping it open would work for how many emails
        s = smtplib.SMTP('localhost')
        try:
            s.send_message(msg)
        except Exception:
            print('Error sending: ',to,subject,E)
        s.quit()

