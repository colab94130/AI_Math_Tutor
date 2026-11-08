from fastapi import FastAPI, Body, HTTPException, File, UploadFile, Form
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import json, os, asyncio, random, math
from datetime import datetime
from typing import Optional
import shutil
from contextlib import asynccontextmanager

from sqladmin import Admin, ModelView
from .database import engine, Problem, SessionLocal
from .model import (process_qwen_ocr_only, process_explanation, process_classification, load_model,
                    process_quiz_ocr, process_quiz_judge, process_quiz_explain)

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🌟 伺服器啟動中，準備喚醒數學家教 AI...")
    load_model()
    yield
    print("💤 伺服器關閉中...")

app = FastAPI(lifespan=lifespan)

from fastapi.staticfiles import StaticFiles
app.mount("/static", StaticFiles(directory="static"), name="static")

app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"],
)

admin = Admin(app, engine)
class ProblemAdmin(ModelView, model=Problem):
    column_list = [Problem.id, Problem.category, Problem.question_text, Problem.image_path]
    column_searchable_list = [Problem.category, Problem.question_text]
    name = "數學題庫"
    name_plural = "數學題庫管理"
    icon = "fa-solid fa-calculator"
admin.add_view(ProblemAdmin)

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
            history_entry = {
                "query": data.get("query", ""),
                "answer": data.get("answer", ""),
                "explanation": data.get("explanation", ""),
                "image_url": data.get("image_url", ""),
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

@app.post("/solve")
async def solve_endpoint(data: dict = Body(...)):
    query = data.get("query")
    streamer = process_explanation(query) 
    
    async def generate_wrapper():
        metadata = {"answer": "請看下方老師詳解", "translated_eq": "輸入/情境：" + query[:30] + "...", "plot": None, "image_url": ""}
        yield json.dumps(metadata) + "\n--SEP--\n"
        for chunk in streamer:
            if chunk:
                yield chunk
                await asyncio.sleep(0.01)
                
        category_text = await process_classification(query)
        yield f"\n\n---\n單元分類：{category_text}"
                
    return StreamingResponse(generate_wrapper(), media_type="text/plain")

@app.post("/ocr_solve")
async def ocr_solve_endpoint(file: UploadFile = File(...)):
    try:
        file_extension = file.filename.split(".")[-1]
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        unique_filename = f"upload_{timestamp}.{file_extension}"
        file_path = os.path.join(UPLOAD_DIR, unique_filename)
        
        # 🛡️ 恢復原本最單純、最穩定的檔案儲存法
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        with open(file_path, "rb") as f:
            image_content = f.read()
            
        extracted_latex = await process_qwen_ocr_only(image_content)
        streamer = process_explanation(extracted_latex)
        
        async def generate_wrapper():
            metadata = {"answer": "", "translated_eq": "【辨識算式】\n" + extracted_latex, "plot": None, "image_url": "/" + file_path}
            yield json.dumps(metadata) + "\n--SEP--\n"
            
            for chunk in streamer:
                if chunk:
                    yield chunk
                    await asyncio.sleep(0.01)
            
            category_text = await process_classification(extracted_latex)
            yield f"\n\n---\n單元分類：{category_text}"

        return StreamingResponse(generate_wrapper(), media_type="text/plain")
    except Exception as e:
        print(f"❌ 發生異常: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


CAT_MAPPING = {
    "01": "國二上-1-1-乘法公式", "02": "國二上-1-2-多項式的加減", "03": "國二上-1-3-多項式的乘除",
    "04": "國二上-2-1-平方根的意義", "05": "國二上-2-2-根式的運算", "06": "國二上-2-3-畢氏定理",
    "07": "國二上-3-1-提公因式與乘法公式作因式分解", "08": "國二上-3-2-利用十字交乘法因式分解",
    "09": "國二上-4-1-因式分解法解一元二次方程式", "10": "國二上-4-2-配方法與公式解", "11": "國二上-4-3-應用問題"
}

@app.post("/generate_quiz")
async def generate_quiz_endpoint(data: dict = Body(...)):
    _categories = data.get("categories", [])
    
    db_categories = []
    for c in _categories:
        prefix = c[:2] 
        if prefix in CAT_MAPPING:
            db_categories.append(CAT_MAPPING[prefix])
        else:
            db_categories.append(c)

    db = SessionLocal()
    try:
        final_selected = []
        total_topics = len(db_categories)
        if total_topics == 0:
            return []

        base_quota = 3 // total_topics
        remainder = 3 % total_topics

        for i, category in enumerate(db_categories):
            quota = base_quota + (1 if i < remainder else 0)
            if quota == 0:
                continue
            available_problems = db.query(Problem).filter(Problem.category == category).all()
            if available_problems:
                actual_quota = min(quota, len(available_problems))
                selected = random.sample(available_problems, actual_quota)
                final_selected.extend(selected)

        result = [{"id": p.id, "category": p.category, "question_text": p.question_text, "image_path": p.image_path, "detailed_solution": p.detailed_solution} for p in final_selected]
        random.shuffle(result)
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
        
        # 🛡️ 立即實體化圖片 (Safe Bytes) - 防止考卷第三題當機資料遺失
        safe_file_bytes = []
        for f in [file_0, file_1, file_2]:
            if f and f.filename:
                content = await f.read()
                safe_file_bytes.append(content)
            else:
                safe_file_bytes.append(None)
        
        async def generate_wrapper():
            metadata = {"answer": "綜合批改完成", "translated_eq": "智慧測驗多模態混合閱卷", "plot": None}
            yield json.dumps(metadata) + "\n--SEP--\n"
            
            for i, item in enumerate(answers_list):
                chinese_num = ["一", "二", "三"][i]
                yield f"### --- 第 {chinese_num} 題 ---\n"
                yield f"**【題目】**：{item['question_text']}\n\n"
                
                # ----------------------------------------------------
                # 第一步：呼叫眼睛 (OCR)
                # ----------------------------------------------------
                img_bytes = safe_file_bytes[i] if i < len(safe_file_bytes) else None
                ocr_text = "無上傳圖片"
                if img_bytes:
                    yield "*🔍 正在仔細掃描您的手寫算式（絕不漏看）...*\n\n"
                    ocr_text = await process_quiz_ocr(img_bytes)
                    yield f"**【手寫辨識結果】**：\n{ocr_text}\n\n"
                else:
                    yield "**【手寫辨識結果】**：未上傳圖片\n\n"
                
                # ----------------------------------------------------
                # 第二步：呼叫法官 (Judge)
                # ----------------------------------------------------
                yield "*⚖️ 老師正在嚴格判定對錯...*\n\n"
                judge_result = await process_quiz_judge(
                    item['question_text'], item['detailed_solution'], ocr_text, item['text_answer']
                )
                yield f"**【判定結果】**：{judge_result}\n\n"
                
                # ----------------------------------------------------
                # 第三步：條件觸發導師 (Explain) - 只有錯才啟動
                # ----------------------------------------------------
                if "0分" in judge_result or "0" in judge_result:
                    yield "*📝 診斷錯誤原因與詳細教學...*\n\n"
                    streamer = process_quiz_explain(
                        item['question_text'], item['detailed_solution'], ocr_text, item['text_answer']
                    )
                    for chunk in streamer:
                        if chunk:
                            yield chunk
                            await asyncio.sleep(0.01)
                
                yield "\n\n<br><br>\n\n"

        return StreamingResponse(generate_wrapper(), media_type="text/plain")
    except Exception as e:
        print(f"❌ 發生異常: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))