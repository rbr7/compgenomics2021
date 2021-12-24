from django import forms  

class Fullpipeform(forms.Form):  
    name = forms.CharField(label="Enter your Name", max_length = 50)  
    #last_name  = forms.CharField(label="Last name", max_length = 50)  
    email_id = forms.EmailField(label="Enter Email")  
    files = forms.FileField() 