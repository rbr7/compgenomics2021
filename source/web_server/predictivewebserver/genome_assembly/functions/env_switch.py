import subprocess
import os
# run_bash_command_in_different_env() runs that command a different conda environment.
#
# command - a bash command
# env - name of a conda environment
 
def run_bash_command_in_different_env(command, env):
    full_command = 'bash -c ' \
    ' "source /home/abharadwaj61/anaconda3/etc/profile.d/conda.sh; ' \
    ' conda activate ' \
    + env + ' ; ' \
    + command + ' "'
    print("Full Python Subrocess Command: " + str(full_command))

 
    #out = subprocess.run(full_command, shell=True, stdout=subprocess.DEVNULL)
    out = subprocess.run(full_command, shell=True)

def run_genomeAssembly(filepath, email):
    command = 'python /projects/team-2/abharadwaj61/django/predictivewebserver/genome_assembly/genome_assembly_pipeline/pipeline.py -i ' + filepath + ' -S -l'
    run_bash_command_in_different_env(command, "GA")
    #send the pipeline completed email here - with the link
    folder_name = filepath.split('/')[-1]
    link = 'http://team2.predict2021.biosci.gatech.edu/ga/results/' + folder_name +'/'
    send_email(link, email) 

def run_genePrediction(filepath, email):
    #command = 'python pipeline.py -i ~/7210/test/data -S -l'
    #make a change to run this as a zip format file
    command = 'python3 /projects/team-2/abharadwaj61/django/predictivewebserver/genome_assembly/gene_prediction_pipeline/geneprediction_pipeline.py -i ' + filepath +'/*' \
    ' -d /home/abharadwaj61/Databases/Ecoli_k12_mg1655_refdb_protein.faa' \
    ' -b /home/abharadwaj61/Databases/Ecoli_k12_mg1655_refdb_protein.faa -f /home/abharadwaj61/Databases/Rfam.cm -m 0.99'
    run_bash_command_in_different_env(command, "gene_prediction")
    folder_name = filepath.split('/')[-1]
    link = 'http://team2.predict2021.biosci.gatech.edu/gp/results/' +folder_name +'/'
    send_email(link, email)

def run_functionalAnnotation(filepath, email):
    #command = 'python pipeline.py -i ~/7210/test/data -S -l'
    command = 'python3 /projects/team-2/abharadwaj61/django/predictivewebserver/genome_assembly/functional_annotation/main_pipeline.py -I ' + filepath
    run_bash_command_in_different_env(command, "functional_annotation")
    folder_name = filepath.split('/')[-1]
    link = 'http://team2.predict2021.biosci.gatech.edu/fa/results/' +folder_name +'/'
    send_email(link, email)

def run_comparitiveGenomics(filepath, email):
    #command = 'python pipeline.py -i ~/7210/test/data -S -l'
    #user requirements, fastq, fastas and scaffolds
    #write a helper functions to give it in this format
    #filename = os.listdir(filepath)[0] 
    command = 'python3 /projects/team-2/abharadwaj61/django/predictivewebserver/genome_assembly/comparative_genomics_pipeline/comp_gen_pipeline.py -d ' + filepath 
    run_bash_command_in_different_env(command, "comp_genom")
    folder_name = filepath.split('/')[-1]
    link = 'http://team2.predict2021.biosci.gatech.edu/cg/results/' +folder_name +'/'
    send_email(link, email)


def run_fullpipeline(filepath, email):
    #command = 'python pipeline.py -i ~/7210/test/data -S -l'
    #user requirements, fastq, fastas and scaffolds
    #write a helper functions to give it in this format
    #filename = os.listdir(filepath)[0] 

    # genoem assembly
    command = 'python /projects/team-2/abharadwaj61/django/predictivewebserver/genome_assembly/genome_assembly_pipeline/pipeline.py -i ' + filepath + ' -S -l'
    run_bash_command_in_different_env(command, "GA")
    #send the pipeline completed email here - with the link
    folder_name = filepath.split('/')[-1]
    
    """
    # gene pred
    command = 'python3 /projects/team-2/abharadwaj61/django/predictivewebserver/genome_assembly/gene_prediction_pipeline/geneprediction_pipeline.py -i ' + filepath +'/*' \
    ' -d /home/abharadwaj61/Databases/Ecoli_k12_mg1655_refdb_protein.faa' \
    ' -b /home/abharadwaj61/Databases/Ecoli_k12_mg1655_refdb_protein.faa -f /home/abharadwaj61/Databases/Rfam.cm -m 0.99'
    run_bash_command_in_different_env(command, "gene_prediction")

    # functional annotate
    command = 'python3 /projects/team-2/abharadwaj61/django/predictivewebserver/genome_assembly/functional_annotation/main_pipeline.py -I ' + filepath
    run_bash_command_in_different_env(command, "functional_annotation")
    folder_name = filepath.split('/')[-1]

    # comp genomics
    command = 'python3 /projects/team-2/abharadwaj61/django/predictivewebserver/genome_assembly/comparative_genomics_pipeline/comp_gen_pipeline.py -d ' + filepath 
    run_bash_command_in_different_env(command, "comp_genom")
    folder_name = filepath.split('/')[-1]
    """

    #command = 'python3 /projects/team-2/abharadwaj61/django/predictivewebserver/genome_assembly/comparative_genomics_pipeline/comp_gen_pipeline.py -d ' + filepath 
    #run_bash_command_in_different_env(command, "comp_genom")
    #folder_name = filepath.split('/')[-1]
    
    #
    link = 'http://team2.predict2021.biosci.gatech.edu/fp/results/' +folder_name +'/'
    send_email(link, email)


if __name__ == "__main__":

    print('testing out the env switch: Running this in base first')

    run_comparativeGenomics('sample_file_path')
