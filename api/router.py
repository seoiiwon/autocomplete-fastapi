from fastapi import APIRouter, Depends, Request, status, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from config.database import get_db
from typing import Union
from api import crud, autocomplete
from api.autocomplete import SubjectName, returnTrie_ver3

router = APIRouter(prefix="/api/post")
templates = Jinja2Templates(directory="templates")

# TRIE로 AUTOCOPLETE할 때 서버
# head = autocomplete.returnTrie()
# trie = Trie()
# @router.get("/")
# def return_value(q : Union[str, None]=None):
#     if q is None:
#         return None
#     else:
#         current = head
#         for key in q:
#             if key in current.children:
#                 current = current.children[key]
#             else:
#                 break
#         return {"brand" : current.data if isinstance(current.data, list) else []}

# JAMO 포함 AUTOCOMPLETE할 때 서버
# subjectName = SubjectName()

# @router.get("/")
# def return_value(q : Union[str, None] = None):
#     result = subjectName.searchTrie(q)
#     return {"brand" : result}


@router.get("/")
def return_value(q: str = None):
    result = returnTrie_ver3(q)
    return {"brand": result if q is not None else []}


@router.get("/list", response_class=HTMLResponse)
def post_list_html(request: Request, db: Session = Depends(get_db), q: Union[str, None] = None):
    _post_list = crud.get_post_list(db) 
    return templates.TemplateResponse("post_list.html", {"request": request, "post_list" : _post_list})


@router.get("/search", response_class=HTMLResponse)
def search_post_html(request : Request, keyword : str=None, db : Session=Depends(get_db)):
    _post_list_ = crud.search_posts(db, keyword)
    return templates.TemplateResponse("post_list.html", {"request" : request, "post_list" : _post_list_})
