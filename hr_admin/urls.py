from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import *

urlpatterns = [
    path("", dashboard, name="home"),
    path('update_inputs_form/', update_inputs_form, name='update_inputs_form'),
    path('view_inputs_form/', view_inputs_form, name='view_inputs_form'),
    path('fill_inputs_form/', fill_inputs_form, name='fill_inputs_form'),
    
    
    path('view_companies/', view_companies, name='view_companies'),
    path("createcompany/", createcompany, name="Create Company"),
    path("updatecompany/<str:pk>", updatecompany, name="Update Company"),
    path("companyprofile/<str:pk>", companyprofile, name="Company Profile"),
    
    path('view_consultants/', view_consultants, name='view_consultants'),
    



] + static (settings.MEDIA_URL, document_root= settings.MEDIA_ROOT )
