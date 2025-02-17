from django.urls import path
from .views import (
    verify_user,
    send_test_email,
    login_user,
    register_user,
    render_login_modal,
    render_register_modal,
)
from .validation_views import *

urlpatterns = [
    path("verify/<str:token>/", verify_user, name="verify_user"),
    path("send-test-email/", send_test_email, name="send_test_email"),
]

htmx_patterns = [
    path("htmx/login-user/", login_user, name="login_user"),
    path("htmx/register-user/", register_user, name="register_user"),
    path("htmx/render-login-modal/", render_login_modal, name="render_login_modal"),
    path("htmx/render-register-modal/", render_register_modal, name="render_register_modal"),
]

validation_patterns = [
    path("htmx/user-registration-email/", user_registration_email, name="user_registration_email"),
    path(
        "htmx/user-registartion-pass/",
        user_registration_pass,
        name="user_registration_pass",
    ),
    path("htmx/validate-email/", validate_email, name="validate_email"),
    path("htmx/validate-password/", validate_password, name="validate_password"),
    path("htmx/validate-confirm-password/", validate_password, name="validate_confirm_password"),
]

urlpatterns += htmx_patterns
urlpatterns += validation_patterns
