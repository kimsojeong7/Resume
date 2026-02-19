import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(subject, body):
    sender_email = os.getenv("ALERT_EMAIL")
    sender_password = os.getenv("ALERT_PASSWORD")
    receiver_email = os.getenv("ALERT_RECEIVER")

    msg = MIMEMultipart()
    msg["From"] = "sj"
    msg["To"] = receiver_email
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()
        print("메일 전송 성공")
    except Exception as e:
        print("메일 전송 실패:", e)


if __name__ == "__main__":
    send_email(
        subject="🚨 Resume Repository Alert",
        body="Resume 저장소에서 에러 또는 로그 초과가 감지되었습니다."
    )
