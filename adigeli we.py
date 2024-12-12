from fastapi import FastAPI, Path, HTTPException, Request
from typing import Annotated, List
from pydantic import BaseModel
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

app = FastAPI(swagger_ui_parameters=({"TryItOut Enabled": True}))
templates = Jinja2Templates

# users = {'1': 'Имя: Example, возраст: 18'}
users = []


class User(BaseModel):
    id: int
    username: str
    age: int


@app.get("/")
async def root(request: Request) -> HTMLResponse:
    return templates.TemplateResponse('users.html', {'request': request, 'user': user})


@app.get("/user/{user_id}")
async def get_user_page(request: Request,
                        user_id: Annotated[int, Path(ge=1, le=100, description="Enter User ID", example=1)]) -> HTMLResponse:
    for user in users:
        if int(user_id) == user_id:
            return templates.TemplateResponse('user.html', {'request': request, 'user': user})
    raise HTTPException(status_code=404, detail='User was not found')


@app.get('/users')
async def get_users() -> List[User]:
    return users


@app.post('/user/{username}/{age}')
async def add_user(username: Annotated[str, Path(min_length=5, max_length=20,
                                                 description='Enter username', example='UrbanUser')],
                   age: Annotated[int, Path(ge=18, le=120, description='Enter age', example='24')]) -> User:
    user_id = max(users, key=lambda x: int(x.id)).id + 1 if users else 1
    user = User(id=user_id, username=username, age=age)
    users.append(user)
    return user


@app.put('/user/{user_id}/{username}/{age}')
async def update_user(user_id: Annotated[int, Path(ge=1, le=100, description='Enter User ID', example='1')],
                      username: Annotated[str, Path(min_length=5, max_length=20,
                                                    description='Enter username', example='UrbanUser')],
                      age: Annotated[int, Path(ge=18, le=120, description='Enter age', example='24')]) -> User:
    for user in users:
        if user.id == user_id:
            user.username = username
            user.age = age
            return user
    raise HTTPException(status_code=404, detail="User was not found")


@app.delete('/user/{user_id}')
async def users_del(user_id: Annotated[int, Path(ge=1, le=100, description='Enter User ID', example='1')]) -> User:
    for user in users:
        if user.id == user_id:
            users.remove(user)
            return user
