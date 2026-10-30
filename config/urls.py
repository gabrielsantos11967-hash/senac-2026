from django.contrib import admin
from django.urls import path

from config.funcionarios_views import funcionarios_list
from config.views import financeiro_list

urlpatterns = [
    path('', financeiro_list, name='financeiro_list'),
    path('funcionarios/', funcionarios_list, name='funcionarios_list'),
    path('admin/', admin.site.urls),
]
