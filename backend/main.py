from fastapi import FastAPI, Body, HTTPException, File, UploadFile, Form
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import json, os, asyncio, random
from datetime import datetime
from typing import Optional
import shutil

# 匯入 SQLAdmin 與資料庫模組
from sqladmin import Admin, ModelView
from .database import engine, Problem, SessionLocal
from .model import process_with_qwen_vl, process_quiz_grading # 載入新增的多圖文批改函式

app = FastAPI()

from fastapi.staticfiles import StaticFiles
app.mount("/static", StaticFiles(directory="static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 註冊 SQLAdmin 後台
admin = Admin(app, engine)

class ProblemAdmin(ModelView, model=Problem):
    column_list = [Problem.id, Problem.category, Problem.question_text, Problem.image_path]
    column_searchable_list = [Problem.category, Problem.question_text]
    name = "數學題庫"
    name_plural = "數學題庫管理"
    icon = "fa-solid fa-calculator"

admin.add_view(ProblemAdmin)

# ================= 會員與歷史紀錄功能 =================
USER_FILE = "users.json"

def load_users():
    if not os.path.exists(USER_FILE): return []
    with open(USER_FILE, "r", encoding="utf-8") as f:
        try: return json.load(f)
        except: return []

def save_users(users):
    with open(USER_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=4)

@app.post("/register")
async def register(data: dict = Body(...)):
    users = load_users()
    if any(u['username'] == data['username'] for u in users):
        raise HTTPException(status_code=400, detail="帳號已存在")
    users.append({**data, "history": []})
    save_users(users)
    return {"status": "success"}

@app.post("/login")
async def login(data: dict = Body(...)):
    users = load_users()
    user = next((u for u in users if u['username'] == data['username'] and u['password'] == data['password']), None)
    if user: return {"status": "success", "name": user['name']}
    raise HTTPException(status_code=401, detail="驗證失敗")

UPLOAD_DIR = "static/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/save_history")
async def save_history(data: dict = Body(...)):
    users = load_users()
    for u in users:
        if u['username'] == data.get("username"):
            # 接收前端傳來的 image_url
            history_entry = {
                "query": data.get("query", ""),
                "answer": data.get("answer", ""),
                "explanation": data.get("explanation", ""),
                "image_url": data.get("image_url", ""), # 新增圖片路徑欄位
                "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            u['history'].append(history_entry)
            break
    save_users(users)
    return {"status": "success"}

@app.get("/get_history/{username}")
async def get_history(username: str):
    users = load_users()
    user = next((u for u in users if u['username'] == username), None)
    return user.get('history', []) if user else []

# ================= AI 解題核心功能 =================
@app.post("/solve")
async def solve_endpoint(data: dict = Body(...)):
    query = data.get("query")
    streamer = process_with_qwen_vl(text_query=query)
    
    async def generate_wrapper():
        metadata = {"answer": "請看下方老師詳解", "translated_eq": f"輸入/情境：{query[:30]}...", "plot": None}
        yield json.dumps(metadata) + "\n--SEP--\n"
        for chunk in streamer:
            if chunk:
                yield chunk
                await asyncio.sleep(0.01)
                
    return StreamingResponse(generate_wrapper(), media_type="text/plain")

@app.post("/ocr_solve")
async def ocr_solve_endpoint(file: UploadFile = File(...)):
    try:
        # 產生獨一無二的檔名並儲存圖片
        file_extension = file.filename.split(".")[-1]
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        unique_filename = f"upload_{timestamp}.{file_extension}"
        file_path = os.path.join(UPLOAD_DIR, unique_filename)
        
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        # 讀取已儲存的圖片供模型推論
        with open(file_path, "rb") as f:
            image_content = f.read()
            
        streamer = process_with_qwen_vl(image_bytes=image_content)
        
        async def generate_wrapper():
            # 將圖片路徑回傳給前端，以便前端儲存進歷史紀錄
            metadata = {
                "answer": "", 
                "translated_eq": "", 
                "plot": None,
                "image_url": f"/{file_path}" # 回傳圖片的 URL 路徑
            }
            yield json.dumps(metadata) + "\n--SEP--\n"
            for chunk in streamer:
                if chunk:
                    yield chunk
                    await asyncio.sleep(0.01)

        return StreamingResponse(generate_wrapper(), media_type="text/plain")
    except Exception as e:
        print(f"❌ Qwen-VL OCR Solve 發生異常: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# ================= 智慧出題 (Active Recall) =================
@app.post("/generate_quiz")
async def generate_quiz_endpoint(data: dict = Body(...)):
    _categories = data.get("categories", [])
    
    # TODO: 之後記得改！目前強制鎖定範圍。
    target_category = "國一下-1-1重點一" 
    
    db = SessionLocal()
    try:
        available_problems = db.query(Problem).filter(Problem.category == target_category).all()
            
        if len(available_problems) >= 3:
            selected = random.sample(available_problems, 3)
        else:
            selected = available_problems
            
        result = [
            {
                "id": p.id,
                "category": p.category,
                "question_text": p.question_text,
                "image_path": p.image_path
            } for p in selected
        ]
        return result
    finally:
        db.close()

# 🧩 拼圖三修正：全新開發支援多圖文上傳的智慧測驗批改路由
@app.post("/grade_quiz")
async def grade_quiz_endpoint(
    answers: str = Form(...), # 接收 JSON 字串格式的學生作答文字陣列
    file_0: Optional[UploadFile] = File(None),
    file_1: Optional[UploadFile] = File(None),
    file_2: Optional[UploadFile] = File(None)
):
    try:
        answers_list = json.loads(answers)
        images_dict = {}
        
        # 將讀取到的選填圖片二進位資料存入字典中
        if file_0: images_dict[0] = await file_0.read()
        if file_1: images_dict[1] = await file_1.read()
        if file_2: images_dict[2] = await file_2.read()
        
        # 呼叫 model.py 的特製多模態批改流
        streamer = process_quiz_grading(answers_list, images_dict)
        
        async def generate_wrapper():
            # 建立符合前端 handleStream 解析的 metadata 頭部
            metadata = {"answer": "綜合批改完成", "translated_eq": "智慧測驗多模態混合閱卷", "plot": None}
            yield json.dumps(metadata) + "\n--SEP--\n"
            for chunk in streamer:
                if chunk:
                    yield chunk
                    await asyncio.sleep(0.01)

        return StreamingResponse(generate_wrapper(), media_type="text/plain")
    except Exception as e:
        print(f"❌ 智慧批改管線發生異常: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))