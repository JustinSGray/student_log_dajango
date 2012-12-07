from django.contrib.auth.forms import AuthenticationForm as AF
from django.utils.translation import ugettext_lazy as _

from django.forms import BooleanField
from bootstrap.forms import BootstrapMixin

    

class AuthenticationForm(BootstrapMixin, AF):
    #monkey patch to adjust error messages
    error_messages = {
            'invalid_login': _("Please enter a correct username and password. "
                               "Note that both fields are case-sensitive."),
            'no_cookies': _("Your Web browser doesn't appear to have cookies "
                            "enabled. Cookies are required for logging in."),
            'inactive': _("This account is inactive. Please check your email for you activation code"),
        }  
    
    remember_me = BooleanField (
        label = _( 'Remember Me' ),
        initial = False,
        required = False,
        )
