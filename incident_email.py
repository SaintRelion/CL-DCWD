import smtplib
from email.message import EmailMessage

from database.db_users import get_all_tubero_emails


def send_incident_email(incident_details):
    recipients = get_all_tubero_emails()
    if not recipients:
        print("[Email] No recipients found. Skipping.")
        return

    # Extract details for easier access
    category = (
        incident_details.get("category", "General Incident").replace("_", " ").upper()
    )
    location = incident_details.get("location", "Unknown Location")
    priority = incident_details.get("priority", "Normal")
    lat = incident_details.get("latitude")
    lon = incident_details.get("longitude")
    raw_text = incident_details.get("raw_text", "No description provided.")

    # Create Google Maps Link if coordinates exist
    maps_link = ""
    if lat and lon:
        maps_link = f"https://www.google.com/maps/search/?api=1&query={lat},{lon}"

    msg = EmailMessage()
    msg["Subject"] = f"🚨 {priority} Alert: {category} at {location}"
    msg["From"] = "pyromaniac33143@gmail.com"
    msg["To"] = ", ".join(recipients)

    # Plain text fallback
    text_content = f"""
    ALERT: New Verified Incident
    ---------------------------
    Type: {category}
    Priority: {priority}
    Location: {location}
    Coordinates: {lat}, {lon}
    
    Description: "{raw_text}"
    
    Open in Google Maps: {maps_link}
    """

    # HTML Version for a professional look and clickable link
    html_content = f"""
    <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <h2 style="color: #d9534f;">🚨 New Incident Verified</h2>
            <p>A new report has been verified and requires attention.</p>
            <table style="width: 100%; border-collapse: collapse;">
                <tr>
                    <td style="padding: 8px; border: 1px solid #ddd; font-weight: bold; width: 30%;">Category:</td>
                    <td style="padding: 8px; border: 1px solid #ddd;">{category}</td>
                </tr>
                <tr>
                    <td style="padding: 8px; border: 1px solid #ddd; font-weight: bold;">Priority:</td>
                    <td style="padding: 8px; border: 1px solid #ddd; color: {'red' if priority == 'High Priority' else 'black'}; font-weight: bold;">{priority}</td>
                </tr>
                <tr>
                    <td style="padding: 8px; border: 1px solid #ddd; font-weight: bold;">Location:</td>
                    <td style="padding: 8px; border: 1px solid #ddd;">{location}</td>
                </tr>
            </table>
            
            <p><strong>Original Report:</strong><br>
            <i style="color: #555;">"{raw_text}"</i></p>
            
            <div style="margin-top: 20px;">
                <a href="{maps_link}" 
                   style="background-color: #0275d8; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; font-weight: bold;">
                   📍 View on Google Maps
                </a>
            </div>
            <br>
            <p style="font-size: 0.8em; color: #888;">This is an automated alert from the DCWD Incident Monitor.</p>
        </body>
    </html>
    """

    msg.set_content(text_content)
    msg.add_alternative(html_content, subtype="html")

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login("pyromaniac33143@gmail.com", "lgun rdsg lwye vfvd")
            server.send_message(msg)
            print(f"[Email] Alert sent to {len(recipients)} recipients.")
    except Exception as e:
        print(f"Failed to send email: {e}")
