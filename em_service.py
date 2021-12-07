import yagmail
import keyring


def sendemail(email,subj, body):
    keyring.set_password('yagmail', 'aus.pcparts1@gmail.com', 'ihatedav1-')
    yag = yagmail.SMTP("aus.pcparts1@gmail.com")
    yag.send(
    to=email,
    subject=subj,
    contents=body,
    )