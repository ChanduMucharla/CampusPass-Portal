from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
import qrcode
import io

from .forms import OutpassForm
from .models import Outpass
from accounts.models import User

# ------------------------------
# Student applies for an outpass
# ------------------------------
@login_required
def apply_outpass(request):
    if request.user.role != 'student':
        return HttpResponseBadRequest('Only students can apply.')

    if request.method == 'POST':
        form = OutpassForm(request.POST, request.FILES)
        if form.is_valid():
            op = form.save(commit=False)
            op.student = request.user

            # Auto-assign warden or faculty if none selected
            if not op.warden:
                w = User.objects.filter(role='warden').first() or User.objects.filter(role='faculty').first()
                if w:
                    op.warden = w

            op.save()

            # If AJAX request -> return JSON response
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'ok': True, 'id': op.id, 'status': op.status})

            messages.success(request, 'Outpass submitted.')
            return redirect('my_outpasses')

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'ok': False, 'errors': form.errors}, status=400)

    else:
        form = OutpassForm()

    return render(request, 'outpasses/apply.html', {'form': form})


# ------------------------------
# Student views their outpasses
# ------------------------------
@login_required
def my_outpasses(request):
    if request.user.role != 'student':
        return HttpResponseBadRequest('Only students.')
    items = Outpass.objects.filter(student=request.user).order_by('-created_at')
    return render(request, 'outpasses/my.html', {'items': items})


# ------------------------------
# Faculty/Warden manage requests
# ------------------------------
@login_required
def manage_outpasses(request):
    if request.user.role not in ['faculty', 'warden']:
        return HttpResponseBadRequest('Only staff.')
    pending = Outpass.objects.filter(status='pending').order_by('created_at')
    history = Outpass.objects.exclude(status='pending').order_by('-updated_at')[:50]
    return render(request, 'outpasses/manage.html', {'pending': pending, 'history': history})


# ------------------------------
# Approve an Outpass
# ------------------------------
@login_required
def approve_outpass(request, pk):
    if request.user.role not in ['faculty', 'warden']:
        return HttpResponseBadRequest('Only staff.')
    op = get_object_or_404(Outpass, pk=pk)
    op.status = 'approved'
    op.save()
    token = op.generate_token()

    # Send email notification
    try:
        send_mail(
            'Outpass Approved',
            f'Your outpass #{op.id} has been approved. Token: {token}',
            settings.DEFAULT_FROM_EMAIL,
            [op.student.email],
            fail_silently=True
        )
    except Exception:
        pass

    # AJAX support
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'ok': True, 'id': op.id, 'status': op.status})

    messages.success(request, f'Approved outpass #{op.id}.')
    return redirect('manage_outpasses')


# ------------------------------
# Reject an Outpass
# ------------------------------
@login_required
def reject_outpass(request, pk):
    if request.user.role not in ['faculty', 'warden']:
        return HttpResponseBadRequest('Only staff.')
    op = get_object_or_404(Outpass, pk=pk)
    op.status = 'rejected'
    op.save()

    # Send email notification
    try:
        send_mail(
            'Outpass Rejected',
            f'Your outpass #{op.id} has been rejected.',
            settings.DEFAULT_FROM_EMAIL,
            [op.student.email],
            fail_silently=True
        )
    except Exception:
        pass

    # AJAX support
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'ok': True, 'id': op.id, 'status': op.status})

    messages.warning(request, f'Rejected outpass #{op.id}.')
    return redirect('manage_outpasses')


# ------------------------------
# Generate QR code for approved outpasses
# ------------------------------
@login_required
def outpass_qr(request, pk):
    if request.user.role == 'student':
        op = get_object_or_404(Outpass, pk=pk, student=request.user)
    else:
        op = get_object_or_404(Outpass, pk=pk)

    if op.status != 'approved':
        return HttpResponseBadRequest('QR available only for approved outpasses.')

    if not op.qr_token:
        op.generate_token()

    # Encode a full URL so scanners open a web page instead of raw text
    from django.urls import reverse
    verify_url = request.build_absolute_uri(reverse('verify_outpass', args=[op.qr_token]))
    img = qrcode.make(verify_url)
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    return HttpResponse(buf.getvalue(), content_type='image/png')
@login_required
def verify_outpass(request, token):
    try:
        outpass = Outpass.objects.get(qr_token=token)
        return render(request, 'outpasses/verify.html', {'outpass': outpass})
    except Outpass.DoesNotExist:
        messages.error(request, 'Invalid or expired QR token.')
        return redirect('dashboard')
