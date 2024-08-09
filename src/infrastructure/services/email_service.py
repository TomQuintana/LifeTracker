import smtplib


class EmailService:
    def __init__(self, user_email, password):
        self.email = user_email
        self.password = password

    def send(self, person):
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=self.email, password=self.password)
            connection.sendmail(from_addr=self.email, to_addrs=person, msg="Subject: Hello Tom")
