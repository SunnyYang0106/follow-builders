import os
import smtplib
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

SMTP_USER = os.environ.get("SMTP_USER")
SMTP_PASS = os.environ.get("SMTP_PASS")
TO_EMAIL = os.environ.get("TO_EMAIL")
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")

BUILDERS = [
    "Sam Altman", "Greg Brockman", "Andrej Karpathy",
    "Yann LeCun", "Demis Hassabis", "Dario Amodei",
    "Ilya Sutskever", "George Hotz", "Emad Mostaque"
]

def get_digest():
    today = datetime.now().strftime('%Y年%m月%d日')
    prompt = f"""今天是 {today}。

请总结以下 AI 领域重要人物最近的动态和新闻：
{', '.join(BUILDERS)}

格式要求：
- 每个人物单独一段
- 先用中文总结，再用英文总结
- 如果没有新动态就跳过
- 每人不超过100字"""

    response = requests.post(
        "https://api.anthropic.com/v1/messages",
        headers={
            "x-api-key": ANTHROPIC_API_KEY,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        },
        json={
            "model": "claude-haiku-4-5-20251001",
            "max_tokens": 2000,
            "messages": [{"role": "user", "content": prompt}]
        }
    )
    data = response.json()
    text = ""
    for block in data.get("content", []):
        if block.get("type") == "text":
            text += block.get("text", "")
      print("API响应:", data)
      return text

def send_email(content):
    today = datetime.now().strftime('%Y-%m-%d')
    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"🤖 AI Builders 每日动态 {today}"
    msg["From"] = SMTP_USER
    msg["To"] = TO_EMAIL

    body = f"""
<html><body>
<h2>🤖 AI Builders 每日动态 — {today}</h2>
<hr>
<pre style="font-family:sans-serif;font-size:15px;line-height:1.8">{content}</pre>
<hr>
<p style="color:gray;font-size:12px">由 GitHub Actions + Claude AI 自动生成</p>
</body></html>
"""
    msg.attach(MIMEText(body, "html"))
    with smtplib.SMTP_SSL("smtp.qq.com", 465) as server:
        server.login(SMTP_USER, SMTP_PASS)
        server.sendmail(SMTP_USER, TO_EMAIL, msg.as_string())
    print("邮件发送成功！")

if __name__ == "__main__":
    print("正在获取 AI Builders 动态...")
    content = get_digest()
    print(content)
    send_email(content)
