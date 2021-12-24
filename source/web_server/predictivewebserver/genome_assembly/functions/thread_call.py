from genome_assembly.functions import env_switch

def thread_function(filepath):
    print('calling the thread in the background')
    dummy_pipeline.call_main(filepath, ga=True)


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

def call_fullpipeline_thread(filepath, email):
    env_switch.run_fullpipeline(filepath, email)