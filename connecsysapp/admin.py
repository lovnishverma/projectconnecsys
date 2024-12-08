import os
import pandas as pd
from PIL import Image
import qrcode
from django.contrib import admin, messages
from django.http import HttpResponse
from django.conf import settings
from .models import avrBootcampCertificates, CertificateAttributes
from .Card.GenerateCard import write_text, write_qr


def generate_certificates(modeladmin, request, queryset):
    # Template Path
    template_path = r"C:\Users\princ\Desktop\projectconnecsys\static\templates\fsp-avr-certificate.png"

    if not os.path.exists(template_path):
        modeladmin.message_user(request, "Template file does not exist.", level=messages.ERROR)
        return

    # Output Directory
    output_dir = os.path.join(settings.MEDIA_ROOT, 'certificates')
    os.makedirs(output_dir, exist_ok=True)

    # Fetch default attribute
    try:
        default_attr = CertificateAttributes.objects.get(attribute_name="defaultatt")
    except CertificateAttributes.DoesNotExist:
        modeladmin.message_user(request, "Default CertificateAttributes 'defaultatt' not found.", level=messages.ERROR)
        return

    for obj in queryset:
        try:
            # Skip invalid full_name
            if not obj.full_name or pd.isna(obj.full_name):
                modeladmin.message_user(request, f"Skipping invalid user: {obj.full_name}.", level=messages.WARNING)
                continue

            # Generate QR Code
            qr_content = (f"Name: {obj.full_name}\n"
              f"Father's Name: {obj.father_name}\n"
              f"Course Name: {obj.course_name}\n"
              f"From: {obj.start_date} To: {obj.end_date}\n"
              f"Email: {obj.email}\n"
              f"Issue Date: {obj.issue_date}\n"
              f"Certificate No.: {obj.cert_no}")

            qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
            qr.add_data(qr_content)
            qr.make(fit=True)
            qr_img = qr.make_image(fill_color="black", back_color="white")

            # Save QR Code Image
            qr_code_directory = os.path.join(settings.STATICFILES_DIRS[0], 'QR') if hasattr(settings, 'STATICFILES_DIRS') else os.path.join(settings.BASE_DIR, 'static', 'QR')
            os.makedirs(qr_code_directory, exist_ok=True)
            qr_image_path = os.path.join(qr_code_directory, f"{obj.full_name}.png")
            qr_img.save(qr_image_path)

            # Fetch Certificate Attributes or use default
            try:
                name_attr = CertificateAttributes.objects.filter(attribute_name=obj.full_name.strip()).first()
                if not name_attr:
                    name_attr = default_attr
            except Exception as e:
                modeladmin.message_user(request, f"Error fetching attributes for {obj.full_name}: {e}", level=messages.ERROR)
                continue

            # Fetch values from the model's attributes
            name_font_size = name_attr.font_size  # Use dynamic font size from model
            name_font_color = name_attr.font_color  # Use dynamic font color from model
            pos_x = name_attr.pos_x  # Use dynamic X position from model
            pos_y = name_attr.pos_y  # Use dynamic Y position from model
            x_offset = name_attr.x_offset  # Use dynamic X offset from model
            center = name_attr.center  # Use dynamic center alignment from model

            # Write Text and QR to Template
            try:
                write_text(obj.full_name, obj.issue_date, obj.cert_no, template_path, name_attr)
                write_qr(qr_image_path, obj.full_name)

                # Convert Certificate to PDF
                certificate_image_path = os.path.join(output_dir, f"{obj.full_name}_certificate.png")
                pdf_path = certificate_image_path.replace(".png", ".pdf")
                with Image.open(certificate_image_path) as img:
                    img.convert('RGB').save(pdf_path)

                # Update Certificate Path in the Model
                obj.certificate = f'certificates/{os.path.basename(pdf_path)}'
                obj.save()

            except Exception as e:
                modeladmin.message_user(request, f"Error while generating certificate for {obj.full_name}: {e}", level=messages.ERROR)

        except Exception as e:
            modeladmin.message_user(request, f"Error processing {obj.full_name}: {str(e)}", level=messages.ERROR)

    # Completion Message
    modeladmin.message_user(request, "Certificates generated successfully.", level=messages.SUCCESS)



# Export Internships to Excel Action
def export_user_internships_to_excel(modeladmin, request, queryset):
    data = list(queryset.values(
        'user__username', 'internship__name', 'batch__batch_date', 'full_name', 'email', 
        'start_date', 'batch_date', 'current_date', 'is_completed', 'offer_letter', 'certificate'
    ))
    df = pd.DataFrame(data)

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="user_internships.xlsx"'

    with pd.ExcelWriter(response, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='User Internships')

    return response


export_user_internships_to_excel.short_description = "Export selected User Certificates Details to Excel"


# Admin Classes
class avrCertificatesAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'start_date', 'end_date', 'certificate')
    search_fields = ('full_name', 'email')
    list_filter = ('start_date', 'end_date')
    ordering = ('start_date',)
    actions = [generate_certificates, export_user_internships_to_excel]


# class CertificateAttributesAdmin(admin.ModelAdmin):
#     list_display = ('attribute_name', 'pos_x', 'pos_y', 'x_offset', 'font_color', 'center')
#     search_fields = ('attribute_name',)


# Register Models
admin.site.register(avrBootcampCertificates, avrCertificatesAdmin)
# admin.site.register(CertificateAttributes, CertificateAttributesAdmin)