from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model


class UserCreateForm(UserCreationForm):
    class Meta:
        fields = ('username', 'email', 'password1', 'password2',
                  'avatar', 'display_name', 'twitter', 'bio', 'available',
                  'monthly', 'thumbnail_price', 'channel_art_price')
        model = get_user_model()  # need this for forms as the cant take strings to define the model

    def __init__(self, *args, **kwargs):
        super(UserCreateForm, self).__init__(*args, **kwargs)

        # labels and placeholders
        self.fields['email'].label = 'Email address'
        self.fields['thumbnail_price'].min_value = 0.25

        # required fields
        self.fields['username'].required = True
        self.fields['thumbnail_price'].required = True
        self.fields['channel_art_price'].required = True


rating_choices = (
    ('0', '0-25'), ('25', '25-50'), ('50', '50-75'), ('75', '75-100'), ('100', '100+'),
)
thumbnail_choices = (
    ('0', '0-1'), ('1', '1-2'), ('2', '2+'),
            )


class FilterDesigners(forms.Form):
    rating = forms.ChoiceField(widget=forms.Select(), choices=rating_choices, required=False, )
    can_work = forms.BooleanField(required=False, label='Available')
    thumbnail_cost = forms.ChoiceField(
        widget=forms.Select(), choices=thumbnail_choices, required=False, label='Thumbnail Price Range')
    does_monthly = forms.BooleanField

