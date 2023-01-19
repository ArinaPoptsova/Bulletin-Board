from . import views
from django.urls import path

urlpatterns = [
    path('', views.BulletinListView.as_view(), name='bulletins'),
    path('create/', views.BulletinCreateView.as_view(), name='create_bulletin'),
    path('edit/<str:slug>/', views.BulletinUpdateView.as_view(), name='edit_bulletin'),
    path('responses/', views.ResponseView.as_view(), name='responses'),
    path('responses/accept/<int:pk>/', views.accept, name='accept'),
    path('responses/delete/<int:pk>/', views.delete_response, name='delete_response'),
    path('<str:slug>/', views.BulletinDetailView.as_view(), name='bulletin'),
    path('response/<str:slug>/', views.AddResponse.as_view(), name='add_response'),

]
