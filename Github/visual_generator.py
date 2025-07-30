import os
from PIL import Image, ImageDraw, ImageFont
import textwrap
import json

def wrap_text(text, font, max_width):
    lines = []
    if not text:
        return [""]
    for paragraph in text.split("\n"):
        line = []
        for word in paragraph.split():
            test_line = " ".join(line + [word])
            if font.getsize(test_line)[0] <= max_width:
                line.append(word)
            else:
                lines.append(" ".join(line))
                line = [word]
        lines.append(" ".join(line))
    return lines

def draw_section(draw, title, content, font_title, font_text, x, y, max_width, spacing=10):
    draw.text((x, y), title, font=font_title, fill="black")
    y += font_title.getsize(title)[1] + 5
    lines = wrap_text(content, font_text, max_width)
    for line in lines:
        draw.text((x, y), line, font=font_text, fill="black")
        y += font_text.getsize(line)[1] + spacing
    return y + spacing

def generate_visual_persona(username):
    data_path = f"Github/output/Script/{username}_github_profile.txt"
    if not os.path.exists(data_path):
        print(f"❌ Text profile not found at: {data_path}")
        return

    with open(data_path, "r", encoding="utf-8") as f:
        content = f.read()

    sections = {}
    current_title = None
    for line in content.splitlines():
        if line.strip().startswith("##"):
            current_title = line.strip().replace("##", "").strip()
            sections[current_title] = ""
        elif current_title:
            sections[current_title] += line.strip() + " "

    # Load fonts
    font_path = "arial.ttf"  # Adjust this to your system
    font_title = ImageFont.truetype(font_path, 28)
    font_text = ImageFont.truetype(font_path, 20)

    image_width = 1200
    max_text_width = image_width - 80
    y = 40

    # Estimate height
    total_height = 200
    for section in sections.values():
        lines = wrap_text(section, font_text, max_text_width)
        total_height += len(lines) * 30 + 60

    image = Image.new("RGB", (image_width, total_height), "white")
    draw = ImageDraw.Draw(image)

    # Draw title
    draw.text((40, y), f"GitHub Persona: {username}", font=font_title, fill="black")
    y += 60

    # Draw each section
    for title, content in sections.items():
        y = draw_section(draw, title, content.strip(), font_title, font_text, 40, y, max_text_width)

    # Save image
    os.makedirs(f"Github/output/Image", exist_ok=True)
    output_path = f"Github/output/Image/{username}_github_persona.png"
    image.save(output_path)
    print(f"✅ GitHub persona image saved to {output_path}")