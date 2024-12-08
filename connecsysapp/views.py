# myapp/views.py
import openpyxl
from django.contrib.auth import login, authenticate
from .forms import SignUpForm, LoginForm, ExcelUploadForm
from django.contrib.auth.views import LogoutView
from .models import avrBootcampCertificates
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse


def signup_view(request):
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            messages.success(
                request,
                'Signup successful! Notifications: {}'.format(
                    'Enabled' if form.cleaned_data.get('notifications') else 'Disabled'
                )
            )
            return redirect('index')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f'You are now logged in as {username}.')
                return redirect('index')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


class CustomLogoutView(LogoutView):
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


def index_view(request):
    return render(request, 'index.html')


def import_certificates(request):
    if request.method == 'POST' and request.FILES['excel_file']:
        excel_file = request.FILES['excel_file']
        wb = openpyxl.load_workbook(excel_file)
        sheet = wb.active

        # Skip the first row if it's the header row
        for row in sheet.iter_rows(min_row=2, values_only=True):
            full_name, father_name, course_name, email, start_date, end_date, issue_date, qr_url, cert_no, certificate_url, = row

            # Create a new certificate entry in the database
            avrBootcampCertificates.objects.create(
                full_name=full_name,
                father_name=father_name,
                course_name=course_name,
                email=email,
                start_date=start_date,
                end_date=end_date,
                issue_date=issue_date,
                qr_url=qr_url,  # This can be None or blank
                cert_no=cert_no,  # This can also be None or blank
                certificate=certificate_url
            )

        return HttpResponse("Excel file imported successfully.")

    form = ExcelUploadForm()
    return render(request, 'import_certificates.html', {'form': form})
