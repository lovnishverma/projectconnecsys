import qrcode
import cv2
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageColor
from django.conf import settings


def add_text_to_image(image, text, position, font, font_color, center=True, x_offset=0):
    pil_image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(pil_image)
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]

    if center:
        x = (pil_image.width - text_width) // 2
    else:
        x = pil_image.width - text_width - 100

    x += x_offset
    y = position[1]

    draw.text((x, y), text, font=font, fill=font_color)
    return cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)


def write_text(Name, Issued_date, Certificate_no, TEMPLATE_PATH, name_attr):
    positions = [
        (0, 580),   # Name position (can change this value to modify name placement)
        (0, 785),   # Internship position (commented out, can modify if needed)
        (0, 2180),  # Certificate number position (change position for cert number)
        (0, 2180),  # Issue date position (can adjust for issue date placement)
    ]

    image = cv2.imread(TEMPLATE_PATH)

    if image is None:
        print(f"Failed to read image from path: {TEMPLATE_PATH}")
        return

    font_color = (0, 0, 0)
    font_path = os.path.join(settings.BASE_DIR, "static", "card", "MartianMono_SemiCondensed-Regular.ttf")
    times_roman_font_path = os.path.join(settings.BASE_DIR, "static", "card", "Times_New_Roman.ttf")

    if not os.path.exists(font_path) or not os.path.exists(times_roman_font_path):
        print("Font files missing. Ensure both fonts are available.")
        return

    name_font = None
    internship_font = None
    certificate_no_font = None
    Issued_date_font = None

    try:
        name_font_size = 131  # Name font size (can modify this if needed)
        internship_font_size = 35
        certificate_no_font_size = 32
        Issued_date_font_size = 32

        # Load fonts for different sections
        name_font = ImageFont.truetype(times_roman_font_path, size=name_font_size)
        internship_font = ImageFont.truetype(font_path, size=internship_font_size)
        certificate_no_font = ImageFont.truetype(font_path, size=certificate_no_font_size)
        Issued_date_font = ImageFont.truetype(font_path, size=Issued_date_font_size)
    except Exception as e:
        print(f"Error loading fonts: {e}")
        return

    try:
        # Candidate name in orange color using Times New Roman
        name_font_color = (255, 165, 0)  # Modify this color if needed
        x_offset = 100  # Modify to move name to the right/left if necessary
        image = add_text_to_image(image, Name, positions[0], name_font, name_font_color, x_offset=x_offset)
        x_offset = -520  # Modify x_offset for other elements like certificate number

    except Exception as e:
        print(f"Error adding text to image: {e}")
        return

    try:
        # Certificate number
        certificate_no_x_offset = x_offset + 20  # Shift right by 20 pixels
        image = add_text_to_image(image, f"{Certificate_no}", positions[2], certificate_no_font, font_color,
                                  center=False, x_offset=certificate_no_x_offset)

        # Issue date
        issue_date_x_offset = -2000  # Modify for different placement
        image = add_text_to_image(image, f"{Issued_date}", positions[3], Issued_date_font, font_color,
                                  center=False, x_offset=issue_date_x_offset)

    except Exception as e:
        print(f"Error adding certificate number: {e}")
        return

    try:
        certificate_directory = os.path.join(settings.MEDIA_ROOT, 'certificates')
        os.makedirs(certificate_directory, exist_ok=True)
        certificate_path = os.path.join(certificate_directory, f"{Name}_certificate.png")
        print(f"Saving certificate to path: {certificate_path}")
        cv2.imwrite(certificate_path, image)
    except Exception as e:
        print(f"Error saving certificate image: {e}")
        return


def write_qr(QR_PATH, Name):
    certificate_directory = os.path.join(settings.MEDIA_ROOT, 'certificates')
    os.makedirs(certificate_directory, exist_ok=True)
    certificate_path = os.path.join(certificate_directory, f"{Name}_certificate.png")
    print(f"Reading certificate from path: {certificate_path}")
    existing_image = cv2.imread(certificate_path)

    if existing_image is None:
        print(f"Failed to read existing certificate image from path: {certificate_path}")
        return

    profile_image = cv2.imread(QR_PATH)
    if profile_image is None:
        print(f"Failed to read QR image from path: {QR_PATH}")
        return

    pil_existing_image = Image.fromarray(cv2.cvtColor(existing_image, cv2.COLOR_BGR2RGB))

    custom_width = 250
    custom_height = 250
    profile_image_resized = cv2.resize(profile_image, (custom_width, custom_height))

    # x_start = 390  # Modify this if QR should appear in a different spot
    # y_start = 1620  # Modify this if QR should appear in a different spot
    x_start = 490  # Increased from 390 to 490 to move QR code to the right
    y_start = 1620  # Y-position stays the same, modify if you want to move QR vertically
    existing_image[y_start:y_start+custom_height, x_start:x_start+custom_width] = profile_image_resized

    cv_image_with_text = cv2.cvtColor(existing_image, cv2.COLOR_BGR2RGB)
    pil_image_with_text = Image.fromarray(cv_image_with_text)

    print(f"Saving updated certificate with QR to path: {certificate_path}")
    pil_image_with_text.save(certificate_path)


def generate_qr(qr_url, Registerdata):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(qr_url)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white")

    qr_code_directory = os.path.join(settings.MEDIA_ROOT, 'QR')
    os.makedirs(qr_code_directory, exist_ok=True)
    img_path = os.path.join(qr_code_directory, f"{Registerdata.Name}.png")
    print(f"Saving QR code to path: {img_path}")
    qr_img.save(img_path)
