import torch
from torch import autocast
from diffusers import StableDiffusionPipeline
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Chat, Image
from .forms import ImageForm
from io import BytesIO
from django.core.files.base import ContentFile
from PIL import Image as PILImage
from django.contrib.auth import logout

# Initialize the Stable Diffusion pipeline
model_id = "runwayml/stable-diffusion-v1-5"
device = "cuda" if torch.cuda.is_available() else "cpu"

pipe = StableDiffusionPipeline.from_pretrained(
    model_id,
    torch_dtype=torch.float16 if device == "cuda" else torch.float32,
    use_auth_token="your_auth_token"  # Replace with HuggingFace token
)
pipe.to(device)

@login_required
def dashboard(request):
    return redirect('chat_detail', chat_id='none')

@login_required
def chat_detail(request, chat_id):
    if(chat_id == 'none'):
        if request.method == 'POST':
          title = request.POST.get('title')
          if title:
            Chat.objects.create(title=title, user=request.user)
            print(11)
            return redirect('chat_detail', chat_id=title)
        return render(request, 'chat_detail1.html', {'chaters': Chat.objects.filter(user=request.user), 'nope': "nope"})
    
    chat = get_object_or_404(Chat, title=chat_id, user=request.user)
    images = chat.images.all()
    form = ImageForm()
    chaters = Chat.objects.filter(user=request.user)

    if request.method == 'POST':
        title = request.POST.get('title')
        if title:
            Chat.objects.create(title=title, user=request.user)
            print(11)
            return redirect('chat_detail', chat_id=title)
        form = ImageForm(request.POST)
        if form.is_valid():
            # Generate image using Stable Diffusion
            prompt = form.cleaned_data['prompt']
            with autocast(device):
              generated_image = pipe(prompt, guidance_scale=8.5)["images"][0]

            # Convert PIL image to an in-memory file
            image_buffer = BytesIO()
            generated_image.save(image_buffer, format="PNG")
            image_buffer.seek(0)

            # Save generated image to the database
            if chat.images.count() >= 2:
                     chat.images.order_by('created_at').first().delete()

            new_image = Image(chat=chat, prompt=prompt)
            new_image.image.save(f"{chat.id}_{prompt}.png", ContentFile(image_buffer.read()), save=True)
            new_image.save()
            return redirect('chat_detail', chat_id=chat_id)

    return render(request, 'chat_detail1.html', {'chat': chat, 'images': images, 'form': form, 'chaters': chaters})

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import render, redirect

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Automatically log in the user after registration
            Chat.objects.create(title="First_Chat", user=request.user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

