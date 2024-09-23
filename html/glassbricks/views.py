from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout, get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail, EmailMessage
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string, get_template
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import HttpResponse
from xhtml2pdf import pisa
from django.urls import reverse
from .forms import SignUpForm, PasswordResetForm, PropertyForm, PropertyImageForm, PropertyVideoForm, PropertyFloorPlanForm
from .models import Property, PropertyImage, PropertyVideo, PropertyFloorPlan
import random
import os
from io import BytesIO


def property_pdf(request, property_id):
    property_obj = get_object_or_404(Property, id=property_id)
    template = get_template('property_pdf_template.html')
    html = template.render({'property': property_obj})

    # Generate PDF from HTML
    pdf_file = BytesIO()
    HTML(string=html).write_pdf(pdf_file)

    # Create HTTP response
    response = HttpResponse(pdf_file.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="property_{property_id}.pdf"'
    return response

def send_property_pdf_via_email(request, property_id):
    property_instance = get_object_or_404(Property, id=property_id)
    template = render_to_string('property_pdf_template.html', {'property': property_instance})

    buffer = BytesIO()
    pisa_status = pisa.CreatePDF(template, dest=buffer)

    

    # If there is an error in creating the PDF
    if pisa_status.err:
        return HttpResponse('Error generating PDF')

    # Prepare the email
    email = EmailMessage(
        'Property Details',
        'Please find attached the property details.',
        'shreyashshinde2608@gmail.com',
        ['shreyashshindejj@gmail.com'],
    )
    
    email.attach(f'property_{property_instance.id}.pdf', buffer.getvalue(), 'application/pdf')
    email.send()
    
    return HttpResponse('Email Sent Successfully')

# View for user signup
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save the new user to the database
            
            # Authenticate the user to get the backend and login
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)

            # If the user is authenticated, log them in with the correct backend
            if user is not None:
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                return redirect('home')
        else:
            print(form.errors)  # Debugging; remove in production
    else:
        form = SignUpForm()

    return render(request, 'signup.html', {'form': form})

# View for property submission

def submit_property(request):
    if request.method == 'POST':
        property_form = PropertyForm(request.POST, request.FILES)
        
        if property_form.is_valid():
            property_instance = property_form.save(commit=False)
            property_instance.posted_by = request.user  # Automatically assign the current user
            property_instance.save()
            # Handle multiple image uploads
            images = request.FILES.getlist('images')
            if images:
                print(f"Images uploaded: {[image.name for image in images]}")  # Debugging line
            else:
                print("No images uploaded")  # Debugging line

            for image in images:
                PropertyImage.objects.create(property=property_instance, image=image)
            
            
            floor_plans = request.FILES.getlist('floor_plans')
            if images:
                print(f"Images uploaded: {[image.name for image in images]}")  # Debugging line
            else:
                print("No images uploaded")  # Debugging line
            for floor_plan in floor_plans:
                PropertyFloorPlan.objects.create(property=property_instance, floor_plan=floor_plan)

            # Handle multiple video uploads
            videos = request.FILES.getlist('videos')
            if videos:
                print(f"Videos uploaded: {[video.name for video in videos]}")  # Debugging line
            else:
                print("No videos uploaded")  # Debugging line

            for video in videos:
                PropertyVideo.objects.create(property=property_instance, video=video)

            
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




def contact(request):
    return render(request, 'contact-2.html')

def about(request):
    return render(request, 'about-us.html')

def property(request,property_id):
    property_instance = get_object_or_404(Property,id=property_id)
    images = PropertyImage.objects.filter(property=property_instance)  # Fetch related images
    videos = PropertyVideo.objects.filter(property=property_instance)  # Fetch related videos
    features = {
        'security': property_instance.security,
        'ac': property_instance.ac,
        'club': property_instance.club,
        'elevator': property_instance.elevator,
        'pool': property_instance.pool,
        'wifi': property_instance.wifi,
        'parking': property_instance.parking,
        'gym': property_instance.gym,
        'powerbackup': property_instance.powerbackup,
        
    }
    context = {
        'property': property_instance,
        'images': images,
        'videos': videos,
        'features': features,
    }
    return render(request, 'property.html',context)


@login_required
def update_profile(request):
    return render(request, 'update-profile.html')



def property_listing(request):
    # Get filter values from GET request
    status = request.GET.get('status')
    property_type = request.GET.get('property_type')
    location = request.GET.get('location')
    max_rooms = request.GET.get('max_rooms')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    min_area = request.GET.get('min_area')
    max_area = request.GET.get('max_area')

    # Filter properties based on the inputs
    properties = Property.objects.all()

    if status:
        properties = properties.filter(status=status)
    if property_type:
        properties = properties.filter(property_type=property_type)
    if location:
        properties = properties.filter(city__icontains=location)  # Assuming 'city' is the column name for location
    if max_rooms:
        properties = properties.filter(rooms__lte=max_rooms)
    if min_price and max_price:
        properties = properties.filter(price__gte=min_price, price__lte=max_price)
    if min_area and max_area:
        properties = properties.filter(area__gte=min_area, area__lte=max_area)
    
    for property in properties:
        # Split the comma-separated image paths into a list
        first_image = property.images.first()
        if first_image:
            
            property.first_image_url = first_image.image.url# Display the first 4 images
        else:
            property.first_image_url = None  # Handle case when no images are available


    # Fetch distinct cities from the Property model to populate the location filter
    distinct_cities = Property.objects.values_list('city', flat=True).distinct()

    context = {
        'properties': properties,
        'distinct_cities': distinct_cities,  # Pass distinct cities to the template
        'MEDIA_URL': settings.MEDIA_URL,
    }

    return render(request, 'property_listing.html', context)

    
    




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
@login_required
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