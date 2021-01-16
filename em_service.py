import yagmail
import keyring


def sendemail(subj, body):
    keyring.set_password('yagmail', 'sender email here', 'password for sender email')
    receiver = "dest email"
    yag = yagmail.SMTP("sender email here")
    yag.send(
    to=receiver,
    subject=subj,
    contents=body,
    )