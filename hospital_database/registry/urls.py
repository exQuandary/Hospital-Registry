from django.urls import path
from .views import current_visits
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("patients", views.all_patients, name="patients"),
    path("providers", views.all_providers, name="providers"),
    path("nurses", views.all_nurses, name="nurses"),
    path("bills", views.bills, name="bills"),
    path("<int:bill_id>/letter", views.payment_letter, name="letter"),
    path("new_patient", views.create_patient, name="new_patient"),
    path("new_visit", views.create_visit, name="new_visit"),
    path('discharge/<int:visit_id>/',
         views.discharge_visit, name='discharge_visit'),
    path('discharge/success/', views.discharge_success, name='discharge_success'),
    path('edit_patient/<int:patient_id>',
         views.edit_patient, name="edit_patient"),
    path('patient_detail/<int:patient_id>/',
         views.patient_detail, name="patient_detail"),
    path('pay_bill/<int:bill_id>/', views.pay_bill, name="pay_bill"),
    path('current_visits/', current_visits.as_view(), name="current_visits")
]
