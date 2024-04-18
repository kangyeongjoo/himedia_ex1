from fastapi import FastAPI, Form, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def form(request: Request):
    return templates.TemplateResponse("basic.html", {"request": request, "submitted_text": None})
