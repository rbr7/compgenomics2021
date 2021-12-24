#any import functions, other functinos can be written here and then imported.
import os
from zipfile import ZipFile



def handle_uploaded_file(f):  
    with open('/projects/team-2/abharadwaj61/django/predictivewebserver/genome_assembly/static/upload/'+f.name, 'wb+') as destination:  
        for chunk in f.chunks():  
            destination.write(chunk) 


#take in the zip file input and make a separate folder based on uuid
#initial implementatoin with just the hard coded folder


def ga_unzip_and_move(file_name, folder_name):
    print(file_name, folder_name)
    filepath = '/projects/team-2/abharadwaj61/django/predictivewebserver/genome_assembly/genome_assembly_data/' + folder_name + '/data'
    if str(file_name).endswith('.zip'):
        with ZipFile('/projects/team-2/abharadwaj61/django/predictivewebserver/genome_assembly/static/upload/' + str(file_name), 'r') as f1:
            f1.extractall(filepath)
        return filepath
    else:
        print('some exception handling to be done here')
        return 0

def gp_unzip_and_move(file_name, folder_name):
    print(file_name, folder_name)
    filepath = '/projects/team-2/abharadwaj61/django/predictivewebserver/genome_assembly/gene_prediction_data/' + folder_name + '/data'
    if str(file_name).endswith('.zip'):
        with ZipFile('/projects/team-2/abharadwaj61/django/predictivewebserver/genome_assembly/static/upload/' + str(file_name), 'r') as f1:
            f1.extractall(filepath)
        return filepath
    else:
        print('some exception handling to be done here')
        return 0

def fa_unzip_and_move(file_name, folder_name):
    print(file_name, folder_name)
    filepath = '/projects/team-2/abharadwaj61/django/predictivewebserver/genome_assembly/functional_annotation_data/' + folder_name + '/data'
    if str(file_name).endswith('.zip'):
        with ZipFile('/projects/team-2/abharadwaj61/django/predictivewebserver/genome_assembly/static/upload/' + str(file_name), 'r') as f1:
            f1.extractall(filepath)
        return filepath
    else:
        print('some exception handling to be done here')
        return 0

def cg_unzip_and_move(file_name, folder_name):
    print(file_name, folder_name)
    filepath = '/projects/team-2/abharadwaj61/django/predictivewebserver/genome_assembly/comparative_genomics_data/' + folder_name + '/data'
    if str(file_name).endswith('.zip'):
        with ZipFile('/projects/team-2/abharadwaj61/django/predictivewebserver/genome_assembly/static/upload/' + str(file_name), 'r') as f1:
            f1.extractall(filepath)
        return filepath
    else:
        print('some exception handling to be done here')
        return 0
