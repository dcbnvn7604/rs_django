from django.contrib.auth.views import LoginView

from sr.forms import SRAuthenticationForm


class SRLoginView(LoginView):
    authentication_form = SRAuthenticationForm