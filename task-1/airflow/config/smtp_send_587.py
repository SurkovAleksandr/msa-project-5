import smtplib
from email.mime.text import MIMEText

SMTP_SERVER = "smtp.mail.ru"
SMTP_PORT = 587  # TLS порт
USERNAME = "alesur@bk.ru"
PASSWORD = "Ga2igqxHY16ykTg3YXeV"

sender_email = USERNAME
receiver_email = "surkov.jvm@gmail.com"

subject = "Test Email from Airflow Worker"
body = "Hello, this is a test email sent from Airflow worker using smtplib."

# Создаем email сообщение
msg = MIMEText(body, "plain")
msg["Subject"] = subject
msg["From"] = sender_email
msg["To"] = receiver_email

try:
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(USERNAME, PASSWORD)
        server.sendmail(sender_email, receiver_email, msg.as_string())
    print("Email sent successfully!")
except Exception as e:
    print(f"Failed to send email: {e}")
