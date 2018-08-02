from django import forms
from .models import Item
from django.utils.translation import gettext as _

EMPTY_ITEM_ERROR = _("You can't have an empty list item")

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ('text', )
        widgets = {
            'text': forms.TextInput(attrs={
                'placeholder': 'Enter a to-do item',
                'class': 'form-control input-lg'
            })
        }
        error_messages = {
            'text': {'required': EMPTY_ITEM_ERROR}
        }