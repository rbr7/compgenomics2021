from django import forms  

class StudentForm(forms.Form):  
    first_name = forms.CharField(label="First name", max_length = 50)  
    last_name  = forms.CharField(label="Last name", max_length = 50)  
    email_id = forms.EmailField(label="Enter Email")  
    files = forms.FileField() 