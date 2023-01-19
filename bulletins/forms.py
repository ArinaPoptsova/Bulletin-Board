from django import forms
from .models import Bulletin, Response
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class BulletinForm(forms.ModelForm):
    text = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Bulletin
        fields = ('title', 'category', 'text')


class AddResponseForm(forms.ModelForm):
    # text = forms.CharField(widget=forms.widgets.Textarea)

    class Meta:
        model = Response
        fields = ('text',)
        widgets = {
            'text': forms.widgets.Textarea(),
        }
