
# This is views.py file
from django.shortcuts import render, redirect, HttpResponse
from django.views.generic import CreateView
from .models import *
from .forms import *
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages

# Create your views here.

def dashboard(request):
    companies= Company.objects.all()[0:6]
    consultants=Consultant.objects.all()[0:6]
    
    
    context = {"companies":companies, 'consultants':consultants}
    return render(request,'home.html',context)

def company_attachments(request, company_id):
    company = get_object_or_404(Company, pk=company_id)
    attachments = company.attachments.all()

    if request.method == 'POST':
        form = AttachmentForm(request.POST, request.FILES)
        if form.is_valid():
            attachment = form.save(commit=False)
            attachment.company = company
            attachment.save()
            print("Attachment saved successfully!")  # Add this line
            return redirect('company_attachments', company_id=company_id)
    else:
        form = AttachmentForm()

    return render(request, 'company/company_attachments.html', {'company': company, 'attachments': attachments, 'form': form})


def attachment_widget(request, company_id):
    company = Company.objects.get(pk=company_id)
    attachments = company.attachments.all()
    
    return render(request, 'company/attachment_widget.html', {'company': company, 'attachments': attachments})
def attachment_detail(request, attachment_id):
    attachment = get_object_or_404(Attachment, pk=attachment_id)
    return render(request, 'company/attachment_detail.html', {'attachment': attachment})

def fill_inputs_form(request, pk=None):
    try:
        company = Company.objects.get(id=pk, user=request.user)
    except Company.DoesNotExist:
        return HttpResponse('You are not assigned to this company.', status=403)
    category = InputsCategory.objects.all()
    questions = InputsQuestion.objects.all()
    existing_answers = InputsAnswer.objects.filter(company=company).select_related('question')
    initial_data = {}

    for answer in existing_answers:
        initial_data[f'answer_{answer.question.id}'] = answer.answer
        initial_data[f'notes_{answer.question.id}'] = answer.notes

    if request.method == 'POST':
        form = InputsAnswerForm(request.POST, initial=initial_data)
        if form.is_valid():
            for question in questions:
                answer_field_name = f'answer_{question.id}'
                notes_field_name = f'notes_{question.id}'

                answer = form.cleaned_data.get(answer_field_name, '')
                notes = form.cleaned_data.get(notes_field_name, '')
                InputsAnswer.objects.update_or_create(
                    company=company,
                    question=question,
                    defaults={'answer': answer, 'notes': notes}
                )

            messages.success(request, 'Data submitted successfully.')
            return redirect('fill_inputs_form', pk=pk)
        else:
            # Form is not valid, handle errors or display them in the template
            pass
    else:
        form = InputsAnswerForm(initial=initial_data)

    return render(request, 'fill_inputs_form.html', {'form': form, 'questions': questions, 'company': company, 'pk': pk, 'category': category})



# create the view for evaluation answers form #


def fill_evaluation_form(request, pk=None):
    try:
        company = Company.objects.get(id=pk, user=request.user)
    except Company.DoesNotExist:
        return HttpResponse('You are not assigned to this company.', status=403)

    questions = EvaluationQuestion.objects.all()

    if request.method == 'POST':
        form = EvaluationAnswerForm(request.POST)
        if form.is_valid():
            for question in questions:
                answer_field_name = f'answer_{question.id}'
                notes_field_name = f'notes_{question.id}'

                answer = form.cleaned_data.get(answer_field_name, '')
                notes = form.cleaned_data.get(notes_field_name, '')

                EvaluationAnswer.objects.update_or_create(
                    company=company,
                    question=question,
                    defaults={'answer': answer, 'notes': notes}
                )

            return HttpResponse('Thank you for your inputs')
    else:
        existing_answers = EvaluationAnswer.objects.filter(company=company)
        initial_data = {}
        for answer in existing_answers:
            answer_field_name = f'answer_{answer.question.id}'
            notes_field_name = f'notes_{answer.question.id}'
            initial_data[answer_field_name] = answer.answer
            initial_data[notes_field_name] = answer.notes

        form = EvaluationAnswerForm(initial=initial_data)

    return render(request, 'evaluation_answers_form.html', {'form': form, 'questions': questions, 'company': company, 'pk': pk})





# a view to view/create/update companies data #

def view_companies(request):
    companies = Company.objects.all()
    form = CompanyViewFormCreate()
    return render(request, 'company/view_companies.html', {'companies': companies , 'form': form})

def createcompany(request):
    form =CompanyViewFormCreate()
    if request.method == 'POST':
        form = CompanyViewFormCreate(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/")
    
    context= {'form':form}
    return render(request,'company/companyform.html', context)

def updatecompany(request,pk):
    
    company = Company.objects.get(id=pk)
    form =CompanyViewFormUpdate(instance=company)
    if request.method == 'POST':
        form = CompanyViewFormUpdate(request.POST,instance=company)
        if form.is_valid():
            form.save()
            return redirect("/")
    
    context= {'form':form ,'company': company}
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
    consultantid= Consultant.objects.get(user=pk)
    
    context = {"consultantid":consultantid }
    return render(request, "consultant/consultantprofile.html",context)