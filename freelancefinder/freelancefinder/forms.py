"""Forms for the freelancefinder app."""
from contact_form.forms import ContactForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class CrispyContactForm(ContactForm):
    """Contact form with a crispy form helper."""

    def __init__(self, *args, **kwargs):
        """Add crispy helpers."""
        super(CrispyContactForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Send'))
