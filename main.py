from fastapi import FastAPI,Response,status,HTTPException
from typing import Optional
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
app = FastAPI()

class Post(BaseModel):
    title:str
    content: str
    published: bool = True
    rating: Optional[int] =None
my_posts =[{"title":"title of post 1","content": "content of post 1","id":1},{"title":"favorite food","content":"like pizza","id":2}]

def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p
def find_index_post(id):
    for i,p in enumerate(my_posts):
        if p['id'] == id:
            return i

@app.get("/")
async def root():
    return {"message": "Hello World"}
@app.get("/posts")
def get_post():
    return {"data":"this is your posts"}

@app.post("/posts")
def creat_post(post: Post):
    post_dict = post.dict()
    post_dict['id']= randrange(0,10000)
    my_posts.append(post_dict)
    return {"data":post_dict}

@app.get("/posts/{id}")
def get_post(id:int,response = Response):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post {id} not found")
        #response.status_code = status.HTTP_404_NOT_FOUND
        #return  {"post":f"not found"}
    return {"post_detail":post}

@app.delete("/posts/{id}")
def delete_post(id:int):
    index = find_index_post(id)
    my_posts.pop(index)
    return {'message':"post was sucessful"}
@app.put("/posts/{id}")
def update_post(id:int,post : Post):
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail = f"not exist")
    post_dict = post.dict()
    post_dict['id'] = id
    my_posts[index] = post_dict
    print(post)
    return {"data":post_dict}