from django.test import TestCase
from ..forms import ItemForm, EMPTY_ITEM_ERROR


class ItemFormTest(TestCase):
    def test_form_renders_item_text_inputs(self):
        form = ItemForm()
        expected_text = form.as_p()
        self.assertIn('placeholder="Enter a to-do item"', expected_text)
        self.assertIn('class="form-control input-lg"', expected_text)

    def test_form_validation_for_blank_items(self):
        form = ItemForm(data={'text': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['text'],
            [EMPTY_ITEM_ERROR]
        )