# This is forms.py file
from .models import *
from django.shortcuts import render,HttpResponse
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from django import forms




# Form to handle the company data #
class CompanyViewForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = '__all__'

# Form to handle the company data #
class ConsultantViewForm(forms.ModelForm):
    class Meta:
        model = Consultant
        fields = '__all__'



class InputsAnswerForm(forms.ModelForm):
    class Meta:
        model = InputsAnswer
        fields = ['answer', 'notes']
        

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        questions = InputsQuestion.objects.all()

        for question in questions:
            answer = f'answer_{question.id}'
            notes = f'notes_{question.id}'

            self.fields[answer] = forms.CharField(
                label=question.name,
                required=False
            )

            self.fields[notes] = forms.CharField(
                label=f'Notes',
                widget=forms.Textarea(attrs={'rows': 8}),
                required=False
            )

    def clean(self):
        cleaned_data = super().clean()
        # Additional validation logic if needed
        return cleaned_data
    
    
class InputsAnswerFormUpdate(forms.ModelForm):
    class Meta:
        model = InputsAnswer
        fields = ['answer', 'notes']

    def __init__(self, *args, **kwargs):
        # Get the 'instance' from kwargs
        instance = kwargs.get('instance', None)

        # Remove 'instance' from kwargs
        kwargs.pop('instance', None)

        super().__init__(*args, **kwargs)

        # If there is an instance, populate the form with its data
        if instance:
            self.fields['answer'].initial = instance.first().answer
            self.fields['notes'].initial = instance.first().notes