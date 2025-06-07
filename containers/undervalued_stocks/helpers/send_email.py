import os
import smtplib
from email.message import EmailMessage

def send_simple_message(subject, body_html):
    msg = EmailMessage()
    msg.set_content("This email contains an HTML table of the top 5 mid cap tech growth stocks.")  # Plain text fallback
    msg.add_alternative(body_html, subtype='html')
    msg["Subject"] = subject
    msg["From"] = "syuraj@gmail.com"
    msg["To"] = "syuraj@gmail.com"

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login("syuraj@gmail.com", os.getenv('GAPP_PWD'))
        smtp.send_message(msg)

def send_styled_table_email(subject, dataframe, table_title="Data Table"):
    """Send email with professionally styled table from DataFrame"""

    # Create HTML table with inline styling for better email compatibility
    html_table = dataframe.to_html(
        index=False,
        border=1,
        table_id="growth-stocks",
        escape=False
    )

    # Add email-friendly styling with explicit borders
    styled_html = f"""
    <html>
    <body>
    <h2 style="color: #333; font-family: Arial, sans-serif;">{table_title}</h2>
    <table border="1" cellpadding="8" cellspacing="0" style="
        border-collapse: collapse;
        width: 100%;
        max-width: 800px;
        margin: 20px 0;
        font-family: Arial, sans-serif;
        font-size: 14px;
        border: 2px solid #009879;
    ">
        <thead>
            <tr style="background-color: #009879; color: white;">
    """

    # Add header cells with explicit borders
    for col in dataframe.columns:
        styled_html += f'<th style="border: 1px solid #fff; padding: 12px; text-align: left; font-weight: bold;">{col}</th>'

    styled_html += """
            </tr>
        </thead>
        <tbody>
    """

    # Add data rows with explicit borders
    for i, (_, row) in enumerate(dataframe.iterrows()):
        bg_color = "#f3f3f3" if i % 2 == 1 else "#ffffff"
        styled_html += f'<tr style="background-color: {bg_color};">'

        for j, value in enumerate(row):
            text_align = "left" if j == 0 else "right"  # First column left, others right
            styled_html += f'<td style="border: 1px solid #ddd; padding: 12px; text-align: {text_align};">{value}</td>'

        styled_html += '</tr>'

    styled_html += """
        </tbody>
    </table>
    </body>
    </html>
    """

    # Send email
    msg = EmailMessage()
    msg.set_content(f"This email contains a styled table: {table_title}")  # Plain text fallback
    msg.add_alternative(styled_html, subtype='html')
    msg["Subject"] = subject
    msg["From"] = "syuraj@gmail.com"
    msg["To"] = "syuraj@gmail.com"

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login("syuraj@gmail.com", os.getenv('GAPP_PWD'))
        smtp.send_message(msg)