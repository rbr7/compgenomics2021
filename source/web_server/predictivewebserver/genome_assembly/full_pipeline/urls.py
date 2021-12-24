from django.urls import path
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from . import views

#
urlpatterns = [
    path('', views.UploadView.as_view(), name='fileupload'),
    path('index', views.index, name='uploader-index' ),
    path('index1', views.index1, name='uploader-sampleoutput'),
    #path('functional_annotation', views.generate_annotation, name='helper_fa')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

#