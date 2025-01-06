from django.urls import path
from .views import verify_user, send_test_email

urlpatterns = [
    path("verify/<str:token>/", verify_user, name="verify_user"),
    path("send-test-email/", send_test_email, name="send_test_email"),
]
