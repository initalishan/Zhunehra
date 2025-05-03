from PIL import Image, ImageDraw, ImageFont, ImageOps
import os

async def create_profile_card(photo, full_name, user_id):
    bg = Image.new("RGB", (1280, 720), "#1c1c1c")
    for y in range(720):
        gradient_color = int(28 + (46 - 28) * (y / 720))
        ImageDraw.Draw(bg).line([(0, y), (1280, y)], fill=(gradient_color, gradient_color, gradient_color))

    draw = ImageDraw.Draw(bg)

    font = ImageFont.truetype("fonts/TexgyreadventorBold-90Wn.otf", 48)

    pfp = Image.open(photo).resize((300, 300)).convert("RGBA")

    mask = Image.new("L", (300, 300), 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.ellipse((0, 0, 300, 300), fill=255)

    pfp_circle = ImageOps.fit(pfp, (300, 300), centering=(0.5, 0.5))
    pfp_circle.putalpha(mask)

    border_size = 8
    border = Image.new("RGBA", (300 + border_size * 2, 300 + border_size * 2), (255, 255, 255, 0))
    border_draw = ImageDraw.Draw(border)
    border_draw.ellipse((0, 0, border.size[0], border.size[1]), fill=(255, 255, 255, 255))
    border.paste(pfp_circle, (border_size, border_size), mask=pfp_circle)

    shadow = Image.new("RGBA", border.size, (0, 0, 0, 0))
    shadow_draw = ImageDraw.Draw(shadow)
    shadow_draw.ellipse((5, 5, border.size[0], border.size[1]), fill=(0, 0, 0, 100))

    pos_x = (1280 - border.size[0]) // 2
    pos_y = 80
    bg.paste(shadow, (pos_x, pos_y), shadow)
    bg.paste(border, (pos_x, pos_y), border)
    
    text_color = "white"
    name_text = f"{full_name}"
    id_text = f"ID: {user_id}"

    text_width_name = draw.textlength(name_text, font=font)
    text_width_id = draw.textlength(id_text, font=font)

    draw.text(((1280 - text_width_name) / 2, pos_y + 320), name_text, font=font, fill=text_color)
    draw.text(((1280 - text_width_id) / 2, pos_y + 380), id_text, font=font, fill=text_color)

    output = "config/profile_card.jpg"
    bg.save(output)
    return output
