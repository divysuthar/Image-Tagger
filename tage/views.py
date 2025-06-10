from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
import json
import os
import shutil
from django.http import HttpResponse
from django.conf import settings
from urllib.parse import unquote, urlparse
import zipfile
from io import BytesIO

# Create your views here.


def home(request):
    return render(request, "home.html")


def takeImages(request):
    if request.method == "POST":
        # Handling images
        images = request.FILES.getlist("images")
        fs = FileSystemStorage()
        saved_paths = []
        for image in images:
            file_name = fs.save(image.name, image)
            file_url = fs.url(file_name)
            saved_paths.append(file_url)
        print("Saved image paths:")
        print(saved_paths)

        # Handling tags
        tags = request.POST.get("tags")
        try:
            tags = json.loads(tags)
            tags = [tag["value"] for tag in tags]
        except json.JSONDecodeError:
            tags = []

        return render(
            request, "assign_tags.html", {"images": saved_paths, "suggested_tags": tags}
        )

    return render(request, "takeImages.html")


def assignTags(request):
    if request.method == "POST":
        tags_json = request.POST.get("tags_data")

        try:
            tag_map = json.loads(tags_json)
            print("MEDIA_ROOT:", settings.MEDIA_ROOT)
            print("MEDIA_ROOT exists:", os.path.exists(settings.MEDIA_ROOT))
            print("MEDIA_ROOT writable:", os.access(settings.MEDIA_ROOT, os.W_OK))
            
            temp_dir = os.path.join(settings.MEDIA_ROOT, "tagged_temp")
            print("Full temp_dir path:", temp_dir)
            if not os.path.exists(temp_dir):
                os.makedirs(temp_dir)
                print("Created temporary directory for tagged images.")

            # print("Tag map:", tag_map)
            # print("Temp directory created at:", temp_dir)

            for image_url, tags in tag_map.items():
                # Convert URL to file path
                relative_path = unquote(urlparse(image_url).path.lstrip("/"))
                full_image_path = os.path.join(settings.BASE_DIR, relative_path)
                print("Full image path:", full_image_path)
                if not os.path.exists(full_image_path):
                    continue

                for tag in tags:
                    print("Processing tag:", tag)
                    tag_folder = os.path.join(temp_dir, tag)
                    os.makedirs(tag_folder, exist_ok=True)
                    print("Tag folder created at:", tag_folder)

                    image_name = os.path.basename(full_image_path)
                    dest_path = os.path.join(tag_folder, image_name)
                    print("Destination path for image:", dest_path)

                    if not os.path.exists(dest_path):  # avoid duplicates
                        shutil.copy(full_image_path, dest_path)

            # Create ZIP file
            zip_buffer = BytesIO()
            with zipfile.ZipFile(zip_buffer, "w") as zip_file:
                for root, _, files in os.walk(temp_dir):
                    for file in files:
                        full_path = os.path.join(root, file)
                        arcname = os.path.relpath(full_path, temp_dir)
                        zip_file.write(full_path, arcname)

            # Cleanup temp folder
            shutil.rmtree(temp_dir)

            zip_buffer.seek(0)
            response = HttpResponse(zip_buffer, content_type="application/zip")
            response["Content-Disposition"] = "attachment; filename=tagged_images.zip"
            return response
        except Exception as e:
            print("Error:", e)

        return redirect("home")
