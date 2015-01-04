from flask import current_app

def send_email():
    if current_app.config['EMAIL_METHOD'].lower() == "smtp":
        pass
    elif current_app.config['EMAIL_METHOD'].lower() == "mailgun":
        pass

def send_email_smtp():
    from auth import mail

def send_email_mailgun():
    import requests

    pass