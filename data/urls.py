from django.urls import path, include

from data import views

app_name = 'data'

urlpatterns = [
    path('', views.list_all_datas, name='datas'),
    path('', include('django.contrib.auth.urls')),
    path('create_data/', views.create_data, name='create_data'),
    path('view_data/<int:id>/', views.data_view, name='data_view'),
]