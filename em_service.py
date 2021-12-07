import yagmail
import keyring


def sendemail(email,subj, body):
    keyring.set_password('yagmail', '', '')
    yag = yagmail.SMTP("")
    yag.send(
    to=email,
    subject=subj,
    contents=body,
    )