from django import forms
from .models import Image

class ImageForm(forms.ModelForm):
    prompt = forms.CharField(max_length=255, widget=forms.TextInput(attrs={
        'placeholder': 'Enter your prompt here...',
        'class': 'form-control',
    }))

    class Meta:
        model = Image
        fields = ['prompt']
