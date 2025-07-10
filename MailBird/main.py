import os
import smtplib
from email.message import EmailMessage

# -------------------- CONFIG --------------------
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
SENDER_EMAIL = 'your gmail address here'
SENDER_PASSWORD = 'your app password here not gmail password'
MAILS_DIR = 'mails'
# ------------------------------------------------

def list_templates():
    templates = [f for f in os.listdir(MAILS_DIR) if f.endswith('.html')]
    print("\nAvailable templates:")
    for i, name in enumerate(templates):
        print(f"{i + 1}. {name}")
    return templates

def main():
    recipient = input("Enter recipient email: ").strip()
    subject = input("Enter email subject: ").strip()

    templates = list_templates()
    choice = input(f"Choose template [1-{len(templates)}]: ").strip()

    try:
        template_file = templates[int(choice) - 1]
    except (ValueError, IndexError):
        print("❌ Invalid choice.")
        return

    with open(os.path.join(MAILS_DIR, template_file), 'r', encoding='utf-8') as f:
        html_content = f.read()

    msg = EmailMessage()
    msg['From'] = SENDER_EMAIL
    msg['To'] = recipient
    msg['Subject'] = subject
    msg.set_content("This is a plain text fallback.")
    msg.add_alternative(html_content, subtype='html')

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as smtp:
            smtp.starttls()
            smtp.login(SENDER_EMAIL, SENDER_PASSWORD)
            smtp.send_message(msg)
            print(f"\n✅ Email sent to {recipient} using {template_file}")
    except Exception as e:
        print("\n❌ Failed to send email:", e)

if __name__ == "__main__":
    main()
