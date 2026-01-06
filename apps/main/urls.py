from django.urls import path
from .views import home, contact_view, projects_view,project_detail

urlpatterns = [
    path('', home, name='home'),
    path('projects/', projects_view, name='projects'),
    path('contact/', contact_view, name='contact'),
    path('projects/<slug:slug>/', project_detail, name='project_detail'),

]
