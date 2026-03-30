from django.urls import path
from . import views

urlpatterns = [
    path('', views.DashboardView.as_view(), name='dashboard'),
    path('upload/', views.DataUploadView.as_view(), name='upload_data'),
    path('data/', views.DataListView.as_view(), name='data_list'),
    path('data/<int:pk>/', views.DataDetailView.as_view(), name='data_detail'),
    path('data/<int:pk>/process/', views.ProcessDataView.as_view(), name='process_data'),
    path('reports/', views.ReportListView.as_view(), name='report_list'),
    path('species/', views.SpeciesListView.as_view(), name='species_list'),
    path('species/<int:pk>/', views.SpeciesDetailView.as_view(), name='species_detail'),
    path('species/<int:pk>/delete/', views.SpeciesDeleteView.as_view(), name='species_delete'),
    path('data/<int:pk>/delete/', views.DataDeleteView.as_view(), name='data_delete'),
    path('reports/<int:pk>/delete/', views.ReportDeleteView.as_view(), name='report_delete'),
    path('analytics/', views.ModelAnalyticsView.as_view(), name='model_analytics'),
    
    # Auth
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('register/', views.RegisterView.as_view(), name='register'),
]
