from django.test import TestCase

from lists.forms import ItemForm,EMPTY_ITEM_ERROR
from lists.models import Item,List



# Create your tests here.
class ItemFormTest(TestCase):

    def test_home_page_returns_correct_html(self):
        form=ItemForm()
        self.assertIn('placeholder="请输入待办事项"',form.as_p())
        self.assertIn('class="form-control form-control-lg"',form.as_p())

    def test_form_validation_for_blank_items(self):
        form=ItemForm(data={'text':''})
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['text'],
            [EMPTY_ITEM_ERROR]
        )
    
    
    def test_form_save_handles_saving_to_a_list(self):
        list_=List.objects.create()
        form=ItemForm(data={'text':'do somedata'})
        new_item=form.save(for_list=list_)
        self.assertEqual(new_item,Item.objects.first())
        self.assertEqual(new_item.text,'do somedata')
        self.assertEqual(new_item.list,list_)


