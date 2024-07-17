from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

APP_NAME = 'Administrador de incapacidades'

admin.site.site_header = APP_NAME
admin.site.site_title = APP_NAME
admin.site.index_title = APP_NAME

urlpatterns = [
    # Incapacidades App
    path('', include('incapacidades.urls')),

    path('login/', auth_views.LoginView.as_view(template_name='login.html')),
    path('logout/', auth_views.LogoutView.as_view(next_page='/')),
    path('admin/', admin.site.urls),
]
