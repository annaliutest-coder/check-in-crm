import os
import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build


def get_gmail_service():
    """
    Get Gmail API service instance.
    Returns None if credentials are not configured.
    """
    client_id = os.getenv("GMAIL_CLIENT_ID")
    client_secret = os.getenv("GMAIL_CLIENT_SECRET")
    refresh_token = os.getenv("GMAIL_REFRESH_TOKEN")

    if not all([client_id, client_secret, refresh_token]):
        print("Gmail credentials not configured")
        return None

    credentials = Credentials(
        token=None,
        refresh_token=refresh_token,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=client_id,
        client_secret=client_secret,
    )

    return build("gmail", "v1", credentials=credentials)


async def send_email(
    to_email: str,
    subject: str,
    html_content: str,
    name: str | None = None
) -> bool:
    """
    Send an email using Gmail API.

    Args:
        to_email: Recipient email address
        subject: Email subject
        html_content: HTML content of the email
        name: Optional recipient name for plain text fallback

    Returns:
        True if email sent successfully, False otherwise
    """
    try:
        gmail_user = os.getenv("GMAIL_USER")
        service = get_gmail_service()

        if not service or not gmail_user:
            print("Gmail not configured, skipping email")
            return False

        greeting = f"親愛的 {name}" if name else "親愛的朋友"

        message = MIMEMultipart("alternative")
        message["to"] = to_email
        message["from"] = gmail_user
        message["subject"] = subject

        # Plain text fallback
        text_part = MIMEText(
            f"{greeting}，您好！\n\n此郵件包含 HTML 內容，請使用支援 HTML 的郵件客戶端查看。",
            "plain",
            "utf-8"
        )
        html_part = MIMEText(html_content, "html", "utf-8")

        message.attach(text_part)
        message.attach(html_part)

        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode("utf-8")

        service.users().messages().send(
            userId="me",
            body={"raw": raw_message}
        ).execute()

        print(f"Email sent successfully to {to_email}")
        return True

    except Exception as e:
        print(f"Failed to send email to {to_email}: {e}")
        return False


def get_welcome_email_template(name: str | None = None) -> str:
    """Generate welcome email HTML template."""
    greeting = f"親愛的 {name}" if name else "親愛的朋友"

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            body {{
                font-family: 'Microsoft JhengHei', Arial, sans-serif;
                line-height: 1.8;
                color: #333;
                max-width: 600px;
                margin: 0 auto;
                padding: 20px;
            }}
            .header {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 30px;
                text-align: center;
                border-radius: 10px 10px 0 0;
            }}
            .content {{
                background: #f9f9f9;
                padding: 30px;
                border-radius: 0 0 10px 10px;
            }}
            .button {{
                display: inline-block;
                background: #667eea;
                color: white;
                padding: 12px 30px;
                text-decoration: none;
                border-radius: 5px;
                margin-top: 20px;
            }}
            .footer {{
                text-align: center;
                margin-top: 20px;
                color: #666;
                font-size: 12px;
            }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>華語文教學系</h1>
            <h2>國際與文化組</h2>
        </div>
        <div class="content">
            <p>{greeting}，您好！</p>

            <p>感謝您對華語文教學系國際與文化組的關注與支持！</p>

            <p>我們很高興您今天參加了我們的活動。華語文教學系致力於培養優秀的華語教學人才，
            結合語言學、文化研究與教學方法，為學生提供全方位的學習體驗。</p>

            <p>如果您想了解更多關於我們系所的資訊，歡迎下載我們的簡介手冊：</p>

            <p style="text-align: center;">
                <a href="#" class="button">下載系所簡介 (PDF)</a>
            </p>

            <p>如有任何問題，歡迎隨時與我們聯繫！</p>

            <p>祝您學習愉快！</p>

            <p>華語文教學系 國際與文化組 敬上</p>
        </div>
        <div class="footer">
            <p>此郵件由系統自動發送，請勿直接回覆。</p>
        </div>
    </body>
    </html>
    """


async def send_welcome_email(to_email: str, name: str | None = None) -> bool:
    """
    Send a welcome email using Gmail API.

    Args:
        to_email: Recipient email address
        name: Optional recipient name

    Returns:
        True if email sent successfully, False otherwise
    """
    html_content = get_welcome_email_template(name)
    return await send_email(
        to_email=to_email,
        subject="華語文教學系國際與文化組歡迎您！",
        html_content=html_content,
        name=name
    )


def get_admission_notice_template(name: str | None = None, deadline: str = "") -> str:
    """Generate admission notice email HTML template."""
    greeting = f"親愛的 {name}" if name else "親愛的朋友"

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            body {{
                font-family: 'Microsoft JhengHei', Arial, sans-serif;
                line-height: 1.8;
                color: #333;
                max-width: 600px;
                margin: 0 auto;
                padding: 20px;
            }}
            .header {{
                background: linear-gradient(135deg, #10b981 0%, #059669 100%);
                color: white;
                padding: 30px;
                text-align: center;
                border-radius: 10px 10px 0 0;
            }}
            .content {{
                background: #f9f9f9;
                padding: 30px;
                border-radius: 0 0 10px 10px;
            }}
            .highlight {{
                background: #fef3c7;
                border-left: 4px solid #f59e0b;
                padding: 15px;
                margin: 20px 0;
            }}
            .button {{
                display: inline-block;
                background: #10b981;
                color: white;
                padding: 12px 30px;
                text-decoration: none;
                border-radius: 5px;
                margin-top: 20px;
            }}
            .footer {{
                text-align: center;
                margin-top: 20px;
                color: #666;
                font-size: 12px;
            }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>招生通知</h1>
            <h2>華語文教學系 國際與文化組</h2>
        </div>
        <div class="content">
            <p>{greeting}，您好！</p>

            <p>感謝您之前對華語文教學系的關注！我們很高興通知您：</p>

            <div class="highlight">
                <strong>招生申請現已開放！</strong>
                {f'<p>申請截止日期：{deadline}</p>' if deadline else ''}
            </div>

            <p>華語文教學系國際與文化組致力於培養具備跨文化溝通能力的華語教學專業人才。
            我們的課程結合理論與實務，讓您在學習中獲得豐富的教學經驗。</p>

            <p style="text-align: center;">
                <a href="#" class="button">立即申請</a>
            </p>

            <p>如有任何問題，歡迎與我們聯繫！</p>

            <p>華語文教學系 國際與文化組 敬上</p>
        </div>
        <div class="footer">
            <p>此郵件由系統自動發送，請勿直接回覆。</p>
            <p>如不想再收到此類通知，請點擊 <a href="#">取消訂閱</a></p>
        </div>
    </body>
    </html>
    """
