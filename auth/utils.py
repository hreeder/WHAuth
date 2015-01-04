from threading import Thread

from flask import current_app


def send_email(to, subject, text_body, html_body):
    if current_app.config['EMAIL_METHOD'].lower() == "smtp":
        send_email_smtp(to, subject, text_body, html_body)
    elif current_app.config['EMAIL_METHOD'].lower() == "mailgun":
        send_email_mailgun(to, subject, text_body, html_body)


def send_email_smtp_async(app, mail, msg):
    with app.app_context():
        mail.send(msg)


def send_email_smtp(to, subject, text_body, html_body):
    from auth import mail
    from flask.ext.mail import Message

    msg = Message(subject, recipients=to)
    msg.body = text_body
    msg.html = html_body

    thr = Thread(target=send_email_smtp_async, args=[current_app, mail, msg])
    thr.start()


def send_email_mailgun_async(app, data):
    import requests
    requests.post(
        app.config['MG_ENDPOINT'],
        auth=("api", current_app.config['MG_API']),
        data=data
    )


def send_email_mailgun(to, subject, text_body, html_body):
    data = {
        "from": current_app.config['MG_FROM'],
        "to": to,
        "subject": subject,
        "text": text_body,
        "html": html_body
    }

    thr = Thread(target=send_email_mailgun_async, args=[current_app, data])