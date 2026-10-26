import os
# 1. 強制設定 Hugging Face 模型下載與快取路徑至 E 槽 (必須在 import transformers 前執行)
os.environ["HF_HOME"] = "/home/nic0/HF_Models"

import torch
import io
from PIL import Image
from transformers import Qwen2_5_VLForConditionalGeneration, AutoProcessor, TextIteratorStreamer, BitsAndBytesConfig
from threading import Thread

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

# 一般解題使用的單圖文管線
def process_with_qwen_vl(image_bytes=None, text_query=None):
    system_content = (
        "你是一位專業的台灣國中數學老師。請『絕對、務必』全程使用『繁體中文（zh-TW）』作答，嚴禁出現任何簡體字！\n"
        "你可以自由使用 Markdown 排版（例如標題、粗體、列表）來讓解題步驟更清晰。\n"
        "【排版與數學符號嚴格規定】：\n"
        "1. 所有的數字、未知數與數學算式，請『絕對』使用單一 $ 符號包裹（例如將 $x$ 代入 $5y$）。若需獨立成行的大算式，才使用 $$ 包裹。\n"
        "2. 【嚴禁使用電腦程式符號，全面使用標準 LaTeX 數學符號】：\n"
        "   - 平方：嚴禁寫 x**2，務必寫成 $x^2$。\n"
        "   - 分數：嚴禁使用斜線 (如 x/2)，務必寫成 $\\frac{x}{2}$。\n"
        "   - 根號：嚴禁寫 sqrt(2)，務必寫成 $\\sqrt{2}$。\n"
        "   - 乘法與除法：嚴禁使用 * 或 /，務必使用 $\\times$ 或 $\\div$（或直接省略如 $3x$）。\n"
        f"請參考以下索引來輔助你分類與避錯：\n{MATH_CHEAT_SHEET}"
    )
    
    messages = [{"role": "system", "content": system_content}]
    
    content_list = []
    if image_bytes:
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        max_size = 1024
        if max(image.size) > max_size:
            image.thumbnail((max_size, max_size))
        content_list.append({"type": "image", "image": image})
        
    user_prompt = text_query if text_query else "請辨識這張圖片中的數學題，並給出精確答案與詳細解題步驟。"
    content_list.append({"type": "text", "text": user_prompt})
    messages.append({"role": "user", "content": content_list})
    
    return _run_streamer(messages, content_list)

# 專門處理多題、多圖文混合的智慧測驗批改管線
def process_quiz_grading(answers_list, images_dict):
    # 4. 將小抄注入智慧測驗批改的 System Prompt
    system_content = (
        "你是一位條理分明的台灣國中數學老師。請幫忙逐題批改學生的測驗。\n"
        "請『絕對、務必』全程使用『繁體中文（zh-TW）』作答，嚴禁出現任何簡體字。\n"
       
        "請嚴格遵守以下規則：\n"
        "1. 每一題都是獨立的，請分開批改。若該題學生未作答且無圖片，請直接講評「未作答」。\n"
        "2. 批改格式請務必依照：\n"
        "題目一\n"
        "（題目內容）\n"
        "學生回答：（文字作答與圖片狀況）\n"
        "開始講解：（具體批改與提示）\n\n"
        f"請參考以下索引來精準抓出學生盲點並避錯：\n{MATH_CHEAT_SHEET}\n"
        "請依序完成所有題目的批改，不要重複輸出無意義的邊界符號。"
    )
    
    messages = [{"role": "system", "content": system_content}]
    
    content_list = []
    
    for i, item in enumerate(answers_list):
        chinese_num = ["一", "二", "三", "四", "五"][i]
        
        content_list.append({
            "type": "text", 
            "text": f"\n\n這是第 {chinese_num} 題的資料：\n題目：{item['question_text']}\n學生輸入的文字：{item['text_answer'] or '無'}\n學生的圖片狀況："
        })
        
        if i in images_dict and images_dict[i]:
            try:
                img = Image.open(io.BytesIO(images_dict[i])).convert("RGB")
                if max(img.size) > 1024:
                    img.thumbnail((1024, 1024))
                content_list.append({"type": "text", "text": "有提供圖片，請看圖。\n"})
                content_list.append({"type": "image", "image": img})
            except Exception as e:
                print(f"解析第 {i+1} 題圖片失敗: {e}")
                content_list.append({"type": "text", "text": "檔案損毀。\n"})
        else:
            content_list.append({"type": "text", "text": "學生沒有上傳本題的圖片。\n"})
            
    content_list.append({"type": "text", "text": "\n請開始你的批改："})
    messages.append({"role": "user", "content": content_list})
    
    return _run_streamer(messages, content_list)

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