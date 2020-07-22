from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path

from kucg import views

app_name = 'kucg'

urlpatterns = [
    path('',views.top,name ='Top'),
    path('activity/<int:page>/',views.activity,name='Activity'),
    path('article/<int:article_id>/',views.article,name="Article"),
    path('article/<str:search_word>/<int:page>/',views.article_str,name="Article_str"),
    path('archive/<int:year>/<int:month>/<int:page>/',views.archive,name="Archive"),
    path('contact/',views.contact,name="Contact"),
]

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)