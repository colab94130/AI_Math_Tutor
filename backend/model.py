import os
# 1. 強制設定 Hugging Face 模型下載與快取路徑至 E 槽 (必須在 import transformers 前執行)
os.environ["HF_HOME"] = "/home/nic0/HF_Models"

import torch
import io
from PIL import Image
from transformers import Qwen2_5_VLForConditionalGeneration, AutoProcessor, TextIteratorStreamer, BitsAndBytesConfig
from threading import Thread
from peft import PeftModel

# 宣告全域變數
model = None
processor = None
device = "cuda" if torch.cuda.is_available() else "cpu"

# 2. 建立 11 單元微型資料索引小抄
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
    
    print("⏳ 2/3 載入基礎模型 (Base Model，包含 4-bit 量化以節省顯存)...")
    quant_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_compute_dtype=torch.float16
    )
    base_model = Qwen2_5_VLForConditionalGeneration.from_pretrained(
        MODEL_ID,
        torch_dtype=torch.float16,
        quantization_config=quant_config,
        device_map="auto"
    )
    
    print(f"🔗 3/3 正在掛載 LoRA 微調權重 ({LORA_PATH})...")
    # 將你的專屬權重掛載到基礎模型上
    model = PeftModel.from_pretrained(base_model, LORA_PATH)
    model.eval()
    
    print("✅ 專屬數學家教模型載入完成，隨時準備接客！")

def get_model():
    if model is None or processor is None:
        load_model()
    return model, processor
# 2. 建立 11 單元微型資料索引小抄
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

if torch.cuda.is_available():
    print(f"🚀 偵測到 GPU 環境，啟動硬體加速")
    device = "cuda"
else:
    print("⚠️ 未偵測到 GPU，切換為 CPU 模式運作")
    device = "cpu"

model_id = "Qwen/Qwen2.5-VL-7B-Instruct" 
processor = AutoProcessor.from_pretrained(model_id)

quant_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_compute_dtype=torch.float16
)

model = Qwen2_5_VLForConditionalGeneration.from_pretrained(
    model_id,
    torch_dtype=torch.float16,
    quantization_config=quant_config,
    device_map="auto"
)

# ================= 前方 load_model 等設定保留不變 =================

# 新增一個非同步的純文字生成器，用來在背景取得第一層與第二層的結果
async def _generate_text_async(messages, content_list):
    streamer = _run_streamer(messages, content_list)
    result = ""
    for chunk in streamer:
        if chunk:
            result += chunk
            await asyncio.sleep(0.001)
    return result.strip()

# ---------------------------------------------------------
# [第一層]：純淨手寫 OCR (無情的打字機，防腦補)
# ---------------------------------------------------------
async def process_qwen_ocr_only(image_bytes):
    system_content = (
        "你是一個極度精準的 OCR 數學算式辨識引擎。\n"
        "【嚴格警告】：這是一張學生的手寫算式，學生『極有可能寫錯或漏寫』！\n"
        "請『一字不漏、照實』轉譯圖片中的所有數學式子與符號。\n"
        "絕對不要用你的數學邏輯去「腦補」或「自動修正」錯誤的算式！錯的就讓它是錯的。\n"
        "所有數學式與數字必須使用 LaTeX 格式，單行算式用 $ 包裹，獨立大算式用 $$ 包裹。\n"
        "嚴禁給出任何解答、提示或計算過程，你只需要純粹輸出辨識到的內容。"
    )
    messages = [{"role": "system", "content": system_content}]
    content_list = []
    
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    max_size = 1024
    if max(image.size) > max_size:
        image.thumbnail((max_size, max_size))
        
    content_list.append({"type": "image", "image": image})
    content_list.append({"type": "text", "text": "請精準照實轉譯圖片內容。"})
    messages.append({"role": "user", "content": content_list})
    
    return await _generate_text_async(messages, content_list)

# ---------------------------------------------------------
# [第二層]：單元分類大腦 (利用 Token 餘裕加上小抄)
# ---------------------------------------------------------
async def process_classification(extracted_text):
    system_content = (
        "你是一個專業的台灣中學數學單元分類器。\n"
        f"請參考以下索引小抄來輔助分類：\n{MATH_CHEAT_SHEET}\n\n"
        "請根據學生輸入的算式或題目，判斷其屬於哪一個單元。\n"
        "你只需要輸出結果，絕對不要輸出其他多餘的字。\n"
        "輸出格式必須為：「**本題屬於：[章節名稱]**」。"
    )
    messages = [{"role": "system", "content": system_content}]
    content_list = [{"type": "text", "text": f"題目內容：\n{extracted_text}"}]
    messages.append({"role": "user", "content": content_list})
    
    return await _generate_text_async(messages, content_list)

# ---------------------------------------------------------
# [第三層]：邏輯推演與詳解 (串流回傳給前端)
# ---------------------------------------------------------
def process_explanation(extracted_text, category_text):
    system_content = (
        "你是一位專業的台灣國中數學老師。請『絕對、務必』全程使用『繁體中文（zh-TW）』作答。\n"
        "【排版與數學符號嚴格規定】：\n"
        "1. 所有的數字、未知數與數學算式，請『絕對』使用單一 $ 符號包裹。\n"
        "2. 嚴禁使用電腦程式符號，全面使用標準 LaTeX 數學符號。\n"
    )
    
    user_prompt = f"AI 單元預先判斷：{category_text}\n\n學生上傳的題目內容如下：\n{extracted_text}\n\n請給出精確答案與詳細且溫柔的解題步驟。"
    messages = [{"role": "system", "content": system_content}]
    content_list = [{"type": "text", "text": user_prompt}]
    messages.append({"role": "user", "content": content_list})
    
    return _run_streamer(messages, content_list)

# ---------------------------------------------------------
# [智慧測驗]：多圖文批改 (帶入資料庫詳解與計分機制)
# ---------------------------------------------------------
def process_quiz_grading(answers_list):
    system_content = (
        "你是一位嚴格且細心的台灣國中數學老師。請幫忙逐題批改學生的測驗。\n"
        "請『絕對、務必』全程使用『繁體中文（zh-TW）』作答。\n"
        f"【單元索引小抄】：\n{MATH_CHEAT_SHEET}\n\n"
        "【批改嚴格規則】：\n"
        "1. 每一題都是獨立的。請根據我提供的「題目」與「標準詳解」，來對比學生的「文字作答」與「圖片辨識結果」。\n"
        "2. 批改格式請務必依照：\n"
        "   **單元分類**：(從索引中選出此題單元)\n"
        "   **題目**：(題目內容)\n"
        "   **開始講解**：(具體批改與提示)\n"
        "   **得分**：若學生觀念與答案完全正確，請在該題最後一行加上『+ 20分』；若錯誤或未作答，請加上『+ 0分』。\n"
    )
    
    content = ""
    for i, item in enumerate(answers_list):
        chinese_num = ["一", "二", "三", "四", "五"][i]
        content += f"\n\n--- 第 {chinese_num} 題 ---\n"
        content += f"題目：{item['question_text']}\n"
        content += f"標準詳解：{item['detailed_solution']}\n"
        content += f"學生輸入文字：{item['text_answer'] or '無'}\n"
        content += f"學生圖片辨識結果：{item.get('ocr_text', '無上傳圖片')}\n"
    
    content += "\n\n請開始你的嚴格批改，並記得給分與單元分類："
    
    messages = [{"role": "system", "content": system_content}]
    content_list = [{"type": "text", "text": content}]
    messages.append({"role": "user", "content": content_list})
    
    # 這裡因為前面已經將圖片轉成 OCR 文字，所以不傳送真實圖片給模型，大幅節省算力並避免多圖干擾！
    return _run_streamer(messages, content_list)

# ================= 內部封裝的發送生成器 _run_streamer 保留不變 =================
def _run_streamer(messages, content_list):
    text = processor.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    image_list = [img["image"] for img in content_list if img["type"] == "image"]
    # ... (下方代碼與你原本的完全相同，省略)

# 內部封裝的發送生成器
def _run_streamer(messages, content_list):
    text = processor.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    image_list = [img["image"] for img in content_list if img["type"] == "image"]
    
    if len(image_list) > 0:
        inputs = processor(text=[text], images=image_list, padding=True, return_tensors="pt")
    else:
        inputs = processor(text=[text], padding=True, return_tensors="pt")
        
    inputs = {k: v.to(device) for k, v in inputs.items()}
    
    streamer = TextIteratorStreamer(processor.tokenizer, skip_prompt=True, skip_special_tokens=True)
    
    # 將原本的 generation_kwargs 替換為以下設定
    generation_kwargs = dict(
        **inputs, 
        streamer=streamer, 
        max_new_tokens=1024, 
        do_sample=True,            # 開啟採樣，讓模型有微小的彈性跳出迴圈
        temperature=0.1,           # 溫度壓到極低（0.1），確保數學邏輯依然嚴謹不出錯
        top_p=0.9,                 # 限制選字範圍，防堵幻覺
        repetition_penalty=1.05    # 將懲罰值微調至 1.05 的黃金平衡點
    )
    thread = Thread(target=model.generate, kwargs=generation_kwargs)
    thread.start()
    
    return streamer