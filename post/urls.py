from django.urls import path
from .views import *

app_name = "post"
urlpatterns = [
    path('detail/<slug:slug>', detail, name="detail"),
    path('delete/<int:id>/<slug:slug>', delete_post, name="delete"),

    path('category/<int:id>/<slug:slug>', category, name='category'),
    path('tag/<int:id>/<slug:slug>', tag, name='tag'),
]
