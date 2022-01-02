import smtplib
import csv
from string import Template
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def read_template(filename):
    with open(filename, 'r', encoding='utf-8') as template_file:
        template_file_content = template_file.read()
        return Template(template_file_content)

from secrets import MY_ADDRESS
from secrets import PASSWORD

def main():
    message_template = read_template('templates/test_email_template.txt')
    # set up the SMTP server
    s = smtplib.SMTP(host='smtp.gmail.com', port=587)
    s.starttls()
    s.login(MY_ADDRESS, PASSWORD)

    with open("email-info/email_info.csv", "r") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        # the below statement will skip the first row
        next(csv_reader)
        
        for user in csv_reader:
            msg = MIMEMultipart() # create a message
            # add in the actual person name to the message template
            message = message_template.substitute(PERSON_NAME=user[0])
            #print(message)
            # setup the parameters of the message
            msg['From']=MY_ADDRESS
            msg['To']=user[1]
            msg['Subject']="Test Email"
            # add in the message body
            msg.attach(MIMEText(message, 'plain'))
            # send the message via the server set up earlier.
            s.send_message(msg)
            del msg
        
    # Terminate the SMTP session and close the connection
    s.quit()
if __name__ == '__main__':
 main()