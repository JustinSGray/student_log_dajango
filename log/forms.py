from django.contrib.auth.forms import AuthenticationForm as AF
from django.utils.translation import ugettext_lazy as _

from django.forms import BooleanField

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
    

class AuthenticationForm(AF):
    
    remember_me = BooleanField (
        label = _( 'Remember Me' ),
        initial = False,
        required = False,
        )

    def __init__(self,*args,**kwargs): 
        self.helper = FormHelper()

        #self.helper.form_id = 'id-exampleForm'
        #self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.form_action = '/login/'

        self.helper.add_input(Submit('submit', 'Submit'))
        super(AuthenticationForm,self).__init__(*args,**kwargs)
