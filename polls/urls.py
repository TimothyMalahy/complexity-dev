from django.urls import path
from . import views, validation_views


urlpatterns = [
    path("", views.home, name="home"),
    path("topic-detail/<int:topic_id>/", views.topic_detail, name="topic_detail"),
    path("random-topic-detail/", views.random_topic_detail, name="random_topic_detail"),
    path("modal/", views.render_modal, name="render_modal"),
]

htmx_patterns = [
    path("htmx/topics-search/", views.topics_search, name="topics_search"),
    path("htmx/add-topic/", views.add_topic, name="add_topic"),
]

validation_patterns = [
    path("htmx/validate-topic/", validation_views.validate_topic, name="validate_topic"),
]


urlpatterns += htmx_patterns
urlpatterns += validation_patterns
