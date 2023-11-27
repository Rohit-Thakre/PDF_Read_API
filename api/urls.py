from django.urls import path
from . import views

urlpatterns = [
   path('upload/', views.PDF_TO_CSV.as_view(), name='pdf_to_csv'),
]
