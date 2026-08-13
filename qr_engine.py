import qrcode
from PIL import Image, ImageDraw
import os

# Resolve static dir relative to this file so it works on Render
_BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def generate_beautified_qr(business_id, business_name, category, custom_category=None):
    """
    Programmatically builds a marketing layout asset matching PRD Section 8.2 specifications.
    """
    # Visual Archetype configurations mapped precisely to PRD Section 8.2
    themes = {
        "Restaurant": {"bg": (194, 65, 12), "accent": (67, 20, 7), "tagline": "Rate Your Dining Experience!"}, # Warm Terracotta
        "Automobile": {"bg": (51, 65, 85), "accent": (249, 115, 22), "tagline": "Rate Our Mechanical Service!"}, # Charcoal + Safety Orange
        "Retail": {"bg": (244, 114, 182), "accent": (30, 41, 59), "tagline": "Rate Your Fashion Experience!"}, # Soft Blush + Charcoal
        "Salon": {"bg": (167, 139, 250), "accent": (124, 45, 18), "tagline": "Rate Your Relaxation Spa!"}, # Lavender + Rose Gold
        "Hospitality": {"bg": (23, 37, 84), "accent": (234, 179, 8), "tagline": "Rate Your Premium Stay!"} # Deep Navy + Gold
    }
    
    theme = themes.get(category, {"bg": (79, 70, 229), "accent": (49, 46, 129), "tagline": "We Value Your Feedback!"})
    display_category = custom_category if custom_category else category

    # Initialize A6 proportional physical printing boundaries
    card_width = 400
    card_height = 550
    card = Image.new("RGB", (card_width, card_height), color=(255, 255, 255))
    image_draw = ImageDraw.Draw(card)
    
    # Render upper category template frame block
    image_draw.rectangle([0, 0, card_width, 110], fill=theme["bg"])
    
    # Compile the target customer-facing entry endpoint parameters
    base_url = os.getenv("BASE_URL", "http://127.0.0.1:5000")
    customer_facing_url = f"{base_url}/review/{business_id}"
    
    # Configure QR matrix configurations
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=0,
    )
    qr.add_data(customer_facing_url)
    qr.make(fit=True)
    
    qr_img = qr.make_image(fill_color=theme["bg"], back_color="white").convert("RGB")
    qr_img = qr_img.resize((260, 260))
    
    # Insert QR into white canvas center grid position
    card.paste(qr_img, ((card_width - 260) // 2, 165))
    
    # Text overlays utilizing fallback structural canvas coordinates for clean output visibility
    # The default font doesn't support anchor="mm", so we calculate approximate width (approx 6px per char)
    def draw_centered_text(y_pos, text, fill_color):
        w = len(text) * 6
        image_draw.text((card_width // 2 - w // 2, y_pos), text, fill=fill_color)

    draw_centered_text(35, business_name.upper(), (255, 255, 255))
    draw_centered_text(70, "SCAN TO SHARE FEEDBACK", (255, 255, 255))
    
    # Render bottom footer presentation blocks
    image_draw.rectangle([0, card_height - 90, card_width, card_height], fill=(248, 250, 252))
    
    draw_centered_text(card_height - 60, theme["tagline"], theme["accent"])
    draw_centered_text(card_height - 30, f"Powered by ReviewFlow AI • {display_category}", (148, 163, 184))
    
    qr_dir = os.path.join(_BASE_DIR, "static", "qr_codes")
    os.makedirs(qr_dir, exist_ok=True)
    output_filename = os.path.join(qr_dir, f"tenant_{business_id}.png")
    card.save(output_filename, "PNG")
    # Return a relative path for use with Flask's url_for / static serving
    return f"static/qr_codes/tenant_{business_id}.png"