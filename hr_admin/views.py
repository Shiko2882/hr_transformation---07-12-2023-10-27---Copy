
# This is views.py file
from django.shortcuts import render, redirect, HttpResponse
from django.views.generic import CreateView
from .models import *
from .forms import *
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
# Create your views here.

def dashboard(request):
    companies= Company.objects.all()[0:6]
    consultants=Consultant.objects.all()
    
    
    context = {"companies":companies, 'consultants':consultants}
    return render(request,'home.html',context)


def fill_inputs_form(request):
    questions = InputsQuestion.objects.all()

    if request.method == 'POST':
        form = InputsAnswerForm(request.POST)

        if form.is_valid():
            # Assuming the user is authenticated
            user = request.user

            # Save each answer to the database
            for question in questions:
                answer_field_name = f'answer_{question.id}'
                notes_field_name = f'notes_{question.id}'

                answer = form.cleaned_data.get(answer_field_name, '')
                notes = form.cleaned_data.get(notes_field_name, '')

                # Use get_or_create to avoid duplicates
                InputsAnswer.objects.get_or_create(
                    user=user,
                    question=question,
                    defaults={'answer': answer, 'notes': notes}
                )

            return HttpResponse('Thank you for your inputs')  # Redirect to a success page
    else:
        # Create a form dynamically with fields for each question
        form = InputsAnswerForm()
    return render(request, 'fill_inputs_form.html', {'form': form, 'questions': questions})



@login_required
def update_inputs_form(request):
    user = request.user

    # Get all InputsAnswer objects associated with the user
    instances = InputsAnswer.objects.filter(user=user)

    if request.method == 'POST':
        form = InputsAnswerForm(request.POST)

        if form.is_valid():
            # Iterate through all questions and update corresponding answers
            for question in InputsQuestion.objects.all():
                answer_field_name = f'answer_{question.id}'
                notes_field_name = f'notes_{question.id}'

                answer = form.cleaned_data.get(answer_field_name, '')
                notes = form.cleaned_data.get(notes_field_name, '')

                # Update the existing InputsAnswer objects
                InputsAnswer.objects.filter(user=user, question=question).update(
                    answer=answer,
                    notes=notes
                )

            return HttpResponse('Thank you for updating your inputs')  # Redirect to a success page
    else:
        # Create a form with instances
        form = InputsAnswerForm(instance=instances)

    return render(request, 'update_inputs_form.html', {'form': form, 'instances': instances})

def view_inputs_form(request):
    user = request.user
    questions = InputsQuestion.objects.all()
    instance = get_object_or_404(InputsAnswer, user=user)
    form = InputsAnswerForm(instance=instance)  
    return render(request, 'view_inputs_form.html', {'form': form, 'questions': questions})


# a view to view/create/update companies data #

def view_companies(request):
    companies = Company.objects.all()
    form = CompanyViewForm()
    return render(request, 'company/view_companies.html', {'companies': companies , 'form': form})

def createcompany(request):
    form =CompanyViewForm()
    if request.method == 'POST':
        form = CompanyViewForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/")
    
    context= {'form':form}
    return render(request,'company/companyform.html', context)

def updatecompany(request,pk):
    
    company = Company.objects.get(id=pk)
    form =CompanyViewForm(instance=company)
    if request.method == 'POST':
        form = CompanyViewForm(request.POST,instance=company)
        if form.is_valid():
            form.save()
            return redirect("/")
    
    context= {'form':form}
    return render(request,'company/companyform.html', context)


def companyprofile(request,pk):
    companyid= Company.objects.get(id=pk)
    
    context = {"companyid":companyid }
    return render(request, "company/companyprofile.html",context)


# a view to view/create/update consultants data #

def view_consultants(request):
    consultants = Consultant.objects.all()
    form = ConsultantViewForm()
    return render(request, 'consultant/view_consultant.html', {'consultants': consultants , 'form': form})

def createconsultant(request):
    form =ConsultantViewForm()
    if request.method == 'POST':
        form = ConsultantViewForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/")
    
    context= {'form':form}
    return render(request,'consultant/consultantform.html', context)

def updateconsultant(request,pk):
    
    company = Consultant.objects.get(id=pk)
    form =ConsultantViewForm(instance=Consultant)
    if request.method == 'POST':
        form = ConsultantViewForm(request.POST,instance=Consultant)
        if form.is_valid():
            form.save()
            return redirect("/")
    
    context= {'form':form}
    return render(request,'consultant/consultantform.html', context)


def consultantprofile(request,pk):
    consultantid= Consultant.objects.get(id=pk)
    
    context = {"consultantid":consultantid }
    return render(request, "consultant/consultantprofile.html",context)