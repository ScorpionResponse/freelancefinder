
from django.views.generic.base import TemplateView


class UserProfileView(TemplateView):

    template_name = "users/profile.html"
