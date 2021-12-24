import os
from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.http import HttpResponse, Http404
from django.shortcuts import redirect
from .models import FunctionalAnnotation
from genome_assembly.functions.functions import handle_uploaded_file, unzip_and_move
from .helper_fa import Annotation_user
from account.models import End_user
from .main_pipeline import run_main
from .forms import StudentForm

# Create your views here.

#
def fa_main(request):
    #
    #
    if request.method == 'POST':
        user = StudentForm(request.POST, request.FILES)
        if user.is_valid():
        eid = request.POST['email_id']
        annot = Annotation_user()
        uid, data_path, results_path = annot.create_specific_user()
        #
        person = End-user(email_id = eid, uid = uid)
        person.save()

        person_record = FunctionalAnnotation(user = person,input_folder = data_path,
         charts_folder = os.path.join(results_path, "output_plots"),output_folder = results_path)
        person_record.save()

        #
        file_name = request.FILES['file']
        handle_uploaded_file(request.FILES['file'])
        unzip_and_move(file=file_name, data_path=data_path)
        # method invoke for fa
        run_main()
        base = render(request, 'functional-annotation_home.html')
        return HttpResponse(base)
    else:
        # some error or do below
        user = StudentForm()
        #print('')
        return render(request,"uploader/functional-annotation_form.html", {'form':user})

    # method for running fa pipeline



    #

class UploadView(CreateView):
    #
    model = Upload
    fields = ['upload_file', ]
    success_url = reverse_lazy('fileupload')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['documents'] = Upload.objects.all()
        return context

def index1(request):  
    return render(request, "uploader/upload_success.html" )
