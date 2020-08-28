from django.urls import path

from .views import *


urlpatterns = [
    path('ebooks/', EbookListCreateAPIView.as_view(), name='ebook-list'),

]
