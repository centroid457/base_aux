# ============================================================
# FASTAPI – ПОЛНЫЙ СПРАВОЧНИК ПО POST ЗАПРОСАМ
# Запуск: uvicorn main:app --reload
# Документация: http://localhost:8000/docs
# ============================================================

from fastapi import FastAPI, File, Form, UploadFile, HTTPException, Depends, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
import uvicorn
import json

app = FastAPI(
    title="FastAPI POST Examples",
    description="Демонстрация всех способов обработки POST запросов",
    version="1.0.0"
)

# -------- 1. МОДЕЛИ ДЛЯ ВАЛИДАЦИИ (Pydantic) --------
class ItemCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=50, description="Название товара")
    price: float = Field(..., gt=0, description="Цена")
    tags: Optional[List[str]] = []

    # Кастомная валидация
    @field_validator('price')
    def price_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError('price must be greater than 0')
        return v

# -------- 2. БАЗОВЫЙ POST С JSON ТЕЛОМ --------
@app.post("/items/", response_model=ItemCreate)
async def create_item(item: ItemCreate):
    """
    Ожидает JSON с полями name, price, tags (опционально).
    Возвращает созданный объект с присвоенным ID.
    """
    # Симуляция сохранения в БД
    saved_item = item.dict()
    saved_item['id'] = 123  # например, из БД
    return saved_item

# -------- 3. POST С ФАЙЛОМ (один файл) --------
@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    """
    Загрузка одного файла (multipart/form-data).
    Возвращает имя, размер, тип содержимого.
    """
    contents = await file.read()
    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "size": len(contents),
        "first_100_bytes": contents[:100].decode('utf-8', errors='ignore')
    }

# -------- 4. POST С НЕСКОЛЬКИМИ ФАЙЛАМИ --------
@app.post("/upload-multiple/")
async def upload_multiple(files: List[UploadFile] = File(...)):
    """
    Загрузка нескольких файлов одновременно.
    """
    result = []
    for file in files:
        content = await file.read()
        result.append({
            "filename": file.filename,
            "size": len(content)
        })
    return {"uploaded": result}

# -------- 5. POST С ДАННЫМИ ФОРМЫ (application/x-www-form-urlencoded) --------

@app.post("/form/")
async def process_form(
    username: str = Form(..., min_length=3, max_length=20),
    password: str = Form(..., min_length=6),
    remember: bool = Form(False)
):
    """
    Получение данных из HTML-формы (не JSON).
    """
    return {
        "username": username,
        "password_length": len(password),
        "remember": remember
    }

# -------- 6. СМЕШАННЫЙ ЗАПРОС: ФАЙЛ + JSON-ПОЛЕ (через Form) --------

@app.post("/mixed/")
async def mixed_request(
    file: UploadFile = File(...),
    description: str = Form(...),
    category: str = Form("general")
):
    """
    Принимает файл и текстовые поля в одном multipart запросе.
    """
    content = await file.read()
    return {
        "file": {
            "name": file.filename,
            "size": len(content)
        },
        "description": description,
        "category": category
    }

# -------- 7. ПОЛУЧЕНИЕ СЫРОГО ТЕЛА (RAW) --------

@app.post("/raw/")
async def raw_request(request: Request):
    """
    Принимает сырое тело запроса (текст, JSON, бинарные данные) как есть.
    """
    body_bytes = await request.body()
    try:
        # Пытаемся интерпретировать как JSON
        data = json.loads(body_bytes)
        return {"type": "json", "data": data}
    except json.JSONDecodeError:
        # Если не JSON, возвращаем как текст или бинарные данные
        try:
            text = body_bytes.decode('utf-8')
            return {"type": "text", "data": text[:200]}  # обрезаем для демонстрации
        except UnicodeDecodeError:
            return {"type": "binary", "size": len(body_bytes)}

# -------- 8. ИСПОЛЬЗОВАНИЕ ЗАВИСИМОСТЕЙ (DEPENDENCIES) --------

# Фейковая проверка токена
def verify_token(authorization: Optional[str] = None):
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing Authorization header")
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid token format")
    token = authorization.split(" ")[1]
    if token != "secret123":
        raise HTTPException(status_code=403, detail="Invalid token")
    return {"user": "admin", "role": "admin"}

@app.post("/secure/")
async def secure_endpoint(item: ItemCreate, user_info: dict = Depends(verify_token)):
    """
    Доступен только с валидным Bearer токеном.
    Токен: 'secret123' (для примера)
    """
    return {
        "message": "Access granted",
        "user": user_info,
        "item": item
    }

# -------- 9. ОБРАБОТКА ОШИБОК И HTTPException --------

@app.post("/with-error/")
async def with_error(should_fail: bool = Form(False), message: str = Form("Ошибка по запросу")):
    """
    Демонстрация явного выброса HTTPException с разными кодами.
    """
    if should_fail:
        raise HTTPException(status_code=400, detail=message)
    return {"status": "ok", "message": "Запрос выполнен успешно"}

# -------- 10. ПОДДЕРЖКА OPTIONS (CORS) – если нужно --------

# from fastapi.middleware.cors import CORSMiddleware
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# -------- 11. ЗАПУСК (если файл запущен напрямую) --------

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)


# ============================================================
# ПРИМЕРЫ FETCH ДЛЯ КАЖДОГО ЭНДПОИНТА
# ============================================================
#
# 1. POST /items/ (JSON)
# ----------------------
# fetch('http://localhost:8000/items/', {
#     method: 'POST',
#     headers: { 'Content-Type': 'application/json' },
#     body: JSON.stringify({
#         name: 'Телефон',
#         price: 599.99,
#         tags: ['electronics', 'mobile']
#     })
# }).then(r => r.json()).then(console.log)
#
# 2. POST /upload/ (один файл)
# ----------------------------
# const formData = new FormData();
# formData.append('file', document.querySelector('input[type=file]').files[0]);
# fetch('http://localhost:8000/upload/', {
#     method: 'POST',
#     body: formData
# }).then(r => r.json()).then(console.log)
#
# 3. POST /upload-multiple/ (несколько файлов)
# --------------------------------------------
# const fd = new FormData();
# const files = document.querySelector('input[type=file]').files;
# for (let i = 0; i < files.length; i++) {
#     fd.append('files', files[i]);
# }
# fetch('http://localhost:8000/upload-multiple/', {
#     method: 'POST',
#     body: fd
# }).then(r => r.json()).then(console.log)
#
# 4. POST /form/ (URL-encoded форма)
# ----------------------------------
# const urlEncoded = new URLSearchParams({
#     username: 'john_doe',
#     password: '123456',
#     remember: 'true'
# });
# fetch('http://localhost:8000/form/', {
#     method: 'POST',
#     headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
#     body: urlEncoded
# }).then(r => r.json()).then(console.log)
#
# 5. POST /mixed/ (файл + поля формы)
# -----------------------------------
# const fd = new FormData();
# fd.append('file', fileInput.files[0]);
# fd.append('description', 'My file');
# fd.append('category', 'images');
# fetch('http://localhost:8000/mixed/', {
#     method: 'POST',
#     body: fd
# }).then(r => r.json()).then(console.log)
#
# 6. POST /raw/ (сырое тело)
# --------------------------
# fetch('http://localhost:8000/raw/', {
#     method: 'POST',
#     body: 'Hello, server!'
# }).then(r => r.json()).then(console.log)
#
# 7. POST /secure/ (с токеном)
# -----------------------------
# fetch('http://localhost:8000/secure/', {
#     method: 'POST',
#     headers: {
#         'Content-Type': 'application/json',
#         'Authorization': 'Bearer secret123'
#     },
#     body: JSON.stringify({
#         name: 'Ноутбук',
#         price: 1200.00
#     })
# }).then(r => r.json()).then(console.log)
#
# 8. POST /with-error/ (ошибка)
# -----------------------------
# const formData = new FormData();
# formData.append('should_fail', 'true');
# formData.append('message', 'Тестовая ошибка');
# fetch('http://localhost:8000/with-error/', {
#     method: 'POST',
#     body: formData
# }).then(r => r.json()).catch(e => console.error('Ошибка:', e))