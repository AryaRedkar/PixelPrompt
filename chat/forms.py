from django import forms
from .models import Image

class ImageForm(forms.ModelForm):
    prompt = forms.CharField(max_length=255, widget=forms.Textarea(attrs={
        'placeholder': '''Describe the image you want to generate...
Try: &quot;Fantasy landscape with dragons and waterfalls&quot;, &quot;Cyberpunk city at night&quot;''',
        
        'class': 'w-full p-4 pr-20 rounded-xl border border-neutral-300 focus:border-primary-500 focus:ring focus:ring-primary-200 resize-none h-24 transition duration-200',
    }))

    class Meta:
        model = Image
        fields = ['prompt']
