from django import forms

from lists.models import Item

EMPTY_ITEM_ERROR='你不能输入空项目'
class ItemForm(forms.models.ModelForm):
    class Meta:
        model=Item
        fields=('text',)
        widgets={
            'text':forms.fields.TextInput(attrs={
            'placeholder':'请输入待办事项',
            'class':'form-control form-control-lg',
            }),
        }
        error_messages={
            'text':{'required':EMPTY_ITEM_ERROR}
        }
