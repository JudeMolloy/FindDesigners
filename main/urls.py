from django.conf.urls import url

from . import views


app_name = 'main'
urlpatterns = [
    #url(r'^$', views., name='find'),
    url(r'(?P<designer_id>[0-9]+)', views.designer_detail, name='designer_detail'),
]
