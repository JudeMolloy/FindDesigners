from django import forms


rating_choices = (
    ('0', '0-25'), ('25', '25-50'), ('50', '50-75'), ('75', '75-100'), ('100', '100+'),
)
thumbnail_choices = (
    ('0', '£0-1'), ('1', '£1-2'), ('2', '£2+'),
            )


class FilterDesigners(forms.Form):
    rating = forms.ChoiceField(widget=forms.Select(), choices=rating_choices, required=False, )
    can_work = forms.BooleanField(required=False, label='Available')
    thumbnail_cost = forms.ChoiceField(
        widget=forms.Select(), choices=thumbnail_choices, required=False, label='Thumbnail Price Range')
    does_monthly = forms.BooleanField
