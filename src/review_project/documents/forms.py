from django import forms
from django.core.validators import FileExtensionValidator
from django.utils.timezone import now

from documents.models import Document


class ChangeDocForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('file',)

    file = forms.FileField(
        widget=forms.FileInput(attrs={'class': 'form-control', 'placeholder': 'Обновить файл'}),
        validators=[FileExtensionValidator(allowed_extensions=['py'])],
        label='Обновить файл')

    def save(self, commit=True):
        self.instance.updated = now()
        self.instance.status = Document.UPDATED
        return super().save(commit=True)


class CreateDocForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('file',)

    file = forms.FileField(
        widget=forms.FileInput(attrs={'class': 'form-control', 'placeholder': 'Загрузить файл'}),
        validators=[FileExtensionValidator(allowed_extensions=['py'])],
        label='Загрузить файл', )
