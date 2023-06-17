from django.shortcuts import render, redirect, get_object_or_404
from .forms import PatientEditForm
from .models import Patient
from .forms import VisitForm
from .forms import PatientForm, VisitForm, PatientEditForm
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from .models import Patient, Nurse, Provider, Bill, Visit
from django.utils import timezone
from django.views import View
# Create your views here.


from django.http import HttpResponse


def index(request):
    return render(request, 'registry/index.html')


def all_patients(request):
    patients = Patient.objects.all()
    return render(request, 'registry/patients.html', {'patients': patients})


def all_providers(request):
    providers = Provider.objects.all()
    return render(request, 'registry/providers.html', {'providers': providers})


def all_nurses(request):
    nurses = Nurse.objects.all()
    return render(request, 'registry/nurses.html', {'nurses': nurses})


def bills(request):
    bills = Bill.objects.select_related('patient', 'visit', 'status').all()
    return render(request, 'registry/bills.html', {'bills': bills})


def payment_letter(request, bill_id):
    bill = get_object_or_404(Bill.objects.select_related(
        'patient', 'visit'), id=bill_id)

    if bill.paid:
        return HttpResponse("Bill paid")

    return render(request, 'registry/letter.html', {'bill': bill})


def create_patient(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'registry/create_patient.html', {'form': form, 'success_message': 'New Patient Created'})
            # Redirect or perform any desired action
    else:
        form = PatientForm()

    return render(request, 'registry/create_patient.html', {'form': form})


def create_visit(request):
    if request.method == 'POST':
        form = VisitForm(request.POST)
        if form.is_valid():
            visit = form.save(commit=False)
            visit.discharge_time = None
            visit.save()
            return render(request, 'registry/create_visit.html', {'form': form, 'success_message': 'New Visit Created'})
            # Redirect or perform any desired action
    else:
        form = VisitForm()

    return render(request, 'registry/create_visit.html', {'form': form})


def discharge_visit(request, visit_id):
    visit = Visit.objects.get(pk=visit_id)
    if request.method == 'POST':
        form = VisitDischargeForm(request.POST, instance=visit)
        if form.is_valid():
            visit = form.save(commit=False)
            visit.discharge_time = timezone.now()
            visit.save()
            return render(request, 'registry/discharge_visit.html', {'form': form, 'success_message': 'Patient Discharged'})
            # Redirect or perform any desired action
    else:
        form = VisitDischargeForm(instance=visit)

    return render(request, 'registry/discharge_visit.html', {'form': form, 'visit': visit})


def discharge_visit(request, visit_id):
    visit = Visit.objects.get(pk=visit_id)

    if request.method == 'POST':
        visit.discharge_time = timezone.now()
        visit.save()

        amount = visit.status.cost
        bill = Bill.objects.create(
            amount=amount,
            status=visit.status,
            visit=visit,
            patient=visit.patient,
        )
        return redirect('discharge_success')

    return render(request, 'registry/discharge_visit.html', {'visit': visit})


def discharge_success(request):
    success_message = "Patient Discharged Successfully"
    return render(request, 'registry/discharge_success.html', {'success_message': success_message})


def edit_patient(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)

    if request.method == 'POST':
        form = PatientEditForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            return redirect('patient_detail', patient_id=patient.id)
    else:
        form = PatientEditForm(instance=patient)

    return render(request, 'registry/edit_patient.html', {'form': form, 'patient': patient})


def patient_detail(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    return render(request, 'registry/patient_detail.html', {'patient': patient})


def pay_bill(request, bill_id):
    bill = Bill.objects.get(pk=bill_id)

    if request.method == 'POST':
        bill.paid = True
        bill.save()
        return render(request, 'registry/bill_paid.html')
        # Additional logic or redirection

    return render(request, 'registry/pay_bill.html', {'bill': bill})


class current_visits(View):
    def get(self, request):
        visits = Visit.objects.filter(discharge_time__isnull=True)
        return render(request, 'registry/current_visits.html', {'visits': visits})
