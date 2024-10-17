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
    
    path('property_admin_listing/', views.property_admin_listing, name='property_admin_listing'),
    path('property_admin/<int:property_id>', views.property_admin, name='property_admin'),

    path('footer/', views.footer, name='footer'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('update_profile_picture/', views.update_profile_picture, name='update_profile_picture'),
    path('submit_property/',views.submit_property ,name='submit_property'),
    path('update_profile/',views.update_profile ,name='update_profile'),
    path('profile/',views.profile ,name='profile'),
    path('property-listing/',views.property_listing ,name='property-listing'),
    path('property/<int:property_id>',views.property ,name='property'),
    path('property/<int:property_id>/pdf/', views.property_pdf, name='generate_property_pdf'),
    path('property/<int:property_id>/send_email/', views.send_property_pdf_via_email, name='send_property_pdf_via_email'),
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
    
    
    path('auth/', include('social_django.urls', namespace='social')),
    
   
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)