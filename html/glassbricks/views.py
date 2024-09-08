from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout, get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.urls import reverse
from .forms import SignUpForm, PasswordResetForm, PropertyForm
from .models import Property
import random
import os

# Function to send OTP via email
def send_otp(email):
    otp = str(random.randint(100000, 999999))  # Ensure OTP is a string for comparison
    subject = "Your OTP Code"
    message = f"Your OTP code is {otp}"
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email], fail_silently=False)
    return otp

# View for OTP verification
def otp_verification(request):
    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        stored_otp = request.session.get('otp')
        
        if entered_otp == stored_otp:
            user_data = request.session.get('user_data')
            if user_data:
                user = get_user_model().objects.create_user(
                    username=user_data['username'],
                    email=user_data['email'],
                    password=user_data['password'],
                )
                user.save()
                login(request, user)
                request.session.pop('otp', None)
                request.session.pop('user_data', None)
                return redirect('home')
        return render(request, 'otp_verification.html', {'error': 'Invalid OTP'})
    
    return render(request, 'otp_verification.html')

# View for user signup
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user_data = {
                'username': form.cleaned_data.get('username'),
                'email': form.cleaned_data.get('email'),
                'password': form.cleaned_data.get('password1'),
            }
            request.session['user_data'] = user_data
            otp = send_otp(user_data['email'])
            request.session['otp'] = otp
            return redirect('otp_verification')
        else:
            print(form.errors)  # Debugging; remove in production
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

# View for property submission
@login_required
def submit_property(request):
    if request.method == 'POST':
        property_form = PropertyForm(request.POST, request.FILES)
        
        if property_form.is_valid():
            property_instance = property_form.save(commit=False)
            property_instance.posted_by = request.user  # Automatically assign the current user
            
            # Handle multiple image uploads
            images = request.FILES.getlist('images')
            if images:
                print(f"Images uploaded: {[image.name for image in images]}")  # Debugging line
            else:
                print("No images uploaded")  # Debugging line

            image_paths = []
            for image in images:
                image_path = os.path.join('property_images', image.name)
                full_path = os.path.join(settings.MEDIA_ROOT, image_path)
                with open(full_path, 'wb+') as destination:
                    for chunk in image.chunks():
                        destination.write(chunk)
                image_paths.append(image_path)
            property_instance.images = ','.join(image_paths)

            # Handle multiple video uploads
            videos = request.FILES.getlist('videos')
            if videos:
                print(f"Videos uploaded: {[video.name for video in videos]}")  # Debugging line
            else:
                print("No videos uploaded")  # Debugging line

            video_paths = []
            for video in videos:
                video_path = os.path.join('property_videos', video.name)
                full_path = os.path.join(settings.MEDIA_ROOT, video_path)
                with open(full_path, 'wb+') as destination:
                    for chunk in video.chunks():
                        destination.write(chunk)
                video_paths.append(video_path)
            property_instance.videos = ','.join(video_paths)

            property_instance.save()
            return redirect('home')  # Redirect to a success page after saving
        else:
            # Print form errors for debugging
            print("Form errors:", property_form.errors)
            return render(request, 'submit-property.html', {
                'property_form': property_form,
                'form_errors': property_form.errors
            })
    else:
        property_form = PropertyForm()

    return render(request, 'submit-property.html', {
        'property_form': property_form,
    })

# View for the home page
def home(request):
    return render(request, 'index.html')

@login_required
def user_profile(request):
    return render(request, 'user-profile.html')

@login_required
def update_profile(request):
    return render(request, 'update-profile.html')

@login_required
def update_profile1(request):
    return render(request, 'update-profile-demo.html')

# View for the header
def header(request):
    return render(request, 'headerall.html')

# View for the footer
def footer(request):
    return render(request, 'footerdark.html')

# View for user signin
def signin(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                form.add_error(None, 'Invalid username or password')
        else:
            print(form.errors)
    else:
        form = AuthenticationForm()
    return render(request, 'signin.html', {'form': form})

# View for user logout
def user_logout(request):
    logout(request)
    return redirect('signin')

# View for forgot password
def forgot_password(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            User = get_user_model()
            associated_users = User.objects.filter(email=email)
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Request for Your Account"
                    uid = urlsafe_base64_encode(force_bytes(user.pk))
                    token = default_token_generator.make_token(user)
                    reset_url = request.build_absolute_uri(
                        reverse('password_reset_confirm', kwargs={'uidb64': uid, 'token': token})
                    )
                    context = {
                        'user': user,
                        'reset_url': reset_url,
                        'site_name': 'Glassbrix',
                    }
                    email_body = render_to_string('password_reset_email.txt', context)
                    try:
                        send_mail(
                            subject,
                            email_body,
                            settings.DEFAULT_FROM_EMAIL,
                            [user.email],
                            fail_silently=False,
                        )
                    except Exception as e:
                        print(f"Error sending email: {e}")
                return redirect('password_reset_done')
            else:
                return render(request, 'forgot-password.html', {
                    'form': form,
                    'error': 'No account found with this email address.'
                })
    else:
        form = PasswordResetForm()
    return render(request, 'forgot-password.html', {'form': form})