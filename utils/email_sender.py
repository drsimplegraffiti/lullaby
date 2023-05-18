import smtplib
from email.message import EmailMessage



def send_email(subject, to, html_content):
    email = EmailMessage()
    email['from'] = 'Abayomi Ogunnusi'
    email['to'] = to
    email['subject'] = subject

    email.set_content(html_content, 'html')

    with smtplib.SMTP(host='sandbox.smtp.mailtrap.io', port=587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.login('aaa5ecc1a6c063', 'd8179f9411ebda')
        smtp.send_message(email)
        print("Email sent successfully")

