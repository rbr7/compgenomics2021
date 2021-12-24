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
    re_path(r'^result/(?P<variable>[a-z0-9]{7})', views.results, name='ga-resultsview'),
]