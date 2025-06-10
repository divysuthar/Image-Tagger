from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
import json
import os
from django.http import HttpResponse, FileResponse
from django.conf import settings
from urllib.parse import unquote, urlparse
import zipfile
from io import BytesIO
from django.views.decorators.csrf import csrf_exempt


def home(request):
    return render(request, "home.html")


@csrf_exempt
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


@csrf_exempt
def assignTags(request):
    # Ensure the request method is POST
    if request.method != "POST":
        return HttpResponse("Method not allowed", status=405)

    # Get tags_data from request.POST
    tags_data = request.POST.get("tags_data")
    if not tags_data:
        return HttpResponse("No tags_data provided", status=400)

    try:
        tags_data = json.loads(tags_data)
        print("Parsed tags_data:", tags_data)

        # Initialize hash map and ZIP file
        tag_hash = {}
        file_contents = BytesIO()
        fs = FileSystemStorage()

        with zipfile.ZipFile(file_contents, "w", zipfile.ZIP_DEFLATED) as zipf:
            for image_url, tags in tags_data.items():
                # Clean the URL to get the file name
                parsed_url = urlparse(image_url)
                path_parts = parsed_url.path.split("/")
                file_name = unquote(path_parts[-1] if path_parts else "")

                tag_hash[file_name] = tags

                image_path = os.path.join(settings.MEDIA_ROOT, file_name)
                if not os.path.exists(image_path):
                    print(f"Warning: Image not found at {image_path}")
                    continue

                with open(image_path, "rb") as image_file:
                    image_data = image_file.read()

                if not tags:
                    # If no tags, place in 'tags/untagged/'
                    zip_path = f"untagged/{file_name}"
                    zipf.writestr(zip_path, image_data)
                else:
                    # In their respective tag folders
                    for tag in tags:
                        zip_path = f"{tag}/{file_name}"
                        zipf.writestr(zip_path, image_data)

        # Rewind the BytesIO buffer
        file_contents.seek(0)

        # Return the ZIP file as a downloadable FileResponse
        response = FileResponse(
            file_contents, as_attachment=True, filename="tags_data.zip"
        )
        print("tag_hash:", tag_hash)  # For debugging
        return response

    except json.JSONDecodeError:
        return HttpResponse("Invalid JSON format in tags_data", status=400)
