# from django.shortcuts import render


# def index(request):
#     return render(request, 'index.html')

# def about(request):
#     return render(request, 'about.html')

# def register(request):
#     return render(request, 'register.html')

# def login(request):
#     return render(request, 'login.html')

# def userhome(request):
#     return render(request, 'home.html')

# def caption(request):
#     return render(request, 'caption.html')

# def history(request):
#     return render(request, 'history.html')

# def logout(request):
#     return render(request, 'index.html')


from django.shortcuts import render, redirect
from .models import Registration, CaptionHistory
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration

from .logic import *

# Load BLIP model once
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")


# ---------------- PUBLIC PAGES ----------------

def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')


def register(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        password = request.POST.get("password")

        Registration.objects.create(
            name=name,
            email=email,
            password=password
        )
        return redirect('login')

    return render(request, 'register.html')


def login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user = Registration.objects.get(email=email, password=password)
            request.session['user_id'] = user.id
            request.session['user_name'] = user.name
            return redirect('userhome')
        except Registration.DoesNotExist:
            return render(request, 'login.html', {'error': 'Invalid email or password'})

    return render(request, 'login.html')


# ---------------- USER PAGES ----------------
def userhome(request):
    if 'user_id' not in request.session:
        return redirect('login')

    context = {
        'username': request.session.get('user_name')
    }
    return render(request, 'home.html', context)


def caption(request):
    if 'user_id' not in request.session:
        return redirect('login')
    
    caption_text = None
    image_url = None

    if request.method == "POST":
        image_file = request.FILES.get("image")
        user = Registration.objects.get(id=request.session['user_id'])

        if image_file:
            file_path = f'media/{image_file.name}'
            with open(file_path, 'wb+') as e:
                for chunk in image_file.chunks():
                    e.write(chunk)

            image = Image.open(file_path).convert("RGB")
            inputs = processor(image, return_tensors="pt")
            output = model.generate(**inputs)
            caption_text = processor.decode(output[0], skip_special_tokens=True)

            user_data = {
                'Type': 'ImageStore',
                "user_id": user.id,
                "image_data": file_path,
                "caption": caption_text
            }

            blockchain_status = addNewData(user_data)
            print('blockchain:', blockchain_status)

    data = retrieveData()

    filtered_data = [entry for entry in data if entry['user_id'] == request.session['user_id']]

    most_recent_data = sorted(filtered_data, key=lambda x: x['sumID'], reverse=True)

    if most_recent_data:
        image_url = most_recent_data[0]['image_data']
        caption_text = most_recent_data[0]['caption']

    return render(request, 'caption.html', {
        'caption': caption_text,
        'image_url': image_url,
    })



def history(request):
    if 'user_id' not in request.session:
        return redirect('login')
    blockchain_data = retrieveData()
    user_history = [post for post in blockchain_data if post['user_id'] == request.session['user_id']]

    context = {
        'history': user_history,
        'username': request.session.get('user_name')
    }

    return render(request, 'history.html', context)



def logout(request):
    request.session.flush()
    return redirect('index')
