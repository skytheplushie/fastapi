from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return "Главная страница"


@app.get("/user/admin")
async def get_admin_page():
    return "Вы вошли как администратор"


@app.get("/user")
async def get_user_page(user_id: int):
    return f"Вы вошли как пользователь № {user_id}"


@app.post("/user")
async def get_user_info(username: str, age: int):
    return f"Информация о пользователе. Имя: {username}, Возраст: {age}"
