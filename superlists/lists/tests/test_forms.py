from django.test import TestCase
from .. import forms
from ..models import List, Item


class ItemFormTest(TestCase):
    def test_form_renders_item_text_input(self):
        list_ = List.objects.create()
        form = forms.ExistingListItemError(for_list=list_)
        expected_text = form.as_p()
        self.assertIn('placeholder="Enter a to-do item"', expected_text)
        self.assertIn('class="form-control input-lg"', expected_text)

    def test_form_validation_for_blank_items(self):
        list_ = List.objects.create()
        form = forms.ExistingListItemError(for_list=list_, data={'text': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['text'],
            [forms.EMPTY_ITEM_ERROR]
        )

    def test_form_validation_for_duplicate_items(self):
        list_ = List.objects.create()
        Item.objects.create(list=list_, text='no twins!')
        form = forms.ExistingListItemError(for_list=list_, data={'text': 'no twins!'})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'], [forms.DUPLICATE_ITEM_ERROR])

    def test_save_handles_saving_to_a_list(self):
        list_ = List.objects.create()
        form = forms.ItemForm(data={'text': 'do me'})
        new_item = form.save(for_list=list_)
        self.assertEqual(new_item, Item.objects.first())
        self.assertEqual(new_item.text, 'do me')
        self.assertEqual(new_item.list, list_)