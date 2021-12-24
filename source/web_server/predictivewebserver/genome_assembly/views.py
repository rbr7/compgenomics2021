from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy


from django.shortcuts import render  
from django.http import HttpResponse , FileResponse
from genome_assembly.functions.functions import * 
from genome_assembly.forms import *  

from genome_assembly.genome_assembly_pipeline.pipeline import call_main

from genome_assembly.dummy_pipeline import dummy_pipeline

from uuid import uuid4

from threading import Thread 

from genome_assembly.functions import env_switch
import os
import shutil

# Create your views here.


#threading functions

def call_genomeAssembly_thread(filepath, email):
    #print('calling the genome assembly pipeline')
    env_switch.run_genomeAssembly(filepath, email)

def call_genePrediction_thread(filepath, email):
    #print('calling the genome assembly pipeline')
    env_switch.run_genePrediction(filepath, email)

def call_functionalAnnotation_thread(filepath, email):
    #print('calling the genome assembly pipeline')
    env_switch.run_functionalAnnotation(filepath, email)

def call_comparitiveGenomics_thread(filepath, email):
    #print('calling the genome assembly pipeline')
    env_switch.run_comparitiveGenomics(filepath, email)

def call_fullpipeline_thread(filepath, email):
    env_switch.run_fullpipeline(filepath, email)

def index(request):
    return render(request, "genome_assembly/index.html")


#function to run the assembly
def run_assembly(request):
    #return render(request, "uploader/genome_assembly_form.html")
    if request.method == 'POST':  
        ga = genome_assembly_form(request.POST, request.FILES)  
        if ga.is_valid():  
            #this is the place where I need to generate the ID and give it to the user
            #instead of returning the http response, redirect the user to the page with the link to the output.
            #how to I save the post information?
            #figure out how to use models here
            print(request.POST)
            file_name = request.FILES['file']
            email = request.POST['email']
            handle_uploaded_file(request.FILES['file'])  
            #post to the model db here, get a uuid for that request and generate a folder in that name
            folder_name = uuid4().hex[:15]
            filepath = ga_unzip_and_move(file_name, folder_name)
            #call_main(i=filepath, S=True, l=True)

            #calling the dummy pipeline here
            t = Thread(target=call_genomeAssembly_thread, args=(filepath,email, ))
            #t.setDaemon(True)
            t.start()

            #sendemail('job has been sucessfully submitted, you')
            #dummy_pipeline.call_main(filepath, ga=True)
            #for the actual pipeline call, the helper funtion to change the environment will be given.

            #after this is called, this has to render something temp page
            message = 'Your job has been successfully submitted, you will recieve an email when it finishes, Job ID:' + folder_name
            return HttpResponse(message)  
        else:
            print('form is not valid')
    else:  
        ga = genome_assembly_form()  
        return render(request,"genome_assembly/genome_assembly.html",{'form':ga})


#function to run gene_prediction
def run_geneprediction(request):
    #return render(request, "uploader/genome_assembly_form.html")
    if request.method == 'POST':  
        gp = gene_prediction_form(request.POST, request.FILES)  
        if gp.is_valid():  
            #this is the place where I need to generate the ID and give it to the user
            #instead of returning the http response, redirect the user to the page with the link to the output.
            #how to I save the post information?
            #figure out how to use models here
            print(request.POST)
            file_name = request.FILES['file']
            email = request.POST['email']
            handle_uploaded_file(request.FILES['file'])  
            #post to the model db here, get a uuid for that request and generate a folder in that name
            folder_name = uuid4().hex[:15]
            filepath = gp_unzip_and_move(file_name, folder_name)
            #make the call to the pipeline here

            #make the call to the dummy pipeline here.
            t = Thread(target=call_genePrediction_thread, args=(filepath,email, ))
            t.start()
            #dummy_pipeline.call_main(filepath, gp=True)
            #call_main(i=filepath, S=True, l=True)
            #after this is called, this has to render something temp page
            message = 'Your job has been successfully submitted, you will recieve an email when it finishes, Job ID:' + folder_name
            return HttpResponse(message)  
        else:
            print('form is not valid')
    else:  
        gp = gene_prediction_form()  
        return render(request,"genome_assembly/gene_prediction.html",{'form':gp})


#function to run functional annotation
def run_functionalAnnotation(request):
    #return render(request, "uploader/genome_assembly_form.html")
    if request.method == 'POST':  
        fa = functional_annotation_form(request.POST, request.FILES)  
        if fa.is_valid():  
            print(request.POST)
            file_name = request.FILES['file']
            email = request.POST['email']
            handle_uploaded_file(request.FILES['file'])  
            #post to the model db here, get a uuid for that request and generate a folder in that name
            folder_name = uuid4().hex[:15]
            filepath = fa_unzip_and_move(file_name, folder_name)
            #make the call to the pipeline here

            #make the call to the dummy pipeline here.
            t = Thread(target=call_functionalAnnotation_thread, args=(filepath, email ))
            t.start()
            #dummy_pipeline.call_main(filepath, fa=True)
            #call_main(i=filepath, S=True, l=True)
            #after this is called, this has to render something temp page
            message = 'Your job has been successfully submitted, you will recieve an email when it finishes, Job ID:' + folder_name
            return HttpResponse(message)   
        else:
            print('form is not valid')
    else:  
        fa = functional_annotation_form()  
        return render(request,"genome_assembly/functional_annotation.html",{'form':fa})


#function to run functional annotation
def run_comparitiveGenomics(request):
    #return render(request, "uploader/genome_assembly_form.html")
    if request.method == 'POST':  
        cg = comparitive_genomics_form(request.POST, request.FILES)  
        if cg.is_valid():  
            #this is the place where I need to generate the ID and give it to the user
            #instead of returning the http response, redirect the user to the page with the link to the output.
            #how to I save the post information?
            #figure out how to use models here
            print(request.POST)
            file_name = request.FILES['file']
            email = request.POST['email']
            handle_uploaded_file(request.FILES['file'])  
            #post to the model db here, get a uuid for that request and generate a folder in that name
            folder_name = uuid4().hex[:15]
            filepath = cg_unzip_and_move(file_name, folder_name)
            #make the call to the pipeline here

            #make the call to the dummy pipeline here.
            t = Thread(target=call_comparitiveGenomics_thread, args=(filepath, email ))
            t.start()
            #dummy_pipeline.call_main(filepath, cg=True)
            #call_main(i=filepath, S=True, l=True)
            #after this is called, this has to render something temp page
            message = 'Your job has been successfully submitted, you will recieve an email when it finishes, Job ID:' + folder_name
            return HttpResponse(message)   
        else:
            print('form is not valid')
    else:  
        cg = comparitive_genomics_form()  
        return render(request,"genome_assembly/comparitive_genomics.html",{'form':cg})


#method to run the full pipeline
def run_fullpipeline(request):
    if request.method == 'POST':  
        fp = full_pipeline_form(request.POST, request.FILES)  
        if fp.is_valid():  
            #this is the place where I need to generate the ID and give it to the user
            #instead of returning the http response, redirect the user to the page with the link to the output.
            #how to I save the post information?
            #figure out how to use models here
            print(request.POST)
            file_name = request.FILES['file']
            email = request.POST['email']
            handle_uploaded_file(request.FILES['file'])  
            #post to the model db here, get a uuid for that 
            folder_name = uuid4().hex[:15]
            filepath = fp_unzip_and_move(file_name, folder_name)
            #make the call to the pipeline here

            t = Thread(target=call_fullpipeline_thread, args=(filepath, email ))
            t.start()
            
            message = 'Your job has been successfully submitted, you will recieve an email when it finishes, Job ID:' + folder_name
            return HttpResponse(message)   
        else:
            print('form is not valid')
    else:  
        fp = full_pipeline_form()  
        return render(request,"genome_assembly/full_pipeline.html",{'form':fp})



#dynamic link generation - send the link to the folder as a variable in a dictionary, this has to be specific to each results page.
def view_results(request):
    if request.method == 'POST':
        host = 'http://team2.predict2021.biosci.gatech.edu/'  
        vr = view_results_form(request.POST)
        if vr.is_valid():
            print(request.POST)
            jobId = request.POST['jobId']
            pipeline = request.POST['pipeline_name']
            print(jobId, pipeline)
            if pipeline == 'GA':
                link = host + 'ga/result/'+jobId
            if pipeline == 'GP':
                link = host + 'gp/result/'+jobId
            if pipeline == 'FA':
                link = host + 'fa/result/'+jobId
            if pipeline == 'CG':
                link = host + 'cg/result/'+jobId
            if pipeline == 'FULL':
                link = host + 'fp/result/'+jobId
            return render(request, "genome_assembly/download_results.html", {"link": link})
        else:
            print('invalid form')

    else:
        vr = view_results_form()
        return render(request, "genome_assembly/view_results.html", {'form':vr})
    

def ga_results(request, variable):
    print(variable)
    filepath = '/projects/team-2/abharadwaj61/django/predictivewebserver/genome_assembly/genome_assembly_data/' + variable 
    shutil.make_archive(filepath+'/genome_assembly_results', 'zip', filepath+'/genome_assembly_results' )
    zipfile = open(filepath+'/genome_assembly_results.zip', 'rb')
    return FileResponse(zipfile)


def gp_results(request, variable):
    print(variable)
    filepath = '/projects/team-2/abharadwaj61/django/predictivewebserver/genome_assembly/gene_prediction_data/' + variable
    shutil.make_archive(filepath +'/gene_prediction_results', 'zip', filepath+'/data/gene_prediction_results' )
    zipfile = open(filepath+'/gene_prediction_results.zip', 'rb')
    return FileResponse(zipfile)


def fa_results(request, variable):
    print(variable)
    filepath = '/projects/team-2/abharadwaj61/django/predictivewebserver/genome_assembly/functional_annotation_data/' + variable
    shutil.make_archive(filepath +'/functional_annotation_results', 'zip', filepath+'/functional_annotation_results' )
    zipfile = open(filepath+'/functional_annotation_results.zip', 'rb')
    return FileResponse(zipfile)

def cg_results(request, variable):
    print(variable)
    filepath = '/projects/team-2/abharadwaj61/django/predictivewebserver/genome_assembly/comparative_genomics_data/' + variable
    shutil.make_archive(filepath + '/comparative_genomics_results', 'zip', filepath+'/comparative_genomics_results' )
    zipfile = open(filepath+'/comparative_genomics_results.zip', 'rb')
    return FileResponse(zipfile)

def fp_results(request, variable):
    print(variable)
    filepath = '/projects/team-2/abharadwaj61/django/predictivewebserver/genome_assembly/full_pipeline_data/' + variable
    shutil.make_archive(filepath + '/full_pipeline_results', 'zip', filepath+'/full_pipeline_results' )
    zipfile = open(filepath+'/full_pipeline_results.zip', 'rb')
    return FileResponse(zipfile)
