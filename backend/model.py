import os
os.environ["HF_HOME"] = "/home/nic0/HF_Models"

import asyncio
import torch
import io
from PIL import Image
from transformers import Qwen2_5_VLForConditionalGeneration, AutoProcessor, TextIteratorStreamer, BitsAndBytesConfig
from threading import Thread
from peft import PeftModel

model = None
processor = None
device = "cuda" if torch.cuda.is_available() else "cpu"

MATH_CHEAT_SHEET = """
01 乘法公式：(a±b)²、a²-b²、展開、面積分割、平方和差、分配律。
02 多項式加減：單項式、常數項、同類項合併、降升冪、去括號、項數。
03 多項式乘除：長除法、分離係數、商餘式、缺項補零、除法原理。
04 平方根意義：√、正負平方根、完全平方數、十分逼近法。
05 根式運算：最簡根式、有理化分母、同類根式、共軛、根號加減。
06 畢氏定理：直角三角形、斜邊、兩股、a²+b²=c²、畢氏數、兩點距離。
07 提公因式與乘法公式：因式分解、提公因式、質因式、分組、完全平方式。
08 十字交乘法：十字交乘、二次項與常數項分解、同異號判斷。
09 因式分解解方程式：一元二次方程式、=0、零積性質、方程式的根、重根。
10 配方法與公式解：配完全平方式、b²-4ac、判別式、公式解、相異兩實根、無解。
11 應用問題：假設未知數、依題意列式、速率/工程問題、務必檢查答案是否不合題意。
"""

def load_model():
    global model, processor
    MODEL_ID = "Qwen/Qwen2.5-VL-7B-Instruct"
    LORA_PATH = "./model/qwen-vl-math-tutor-final" 

    print("⏳ 1/3 載入處理器 (Processor)...")
    processor = AutoProcessor.from_pretrained(MODEL_ID)
    
    print("⏳ 2/3 載入基礎模型 (包含 4-bit 量化)...")
    quant_config = BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_compute_dtype=torch.float16)
    base_model = Qwen2_5_VLForConditionalGeneration.from_pretrained(
        MODEL_ID, torch_dtype=torch.float16, quantization_config=quant_config, device_map="auto"
    )
    
    print(f"🔗 3/3 正在掛載 LoRA 微調權重 ({LORA_PATH})...")
    model = PeftModel.from_pretrained(base_model, LORA_PATH)
    model.eval()
    print("✅ 專屬數學家教模型載入完成！")

async def _generate_text_async(messages, content_list):
    streamer = _run_streamer(messages, content_list)
    result = ""
    for chunk in streamer:
        if chunk:
            result += chunk
            await asyncio.sleep(0.001)
    return result.strip()

# =========================================================
# 首頁與共同模組
# =========================================================
async def process_qwen_ocr_only(image_bytes):
    system_content = (
        "你是一個極度精準的 OCR 數學算式辨識引擎。\n"
        "【最高指導原則】：請照實轉譯圖片中的所有『算式』與『題目文字』（不論是手寫還是電腦打字）。\n"
        "學生極有可能計算錯誤，錯的就讓它是錯的。你只需要純粹輸出辨識到的內容，嚴禁給出解答。\n"
        "⚠️ 若圖片完全是一張風景照或無關圖片，才輸出『圖片中無數學內容』。"
    )
    messages = [{"role": "system", "content": system_content}]
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    if max(image.size) > 1024: image.thumbnail((1024, 1024))
    content_list = [{"type": "image", "image": image}, {"type": "text", "text": "請精準照實轉譯圖片內容。"}]
    messages.append({"role": "user", "content": content_list})
    return await _generate_text_async(messages, content_list)

def process_explanation(extracted_text):
    system_content = (
        "你是一位專業且溫柔的台灣國中數學老師。請全程使用繁體中文（zh-TW）。\n"
        "【任務】：請幫學生解出這題數學題目。\n"
        "【解題原則】：請讓自己一步一步自由思考。先分析題目、列出算式並推導過程，確認無誤後，再於最後給出最終答案。\n"
        "所有的數字、未知數與數學算式，請絕對使用單一 $ 符號包裹。"
    )
    user_prompt = (
        f"請幫我解這題題目：\n"
        f"【題目內容】：\n{extracted_text}\n\n"
        f"請一步一步給出詳細的解題過程："
    )
    messages = [{"role": "system", "content": system_content}]
    content_list = [{"type": "text", "text": user_prompt}]
    messages.append({"role": "user", "content": content_list})
    return _run_streamer(messages, content_list)

# ⚠️ 微型 RAG：單元分類大腦 (包含小抄)
async def process_classification(extracted_text):
    system_content = (
        "你是一個專業的台灣中學數學單元分類器。\n"
        f"【索引小抄（必讀）】：\n{MATH_CHEAT_SHEET}\n\n"
        "請根據題目內容，嚴格比對上述小抄，判斷其屬於哪一個單元。\n"
        "【嚴格輸出規定】：\n"
        "1. 你『只能』從小抄中挑選完全一致的單元名稱。\n"
        "2. 輸出格式必須包含編號與名稱，例如：「01 乘法公式」或「05 根式運算」。\n"
        "3. 絕對不准輸出其他任何廢話、標點符號或解釋！"
    )
    messages = [{"role": "system", "content": system_content}]
    content_list = [{"type": "text", "text": f"題目內容：\n{extracted_text}"}]
    messages.append({"role": "user", "content": content_list})
    return await _generate_text_async(messages, content_list)


# =========================================================
# 智慧考卷專區：三階段獨立任務 (OCR -> 法官 -> 導師)
# =========================================================

async def process_quiz_ocr(image_bytes):
    system_content = (
        "你是一個極度精準的 OCR 數學算式辨識引擎。\n"
        "【最高指導原則】：請照實轉譯圖片中的所有『算式』與『文字』（不論是手寫還是電腦打字）。\n"
        "學生極有可能計算錯誤，錯的就讓它是錯的。你只需要純粹輸出辨識到的算式，嚴禁給出解答。\n"
        "⚠️ 若圖片中沒有任何數學算式，請直接輸出『未辨識到算式』。"
    )
    messages = [{"role": "system", "content": system_content}]
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    if max(image.size) > 1024: image.thumbnail((1024, 1024))
    content_list = [{"type": "image", "image": image}, {"type": "text", "text": "請精準照實轉譯圖片內容。"}]
    messages.append({"role": "user", "content": content_list})
    return await _generate_text_async(messages, content_list)

async def process_quiz_judge(question_text, standard_solution, ocr_text, text_answer):
    system_content = (
        "你是一位嚴格無私的數學閱卷官。你的『唯一任務』是判定學生的算式邏輯與最終答案是否正確。\n"
        "【判定基準】：殊途同歸原則。只要學生的推導邏輯合理、答案無誤，即為正確，不需與標準詳解完全一樣。\n"
        "【強制輸出格式】：\n"
        "1. 若學生完全正確，你『只能』輸出這句話：「這題得到+20分。」\n"
        "2. 若學生有任何一行邏輯算錯或答案錯，你『只能』輸出這句話：「這題得到0分。」\n"
        "⚠️ 絕對禁止輸出任何解釋、步驟或標點符號之外的文字！"
    )
    user_prompt = (
        f"【題目】：{question_text}\n"
        f"【標準詳解】：{standard_solution}\n"
        f"【學生文字作答】：{text_answer or '無'}\n"
        f"【學生手寫算式辨識結果】：\n{ocr_text}\n\n"
        "請判定："
    )
    messages = [{"role": "system", "content": system_content}]
    content_list = [{"type": "text", "text": user_prompt}]
    messages.append({"role": "user", "content": content_list})
    return await _generate_text_async(messages, content_list)

def process_quiz_explain(question_text, standard_solution, ocr_text, text_answer):
    system_content = (
        "你是一位充滿耐心的台灣國中數學老師。這名學生在此題被判定為錯誤（0分）。\n"
        "【任務】：請明確指出學生的『手寫算式』或『文字作答』中，具體是『哪一行』發生了什麼錯誤（例如移項忘記除以數字、平方算錯）。\n"
        "指出錯誤後，請給出完整的正確解答流程來教導學生。請全程使用繁體中文（zh-TW），所有數學式請用 $ 包裹。"
    )
    user_prompt = (
        f"【題目】：{question_text}\n"
        f"【標準詳解】：{standard_solution}\n"
        f"【學生文字作答】：{text_answer or '無'}\n"
        f"【學生手寫算式辨識結果】：\n{ocr_text}\n\n"
        "請詳細點出學生的錯誤並給予正確詳解："
    )
    messages = [{"role": "system", "content": system_content}]
    content_list = [{"type": "text", "text": user_prompt}]
    messages.append({"role": "user", "content": content_list})
    return _run_streamer(messages, content_list)

def _run_streamer(messages, content_list):
    text = processor.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    image_list = [img["image"] for img in content_list if img["type"] == "image"]
    if len(image_list) > 0:
        inputs = processor(text=[text], images=image_list, padding=True, return_tensors="pt")
    else:
        inputs = processor(text=[text], padding=True, return_tensors="pt")
    inputs = {k: v.to(device) for k, v in inputs.items()}
    streamer = TextIteratorStreamer(processor.tokenizer, skip_prompt=True, skip_special_tokens=True)
    generation_kwargs = dict(**inputs, streamer=streamer, max_new_tokens=1024, do_sample=True, temperature=0.1, top_p=0.9, repetition_penalty=1.05)
    thread = Thread(target=model.generate, kwargs=generation_kwargs)
    thread.start()
    return streamer