from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
import json
# Create your views here.


def home(request):
    return render(request, 'home.html')

def takeImages(request):
    if request.method == 'POST':
        # Handling images 
        images = request.FILES.getlist('images')
        fs = FileSystemStorage()
        saved_paths = []
        for image in images:
            file_name = fs.save(image.name, image)
            file_url = fs.url(file_name)
            saved_paths.append(file_url)
        print(saved_paths)

        # Handling tags
        tags = request.POST.get('tags')
        try:  
            tags = json.loads(tags)
            tags = [tag['value'] for tag in tags]
        except json.JSONDecodeError:
            tags = []
        
        return render(request, 'assign_tags.html', {
            'images': saved_paths,
            'suggested_tags': tags
        })
        
    return render(request, 'takeImages.html')

def assignTags(request):
    if request.method == 'POST':
        tags_json = request.POST.get('tags_data')

        try:
            tag_map = json.loads(tags_json)
            for image_url, tags in tag_map.items():
                print(f"{image_url}: {tags}")
                # Save to DB
        except Exception as e:
            print("Error:", e)

        return redirect('home')