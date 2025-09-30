import os, json
from fastapi import FastAPI, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from category import Category

BASE_DIR = os.path.dirname(__file__)
DATA_FILE = os.path.join(BASE_DIR, "categories.json")

app = FastAPI()
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            raw = json.load(f)
            return {k: Category.from_dict(v) for k, v in raw.items()}
    return {}

def save_data(categories):
    raw = {k: v.to_dict() for k, v in categories.items()}
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(raw, f, ensure_ascii=False, indent=2)

categories = load_data()

@app.get("/")
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "categories": list(categories.values())})

@app.get("/add")
def add_form(request: Request):
    return templates.TemplateResponse("add_category.html", {"request": request})

@app.post("/add")
def add_category(name: str = Form(...), description: str = Form("")):
    cat = Category(name=name, description=description)
    categories[cat.id] = cat
    save_data(categories)
    return RedirectResponse("/", status_code=303)

@app.get("/category/{cat_id}")
def details(request: Request, cat_id: str):
    cat = categories.get(cat_id)
    return templates.TemplateResponse("category_details.html", {"request": request, "category": cat})

@app.get("/category/{cat_id}/edit")
def edit_form(request: Request, cat_id: str):
    cat = categories.get(cat_id)
    return templates.TemplateResponse("edit_category.html", {"request": request, "category": cat})

@app.post("/category/{cat_id}/edit")
def edit_category(cat_id: str, name: str = Form(...), description: str = Form("")):
    cat = categories.get(cat_id)
    if cat:
        cat.update(name=name, description=description)
        save_data(categories)
    return RedirectResponse("/", status_code=303)

@app.post("/category/{cat_id}/toggle")
def toggle_category(cat_id: str):
    cat = categories.get(cat_id)
    if cat:
        if cat.is_active:
            cat.deactivate()
        else:
            cat.activate()
        save_data(categories)
    return RedirectResponse("/", status_code=303)

@app.post("/category/{cat_id}/delete")
def delete_category(cat_id: str):
    if cat_id in categories:
        del categories[cat_id]
        save_data(categories)
    return RedirectResponse("/", status_code=303)

