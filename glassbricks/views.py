from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.core.mail import send_mail, EmailMessage
from django.template.loader import render_to_string
from weasyprint import HTML
from django.http import HttpResponse
from .forms import SignUpForm, PropertyForm
from .models import Property, PropertyImage, PropertyVideo
import random
import os
from io import BytesIO

# Property brochure view
def property_brochure_view(request, property_id):
    template_type = request.GET.get('template_type', 'template1')  # Default to 'template1' if not selected
    property = get_object_or_404(Property.objects.prefetch_related('images'), id=property_id)

    # Get the appropriate template based on the selected template_type
    template_name = f'{template_type}.html'  # Example: 'template1.html', 'template2.html', etc.
    
    try:
        # Render the template with property data
        html_content = render_to_string(template_name, {'property': property, 'property_link': request.build_absolute_uri(f'/property/{property.id}/')})
    except Exception as e:
        return HttpResponse(f"Error rendering template: {e}", status=500)

    return HttpResponse(html_content)

# PDF generation function
def print_property_to_pdf(request, property_id, template_type='template1'):
    property_brochure_url = request.build_absolute_uri(f'/property-brochure/{property_id}/') + f'?template_type={template_type}'
    
    try:
        # WeasyPrint renders the HTML from the URL
        html = HTML(url=property_brochure_url)  
        pdf_bytes = html.write_pdf()  # Convert the HTML content to PDF
        return pdf_bytes
    except Exception as e:
        print(f"Error generating PDF: {e}")
        return None

# Email sending function with the PDF attached
def send_property_pdf_via_email(request, property_id):
    property_instance = get_object_or_404(Property, pk=property_id)

    if request.method == "POST":
        recipient_email = request.POST.get('recipient_email')
        template_type = request.POST.get('template_type', 'template1')  # Default to 'template1'

        # Generate the PDF with the selected template
        pdf_bytes = print_property_to_pdf(request, property_id, template_type)
        if pdf_bytes is None:
            return render(request, 'error.html', {'message': 'Unable to generate PDF.'})

        # Compose the email with the PDF attached
        subject = f"Property Details: {property_instance.property_name}"
        message = f"Please find attached the property details for {property_instance.property_name}."
        email = EmailMessage(
            subject=subject,
            body=message,
            from_email=request.user.email,  # Sender's email (current logged-in user)
            to=[recipient_email],
        )
        
        email.attach(f"{property_instance.property_name}_details.pdf", pdf_bytes, 'application/pdf')

        # Send the email
        try:
            email.send()
            return render(request, 'email_sent.html', {'message': 'Email sent successfully.'})
        except Exception as e:
            return render(request, 'error.html', {'message': f"Failed to send email: {str(e)}"})

    return render(request, 'error.html', {'message': 'Invalid request method.'})

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()  
            
            
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            email = form.cleaned_data.get('email')
            user = authenticate(username=username, password=password)

            allowed_domains = ['glassbrix.in', 'alphamotion.in']  
            user_email_domain = email.split('@')[-1]
            
            if user_email_domain in allowed_domains:
                user.is_staff = True  
                user.save()
                
            
            if user is not None:
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                
                
                if user.is_staff:
                    return redirect('approve_property_listing')  
                else:
                    return redirect('home')
        else:
            print(form.errors)  
    else:
        form = SignUpForm()

    return render(request, 'signup.html', {'form': form})


def submit_property(request):
    if request.method == 'POST':
        property_form = PropertyForm(request.POST, request.FILES)
        if property_form.is_valid():
            property_instance = property_form.save(commit=False)
            property_instance.posted_by = request.user  
            property_instance.save()
            images = request.FILES.getlist('images')
            if images:
                print(f"Images uploaded: {[image.name for image in images]}") 
            else:
                print("No images uploaded") 
            for image in images:
                PropertyImage.objects.create(property=property_instance, image=image)    
            floor_plans = request.FILES.getlist('floor_plans')
            if images:
                print(f"Images uploaded: {[image.name for image in images]}")  
            else:
                print("No images uploaded")  
            for floor_plan in floor_plans:
                PropertyFloorPlan.objects.create(property=property_instance, floor_plan=floor_plan)
            videos = request.FILES.getlist('videos')
            if videos:
                print(f"Videos uploaded: {[video.name for video in videos]}")  
            else:
                print("No videos uploaded")  
            for video in videos:
                PropertyVideo.objects.create(property=property_instance, video=video)

            
            return redirect('home')  
        else:
            
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


def home(request):
    # Get the selected city from the URL parameters
    selected_city = request.GET.get('city')

    if selected_city:
        # Filter properties based on the selected city
        properties_in_city = Property.objects.filter(city__iexact=selected_city)

        # Randomly select 3 properties if more than 3 are available
        if properties_in_city.count() > 3:
            properties = random.sample(list(properties_in_city), 3)
        else:
            properties = properties_in_city
    else:
        # If no city is selected, randomly select 3 properties from all available properties
        all_properties = Property.objects.all()
        if all_properties.count() > 3:
            properties = random.sample(list(all_properties), 3)
        else:
            properties = all_properties

    # Pass data to the context for rendering
    context = {
        'properties': properties,
        'selected_city': None,
    }

    return render(request, 'index.html', context)


def signup_company(request):
    if request.method == 'post':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_staff = True  # Mark this user as a staff member
            user.save()
            login(request, user)  # Log in the user after signup
            return redirect('property_dashboard')  # Redirect to custom property dashboard    
    else:
        form = UserCreationForm()
        
    return render(request, 'signup.html',{'form':form})


def signin_company(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_staff:  # Only allow staff (Person 'A') to log in
            login(request, user)
            return redirect('property_dashboard')  # Redirect to the custom dashboard
        else:
            return render(request, 'signin.html', {'error': 'Invalid credentials or access denied'})
    return render(request, 'signin.html')
    
    
    
    

def contact(request):
    return render(request, 'contact-2.html')

@login_required
def profile(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        user_profile = UserProfile.objects.create(user=request.user)
        
    
    return render(request, 'profile.html', {'user_profile': user_profile})

def property_admin(request,property_id):
    property_instance = get_object_or_404(Property,id=property_id)
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'approve':
            property_instance.approved = True
            property_instance.save()
        elif action == 'deny':
            property_instance.approved = False
            property_instance.save()
        return redirect('approve_property_listing')  # Redirect back to the unapproved properties list
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
    return render(request, 'property_admin.html',context)

@login_required
def approve_deny_property(request, property_id):
    # Fetch the property by ID
    property_instance = get_object_or_404(Property, id=property_id)

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'approve':
            property_instance.approved = True
        elif action == 'deny':
            property_instance.approved = False

        property_instance.save()

        # Redirect back to the admin listing after action is taken
        return redirect('property_admin_listing')

    # If not a POST request, redirect to the property listing
    return redirect('property_admin_listing')


@login_required
def property_admin_listing(request):
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
    properties = Property.objects.filter(approved=False)

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

    return render(request, 'property_admin_listing.html', context)


def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_staff:  # only allow staff users
            login(request, user)
            return redirect('admin_dashboard')
        else:
            return render(request, 'admin_login.html',{'error':'Invalid credentials or access denied'})
    return render(request, 'admin_login.html')

@login_required
def admin_dashboard(request):
    if request.user.is_staff:
        properties = Property.objects.filter(approved=False)  # list unapproved properties
        return render(request, 'admin_dashboard.html', {'properties': properties})
    else:
        return redirect('admin_login')

@login_required
def update_profile(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        print("POST data:", request.POST)          # Log POST data
        print("FILES data:", request.FILES)        # Log FILES data

        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            print("Form is valid")
            form.save()                            # Save the form
            return redirect('profile')             # Redirect after saving
        else:
            print("Form errors:", form.errors)     # Log form errors
    else:
        form = UserProfileForm(instance=user_profile)

    return render(request, 'change_profile.html', {'form': form, 'user_profile': user_profile})


@login_required
def update_profile_picture(request):
    user_profile = UserProfile.objects.get(user=request.user)

    if request.method == 'POST':
        form = ProfilePictureForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('update_profile')
    
    else:
        form = ProfilePictureForm(instance=user_profile)

    return render(request, 'change_profile_picture.html', {
        'form': form,
        'user_profile': user_profile,
    })

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
    properties = Property.objects.filter(approved = True)

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
    
    # Get distinct cities for the dropdown
    cities = Property.objects.values_list('city', flat=True).distinct()

    # Pass the cities to the context
    context = {
        'cities': cities,
    }
    
    return render(request, 'headerall.html', context)

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
                
                email = user.email
                allowed_domains = ['glassbrix.in', 'alphamotion.in']  # Allowed domains
                user_email_domain = email.split('@')[-1]

                if user_email_domain in allowed_domains:
                    user.is_staff = True  # Ensure they are marked as staff for admin dashboard access
                    user.save()
                    return redirect('property_admin_listing')  # Redirect to admin dashboard
                else:
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

@login_required
def unapproved_property_list(request):
    if request.user.is_staff:  # Only allow admin to view this
        properties = Property.objects.filter(approved=False)
        return render(request, 'property_listing.html', {'properties': properties})
    else:
        return redirect('home')  # Redirect non-admin users to the home page

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
