from api import crud, schema, models
from fastapi import APIRouter, Depends, Request, status, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from config.database import get_db
from typing import Union


router = APIRouter(
    prefix = "/api/post",
)

templates = Jinja2Templates(directory="templates")

@router.get("/list", response_class=HTMLResponse)
def post_list_html(request : Request, db : Session=Depends(get_db)):
    _post_list = crud.get_post_list(db)
    return templates.TemplateResponse("post_list.html", {"request" : request, "post_list" : _post_list})

@router.get("/search", response_class=HTMLResponse)
def search_post_html(request : Request, keyword : str=None, db : Session=Depends(get_db)):
    _post_list_ = crud.search_posts(db, keyword)
    return templates.TemplateResponse("post_list.html", {"request" : request, "post_list" : _post_list_})
