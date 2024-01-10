
# urls.py file
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import *

urlpatterns = [
    path("", dashboard, name="home"),
    path('fill_inputs_form/<int:pk>/', fill_inputs_form, name='fill_inputs_form'),
    path('fill_evaluation_form/<int:pk>/', fill_evaluation_form, name='fill_evaluation_form_with_pk'),
    
    path('view_companies/', view_companies, name='view_companies'),
    path("createcompany/", createcompany, name="Create Company"),
    path("updatecompany/<str:pk>", updatecompany, name="Update Company"),
    path("companyprofile/<str:pk>", companyprofile, name="Company Profile"),
    
    path('view_consultants/', view_consultants, name='view_consultants'),
    path("createconsultant/", createconsultant, name="Create consultant"),
    path("updateconsultant/<str:pk>", updateconsultant, name="Update consultant"),
    path("consultantprofile/<str:pk>", consultantprofile, name="Consultant Profile"),    

    path('attachments/<str:pk>', company_attachments, name='company_attachments'),
    path('attachment-widget/<str:pk>', attachment_widget, name='attachment_widget'),
    path('attachment/<int:attachment_id>/', attachment_detail, name='attachment_detail'),


] + static (settings.MEDIA_URL, document_root= settings.MEDIA_ROOT )
