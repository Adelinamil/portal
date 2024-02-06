from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_GET

from main.forms import ViolationForm
from main.models import Violation


def index(request):
    return render(request, 'main/index.html')


@login_required
def get_violations(request):
    return render(request, 'main/violations.html', {
        'violations': request.user.violations.all(),
        'violations_count': request.user.violations.count()
    })


@login_required
def create_violation(request):
    if request.method == 'POST':
        form = ViolationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('main:violations')

    form = ViolationForm(initial={'user': request.user})
    return render(request, 'main/create_violation.html', {'form': form})


@login_required
@require_GET
def get_violation(request, violation_id):
    violation = get_object_or_404(Violation, id=violation_id, user=request.user)
    return JsonResponse({
        'id': violation.id,
        'created': violation.created,
        'vehicle_number': violation.vehicle_number,
        'description': violation.description,
        'proof_url': violation.proof.url if violation.proof else None,
        'status': violation.get_status_display()
    })
