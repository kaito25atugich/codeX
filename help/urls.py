from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path

from . import views

app_name='help'
urlpatterns = [
    path('top/', views.Top.as_view(), name='top'),
    path('news/<int:pk>/', views.NewsView.as_view(), name='news'),
]

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)