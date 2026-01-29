#!/usr/bin/env python3
"""
S-Urban Consultancy - Professional Business Profile PDF
Using actual branding: Dark charcoal/black with yellow/gold accents
Version 3: Fixed year to 2026, added Aadhar Equipments, improved client logos alignment, fixed contact page
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from PIL import Image
import os

# Get the directory where this script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGES_DIR = os.path.join(SCRIPT_DIR, 'images')

# Page dimensions
WIDTH, HEIGHT = A4

# Brand Colors - S-Urban Website Theme (Dark with Yellow)
DARK_BG = HexColor('#1a1a1a')         # Main dark background
DARKER_BG = HexColor('#000000')       # Pure black background
ACCENT_YELLOW = HexColor('#f5b041')   # Yellow/Gold accent
ACCENT_DARK_YELLOW = HexColor('#d4a534')  # Darker yellow
WHITE = HexColor('#ffffff')
LIGHT_GRAY = HexColor('#e5e5e5')
MID_GRAY = HexColor('#888888')
CARD_BG = HexColor('#252525')         # Card backgrounds

def draw_rounded_rect(c, x, y, width, height, radius, fill_color=None, stroke_color=None, stroke_width=1):
    """Draw a rounded rectangle"""
    c.saveState()
    if fill_color:
        c.setFillColor(fill_color)
    if stroke_color:
        c.setStrokeColor(stroke_color)
        c.setLineWidth(stroke_width)
    
    p = c.beginPath()
    p.moveTo(x + radius, y)
    p.lineTo(x + width - radius, y)
    p.arcTo(x + width - radius, y, x + width, y + radius, 90)
    p.lineTo(x + width, y + height - radius)
    p.arcTo(x + width - radius, y + height - radius, x + width, y + height, 0)
    p.lineTo(x + radius, y + height)
    p.arcTo(x, y + height - radius, x + radius, y + height, -90)
    p.lineTo(x, y + radius)
    p.arcTo(x, y, x + radius, y + radius, 180)
    p.close()
    
    if fill_color and stroke_color:
        c.drawPath(p, fill=1, stroke=1)
    elif fill_color:
        c.drawPath(p, fill=1, stroke=0)
    else:
        c.drawPath(p, fill=0, stroke=1)
    c.restoreState()

def draw_circular_image(c, img_path, x, y, diameter):
    """Draw an image clipped to a circle"""
    c.saveState()
    
    # Create circular clip path
    p = c.beginPath()
    p.circle(x + diameter/2, y + diameter/2, diameter/2)
    c.clipPath(p, stroke=0)
    
    # Draw image
    try:
        c.drawImage(img_path, x, y, width=diameter, height=diameter, preserveAspectRatio=True, mask='auto')
    except:
        # Fallback if image fails
        c.setFillColor(ACCENT_YELLOW)
        c.circle(x + diameter/2, y + diameter/2, diameter/2, fill=1, stroke=0)
    
    c.restoreState()
    
    # Draw border
    c.setStrokeColor(ACCENT_YELLOW)
    c.setLineWidth(3)
    c.circle(x + diameter/2, y + diameter/2, diameter/2, fill=0, stroke=1)

def draw_client_logo(c, img_path, x, y, width, height, name):
    """Draw a client logo centered in a white card"""
    # White background card
    c.setFillColor(WHITE)
    draw_rounded_rect(c, x, y, width, height, 4*mm, fill_color=WHITE)
    
    # Draw logo centered
    try:
        # Calculate padding for centering
        padding = 5*mm
        img_width = width - 2*padding
        img_height = height - 2*padding
        
        c.drawImage(img_path, x + padding, y + padding, 
                   width=img_width, height=img_height, 
                   preserveAspectRatio=True, mask='auto')
    except Exception as e:
        # Fallback text if image fails
        c.setFillColor(MID_GRAY)
        c.setFont("Helvetica-Bold", 9)
        c.drawCentredString(x + width/2, y + height/2 - 3*mm, name)

def draw_surban_logo(c, center_x, center_y, scale=1.0, dark_bg=True):
    """Draw the S-Urban logo at specified position and scale - pixel perfect version"""
    c.saveState()

    # Colors matching the logo exactly
    yellow = HexColor('#E8B829')  # Golden yellow
    gray_face = HexColor('#9E9E9E')  # Gray for face
    gray_handle = HexColor('#BDBDBD')  # Lighter gray for handles
    text_color = WHITE if dark_bg else HexColor('#1a1a1a')

    s = scale

    # === HELMET ===
    # Helmet dome (top part)
    c.setFillColor(yellow)
    c.setStrokeColor(yellow)
    c.setLineWidth(0)

    # Draw helmet dome as ellipse
    c.ellipse(center_x - 22*s, center_y + 58*s, center_x + 22*s, center_y + 78*s, fill=1, stroke=0)

    # Helmet middle band
    c.ellipse(center_x - 28*s, center_y + 52*s, center_x + 28*s, center_y + 62*s, fill=1, stroke=0)

    # Helmet brim (wider ellipse)
    c.ellipse(center_x - 38*s, center_y + 45*s, center_x + 38*s, center_y + 56*s, fill=1, stroke=0)

    # === FACE/HEAD ===
    c.setFillColor(gray_face)
    c.ellipse(center_x - 18*s, center_y + 28*s, center_x + 18*s, center_y + 52*s, fill=1, stroke=0)

    # === BODY (folder/torso shape) ===
    c.setFillColor(yellow)
    # Main body rectangle with rounded corners
    draw_rounded_rect(c, center_x - 40*s, center_y - 20*s, 80*s, 52*s, 8*s, fill_color=yellow)

    # Folder notch on top left
    c.setFillColor(yellow)
    c.setStrokeColor(HexColor('#1a1a1a') if dark_bg else HexColor('#333333'))
    c.setLineWidth(1.5*s)
    # Draw a small notch line
    c.line(center_x - 30*s, center_y + 32*s, center_x - 30*s, center_y + 22*s)
    c.line(center_x - 30*s, center_y + 22*s, center_x - 18*s, center_y + 22*s)

    # === HANDLES (on sides) ===
    c.setFillColor(gray_handle)
    # Left handle - rounded vertical rectangle
    draw_rounded_rect(c, center_x - 52*s, center_y - 5*s, 12*s, 30*s, 5*s, fill_color=gray_handle)
    # Right handle
    draw_rounded_rect(c, center_x + 40*s, center_y - 5*s, 12*s, 30*s, 5*s, fill_color=gray_handle)

    # === TEXT ===
    # "S-URBAN" - bold white text
    c.setFillColor(text_color)
    c.setFont("Helvetica-Bold", 20 * s)
    c.drawCentredString(center_x, center_y - 42*s, "S-URBAN")

    # "Consultancy" - regular white text
    c.setFillColor(text_color)
    c.setFont("Helvetica", 12 * s)
    c.drawCentredString(center_x, center_y - 56*s, "Consultancy")

    c.restoreState()

def create_profile_pdf(output_path):
    c = canvas.Canvas(output_path, pagesize=A4)
    
    # ==================== PAGE 1 - HERO COVER ====================
    
    # Full page dark background
    c.setFillColor(DARKER_BG)
    c.rect(0, 0, WIDTH, HEIGHT, fill=1, stroke=0)
    
    # Top accent bar (brown/maroon like website header)
    c.setFillColor(HexColor('#5d4037'))
    c.rect(0, HEIGHT - 6*mm, WIDTH, 6*mm, fill=1, stroke=0)
    
    # Decorative diagonal lines (subtle)
    c.setStrokeColor(ACCENT_YELLOW)
    c.setStrokeAlpha(0.1)
    c.setLineWidth(1)
    for i in range(8):
        c.line(WIDTH - 100 + i*15, HEIGHT, WIDTH - 50 + i*15, HEIGHT - 150)
    c.setStrokeAlpha(1)
    
    # Company Logo - use the logo image
    logo_path = os.path.join(IMAGES_DIR, 'logo_full.png')
    try:
        c.drawImage(logo_path, 25*mm, HEIGHT - 95*mm, width=60*mm, height=60*mm,
                   preserveAspectRatio=True, mask='auto')
    except:
        # Fallback to drawn logo
        draw_surban_logo(c, 55*mm, HEIGHT - 55*mm, scale=1.0, dark_bg=True)

    # Tagline
    c.setFillColor(MID_GRAY)
    c.setFont("Helvetica-Oblique", 12)
    c.drawString(30*mm, HEIGHT - 105*mm, "From Queries to Solutions")
    
    # Yellow accent line
    c.setFillColor(ACCENT_YELLOW)
    c.rect(30*mm, HEIGHT - 112*mm, 50*mm, 2*mm, fill=1, stroke=0)

    # Main Title
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 42)
    c.drawString(30*mm, HEIGHT - 145*mm, "BUSINESS")
    c.drawString(30*mm, HEIGHT - 163*mm, "PROFILE")
    
    # Year badge - Updated to 2026
    c.setFillColor(ACCENT_YELLOW)
    draw_rounded_rect(c, 30*mm, HEIGHT - 185*mm, 35*mm, 14*mm, 4*mm, fill_color=ACCENT_YELLOW)
    c.setFillColor(DARK_BG)
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(47.5*mm, HEIGHT - 180*mm, "2026")
    
    # PAN India Services tag
    c.setFillColor(CARD_BG)
    draw_rounded_rect(c, WIDTH - 80*mm, HEIGHT - 95*mm, 50*mm, 10*mm, 3*mm, fill_color=CARD_BG)
    c.setFillColor(ACCENT_YELLOW)
    c.setFont("Helvetica-Bold", 10)
    c.drawCentredString(WIDTH - 55*mm, HEIGHT - 91*mm, "PAN India Services")
    
    # Stats boxes at bottom
    stats = [
        ("8+", "Years", "Experience"),
        ("30+", "Projects", "Completed"),
        ("15+", "Happy", "Clients"),
        ("PAN", "India", "Coverage")
    ]
    
    box_width = 38*mm
    box_height = 42*mm
    start_x = 18*mm
    y_pos = 22*mm
    
    for i, (number, label1, label2) in enumerate(stats):
        x = start_x + i * (box_width + 6*mm)
        
        # Box background
        c.setFillColor(CARD_BG)
        draw_rounded_rect(c, x, y_pos, box_width, box_height, 5*mm, fill_color=CARD_BG)
        
        # Yellow accent on top
        c.setFillColor(ACCENT_YELLOW)
        c.rect(x + 8*mm, y_pos + box_height - 3*mm, 22*mm, 3*mm, fill=1, stroke=0)
        
        # Number
        c.setFillColor(ACCENT_YELLOW)
        c.setFont("Helvetica-Bold", 28)
        c.drawCentredString(x + box_width/2, y_pos + 22*mm, number)
        
        # Label
        c.setFillColor(WHITE)
        c.setFont("Helvetica", 10)
        c.drawCentredString(x + box_width/2, y_pos + 12*mm, label1)
        c.setFillColor(MID_GRAY)
        c.setFont("Helvetica", 9)
        c.drawCentredString(x + box_width/2, y_pos + 5*mm, label2)
    
    c.showPage()
    
    # ==================== PAGE 2 - ABOUT US ====================
    
    # Dark background
    c.setFillColor(DARKER_BG)
    c.rect(0, 0, WIDTH, HEIGHT, fill=1, stroke=0)
    
    # Top accent bar
    c.setFillColor(HexColor('#5d4037'))
    c.rect(0, HEIGHT - 6*mm, WIDTH, 6*mm, fill=1, stroke=0)
    
    # Section header
    c.setFillColor(ACCENT_YELLOW)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(30*mm, HEIGHT - 25*mm, "ABOUT US")
    
    # Yellow underline
    c.rect(30*mm, HEIGHT - 28*mm, 25*mm, 2*mm, fill=1, stroke=0)
    
    # Main title
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 26)
    c.drawString(30*mm, HEIGHT - 48*mm, "Building Excellence")
    c.drawString(30*mm, HEIGHT - 60*mm, "Through Expertise")
    
    # About text
    y_cursor = HEIGHT - 80*mm
    
    about_paragraphs = [
        "S-Urban Consultancy is an emerging Project Management Company driven by a robust workforce of Project Managers, Team Leaders, Engineers, and multi-skilled technical resources.",
        "At S-Urban, our governing principle is to maintain equality, diversity, and integrity in each project. We provide One Stop for Project Management Services with commitment to on-time delivery within budget.",
        "We specialize in managing Big Industrial Projects including RCC Buildings, PEB Sheds, Outside Developments, RCC Roads, Drainage, High-Rise Towers, Commercial Complexes, and Villas across South Gujarat, Daman & Diu, and Dadra & Nagar Haveli."
    ]
    
    c.setFillColor(LIGHT_GRAY)
    c.setFont("Helvetica", 11)
    
    for para in about_paragraphs:
        words = para.split()
        line = ""
        for word in words:
            test_line = line + " " + word if line else word
            if c.stringWidth(test_line, "Helvetica", 11) < 150*mm:
                line = test_line
            else:
                c.drawString(30*mm, y_cursor, line)
                y_cursor -= 6*mm
                line = word
        if line:
            c.drawString(30*mm, y_cursor, line)
            y_cursor -= 6*mm
        y_cursor -= 6*mm
    
    # Core Values section
    y_cursor = 90*mm
    
    c.setFillColor(ACCENT_YELLOW)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(30*mm, y_cursor + 10*mm, "CORE VALUES")
    c.rect(30*mm, y_cursor + 7*mm, 25*mm, 2*mm, fill=1, stroke=0)
    
    values = [
        ("Efficient Delivery", "On-time completion within budget"),
        ("Quality Focus", "Precision in every detail"),
        ("Client First", "Complete satisfaction guaranteed"),
        ("Innovation", "Advanced methods & technology")
    ]
    
    box_w = 75*mm
    box_h = 28*mm
    
    for i, (title, desc) in enumerate(values):
        x = 25*mm + (i % 2) * (box_w + 8*mm)
        y = y_cursor - 10*mm - (i // 2) * (box_h + 8*mm)
        
        # Card background
        c.setFillColor(CARD_BG)
        draw_rounded_rect(c, x, y - box_h, box_w, box_h, 4*mm, fill_color=CARD_BG)
        
        # Left yellow accent
        c.setFillColor(ACCENT_YELLOW)
        c.rect(x, y - box_h + 5*mm, 3*mm, box_h - 10*mm, fill=1, stroke=0)
        
        # Title
        c.setFillColor(WHITE)
        c.setFont("Helvetica-Bold", 12)
        c.drawString(x + 8*mm, y - 10*mm, title)
        
        # Description
        c.setFillColor(MID_GRAY)
        c.setFont("Helvetica", 10)
        c.drawString(x + 8*mm, y - 20*mm, desc)
    
    c.showPage()
    
    # ==================== PAGE 3 - SERVICES ====================
    
    # Dark background
    c.setFillColor(DARKER_BG)
    c.rect(0, 0, WIDTH, HEIGHT, fill=1, stroke=0)
    
    # Top accent
    c.setFillColor(HexColor('#5d4037'))
    c.rect(0, HEIGHT - 6*mm, WIDTH, 6*mm, fill=1, stroke=0)
    
    # Header
    c.setFillColor(ACCENT_YELLOW)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(30*mm, HEIGHT - 22*mm, "AREA OF EXPERTISE")
    c.rect(30*mm, HEIGHT - 25*mm, 35*mm, 2*mm, fill=1, stroke=0)
    
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 26)
    c.drawString(30*mm, HEIGHT - 42*mm, "Our Services")
    
    c.setFillColor(MID_GRAY)
    c.setFont("Helvetica", 12)
    c.drawString(30*mm, HEIGHT - 52*mm, "Comprehensive project management solutions")
    
    # Services grid
    services = [
        ("01", "Project Consultancy", [
            "Client objectives & constraints",
            "Strategic planning process",
            "Engineering deliverables",
            "Value engineering solutions"
        ]),
        ("02", "Project Management", [
            "Document control procedure",
            "Design deliverables",
            "Cost module & parameters",
            "Migration strategy"
        ]),
        ("03", "Planning Services", [
            "Planning packages",
            "Weekly/monthly reporting",
            "What-if analysis",
            "Recovery programs"
        ]),
        ("04", "Claim & Dispute", [
            "Site work survey",
            "Agreement analysis",
            "Mutual settlements",
            "Legal support"
        ]),
        ("05", "Risk Management", [
            "Risk identification",
            "Risk assessment",
            "Response planning",
            "Monitor & control"
        ]),
        ("06", "Quality Assurance", [
            "Quality control",
            "Performance verification",
            "Contract management",
            "Best practices audit"
        ])
    ]
    
    card_w = 80*mm
    card_h = 58*mm
    start_x = 17*mm
    start_y = HEIGHT - 70*mm
    
    for i, (num, title, bullets) in enumerate(services):
        col = i % 2
        row = i // 2
        
        x = start_x + col * (card_w + 8*mm)
        y = start_y - row * (card_h + 6*mm)
        
        # Card background
        c.setFillColor(CARD_BG)
        draw_rounded_rect(c, x, y - card_h, card_w, card_h, 5*mm, fill_color=CARD_BG)
        
        # Number badge
        c.setFillColor(ACCENT_YELLOW)
        draw_rounded_rect(c, x + 6*mm, y - 14*mm, 14*mm, 10*mm, 2*mm, fill_color=ACCENT_YELLOW)
        c.setFillColor(DARK_BG)
        c.setFont("Helvetica-Bold", 12)
        c.drawCentredString(x + 13*mm, y - 10*mm, num)
        
        # Title
        c.setFillColor(WHITE)
        c.setFont("Helvetica-Bold", 13)
        c.drawString(x + 24*mm, y - 11*mm, title)
        
        # Bullets
        c.setFont("Helvetica", 9)
        for j, bullet in enumerate(bullets):
            c.setFillColor(ACCENT_YELLOW)
            c.circle(x + 10*mm, y - 24*mm - j*8*mm, 1.5*mm, fill=1, stroke=0)
            c.setFillColor(LIGHT_GRAY)
            c.drawString(x + 14*mm, y - 26*mm - j*8*mm, bullet)
    
    c.showPage()
    
    # ==================== PAGE 4 - PROJECT LIFECYCLE ====================
    
    # Dark background
    c.setFillColor(DARKER_BG)
    c.rect(0, 0, WIDTH, HEIGHT, fill=1, stroke=0)
    
    # Top accent
    c.setFillColor(HexColor('#5d4037'))
    c.rect(0, HEIGHT - 6*mm, WIDTH, 6*mm, fill=1, stroke=0)
    
    # Header
    c.setFillColor(ACCENT_YELLOW)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(30*mm, HEIGHT - 22*mm, "OUR PROCESS")
    c.rect(30*mm, HEIGHT - 25*mm, 25*mm, 2*mm, fill=1, stroke=0)
    
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 26)
    c.drawString(30*mm, HEIGHT - 42*mm, "Project Lifecycle")
    
    c.setFillColor(MID_GRAY)
    c.setFont("Helvetica", 12)
    c.drawString(30*mm, HEIGHT - 52*mm, "S-Urban adds value throughout the complete lifecycle")
    
    # Timeline visualization
    phases = [
        ("01", "CONCEPT", "Identify needs,", "feasibility, master plans"),
        ("02", "PLANNING", "Architectural plans,", "BOQ, scheduling"),
        ("03", "EXECUTION", "Working drawings,", "contractor management"),
        ("04", "MONITORING", "Quality control,", "performance check"),
        ("05", "CLOSING", "Final reviews,", "handover, docs")
    ]
    
    timeline_y = HEIGHT - 100*mm
    phase_width = 32*mm
    
    # Draw connecting line
    c.setStrokeColor(ACCENT_YELLOW)
    c.setLineWidth(3)
    c.line(28*mm, timeline_y, WIDTH - 28*mm, timeline_y)
    
    for i, (num, title, desc1, desc2) in enumerate(phases):
        x = 22*mm + i * phase_width
        
        # Circle node
        c.setFillColor(ACCENT_YELLOW)
        c.circle(x + 14*mm, timeline_y, 10*mm, fill=1, stroke=0)
        
        # Number in circle
        c.setFillColor(DARK_BG)
        c.setFont("Helvetica-Bold", 12)
        c.drawCentredString(x + 14*mm, timeline_y - 3*mm, num)
        
        # Phase title
        c.setFillColor(WHITE)
        c.setFont("Helvetica-Bold", 10)
        c.drawCentredString(x + 14*mm, timeline_y - 18*mm, title)
        
        # Description
        c.setFillColor(MID_GRAY)
        c.setFont("Helvetica", 8)
        c.drawCentredString(x + 14*mm, timeline_y - 28*mm, desc1)
        c.drawCentredString(x + 14*mm, timeline_y - 35*mm, desc2)
    
    # Why Choose Us section
    y_cursor = HEIGHT - 165*mm

    c.setFillColor(ACCENT_YELLOW)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(30*mm, y_cursor, "WHY CHOOSE US")
    c.rect(30*mm, y_cursor - 3*mm, 30*mm, 2*mm, fill=1, stroke=0)

    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 22)
    c.drawString(30*mm, y_cursor - 18*mm, "What Sets Us Apart")

    y_cursor -= 35*mm

    reasons = [
        ("01", "We Are Creative", "Advanced technology and innovative methods developed through extensive project experience."),
        ("02", "Honest & Dependable", "Highly trained teams selected specifically for each client, solving problems creatively."),
        ("03", "Quality & Time", "Delivering quality work within the given time frame with full commitment."),
        ("04", "Always Improving", "Meeting today's needs without jeopardizing the world of tomorrow.")
    ]

    for i, (num, title, desc) in enumerate(reasons):
        y_box = y_cursor - i * 25*mm
        
        # Number badge
        c.setFillColor(ACCENT_YELLOW)
        draw_rounded_rect(c, 30*mm, y_box - 8*mm, 14*mm, 14*mm, 3*mm, fill_color=ACCENT_YELLOW)
        
        c.setFillColor(DARK_BG)
        c.setFont("Helvetica-Bold", 12)
        c.drawCentredString(37*mm, y_box - 3*mm, num)
        
        # Title
        c.setFillColor(WHITE)
        c.setFont("Helvetica-Bold", 13)
        c.drawString(50*mm, y_box, title)
        
        # Description
        c.setFillColor(MID_GRAY)
        c.setFont("Helvetica", 10)
        # Wrap text
        words = desc.split()
        line = ""
        y_text = y_box - 12*mm
        for word in words:
            test = line + " " + word if line else word
            if c.stringWidth(test, "Helvetica", 10) < 125*mm:
                line = test
            else:
                c.drawString(50*mm, y_text, line)
                y_text -= 5*mm
                line = word
        if line:
            c.drawString(50*mm, y_text, line)
    
    c.showPage()
    
    # ==================== PAGE 5 - CLIENTS ====================
    
    # Dark background
    c.setFillColor(DARKER_BG)
    c.rect(0, 0, WIDTH, HEIGHT, fill=1, stroke=0)
    
    # Top accent
    c.setFillColor(HexColor('#5d4037'))
    c.rect(0, HEIGHT - 6*mm, WIDTH, 6*mm, fill=1, stroke=0)
    
    # Header
    c.setFillColor(ACCENT_YELLOW)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(30*mm, HEIGHT - 22*mm, "TRUSTED BY")
    c.rect(30*mm, HEIGHT - 25*mm, 25*mm, 2*mm, fill=1, stroke=0)
    
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 26)
    c.drawString(30*mm, HEIGHT - 42*mm, "Our Clients")
    
    c.setFillColor(MID_GRAY)
    c.setFont("Helvetica", 12)
    c.drawString(30*mm, HEIGHT - 52*mm, "Partnering with leading organizations across India")
    
    # Client logos - 6 clients + "more" indicator
    clients = [
        (os.path.join(IMAGES_DIR, "param-infraspace.jpeg"), "PARAM Infraspace"),
        (os.path.join(IMAGES_DIR, "elleys.jpeg"), "Elleys"),
        (os.path.join(IMAGES_DIR, "v-trans.jpeg"), "V-Trans"),
        (os.path.join(IMAGES_DIR, "gamma-consultants.jpeg"), "1.5 Gamma Consultants"),
        (os.path.join(IMAGES_DIR, "loparex.jpeg"), "Loparex"),
        (os.path.join(IMAGES_DIR, "aadhar-equipments.jpeg"), "Aadhar Equipments")
    ]

    # Grid layout: 3 columns x 3 rows (6 logos + 1 "more" card)
    logo_w = 50*mm
    logo_h = 30*mm
    margin_x = 20*mm
    gap_x = 12*mm
    gap_y = 10*mm
    start_y = HEIGHT - 68*mm

    for i, (img_path, name) in enumerate(clients):
        col = i % 3
        row = i // 3

        x = margin_x + col * (logo_w + gap_x)
        y = start_y - row * (logo_h + gap_y)

        draw_client_logo(c, img_path, x, y - logo_h, logo_w, logo_h, name)

    # ==================== FOUNDER SECTION ====================

    founder_y = HEIGHT - 160*mm
    
    c.setFillColor(ACCENT_YELLOW)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(30*mm, founder_y, "LEADERSHIP")
    c.rect(30*mm, founder_y - 3*mm, 25*mm, 2*mm, fill=1, stroke=0)
    
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 22)
    c.drawString(30*mm, founder_y - 18*mm, "Meet Our Founder")
    
    # Founder card
    card_y = founder_y - 35*mm
    card_h = 80*mm
    
    c.setFillColor(CARD_BG)
    draw_rounded_rect(c, 25*mm, card_y - card_h, WIDTH - 50*mm, card_h, 6*mm, fill_color=CARD_BG)
    
    # Founder photo (circular)
    photo_diameter = 50*mm
    photo_x = 35*mm
    photo_y = card_y - card_h + 15*mm
    
    draw_circular_image(c, os.path.join(IMAGES_DIR, 'founder.jpeg'), photo_x, photo_y, photo_diameter)
    
    # Founder details
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 18)
    c.drawString(95*mm, card_y - 18*mm, "Suryakesh Kumar Singh")
    
    c.setFillColor(ACCENT_YELLOW)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(95*mm, card_y - 30*mm, "Civil Engineer (B.Tech) | Founder")
    
    c.setFillColor(LIGHT_GRAY)
    c.setFont("Helvetica", 9)
    
    founder_desc = "Over 8+ years of experience managing construction projects including Big Industrial Projects - RCC Building, PEB Sheds, Outside Developments, RCC Roads, Drainage, High-Rise Towers, Commercial Complexes, Villas."
    
    words = founder_desc.split()
    line = ""
    y_text = card_y - 45*mm
    for word in words:
        test = line + " " + word if line else word
        if c.stringWidth(test, "Helvetica", 9) < 85*mm:
            line = test
        else:
            c.drawString(95*mm, y_text, line)
            y_text -= 5*mm
            line = word
    if line:
        c.drawString(95*mm, y_text, line)
    
    # Stats
    founder_stats = [("8+", "Years"), ("30+", "Projects"), ("3", "Regions")]
    stat_y = card_y - 72*mm
    
    for i, (num, label) in enumerate(founder_stats):
        x = 95*mm + i * 30*mm
        
        c.setFillColor(ACCENT_YELLOW)
        c.setFont("Helvetica-Bold", 18)
        c.drawString(x, stat_y + 5*mm, num)
        
        c.setFillColor(MID_GRAY)
        c.setFont("Helvetica", 9)
        c.drawString(x, stat_y - 3*mm, label)
    
    c.showPage()
    
    # ==================== PAGE 6 - CONTACT (FIXED LAYOUT) ====================

    # Dark background
    c.setFillColor(DARKER_BG)
    c.rect(0, 0, WIDTH, HEIGHT, fill=1, stroke=0)

    # Top accent
    c.setFillColor(HexColor('#5d4037'))
    c.rect(0, HEIGHT - 6*mm, WIDTH, 6*mm, fill=1, stroke=0)

    # Header section
    c.setFillColor(ACCENT_YELLOW)
    c.setFont("Helvetica-Bold", 11)
    c.drawCentredString(WIDTH/2, HEIGHT - 25*mm, "GET IN TOUCH")

    # Yellow underline centered
    c.rect(WIDTH/2 - 20*mm, HEIGHT - 28*mm, 40*mm, 2*mm, fill=1, stroke=0)

    # Main title
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 28)
    c.drawCentredString(WIDTH/2, HEIGHT - 48*mm, "Let's Build Something Great")

    # Subtitle
    c.setFillColor(MID_GRAY)
    c.setFont("Helvetica", 12)
    c.drawCentredString(WIDTH/2, HEIGHT - 62*mm, "Ready to start your project? Contact us today for a consultation.")

    # Contact card - properly formatted
    card_x = 30*mm
    card_y = HEIGHT - 80*mm
    card_w = WIDTH - 60*mm
    card_h = 105*mm

    # Card background with rounded corners
    c.setFillColor(CARD_BG)
    draw_rounded_rect(c, card_x, card_y - card_h, card_w, card_h, 8*mm, fill_color=CARD_BG)

    # Yellow accent bar on left side of card
    c.setFillColor(ACCENT_YELLOW)
    c.rect(card_x, card_y - card_h + 12*mm, 4*mm, card_h - 24*mm, fill=1, stroke=0)

    # Content inside card
    content_x = card_x + 18*mm
    content_y = card_y - 12*mm

    # CONTACT PERSON
    c.setFillColor(ACCENT_YELLOW)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(content_x, content_y, "CONTACT PERSON")

    c.setFillColor(WHITE)
    c.setFont("Helvetica", 14)
    c.drawString(content_x, content_y - 10*mm, "Suryakesh Kumar Singh")

    # Row with PHONE and EMAIL
    row2_y = content_y - 28*mm

    c.setFillColor(ACCENT_YELLOW)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(content_x, row2_y, "PHONE")
    c.drawString(content_x + 70*mm, row2_y, "EMAIL")

    c.setFillColor(WHITE)
    c.setFont("Helvetica", 12)
    c.drawString(content_x, row2_y - 10*mm, "+91-7408703061")
    c.drawString(content_x + 70*mm, row2_y - 10*mm, "suryakesh422@gmail.com")

    # Row with ADDRESS and WEBSITE
    row3_y = content_y - 58*mm

    c.setFillColor(ACCENT_YELLOW)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(content_x, row3_y, "OFFICE ADDRESS")
    c.drawString(content_x + 70*mm, row3_y, "WEBSITE")

    c.setFillColor(WHITE)
    c.setFont("Helvetica", 10)
    c.drawString(content_x, row3_y - 10*mm, "Row House no: G-33, Shivay Bungalows")
    c.drawString(content_x, row3_y - 19*mm, "Poniya Road, Behind New Mamlatdar Office")
    c.drawString(content_x, row3_y - 28*mm, "Killa Pardi, Valsad, Gujarat - 396125")

    c.setFont("Helvetica", 12)
    c.drawString(content_x + 70*mm, row3_y - 10*mm, "s-urbanconsultancy.in")

    # Footer with logo - positioned below card with proper spacing
    logo_path = os.path.join(IMAGES_DIR, 'logo_full.png')
    try:
        logo_w = 45*mm
        logo_h = 45*mm
        c.drawImage(logo_path, WIDTH/2 - logo_w/2, 25*mm, width=logo_w, height=logo_h,
                   preserveAspectRatio=True, mask='auto')
    except:
        draw_surban_logo(c, WIDTH/2, 52*mm, scale=0.7, dark_bg=True)

    # Tagline at bottom
    c.setFillColor(MID_GRAY)
    c.setFont("Helvetica-Oblique", 11)
    c.drawCentredString(WIDTH/2, 15*mm, "From Queries to Solutions")
    
    c.save()
    print(f"PDF created successfully: {output_path}")

if __name__ == "__main__":
    output_path = os.path.join(SCRIPT_DIR, "S-Urban_Business_Profile.pdf")
    create_profile_pdf(output_path)
