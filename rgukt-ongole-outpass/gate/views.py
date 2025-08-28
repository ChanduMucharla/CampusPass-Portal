
from django.http import JsonResponse, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core import signing
from outpasses.models import Outpass

def is_staff(user):
    return user.is_authenticated and user.role in ['faculty','warden']

@login_required
@user_passes_test(is_staff)
def scan(request):
    token = request.GET.get('t','')
    if not token:
        return HttpResponseBadRequest('Missing token.')
    try:
        data = signing.loads(token, salt='outpass')
    except Exception:
        return JsonResponse({'valid': False, 'error':'Invalid token'}, status=400)
    op_id = data.get('outpass_id')
    try:
        op = Outpass.objects.get(id=op_id)
    except Outpass.DoesNotExist:
        return JsonResponse({'valid': False, 'error':'Not found'}, status=404)

    # Toggle OUT/IN
    if op.status == 'approved':
        op.status = 'out'
    elif op.status == 'out':
        op.status = 'in'
    op.save()
    return JsonResponse({'valid': True, 'id': op.id, 'status': op.status})
