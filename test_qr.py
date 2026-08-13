from PIL import Image, ImageDraw
try:
    card = Image.new("RGB", (400, 550), color=(255, 255, 255))
    image_draw = ImageDraw.Draw(card)
    image_draw.text((200, 35), "TEST", fill=(0, 0, 0), anchor="mm")
    print("Success")
except Exception as e:
    print(f"Error: {type(e).__name__}: {e}")
