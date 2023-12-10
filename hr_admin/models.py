
# This is models.py file
from django.db import models
from django.contrib.auth.models import User


# create company model with company profile data that related to company user one to one and can be assigned to more than one consultant user

class Company(models.Model):
    name = models.CharField(max_length=120 , blank=True,  null=True)
    user = models.ManyToManyField(User, blank=True)
    consultant = models.ForeignKey(User,on_delete=models.CASCADE ,related_name='consulting_companies', blank=True)
    description = models.TextField( blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    industry = models.CharField(max_length=100, blank=True, null=True)
    size = models.IntegerField(blank=True, null=True)
    founded = models.DateField(blank=True, null=True)
    Legal = models.CharField(max_length=100, blank=True, null=True)
    logo= models.ImageField(upload_to='logos',blank=True,null=True)
    CEO = models.CharField(max_length=100, blank=True, null=True)
    employees = models.IntegerField(blank=True, null=True)
    turnover = models.CharField(max_length=100, blank=True, null=True)
    revenue = models.CharField(max_length=100, blank=True, null=True)
    revenue_range = models.CharField(max_length=100, blank=True, null=True)
    revenue_currency = models.CharField(max_length=100, blank=True, null=True)
    revenue_year = models.IntegerField(blank=True, null=True)
    headquarters = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)
    facebook = models.URLField(blank=True, null=True)
    # assign forms to company (Company InputsForm,Evaluation Form,Action Plan)
    actionplanform = models.ForeignKey('ActionPlanForm', on_delete=models.CASCADE, blank=True, null=True)
    evaluationform = models.ForeignKey('EvaluationForm', on_delete=models.CASCADE, blank=True, null=True)
    companyinputs = models.ForeignKey('InputsForm', on_delete=models.CASCADE, blank=True, null=True)
    # ----------------------
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name



    
# create consultant user model
class Consultant(models.Model):
    name = models.CharField(max_length=100)
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    email = models.EmailField()
    photo = models.ImageField(upload_to='profile',blank=True,null=True)
    phone = models.CharField(max_length=100)
    linkedin = models.URLField( blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name

  

# class to build a form by admin user called (Company Inputs) 
# form should contain a questions grouped under category defined by admin
 

class InputsForm(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField( blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name
    
class InputsCategory(models.Model):
    InputsForm = models.ForeignKey(InputsForm, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.InputsForm.name + '  --->  ' + self.name   

# form Should have a model to create a question that have many options to answer like yes or no , multiple choice or single choice and also a notes field for each question

class InputsQuestion(models.Model):
    InputsCategory = models.ForeignKey(InputsCategory, on_delete=models.CASCADE)   
    name = models.CharField(max_length=100)
    options = models.CharField(max_length=100, choices=[('yes_no', 'Yes or No'), ('multiple_choice', 'Multiple Choice'), ('single_choice', 'Single Choice')], blank=True, null=True)
    notes = models.TextField( blank=True, null=True)
    def __str__(self):
        return self.InputsCategory.InputsForm.name + '  --->  ' + self.InputsCategory.name + '  --->  ' + self.name 

# form and quiestions should be answered by company users one time only, and can be viewed abd edit by admin, company user,assigned consultant user
class InputsAnswer(models.Model):

    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    question = models.ForeignKey(InputsQuestion, on_delete=models.CASCADE)
    answer = models.CharField(max_length=255, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question.name + '  --->  ' + self.answer
    class Meta:
        unique_together = ['company', 'question']
    
    
# create a models for evaluation form that should be created by admin user 
class EvaluationForm(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# and can be viewed and edit by assigned consultant user that assigned to the company

# create a model for the 2 levels of categories that will contain the questions and answers

class EvaluationCategory1(models.Model):
    name = models.CharField(max_length=100)
    EvaluationForm = models.ForeignKey(EvaluationForm, on_delete=models.CASCADE)
    def __str__(self):
        return self.name    
# category 2 will be created under category 1

class EvaluationCategory2(models.Model):
    name = models.CharField(max_length=100)
    EvaluationCategory1 = models.ForeignKey(EvaluationCategory1, on_delete=models.CASCADE)
    def __str__(self):
        return self.EvaluationCategory1.name + '  --->  ' + self.name   
# create a model for the questions and answers under category 2 and the answers should be a score firld [0-10] and a notes field
    
class EvaluationQuestion(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    weight = models.IntegerField(default=10)
    EvaluationCategory2 = models.ForeignKey(EvaluationCategory2, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.EvaluationCategory2.EvaluationCategory1.name + '  --->  ' +self.EvaluationCategory2.name + '  --->  ' + self.name   


    
# create a model for the answers under category 2 and the answers should be a score firld [0-10] and a notes field
class EvaluationAnswer(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    question = models.ForeignKey(EvaluationQuestion, on_delete=models.CASCADE)
    answer = models.IntegerField()
    notes = models.TextField()
    # connect the evaluation answer onetoone relationship with the company input answer
    #InputsAnswer = models.ForeignKey(InputsAnswer, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question.name + '  --->  ' + str(self.answer)

# create a class to save the final score result for each evaluation
class EvaluationResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    evaluationform = models.ForeignKey(EvaluationForm, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.user.company

    
# create a model for action plan form that will be filled by consultant user based on the evaluation answers and questions. The model will be based on each category1 and category2 with extra fields  ["Action / Initiative / Project", "Deliverables / Outcome / Result(s)", "Impact (High - Medium - Low)" , "Difficulty (High - Medium - Low)", "Required Resources", "Tentative Budget", "Accountability", "Time Frame"]
    
class ActionPlanForm(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    category = models.ForeignKey(EvaluationCategory2, on_delete=models.CASCADE)
    action = models.CharField(max_length=100)
    deliverables = models.CharField(max_length=100)
    impact = models.CharField(max_length=100)
    difficulty = models.CharField(max_length=100)
    resources = models.CharField(max_length=100)
    budget = models.CharField(max_length=100)
    accountability = models.CharField(max_length=100)
    timeframe = models.CharField(max_length=100)
    #need it to be oneToOne relationship with EvaluationAnswer 
    #EvaluationAnswer = models.OneToOneField(EvaluationAnswer, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    
# create a model to handle action plan comments and action plan comments answers
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    actionplanform = models.ForeignKey(ActionPlanForm, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    
# create a model to handle action plan comments and action plan comments answers
class CommentAnswer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    commentanswer = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    
class CommentActionPlan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    commentactionplan = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)



    





