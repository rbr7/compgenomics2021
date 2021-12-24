from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy


from django.shortcuts import render  
from django.http import HttpResponse  
from genome_assembly.functions.functions import * 
from genome_assembly.forms import *  

from genome_assembly.genome_assembly_pipeline.pipeline import call_main

from genome_assembly.dummy_pipeline import dummy_pipeline

from uuid import uuid4

from threading import Thread 

from genome_assembly.functions import env_switch
import os
# Create your views here.


#threading functions

def call_genomeAssembly_thread(filepath):
    #print('calling the genome assembly pipeline')
    env_switch.run_genomeAssembly(filepath)

def call_genePrediction_thread(filepath):
    #print('calling the genome assembly pipeline')
    env_switch.run_genePrediction(filepath)

def call_functionalAnnotation_thread(filepath):
    #print('calling the genome assembly pipeline')
    env_switch.run_functionalAnnotation(filepath)

def call_comparitiveGenomics_thread(filepath):
    #print('calling the genome assembly pipeline')
    env_switch.run_comparitiveGenomics(filepath)

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
            handle_uploaded_file(request.FILES['file'])  
            #post to the model db here, get a uuid for that request and generate a folder in that name
            folder_name = uuid4().hex[:15]
            filepath = ga_unzip_and_move(file_name, folder_name)
            #call_main(i=filepath, S=True, l=True)

            #calling the dummy pipeline here
            t = Thread(target=call_genomeAssembly_thread, args=(filepath, ))
            #t.setDaemon(True)
            t.start()
            #dummy_pipeline.call_main(filepath, ga=True)
            #for the actual pipeline call, the helper funtion to change the environment will be given.

            #after this is called, this has to render something temp page
            return HttpResponse("File uploaded successfuly")  
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
            handle_uploaded_file(request.FILES['file'])  
            #post to the model db here, get a uuid for that request and generate a folder in that name
            folder_name = uuid4().hex[:15]
            filepath = gp_unzip_and_move(file_name, folder_name)
            #make the call to the pipeline here

            #make the call to the dummy pipeline here.
            t = Thread(target=call_genePrediction_thread, args=(filepath, ))
            t.start()
            #dummy_pipeline.call_main(filepath, gp=True)
            #call_main(i=filepath, S=True, l=True)
            #after this is called, this has to render something temp page
            return HttpResponse("File uploaded successfuly")  
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
            #this is the place where I need to generate the ID and give it to the user
            #instead of returning the http response, redirect the user to the page with the link to the output.
            #how to I save the post information?
            #figure out how to use models here
            print(request.POST)
            file_name = request.FILES['file']
            handle_uploaded_file(request.FILES['file'])  
            #post to the model db here, get a uuid for that request and generate a folder in that name
            folder_name = uuid4().hex[:15]
            filepath = fa_unzip_and_move(file_name, folder_name)
            #make the call to the pipeline here

            #make the call to the dummy pipeline here.
            t = Thread(target=call_functionalAnnotation_thread, args=(filepath, ))
            t.start()
            #dummy_pipeline.call_main(filepath, fa=True)
            #call_main(i=filepath, S=True, l=True)
            #after this is called, this has to render something temp page
            return HttpResponse("File uploaded successfuly")  
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
            handle_uploaded_file(request.FILES['file'])  
            #post to the model db here, get a uuid for that request and generate a folder in that name
            folder_name = uuid4().hex[:15]
            filepath = cg_unzip_and_move(file_name, folder_name)
            #make the call to the pipeline here

            #make the call to the dummy pipeline here.
            t = Thread(target=call_comparitiveGenomics_thread, args=(filepath, ))
            t.start()
            #dummy_pipeline.call_main(filepath, cg=True)
            #call_main(i=filepath, S=True, l=True)
            #after this is called, this has to render something temp page
            return HttpResponse("File uploaded successfuly")  
        else:
            print('form is not valid')
    else:  
        cg = comparitive_genomics_form()  
        return render(request,"genome_assembly/comparitive_genomics.html",{'form':cg})


#dynamic link generation - send the link to the folder as a variable in a dictionary, this has to be specific to each results page.
def results(request, variable):
    print(variable)
    filepath = 'genome_assembly/genome_assembly_data/' + variable
    print(filepath)
    rs_dict = {}
    rs_dict['contig'] = filepath
    rs_dict['quast'] = filepath
    rs_dict['qc'] = filepath
    #helper function to get the file of fasta and html (just do a .endswith)
    return render(request, "genome_assembly/upload_success.html", {'data':rs_dict})
