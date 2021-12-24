#any import functions, other functinos can be written here and then imported.
import os
from zipfile import ZipFile
import sys
from email.mime.text import MIMEText
from subprocess import Popen, PIPE



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

def fp_unzip_and_move(file_name, folder_name):
    print(file_name, folder_name)
    filepath = '/projects/team-2/abharadwaj61/django/predictivewebserver/genome_assembly/full_pipeline_data/' + folder_name + '/data'
    if str(file_name).endswith('.zip'):
        with ZipFile('/projects/team-2/abharadwaj61/django/predictivewebserver/genome_assembly/static/upload/' + str(file_name), 'r') as f1:
            f1.extractall(filepath)
        return filepath
    else:
        print('some exception handling to be done here')
        return 0

def send_email(link, email):
    msg = MIMEText('Your results from RASP-E are ready and can be accessed at: ' + str(link))
    msg['From'] = 'team2_raspe@biopredict2021.edu'
    msg['To'] = email
    msg['Subject'] = 'RASP-E Results'

    p = Popen(["/usr/sbin/sendmail", "-t", "-oi"], stdin=PIPE)
    # Both Python 2.X and 3.X
    p.communicate(msg.as_bytes() if sys.version_info >= (3,0) else msg.as_string())

    
