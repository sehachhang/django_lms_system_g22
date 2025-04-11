import datetime
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
class RenewBookInstanceDate(forms.Form):
    renewal_date = forms.DateField(help_text="Enter date between now and 4 weeks (default 3).")

    def clean_renewal_date(self):
        data = self.cleaned_data['renewal_date']

        # Check if a date is not in the past.
        if data < datetime.date.today():
            raise ValidationError(_('Invalid date - renewal in past'))

        # Check if a date is in the allowed range (+4 weeks from today).
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_('Invalid date - renewal more than 4 weeks ahead'))

        # Remember to always return the cleaned data.
        return data
    
class Search_Book(forms.Form):

    search_query = forms.CharField(
        max_length=200,
        required=False,
        label="Search Book:",
        widget=forms.TextInput(attrs={"placeholder": 'Search Book..'})
    )

    def clean_search_query(self):
        data = self.cleaned_data['search_query']

        return data