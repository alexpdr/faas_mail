import logging
import json as JSON
import yagmail


def handle(req):
    """
    Takes a pre-defined JSON Request and parses contents to email

    {
        "receiver": "john@example.com",
        "subject": "Meeting next Tuesday",
        "content": [
            "One of many strings",
            "Two of Many strings",
            "...."
        ]
    }
    All values are strings.
    Content can be HTML in string form or plain-text
    """

    SECRETS_DIR: str = '/var/openfaas/secrets/'
    SECRET_USER: str = 'sendmail-username'
    SECRET_PASSWORD: str = 'sendmail-password'
    SECRET_SMTP: str = 'sendmail-smtp'

    USER: str
    PASSWORD: str
    SMTP_SERVER: str

    try:  # To retrieve SECRETS from storage
        with open(SECRETS_DIR+SECRET_USER, 'r') as file:
            USER = file.read().strip()
            logging.info(USER)
        with open(SECRETS_DIR+SECRET_PASSWORD, 'r') as file:
            PASSWORD = file.read().strip()
            logging.info(PASSWORD)
        with open(SECRETS_DIR+SECRET_SMTP, 'r') as file:
            SMTP_SERVER = file.read().strip()
            logging.info(SMTP_SERVER)
    except FileNotFoundError:
        logging.warning('Could not load SECRETS from storage')
        return JSON.dumps({
            'status': 500,
            'message': 'Internal Server Error'
        })

    try:  # To retrieve REQ variables
        data = JSON.loads(req)
        receiver = data['receiver']
        subject = data['subject']
        content = data['content']
    except KeyError:
        logging.warning('Could not load REQ variables')
        return JSON.dumps({
            'status': 500,
            'message': 'Internal Server Error, cannot load REQ variables'
        })
    except JSON.JSONDecodeError:
        logging.warning('Could not load REQ variables')
        return JSON.dumps({
            'status': 500,
            'message': 'Internal Server Error, cannot load REQ variables'
        })

    with yagmail.SMTP(USER, PASSWORD, SMTP_SERVER) as server:
        server.send(
            to=receiver,
            subject=subject,
            contents=content
        )  # Can later be extended to include attachments

    return JSON.dumps({
        'status': 200,
        'message': 'Function executed successfully'
    })
