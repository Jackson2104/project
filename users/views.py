
from django.contrib.auth import authenticate, login, get_user_model,logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect,get_object_or_404
from .forms import UserRegistrationForm, AnnouncementForm
from collections import Counter, defaultdict
from datetime import date
from django.contrib import messages
from .models import Announcement,CustomUser
from django.db.models import Q
from django.http import HttpResponse
import csv
from .models import CustomUser
from .utils import send_bulk_sms  # ← Function tuliyoandika awali
from django.conf import settings
from django.http import HttpResponseForbidden
from .models import Document
from .forms import DocumentForm
from .forms import UpdateProfileForm

@login_required
def view_profile(request):
    if request.method == 'POST':
        form = UpdateProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('view_profile')  # Refresh with updated data
    else:
        form = UpdateProfileForm(instance=request.user)
    return render(request, 'user_profile.html', {'form': form})


@login_required
@user_passes_test(lambda u: u.role == 'kiongozi')
def upload_document(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.uploaded_by = request.user
            document.save()
            messages.success(request, "Umefanikiwa ku-upload document!")
            return redirect('document_list')
    else:
        form = DocumentForm()
    return render(request, 'upload_document.html', {'form': form})

@login_required
def document_list(request):
    documents = Document.objects.all().order_by('-uploaded_at')
    return render(request, 'document_list.html', {'documents': documents})
def format_phone_number(number):
    if number.startswith('0'):
        return '+255' + number[1:]
    return number

@login_required
def send_sms_view(request):
    if request.method == "POST":
        message = request.POST.get("message")

        # Chukua namba zote → format kwa kimataifa
        phone_numbers = [
            format_phone_number(num)
            for num in CustomUser.objects.values_list('phone_no', flat=True)
        ]

        # Tumia key kutoka settings
        api_key = settings.BEEM_API_KEY
        secret_key = settings.BEEM_SECRET_KEY

        status, response = send_bulk_sms(phone_numbers, message, api_key, secret_key)

        if status == 200:
            messages.success(request, "Ujumbe umetumwa kwa mafanikio!")
        else:
            messages.error(request, f"Hitilafu ya kutuma ujumbe: {response}")

        return redirect("sms-page")

    return render(request, "sms_form.html")


def registered_users_view(request):
    query = request.GET.get('q', '')
    role = request.GET.get('role', '')
    gender = request.GET.get('gender', '')
    location = request.GET.get('location', '')

    User = get_user_model()
    users = User.objects.all()

    if query:
        users = users.filter(
            Q(f_name__icontains=query) |
            Q(m_name__icontains=query) |
            Q(l_name__icontains=query) |
            Q(email__icontains=query) |
            Q(phone_no__icontains=query)
        )
    if role:
        users = users.filter(role=role)
    if gender:
        users = users.filter(gender=gender)
    if location:
        users = users.filter(location__icontains=location)

    # Get distinct locations for the filter
    locations = User.objects.values_list('location', flat=True).distinct()

    return render(request, 'user_list.html', {
        'users': users,
        'locations': locations,
    })
def export_users_csv(request):
    query = request.GET.get('q', '')
    role = request.GET.get('role', '')
    gender = request.GET.get('gender', '')
    location = request.GET.get('location', '')

    User = get_user_model()
    users = User.objects.all()

    if query:
        users = users.filter(
            Q(f_name__icontains=query) |
            Q(m_name__icontains=query) |
            Q(l_name__icontains=query) |
            Q(email__icontains=query) |
            Q(phone_no__icontains=query)
        )
    if role:
        users = users.filter(role=role)
    if gender:
        users = users.filter(gender=gender)
    if location:
        users = users.filter(location__icontains=location)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="wanakijiji.csv"'

    writer = csv.writer(response)
    writer.writerow(['Jina Kamili', 'Email', 'Simu', 'Location', 'Gender', 'DOB', 'Role'])

    for user in users:
        writer.writerow([
            f"{user.f_name} {user.m_name or ''} {user.l_name}",
            user.email,
            user.phone_no,
            user.location,
            user.gender,
            user.date_of_birth,
            user.role
        ])

    return response

@login_required
def statistics_view(request):
    users = CustomUser.objects.all()
    gender_counts = Counter(users.values_list('gender', flat=True))
    age_gender_data = get_age_gender_intervals(users)

    if request.user.role == 'kiongozi':
        template_name = 'kiongozi/statistics.html'
    else:
        template_name = 'mwananchi/statistics.html'

    return render(request, template_name, {
        'gender_data': dict(gender_counts),
        'age_gender_data': age_gender_data
    })
def calculate_age(born):
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

def get_age_gender_intervals(users, interval=5):
    age_gender_data = defaultdict(lambda: {'male': 0, 'female': 0})
    
    for user in users:
        age = calculate_age(user.date_of_birth)
        bucket = f"{(age // interval) * interval}-{((age // interval) + 1) * interval - 1}"
        age_gender_data[bucket][user.gender] += 1
    
    sorted_data = dict(sorted(age_gender_data.items(), key=lambda x: int(x[0].split('-')[0])))
    return sorted_data

def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            if user.role == 'kiongozi':
                return redirect('kiongozi_page')
            else:
                return redirect('welcome')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')

@login_required
def welcome_view(request):
    users = CustomUser.objects.all()
    gender_counts = Counter(users.values_list('gender', flat=True))
    age_gender_data = get_age_gender_intervals(users)

    return render(request, 'welcome.html', {
        'gender_data': dict(gender_counts),
        'age_gender_data': age_gender_data
    })

@login_required
def kusoma(request):
    announcements = Announcement.objects.all().order_by('-created_at')

    if request.user.role == 'kiongozi':
        template_name = 'kiongozi/kusoma.html'
    else:
        template_name = 'mwananchi/kusoma.html'

    return render(request, template_name, {'announcements': announcements})

@login_required
@user_passes_test(lambda u: u.role == 'kiongozi')
def kiongozi_view(request):
    users = CustomUser.objects.all()
    gender_counts = Counter(users.values_list('gender', flat=True))
    age_gender_data = get_age_gender_intervals(users)

    return render(request, 'kiongozi.html', {
        'gender_data': dict(gender_counts),
        'age_gender_data': age_gender_data
    })

@login_required
@user_passes_test(lambda u: u.role == 'kiongozi')
def post_announcement(request):
    if request.method == 'POST':
        form = AnnouncementForm(request.POST, request.FILES)
        if form.is_valid():
            ann = form.save(commit=False)
            ann.posted_by = request.user
            ann.save()
            return redirect('kiongozi_page')
    else:
        form = AnnouncementForm()
    return render(request, 'post_announcement.html', {'form': form})

def edit_announcement(request, id):
    ann = get_object_or_404(Announcement, id=id)

    # Ruhusu kuhariri kama ndiye aliye-posti tu
    if request.user != ann.posted_by:
        return redirect('kiongozi_page')

    if request.method == 'POST':
        form = AnnouncementForm(request.POST, request.FILES, instance=ann)
        if form.is_valid():
            form.save()
            return redirect('kiongozi_page')
            
    else:
        form = AnnouncementForm(instance=ann)

    return render(request, 'edit_announcement.html', {'form': form})

def delete_announcement(request, id):
    ann = get_object_or_404(Announcement, id=id)

    if request.user == ann.posted_by:
        ann.delete()
        messages.success(request, 'Umefanikiwa kufuta Tangazo.')

    return redirect('kiongozi_page')

def logout_view(request):
    logout(request)
    return redirect('login')
