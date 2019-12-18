import os
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

    try:  # To retrieve ENV variables
        user: str = os.getenv('EMAIL_USERNAME')
        password: str = os.getenv('EMAIL_PASSWORD')
        smtp_server: str = os.getenv('EMAIL_SMTP')
    except KeyError:
        logging.warning('Could not load ENV variables')
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

    with yagmail.SMTP(user, password, smtp_server) as server:
        server.send(
            to=receiver,
            subject=subject,
            contents=content
        )  # Can later be extended to include attachments

    return JSON.dumps({
        'status': 200,
        'message': 'Function executed successfully'
    })
