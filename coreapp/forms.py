from django import forms
from taggit.forms import TagWidget

from coreapp.models import Shop


class AdminShopForm(forms.ModelForm):
    class Meta:
        model = Shop
        fields = ['name', 'owner', 'location', 'zip_code', 'house_no', 'description', 'tags', 'is_verified']
        widgets = {
            'tags': TagWidget(),
            'location': forms.TextInput(attrs={'list': 'location-suggestions'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['owner'].label_from_instance = lambda obj: obj.get_full_name() or obj.username


class OwnerShopForm(forms.ModelForm):
    class Meta:
        model = Shop
        fields = ['name', 'owner', 'location', 'zip_code', 'house_no', 'description', 'tags']
        widgets = {
            'tags': TagWidget(),
            'location': forms.TextInput(attrs={'list': 'location-suggestions'}),
            'owner': forms.TextInput(attrs={'readonly': 'readonly'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['owner'].label_from_instance = lambda obj: obj.get_full_name() or obj.username
