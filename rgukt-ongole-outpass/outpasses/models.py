
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core import signing

class Outpass(models.Model):
    STATUS = (
        ('pending','Pending'),
        ('approved','Approved'),
        ('rejected','Rejected'),
        ('out','Out'),
        ('in','In'),
    )
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='outpasses')
    warden = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='to_approve')
    reason = models.TextField()
    attachment = models.FileField(upload_to='attachments/', blank=True, null=True)
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=20, choices=STATUS, default='pending')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    qr_token = models.CharField(max_length=255, blank=True)

    def generate_token(self):
        payload = {'outpass_id': self.id, 'user': self.student.username}
        self.qr_token = signing.dumps(payload, salt='outpass')
        self.save()
        return self.qr_token

    def __str__(self):
        return f"Outpass {self.id} - {self.student} - {self.status}"
