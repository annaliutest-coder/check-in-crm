"""
預設郵件範本
使用 {{name}} 作為收件人姓名佔位符
"""

TEMPLATES = {
    "welcome": {
        "name": "歡迎郵件",
        "subject": "華語文教學系國際與文化組歡迎您！",
        "html": """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body { font-family: 'Microsoft JhengHei', Arial, sans-serif; line-height: 1.8; color: #333; max-width: 600px; margin: 0 auto; padding: 20px; }
        .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }
        .content { background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }
        .button { display: inline-block; background: #667eea; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; margin-top: 20px; }
        .footer { text-align: center; margin-top: 20px; color: #666; font-size: 12px; }
    </style>
</head>
<body>
    <div class="header">
        <h1>華語文教學系</h1>
        <h2>國際與文化組</h2>
    </div>
    <div class="content">
        <p>親愛的 {{name}}，您好！</p>
        <p>感謝您對華語文教學系國際與文化組的關注與支持！</p>
        <p>我們很高興您參加了我們的活動。華語文教學系致力於培養優秀的華語教學人才，結合語言學、文化研究與教學方法，為學生提供全方位的學習體驗。</p>
        <p>如果您想了解更多關於我們系所的資訊，歡迎下載我們的簡介手冊：</p>
        <p style="text-align: center;">
            <a href="#" class="button">下載系所簡介 (PDF)</a>
        </p>
        <p>如有任何問題，歡迎隨時與我們聯繫！</p>
        <p>華語文教學系 國際與文化組 敬上</p>
    </div>
    <div class="footer">
        <p>此郵件由系統自動發送，請勿直接回覆。</p>
    </div>
</body>
</html>
"""
    },

    "admission_open": {
        "name": "招生申請開放通知",
        "subject": "【招生通知】華語文教學系國際與文化組招生申請已開放！",
        "html": """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body { font-family: 'Microsoft JhengHei', Arial, sans-serif; line-height: 1.8; color: #333; max-width: 600px; margin: 0 auto; padding: 20px; }
        .header { background: linear-gradient(135deg, #10b981 0%, #059669 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }
        .content { background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }
        .highlight { background: #fef3c7; border-left: 4px solid #f59e0b; padding: 15px; margin: 20px 0; }
        .button { display: inline-block; background: #10b981; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; margin-top: 20px; }
        .footer { text-align: center; margin-top: 20px; color: #666; font-size: 12px; }
    </style>
</head>
<body>
    <div class="header">
        <h1>招生通知</h1>
        <h2>華語文教學系 國際與文化組</h2>
    </div>
    <div class="content">
        <p>親愛的 {{name}}，您好！</p>
        <p>感謝您之前對華語文教學系的關注！我們很高興通知您：</p>
        <div class="highlight">
            <strong>🎉 招生申請現已開放！</strong>
            <p>請把握機會，儘早提交您的申請文件。</p>
        </div>
        <p>華語文教學系國際與文化組致力於培養具備跨文化溝通能力的華語教學專業人才。我們的課程結合理論與實務，讓您在學習中獲得豐富的教學經驗。</p>
        <p style="text-align: center;">
            <a href="#" class="button">立即申請</a>
        </p>
        <p>如有任何問題，歡迎與我們聯繫！</p>
        <p>華語文教學系 國際與文化組 敬上</p>
    </div>
    <div class="footer">
        <p>此郵件由系統自動發送，請勿直接回覆。</p>
    </div>
</body>
</html>
"""
    },

    "admission_reminder": {
        "name": "招生截止提醒",
        "subject": "【提醒】華語文教學系招生申請即將截止！",
        "html": """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body { font-family: 'Microsoft JhengHei', Arial, sans-serif; line-height: 1.8; color: #333; max-width: 600px; margin: 0 auto; padding: 20px; }
        .header { background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }
        .content { background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }
        .urgent { background: #fee2e2; border-left: 4px solid #ef4444; padding: 15px; margin: 20px 0; }
        .button { display: inline-block; background: #ef4444; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; margin-top: 20px; }
        .footer { text-align: center; margin-top: 20px; color: #666; font-size: 12px; }
    </style>
</head>
<body>
    <div class="header">
        <h1>⏰ 截止提醒</h1>
        <h2>華語文教學系 國際與文化組</h2>
    </div>
    <div class="content">
        <p>親愛的 {{name}}，您好！</p>
        <p>這是一封友善提醒：</p>
        <div class="urgent">
            <strong>⚠️ 招生申請即將截止！</strong>
            <p>如果您有意申請華語文教學系，請儘快完成申請程序。</p>
        </div>
        <p>別錯過這次機會！我們期待在新學期見到您。</p>
        <p style="text-align: center;">
            <a href="#" class="button">立即申請</a>
        </p>
        <p>華語文教學系 國際與文化組 敬上</p>
    </div>
    <div class="footer">
        <p>此郵件由系統自動發送，請勿直接回覆。</p>
    </div>
</body>
</html>
"""
    },

    "event_invitation": {
        "name": "活動邀請",
        "subject": "【邀請】華語文教學系活動邀請函",
        "html": """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body { font-family: 'Microsoft JhengHei', Arial, sans-serif; line-height: 1.8; color: #333; max-width: 600px; margin: 0 auto; padding: 20px; }
        .header { background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }
        .content { background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }
        .event-info { background: #ede9fe; border-radius: 8px; padding: 20px; margin: 20px 0; }
        .button { display: inline-block; background: #8b5cf6; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; margin-top: 20px; }
        .footer { text-align: center; margin-top: 20px; color: #666; font-size: 12px; }
    </style>
</head>
<body>
    <div class="header">
        <h1>活動邀請</h1>
        <h2>華語文教學系 國際與文化組</h2>
    </div>
    <div class="content">
        <p>親愛的 {{name}}，您好！</p>
        <p>誠摯邀請您參加我們即將舉辦的活動：</p>
        <div class="event-info">
            <p><strong>📅 活動名稱：</strong>（請填寫活動名稱）</p>
            <p><strong>📍 活動地點：</strong>（請填寫地點）</p>
            <p><strong>🕐 活動時間：</strong>（請填寫時間）</p>
        </div>
        <p>這是一個了解華語文教學系的絕佳機會，歡迎您的參與！</p>
        <p style="text-align: center;">
            <a href="#" class="button">報名參加</a>
        </p>
        <p>華語文教學系 國際與文化組 敬上</p>
    </div>
    <div class="footer">
        <p>此郵件由系統自動發送，請勿直接回覆。</p>
    </div>
</body>
</html>
"""
    },

    "custom": {
        "name": "自訂郵件",
        "subject": "",
        "html": """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body { font-family: 'Microsoft JhengHei', Arial, sans-serif; line-height: 1.8; color: #333; max-width: 600px; margin: 0 auto; padding: 20px; }
        .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }
        .content { background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }
        .footer { text-align: center; margin-top: 20px; color: #666; font-size: 12px; }
    </style>
</head>
<body>
    <div class="header">
        <h1>華語文教學系</h1>
        <h2>國際與文化組</h2>
    </div>
    <div class="content">
        <p>親愛的 {{name}}，您好！</p>
        <p>（請在此輸入您的郵件內容）</p>
        <p>華語文教學系 國際與文化組 敬上</p>
    </div>
    <div class="footer">
        <p>此郵件由系統自動發送，請勿直接回覆。</p>
    </div>
</body>
</html>
"""
    }
}


def get_template(template_id: str) -> dict | None:
    """Get a template by ID."""
    return TEMPLATES.get(template_id)


def get_all_templates() -> list[dict]:
    """Get all available templates."""
    return [
        {"id": tid, "name": t["name"], "subject": t["subject"]}
        for tid, t in TEMPLATES.items()
    ]
