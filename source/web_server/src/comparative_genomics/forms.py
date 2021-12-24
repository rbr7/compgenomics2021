from django import forms  


class StudentForm(forms.Form):  
    firstname = forms.CharField(label="Enter first name",max_length=50)  
    #lastname  = forms.CharField(label="Enter last name", max_length = 10)  
    email     = forms.EmailField(label="Enter Email")  
    file      = forms.FileField() # for creating file input 

#input for genome assembly
class genome_assembly_form(forms.Form):
    #initial values can be set on the form initialization
    name = forms.CharField(label="Enter your name", max_length=25)
    email = forms.EmailField(label="Enter your Email")
    file = forms.FileField()

#input for gene prediction
class gene_prediction_form(forms.Form):
    name = forms.CharField(label='Enter your name', max_length=40)
    email = forms.EmailField(label='Enter your email')
    file = forms.FileField()

#input for functional annotation
class functional_annotation_form(forms.Form):
    name = forms.CharField(label='Enter your name', max_length=40)
    email = forms.EmailField(label='Enter your email')
    file = forms.FileField()

#input for comparitive genomics
class comparitive_genomics_form(forms.Form):
    name = forms.CharField(label='Enter your name', max_length=40)
    email = forms.EmailField(label='Enter your email')
    file = forms.FileField()


