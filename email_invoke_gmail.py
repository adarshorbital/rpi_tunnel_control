#!/usr/bin/env python3
"""
================================================================================
    Script Name:      email_invoke.py
    Description:      Sends automated notification when Boeing Wind Tunnel is powered on, to trusted point of contacts
    
    Author:           Adarsh Agrawal
    Organization:     Purdue University - School of Aeronautics and Astronautics
    Project:          Boeing Wind Tunnel Automation / Monitoring
    Created On:       30-May-2025
    Last Modified:    02-June-2025 by Adarsh Agrawal
    
    Usage:            This script is invoked when the RPi4 Model B detects a signal on its GPIO port 17. 
    
    Requirements:     - Python 3.x
                      - Runs on Raspberry Pi 4 Model B
    
    Notes:            - This script is triggered when the tunnel powers on.
                      - It sends a no-reply email via noreply-bwt-poweron@purdue.edu
                      - Ensure SMTP credentials and system permissions are configured properly.
    
    License:          Created for use by Purdue University, all rights reserved
================================================================================
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timezone


# Sender and recipients
sender_email = "adarsh.agrw@gmail.com"
relyto_email = "adarshagrl@yahoo.com"
recipient_emails = ["adarsh.agrw@gmail.com", "adarshagrl@hotmail.com", "agraw156@purdue.edu"]
app_password = "wtovzodorduafulk"  # Use your Gmail App Password

# Obtain date and time
now = datetime.now()
utc_now = datetime.now(timezone.utc)
tunnel_start_time = now.strftime("%Y-%m-%d %H:%M:%S")
utc_tunnel_start_time = utc_now.strftime("%Y-%m-%d %H:%M:%S")


# Email content
subject = "Boeing Wind Tunnel Powered On"
body = f"""
This is an automated notification from the Boeing Wind Tunnel at Purdue University, Aerospace Sciences Lab.

Status:           ✅ Wind Tunnel POWERED ON
Timestamp:        {tunnel_start_time} Eastern Standard Time
UTC Timestamp: 	  {utc_tunnel_start_time} Coordinated Universal Time

(Timestamp format: YYYY-MM-DD HH:mm:ss)

Please refer to the live camera feed to review the personnel using the tunnel at this time. 
1. For any questions about the wind tunnel, please contact: Tom Bietsch (tbietsch@purdue.edu).
2. For questions related to general programming, automation and LabVIEW, please contact: Adarsh Agrawal (agraw156@purdue.edu). 

Thank you

Best
Aerospace Sciences Lab
School of Aeronautics and Astronautics 
Purdue University
"""
# Create the email
message = MIMEMultipart()
message["From"] = "Boeing Wind Tunnel Notifier"
message["To"] = ", ".join(recipient_emails)  # Displayed in the email client
message["Reply-To"] = relyto_email
message["Subject"] = subject
message.attach(MIMEText(body, "plain"))

try:
    # Connect to Gmail SMTP server with TLS
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(sender_email, app_password)

    # Send email to all recipients
    server.sendmail(sender_email, recipient_emails, message.as_string())
    server.quit()
    print("Email sent successfully to the following contacts:\n")
    print(recipient_emails)
except Exception as e:
    print(f"Failed to send email: {e}")
