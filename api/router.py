from fastapi import APIRouter, Depends, Request, status, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from config.database import get_db
from typing import Union
from api import crud, autocomplete
from api.autocomplete import SubjectName

router = APIRouter(prefix="/api/post")

templates = Jinja2Templates(directory="templates")
# head = autocomplete.returnTrie()
subjectName = SubjectName()
head = subjectName.returnTrie_ver2()

@router.get("/")
def return_value(q : Union[str, None] = None):
    candidate = subjectName.searchTrie(q)
    return {"brand" : candidate}

# @router.get("/")
# def return_value(q: Union[str, None] = None):
#     print(q)
#     if q is None:
#         return None
#     else:
#         current = head
#         for key in q:
#             if key in current.children:
#                 current = current.children[key]
#             else:
#                 break
#         return {"brand": current.data if isinstance(current.data, list) else []}

@router.get("/list", response_class=HTMLResponse)
def post_list_html(request: Request, db: Session = Depends(get_db), q: Union[str, None] = None):
    _post_list = crud.get_post_list(db) 
    return templates.TemplateResponse("post_list.html", {"request": request, "post_list" : _post_list})


@router.get("/search", response_class=HTMLResponse)
def search_post_html(request : Request, keyword : str=None, db : Session=Depends(get_db)):
    _post_list_ = crud.search_posts(db, keyword)
    return templates.TemplateResponse("post_list.html", {"request" : request, "post_list" : _post_list_})
