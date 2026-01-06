from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from .models import Project, Contact


def home(request):
    projects = Project.objects.all().order_by('-created_at')[:3]
    return render(request, 'main/home.html', {'projects': projects})


def contact_view(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        # DB ga saqlash
        Contact.objects.create(
            full_name=full_name,
            email=email,
            message=message
        )

        # 1️⃣ ADMIN’GA EMAIL
        send_mail(
            subject=f"Portfolio Contact: {full_name}",
            message=(
                f"Ism: {full_name}\n"
                f"Email: {email}\n\n"
                f"Xabar:\n{message}"
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.ADMIN_EMAIL],
            fail_silently=False,
        )

        # 2️⃣ USER’GA TASDIQ EMAIL
        send_mail(
            subject="Xabaringiz qabul qilindi",
            message=(
                f"Salom {full_name},\n\n"
                "Xabaringiz muvaffaqiyatli qabul qilindi.\n"
                "Tez orada siz bilan bog‘lanaman.\n\n"
                "Hurmat bilan,\n"
                "Nodirbek Abloqulov"
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=False,
        )

        # ✅ SUCCESS MESSAGE
        messages.success(
            request,
             "Xabaringiz qabul qilindi. Tez orada siz bilan bog‘lanaman."
        )

        # ✅ ENG MUHIM QATOR
        return redirect('contact')

    return render(request, 'main/contact.html')


def projects_view(request):
    projects = Project.objects.all()

    for project in projects:
        project.tech_list = [
            tech.strip() for tech in project.technologies.split(',')
        ]

    return render(request, 'main/projects.html', {'projects': projects})


def project_detail(request, slug):
    project = get_object_or_404(Project, slug=slug)
    return render(
        request,
        'main/project_detail.html',
        {'project': project}
    )
