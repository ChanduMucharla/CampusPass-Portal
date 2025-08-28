
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from accounts.models import User
from .models import Feedback

@login_required
def feedback(request):
    recipients = User.objects.filter(role__in=['warden','faculty'])
    if request.method == 'POST':
        rid = request.POST.get('recipient')
        subject = request.POST.get('subject','').strip()
        message = request.POST.get('message','').strip()
        try:
            to_user = recipients.get(id=rid)
        except User.DoesNotExist:
            messages.error(request, 'Select a valid recipient.')
            return redirect('feedback')
        if not subject or not message:
            messages.error(request, 'Subject and message are required.')
            return redirect('feedback')
        Feedback.objects.create(sender=request.user, recipient=to_user, subject=subject, message=message)
        messages.success(request, 'Feedback sent successfully.')
        return redirect('feedback')
    return render(request, 'notify/feedback.html', {'recipients': recipients})
