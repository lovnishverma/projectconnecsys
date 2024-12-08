# myapp/urls.py

from django.urls import path
from django.contrib.auth.views import LogoutView

from .views import (signup_view, login_view, index_view, CustomLogoutView, import_certificates)

urlpatterns = [
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', LogoutView.as_view(next_page='index'), name='logout'),
    path('', index_view, name='index'),
    path('import-certificates/', import_certificates, name='import_certificates'),
]
