from backend.database import SessionLocal, Problem

def seed_data():
    db = SessionLocal()
    
    if db.query(Problem).count() > 0:
        print("資料庫已有題目，跳過匯入。")
        db.close()
        return

    # 建立「01 乘法公式」的 10 題標準化題庫
    problems_data = [
        {
            "category": "國二上-1-1重點一-乘法公式",
            "image_path": "static/images/empty.jpg",
            "question_text": "展開 $(3x + 2)^2$ 的結果為何？\n(A) $9x^2 + 4$\n(B) $9x^2 + 6x + 4$\n(C) $9x^2 + 12x + 4$\n(D) $3x^2 + 12x + 4$",
            "detailed_solution": "預留詳解區塊"
        },
        {
            "category": "國二上-1-1重點一-乘法公式",
            "image_path": "static/images/empty.jpg",
            "question_text": "利用乘法公式計算 $102^2$ 的值為何？\n(A) $10404$\n(B) $10204$\n(C) $10004$\n(D) $10440$",
            "detailed_solution": "預留詳解區塊"
        },
        {
            "category": "國二上-1-1重點一-乘法公式",
            "image_path": "static/images/empty.jpg",
            "question_text": "展開 $(5x - 3y)^2$ 的結果為何？\n(A) $25x^2 - 9y^2$\n(B) $25x^2 - 30xy + 9y^2$\n(C) $25x^2 - 15xy + 9y^2$\n(D) $25x^2 + 30xy + 9y^2$",
            "detailed_solution": "預留詳解區塊"
        },
        {
            "category": "國二上-1-1重點一-乘法公式",
            "image_path": "static/images/empty.jpg",
            "question_text": "利用乘法公式計算 $98^2$ 的值為何？\n(A) $9604$\n(B) $9804$\n(C) $9904$\n(D) $9504$",
            "detailed_solution": "預留詳解區塊"
        },
        {
            "category": "國二上-1-1重點一-乘法公式",
            "image_path": "static/images/empty.jpg",
            "question_text": "展開 $(2x + 7)(2x - 7)$ 的結果為何？\n(A) $4x^2 - 14x - 49$\n(B) $4x^2 + 49$\n(C) $4x^2 - 49$\n(D) $2x^2 - 49$",
            "detailed_solution": "預留詳解區塊"
        },
        {
            "category": "國二上-1-1重點一-乘法公式",
            "image_path": "static/images/empty.jpg",
            "question_text": "利用乘法公式計算 $203 \\times 197$ 的值為何？\n(A) $39991$\n(B) $40009$\n(C) $39909$\n(D) $39999$",
            "detailed_solution": "預留詳解區塊"
        },
        {
            "category": "國二上-1-1重點一-乘法公式",
            "image_path": "static/images/empty.jpg",
            "question_text": "已知 $a+b=8$ 且 $ab=15$，求 $a^2+b^2$ 的值為何？\n(A) $34$\n(B) $49$\n(C) $64$\n(D) $19$",
            "detailed_solution": "預留詳解區塊"
        },
        {
            "category": "國二上-1-1重點一-乘法公式",
            "image_path": "static/images/empty.jpg",
            "question_text": "化簡 $(x+4)^2 - (x-4)^2$ 的結果為何？\n(A) $16x$\n(B) $8x$\n(C) $2x^2 + 32$\n(D) $0$",
            "detailed_solution": "預留詳解區塊"
        },
        {
            "category": "國二上-1-1重點一-乘法公式",
            "image_path": "static/images/empty.jpg",
            "question_text": "已知 $a-b=5$ 且 $ab=6$，求 $a^2+b^2$ 的值為何？\n(A) $25$\n(B) $37$\n(C) $13$\n(D) $31$",
            "detailed_solution": "預留詳解區塊"
        },
        {
            "category": "國二上-1-1重點一-乘法公式",
            "image_path": "static/images/empty.jpg",
            "question_text": "有一大正方形邊長為 $x$，內部挖去一個邊長為 $y$ 的小正方形，剩餘面積可表示為下列何者？\n(A) $(x-y)^2$\n(B) $(x+y)^2$\n(C) $(x+y)(x-y)$\n(D) $x^2 + y^2$",
            "detailed_solution": "預留詳解區塊"
        }
        
    ]

    for item in problems_data:
        new_prob = Problem(**item)
        db.add(new_prob)
        
    db.commit()
    print(f"✅ 成功匯入 {len(problems_data)} 題測試資料至 SQLite 資料庫！")
    db.close()

if __name__ == "__main__":
    seed_data()