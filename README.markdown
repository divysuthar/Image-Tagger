# Tagger

Tagger is a Django web application for organizing images by tags. Users can upload images to the `media/` directory, assign tags to them via a POST request, and download a ZIP file where images are organized in a subfolders for each tag (e.g., `tags/subfolder/image.jpg`). Images without tags are placed in `tags/untagged/`. The application is designed for efficient image categorization and export.

## Features
- Generate a downloadable ZIP file with images organized by tags.

## Prerequisites
- Python 3.12 (based on your environment)
- Django 4.2 or compatible version

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/divysuthar/ImageTagger.git
   cd tagger
   ```

2. **Create a Virtual Environment**:
   ```bash
   python -m venv venv
   ```
   Activate it:
   ```bash
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Start the Development Server**:
   ```bash
   python manage.py runserver
   ```
   Access the app at `http://localhost:8000`.

5. **Run code with docker**
  ``` bash
  docker build -t my_django_app .
  docker run -p 8000:8000 my_django_app
  # OR
  docker-compose up
```



## Project Structure
```
Tagger/
├── backend/                    # Django project settings
│   ├── __init__.py
│   ├── settings.py             
│   ├── urls.py                
│   ├── wsgi.py
├── tage/                       
│   ├── __init__.py
│   ├── migrations/             
│   ├── urls.py                 
│   ├── views.py                
├── media/                      
├── venv/                       
├── .gitignore                  
├── manage.py                   
├── README.md                   
```

# Images

## Home page
![Home Page](Images/Home.png)

## Upload Images & Tags
![Imgaes & Tags](Images/Upload_images_tags.png)

## Assigning Tags
![Assigning Tags](Images/Assigning_tags.png)

## Flowchart
![FLowchart](Flowchart.png)