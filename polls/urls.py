from django.urls import path
from .views import home, vote, render_modal

urlpatterns = [
    path("", home, name="home"),
    path("vote/<int:topic_id>/", vote, name="vote"),
    path("modal/", render_modal, name="render_modal"),
]
