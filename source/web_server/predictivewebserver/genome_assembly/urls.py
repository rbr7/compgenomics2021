from django.urls import path, re_path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    #path('index', views.UploadView.as_view(), name='fileupload'),
    path('', views.index, name='ga-index' ),
    #path('sample_results_link', views.index1, name='ga-sampleoutput'),
    path('genome_assembly', views.run_assembly, name='ga-genomeassembly'),
    path('gene_prediction', views.run_geneprediction, name='ga-geneprediction'),
    path('functional_annotation', views.run_functionalAnnotation, name='ga-functionalannotation'),
    path('comparitive_genomics', views.run_comparitiveGenomics, name='ga-comparitivegenomics'),
    path('full_pipeline', views.run_fullpipeline, name='ga-fullpipeline'),
    path('view_results', views.view_results, name='ga-viewResults'),
    re_path(r'^ga/result/(?P<variable>[a-z0-9]{15})', views.ga_results, name='ga-resultsview'),
    re_path(r'^gp/result/(?P<variable>[a-z0-9]{15})', views.gp_results, name='gp-resultsview'),
    re_path(r'^fa/result/(?P<variable>[a-z0-9]{15})', views.fa_results, name='fa-resultsview'),
    re_path(r'^cg/result/(?P<variable>[a-z0-9]{15})', views.cg_results, name='cg-resultsview'),
    re_path(r'^fp/result/(?P<variable>[a-z0-9]{15})', views.fp_results, name='fp-resultsview'),
]