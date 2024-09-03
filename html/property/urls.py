from django.contrib import admin
from django.urls import path, include
from glassbricks import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('logout/', views.user_logout, name='logout'),
    path('header/', views.header, name='header'),
    path('footer/', views.footer, name='footer'),
    path('submit-property/',views.submit_property ,name='submitproperty'),
    

    # Password reset URLs
    path('password_reset/', 
         auth_views.PasswordResetView.as_view(
             template_name='forgot-password.html',  # Use your custom template
             email_template_name='password_reset_email.txt',  # Custom email template
         ), 
         name='password_reset'),
    path('password_reset_done/', 
         auth_views.PasswordResetDoneView.as_view(
             template_name='password_reset_done.html'  # Ensure this template exists
         ), 
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(
             template_name='password_reset_confirm.html'  # Ensure this template exists
         ), 
         name='password_reset_confirm'),
    path('reset/done/', 
         auth_views.PasswordResetCompleteView.as_view(
             template_name='password_reset_complete.html'  # Ensure this template exists
         ), 
         name='password_reset_complete'),
    path('otp_verification/', views.otp_verification, name='otp_verification'),
    
    path('auth/', include('social_django.urls', namespace='social')),
    
   
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


