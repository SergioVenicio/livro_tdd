from django import forms
from django.core.exceptions import ValidationError

from .models import Item
from django.utils.translation import gettext as _

EMPTY_ITEM_ERROR = _("You can't have an empty list item")
DUPLICATE_ITEM_ERROR = _("You've already got this in your list")


class ItemForm(forms.ModelForm):
    def save(self, for_list=None, commit=True):
        self.instance.list = for_list
        return super().save(commit=commit)

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


class ExistingListItemError(ItemForm):
    def __init__(self, for_list, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance.list = for_list

    def validate_unique(self):
        try:
            self.instance.validate_unique()
        except ValidationError as e:
            e.error_dict = {'text': [DUPLICATE_ITEM_ERROR]}
            self._update_errors(e)
