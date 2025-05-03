from PIL import Image, ImageDraw, ImageFont, ImageFilter
from textwrap import wrap
from os import remove

async def Thumbnail(thumb_path, title, artist, duration):
    bg = Image.open(thumb_path).convert("RGBA").resize((1280, 720), Image.LANCZOS)
    blurred_bg = bg.filter(ImageFilter.GaussianBlur(radius=6))
    overlay = Image.new("RGBA", blurred_bg.size, (0, 0, 0, 100))
    blurred_bg = Image.alpha_composite(blurred_bg, overlay)
    card_w, card_h = 460, 230
    card = Image.new("RGBA", (card_w, card_h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(card)
    draw.rounded_rectangle([(0, 0), (card_w, card_h)], radius=30, fill=(30, 30, 30, 200))
    thumb = Image.open(thumb_path).convert("RGBA").resize((120, 120), Image.LANCZOS)
    mask = Image.new('L', thumb.size, 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.rounded_rectangle([0, 0, 120, 120], radius=20, fill=255)
    thumb.putalpha(mask)
    card.paste(thumb, (20, 20), thumb)
    title_font = ImageFont.truetype("fonts/TexgyreadventorBold-90Wn.otf", 20)
    artist_font = ImageFont.truetype("fonts/PoppinsRegular.otf", 17)
    small_font = ImageFont.truetype("fonts/PoppinsRegular.otf", 16)
    zhunehra_font = ImageFont.truetype("fonts/PoppinsRegular.otf", 18)
    draw.text((160, 20), "Zhunehra", font=zhunehra_font, fill="white")
    wrapped_title = wrap(title, width=26)[:2]
    for i, line in enumerate(wrapped_title):
        draw.text((160, 40 + i * 20), line, font=title_font, fill="white")
    draw.text((160, 90), artist, font=artist_font, fill=(255, 255, 255, 160))
    bar_y = 120
    bar_start = 160
    bar_end = card_w - 30
    draw.line([(bar_start, bar_y), (bar_end, bar_y)], fill="white", width=2)
    draw.text((bar_start, bar_y + 6), "0:00", font=small_font, fill="white")
    draw.text((bar_end - 35, bar_y + 6), duration, font=small_font, fill="white")
    btn_y = bar_y + 60
    btn_size = 16
    gap = 50
    center_x = (bar_start + bar_end) // 2
    prev_x = center_x - gap - btn_size - 10
    draw.polygon([
        (prev_x, btn_y),
        (prev_x + btn_size, btn_y - btn_size),
        (prev_x + btn_size, btn_y + btn_size)
    ], fill="white")
    draw.rectangle([(center_x - 8, btn_y - btn_size), (center_x - 2, btn_y + btn_size)], fill="white")
    draw.rectangle([(center_x + 2, btn_y - btn_size), (center_x + 8, btn_y + btn_size)], fill="white")
    next_x = center_x + gap + 10
    draw.polygon([
        (next_x, btn_y - btn_size),
        (next_x, btn_y + btn_size),
        (next_x + btn_size, btn_y)
    ], fill="white")
    final = blurred_bg.copy()
    final.paste(card, ((1280 - card_w) // 2, (720 - card_h) // 2), card)
    output_path = thumb_path.replace(".png", "_final.png")
    final.save(output_path, format="PNG")
    remove(thumb_path)
    return output_path