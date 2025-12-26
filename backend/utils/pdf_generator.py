"""
PDF generation for physical emergency cards
"""
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from io import BytesIO
from typing import Dict
import qrcode


def generate_emergency_card_pdf(user_data: Dict, qr_data: str) -> bytes:
    """
    Generate a credit card-sized emergency card PDF
    
    Args:
        user_data: Dictionary containing user emergency information
        qr_data: URL or data to encode in QR code
    
    Returns:
        PDF as bytes
    """
    buffer = BytesIO()
    
    # Credit card size: 3.375" x 2.125"
    card_width = 3.375 * inch
    card_height = 2.125 * inch
    
    # Create PDF with custom page size
    c = canvas.Canvas(buffer, pagesize=(card_width, card_height))
    
    # Set up fonts and colors
    c.setFillColorRGB(0.8, 0, 0)  # Red color for header
    
    # Draw border
    c.setStrokeColorRGB(0, 0, 0)
    c.setLineWidth(2)
    c.rect(0.1*inch, 0.1*inch, card_width-0.2*inch, card_height-0.2*inch)
    
    # Generate QR code
    qr = qrcode.QRCode(version=1, box_size=10, border=2)
    qr.add_data(qr_data)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white")
    
    # Save QR to buffer
    qr_buffer = BytesIO()
    qr_img.save(qr_buffer, format='PNG')
    qr_buffer.seek(0)
    
    # Draw QR code on left side
    qr_size = 1.3 * inch
    c.drawImage(ImageReader(qr_buffer), 0.25*inch, 0.4*inch, 
                width=qr_size, height=qr_size)
    
    # Draw text information on right side
    text_x = 1.8 * inch
    
    # Header
    c.setFillColorRGB(0.8, 0, 0)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(text_x, 1.85*inch, "🚨 EMERGENCY CARD")
    
    # User information
    c.setFillColorRGB(0, 0, 0)
    c.setFont("Helvetica-Bold", 7)
    y_position = 1.6 * inch
    
    if user_data.get('name'):
        c.drawString(text_x, y_position, f"Name: {user_data['name']}")
        y_position -= 0.15 * inch
    
    if user_data.get('blood_group'):
        c.setFillColorRGB(0.8, 0, 0)
        c.drawString(text_x, y_position, f"Blood: {user_data['blood_group']}")
        y_position -= 0.15 * inch
        c.setFillColorRGB(0, 0, 0)
    
    if user_data.get('age'):
        c.drawString(text_x, y_position, f"Age: {user_data['age']}")
        y_position -= 0.15 * inch
    
    # Emergency contact
    c.setFont("Helvetica-Bold", 6)
    if user_data.get('emergency_contact'):
        c.drawString(text_x, y_position, "Emergency Contact:")
        y_position -= 0.12 * inch
        c.setFont("Helvetica", 6)
        c.drawString(text_x, y_position, user_data['emergency_contact']['name'])
        y_position -= 0.10 * inch
        c.drawString(text_x, y_position, user_data['emergency_contact']['phone'])
    
    # Footer text
    c.setFont("Helvetica", 5)
    c.setFillColorRGB(0.3, 0.3, 0.3)
    c.drawString(0.25*inch, 0.15*inch, "Scan QR for full medical details")
    
    c.save()
    buffer.seek(0)
    return buffer.getvalue()


def generate_full_page_card(user_data: Dict, qr_data: str) -> bytes:
    """
    Generate a full letter-sized page with emergency card
    (for easy printing and cutting)
    """
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    
    # Draw multiple cards on one page (for easy printing)
    # You can fit about 6 credit card sized cards on a letter page
    
    # For simplicity, we'll just center one large card
    page_width, page_height = letter
    
    # Center the card
    card_width = 4 * inch
    card_height = 2.5 * inch
    x = (page_width - card_width) / 2
    y = (page_height - card_height) / 2
    
    # Draw cut lines
    c.setDash(3, 3)
    c.setStrokeColorRGB(0.7, 0.7, 0.7)
    c.rect(x, y, card_width, card_height)
    
    # Similar content as above, scaled up
    # Generate QR code
    qr = qrcode.QRCode(version=1, box_size=10, border=2)
    qr.add_data(qr_data)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white")
    
    qr_buffer = BytesIO()
    qr_img.save(qr_buffer, format='PNG')
    qr_buffer.seek(0)
    
    # Draw QR code
    qr_size = 2 * inch
    c.drawImage(ImageReader(qr_buffer), x + 0.3*inch, y + 0.25*inch, 
                width=qr_size, height=qr_size)
    
    # Draw text
    text_x = x + 2.5 * inch
    c.setFillColorRGB(0.8, 0, 0)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(text_x, y + 2.2*inch, "🚨 EMERGENCY INFO CARD")
    
    c.setFillColorRGB(0, 0, 0)
    c.setFont("Helvetica-Bold", 10)
    y_pos = y + 1.8*inch
    
    if user_data.get('name'):
        c.drawString(text_x, y_pos, f"Name: {user_data['name']}")
        y_pos -= 0.2 * inch
    
    if user_data.get('blood_group'):
        c.setFillColorRGB(0.8, 0, 0)
        c.setFont("Helvetica-Bold", 12)
        c.drawString(text_x, y_pos, f"Blood Group: {user_data['blood_group']}")
        y_pos -= 0.25 * inch
        c.setFillColorRGB(0, 0, 0)
        c.setFont("Helvetica-Bold", 10)
    
    if user_data.get('age'):
        c.drawString(text_x, y_pos, f"Age: {user_data['age']}")
        y_pos -= 0.2 * inch
    
    if user_data.get('emergency_contact'):
        c.drawString(text_x, y_pos, "Emergency Contact:")
        y_pos -= 0.18 * inch
        c.setFont("Helvetica", 9)
        c.drawString(text_x, y_pos, f"{user_data['emergency_contact']['name']}")
        y_pos -= 0.15 * inch
        c.drawString(text_x, y_pos, f"{user_data['emergency_contact']['phone']}")
    
    # Instructions
    c.setFont("Helvetica-Bold", 8)
    c.setFillColorRGB(0.3, 0.3, 0.3)
    c.drawString(x + 0.3*inch, y - 0.3*inch, 
                 "Instructions: Cut along dotted line. Scan QR code for complete medical information.")
    
    c.save()
    buffer.seek(0)
    return buffer.getvalue()
