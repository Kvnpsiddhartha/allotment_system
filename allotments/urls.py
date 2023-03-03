from django.urls import path
from . import views


app_name = 'allotments'

urlpatterns = [
    path('new', views.new_allotment, name='new-allotment'),
    path('view', views.display_allotements, name='allotments'),
]