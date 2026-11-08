from fastapi import FastAPI, Body, HTTPException, File, UploadFile, Form
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import json, os, asyncio, random
from datetime import datetime
from typing import Optional
import shutil
from contextlib import asynccontextmanager # ⚠️ 新增這行

# 匯入 SQLAdmin 與資料庫模組
from sqladmin import Admin, ModelView
from .database import engine, Problem, SessionLocal
# ⚠️ 注意這裡：多匯入了 load_model
from .model import process_qwen_ocr_only, process_classification, process_explanation, process_quiz_grading, load_model

# ⚠️ 定義啟動生命週期：伺服器啟動時優先載入 AI 模型
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🌟 伺服器啟動中，準備喚醒數學家教 AI...")
    load_model()
    yield
    print("💤 伺服器關閉中...")

# ⚠️ 將 lifespan 綁定到 app
app = FastAPI(lifespan=lifespan)

from fastapi.staticfiles import StaticFiles
app.mount("/static", StaticFiles(directory="static"), name="static")

# ================= 下方保留你原本的 app.add_middleware 與其他路由 =================

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
    # 純文字輸入：跳過 OCR，直接分類 -> 解題
    category_text = await process_classification(query)
    streamer = process_explanation(query, category_text)
    
    async def generate_wrapper():
        metadata = {"answer": "請看下方老師詳解", "translated_eq": f"【{category_text}】\n輸入/情境：{query[:30]}...", "plot": None}
        yield json.dumps(metadata) + "\n--SEP--\n"
        for chunk in streamer:
            if chunk:
                yield chunk
                await asyncio.sleep(0.01)
                
    return StreamingResponse(generate_wrapper(), media_type="text/plain")

@app.post("/ocr_solve")
async def ocr_solve_endpoint(file: UploadFile = File(...)):
    try:
        file_extension = file.filename.split(".")[-1]
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        file_path = os.path.join(UPLOAD_DIR, f"upload_{timestamp}.{file_extension}")
        
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        with open(file_path, "rb") as f:
            image_content = f.read()
            
        # 🌟 三層式架構啟動！
        print("🔍 [層級一] 純淨手寫 OCR...")
        extracted_latex = await process_qwen_ocr_only(image_content)
        
        print("🧠 [層級二] 單元分類...")
        category_text = await process_classification(extracted_latex)
        
        print("📝 [層級三] 邏輯推演生成...")
        streamer = process_explanation(extracted_latex, category_text)
        
        async def generate_wrapper():
            # 將單元分類與 OCR 算式先回傳給畫面
            metadata = {
                "answer": "", 
                "translated_eq": f"{category_text}\n【辨識算式】\n{extracted_latex}", 
                "plot": None,
                "image_url": f"/{file_path}"
            }
            yield json.dumps(metadata) + "\n--SEP--\n"
            for chunk in streamer:
                if chunk:
                    yield chunk
                    await asyncio.sleep(0.01)

        return StreamingResponse(generate_wrapper(), media_type="text/plain")
    except Exception as e:
        print(f"❌ 發生異常: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# ================= 智慧出題 (Active Recall) =================
@app.post("/generate_quiz")
async def generate_quiz_endpoint(data: dict = Body(...)):
    _categories = data.get("categories", [])
    db = SessionLocal()
    try:
        available_problems = db.query(Problem).filter(Problem.category.in_(_categories)).all()
        selected = random.sample(available_problems, 3) if len(available_problems) >= 3 else available_problems
            
        result = [
            {
                "id": p.id,
                "category": p.category,
                "question_text": p.question_text,
                "image_path": p.image_path,
                "detailed_solution": p.detailed_solution # ⚠️ 新增回傳標準詳解給前端
            } for p in selected
        ]
        return result
    finally:
        db.close()

@app.post("/grade_quiz")
async def grade_quiz_endpoint(
    answers: str = Form(...), 
    file_0: Optional[UploadFile] = File(None),
    file_1: Optional[UploadFile] = File(None),
    file_2: Optional[UploadFile] = File(None)
):
    try:
        answers_list = json.loads(answers)
        
        # 🌟 將收到的學生考卷圖片，先交給防腦補的 OCR 引擎做初步轉譯
        for i, item in enumerate(answers_list):
            file_obj = locals().get(f"file_{i}")
            if file_obj:
                img_bytes = await file_obj.read()
                print(f"🔍 正在解析第 {i+1} 題的學生圖片...")
                item['ocr_text'] = await process_qwen_ocr_only(img_bytes)
            else:
                item['ocr_text'] = "無上傳圖片"
        
        # 圖片已經轉成嚴格的算式字串，連同題庫詳解一起送給模型批改
        streamer = process_quiz_grading(answers_list)
        
        async def generate_wrapper():
            metadata = {"answer": "綜合批改完成", "translated_eq": "智慧測驗多模態混合閱卷", "plot": None}
            yield json.dumps(metadata) + "\n--SEP--\n"
            for chunk in streamer:
                if chunk:
                    yield chunk
                    await asyncio.sleep(0.01)

        return StreamingResponse(generate_wrapper(), media_type="text/plain")
    except Exception as e:
        print(f"❌ 發生異常: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))