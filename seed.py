from backend.database import SessionLocal, Problem

def seed_data():
    db = SessionLocal()
    
    if db.query(Problem).count() > 0:
        print("資料庫已有題目，跳過匯入。若要重新匯入，請先清空 Problem 資料表。")
        db.close()
        return

    problems_data = [
        # ==========================================
        # 1-1 乘法公式 (30題計算題 - 附完整詳解)
        # ==========================================
        {
            "category": "國二上-1-1-乘法公式",
            "image_path": "",
            "question_text": "利用分配律，計算 $21 \\times 104$ 的值為何？",
            "detailed_solution": "利用分配律展開：\n$21 \\times 104$\n$= 21 \\times (100 + 4)$\n$= 21 \\times 100 + 21 \\times 4$\n$= 2100 + 84$\n$= 2184$。"
        },
        {
            "category": "國二上-1-1-乘法公式",
            "image_path": "",
            "question_text": "利用分配律，計算 $18 \\times 97$ 的值為何？",
            "detailed_solution": "利用分配律展開：\n$18 \\times 97$\n$= 18 \\times (100 - 3)$\n$= 18 \\times 100 - 18 \\times 3$\n$= 1800 - 54$\n$= 1746$。"
        },
        {
            "category": "國二上-1-1-乘法公式",
            "image_path": "",
            "question_text": "若 $a$、$b$、$c$ 皆是整數，且 $a^2+b^2+c^2-ab-bc-ca=1$，試推論 $|a-b|$ 可能的值為何？",
            "detailed_solution": "將已知等式兩邊同乘 $2$：\n$2a^2+2b^2+2c^2-2ab-2bc-2ca = 2$\n重新分組配方：\n$(a^2-2ab+b^2) + (b^2-2bc+c^2) + (c^2-2ca+a^2) = 2$\n$(a-b)^2 + (b-c)^2 + (c-a)^2 = 2$\n因為 $a,b,c$ 為整數，所以三個括號的平方必定為大於等於 $0$ 的整數。\n三個完全平方數相加等於 $2$，唯一的組合為 $1 + 1 + 0$。\n因此 $(a-b)^2$ 的值只能是 $1$ 或 $0$。\n推論得出 $|a-b|$ 可能的值為 $1$ 或 $0$。"
        },
        {
            "category": "國二上-1-1-乘法公式",
            "image_path": "",
            "question_text": "請化簡 $(-x+y)^2$。",
            "detailed_solution": "利用差的平方公式，可將括號內提出負號：\n$(-x+y)^2$\n$= (-(x-y))^2$\n負號平方後變為正號：\n$= (x-y)^2$。"
        },
        {
            "category": "國二上-1-1-乘法公式",
            "image_path": "",
            "question_text": "若 $3x+25=9995^2$，則 $x$ 的值為何？",
            "detailed_solution": "移項得：$3x = 9995^2 - 25$\n$3x = 9995^2 - 5^2$\n利用平方差公式 $(a^2-b^2)=(a+b)(a-b)$：\n$3x = (9995+5)(9995-5)$\n$3x = 10000 \\times 9990$\n$3x = 99900000$\n兩邊同除以 $3$：\n$x = 33300000$。"
        },
        {
            "category": "國二上-1-1-乘法公式",
            "image_path": "",
            "question_text": "計算 $\\frac{2000^2+48 \\times 2000+24^2}{96 \\times 80+8^2}$ 之值為何？",
            "detailed_solution": "分子利用和的平方公式 $a^2+2ab+b^2=(a+b)^2$：\n$2000^2 + 2 \\times 24 \\times 2000 + 24^2 = (2000+24)^2 = 2024^2$\n分母整理後利用平方差公式：\n$96 \\times 80 + 8^2$\n$= (88+8)(88-8) + 8^2$\n$= (88^2 - 8^2) + 8^2$\n$= 88^2$\n原式 $= \\frac{2024^2}{88^2} = (\\frac{2024}{88})^2 = 23^2 = 529$。"
        },
        {
            "category": "國二上-1-1-乘法公式",
            "image_path": "",
            "question_text": "小億和小辰參加數學遊戲比賽，從卡片盒中各抽出一張數字卡，誰抽到的數字平方最接近 $2000^2$ 就獲勝。小億抽到 $1985$，小辰抽到 $2015$，請問誰會獲勝？",
            "detailed_solution": "計算兩人數字平方與 $2000^2$ 的差值（取絕對值）：\n小億：$|1985^2 - 2000^2|$\n$= |(2000-15)^2 - 2000^2|$\n$= |(2000^2 - 2 \\times 2000 \\times 15 + 15^2) - 2000^2|$\n$= |-60000 + 225| = 59775$\n小辰：$|2015^2 - 2000^2|$\n$= |(2000+15)^2 - 2000^2|$\n$= |(2000^2 + 2 \\times 2000 \\times 15 + 15^2) - 2000^2|$\n$= |60000 + 225| = 60225$\n因為 $59775 < 60225$，故小億的數字平方比較接近 $2000^2$，小億獲勝。"
        },
        {
            "category": "國二上-1-1-乘法公式",
            "image_path": "",
            "question_text": "已知 $(a+b)^2=7$，$(a-b)^2=4$，試求 $ab$ 之值為何？",
            "detailed_solution": "將兩式相減：\n$(a+b)^2 - (a-b)^2 = 7 - 4$\n展開左式：\n$(a^2+2ab+b^2) - (a^2-2ab+b^2) = 3$\n$4ab = 3$\n$ab = \\frac{3}{4}$。"
        },
        {
            "category": "國二上-1-1-乘法公式",
            "image_path": "",
            "question_text": "利用乘法公式計算 $402^2$ 之值為何？",
            "detailed_solution": "利用和的平方公式：\n$402^2 = (400+2)^2$\n$= 400^2 + 2 \\times 400 \\times 2 + 2^2$\n$= 160000 + 1600 + 4$\n$= 161604$。"
        },
        {
            "category": "國二上-1-1-乘法公式",
            "image_path": "",
            "question_text": "利用乘法公式計算 $303^2 - 2 \\times 303 \\times 3 + 3^2$ 之值為何？",
            "detailed_solution": "觀察式子符合差的平方公式 $a^2 - 2ab + b^2 = (a-b)^2$：\n令 $a=303$，$b=3$\n$303^2 - 2 \\times 303 \\times 3 + 3^2$\n$= (303 - 3)^2$\n$= 300^2$\n$= 90000$。"
        },
        {
            "category": "國二上-1-1-乘法公式",
            "image_path": "static/images/q11.jpg",
            "question_text": "在生活科技課程中，學生製作木工作品，所使用的木板如圖所示。已知甲木板為一個邊長 $70$ 公分的正方形，四個角落各切去一個邊長為 $10$ 公分的小正方形；乙木板為一個邊長 $72$ 公分的正方形，右上角切去一個長 $22$ 公分的小正方形。請計算並比較甲、乙兩塊木板的面積大小關係。",
            "detailed_solution": "甲木板面積 $= 70^2 - 4 \\times 10^2$\n$= 4900 - 4 \\times 100 = 4900 - 400 = 4500$\n乙木板面積 $= 72^2 - 22^2$\n利用平方差公式：\n$= (72+22)(72-22)$\n$= 94 \\times 50 = 4700$\n因為 $4700 > 4500$，所以乙木板面積 $>$ 甲木板面積。"
        },
        {
            "category": "國二上-1-1-乘法公式",
            "image_path": "static/images/q12.jpg",
            "question_text": "在生活科技課程中，王老師設計了一個邊長 $90$ 公分的正方形賽道，且中間挖出一個邊長 $20$ 公分的正方形空間放障礙物，如圖所示。則此賽道的面積為多少平方公分？",
            "detailed_solution": "賽道面積 $=$ 大正方形面積 $-$ 小正方形面積\n$= 90^2 - 20^2$\n利用平方差公式：\n$= (90+20)(90-20)$\n$= 110 \\times 70 = 7700$ 平方公分。"
        },
        {
            "category": "國二上-1-1-乘法公式",
            "image_path": "",
            "question_text": "已知 $299^2 = A + 1$，則 $A$ 的值為何？",
            "detailed_solution": "移項可得：\n$A = 299^2 - 1$\n$A = 299^2 - 1^2$\n利用平方差公式：\n$A = (299+1)(299-1)$\n$A = 300 \\times 298 = 89400$。"
        },
        {
            "category": "國二上-1-1-乘法公式",
            "image_path": "",
            "question_text": "已知 $(1993.5)^2 = 1993^2 + x$，則 $x$ 的值為何？",
            "detailed_solution": "移項可得：\n$x = 1993.5^2 - 1993^2$\n利用平方差公式：\n$x = (1993.5 + 1993)(1993.5 - 1993)$\n$x = 3986.5 \\times 0.5$\n$x = 1993.25$。"
        },
        {
            "category": "國二上-1-1-乘法公式",
            "image_path": "static/images/q15.jpg",
            "question_text": "如圖，將四個面積分別為 $ab$、$ad$、$bc$、$cd$ 的小長方形拼成一個大長方形，請利用因式分解，寫出此大長方形面積的乘積形式為何？",
            "detailed_solution": "大長方形的總面積為四個小長方形面積之和：\n面積 $= ab + ad + bc + cd$\n先將前兩項與後兩項分別提出公因式：\n$= a(b+d) + c(b+d)$\n再提出共同的公因式 $(b+d)$：\n$= (a+c)(b+d)$。"
        },
        {
            "category": "國二上-1-1-乘法公式",
            "image_path": "",
            "question_text": "利用和的平方公式，計算 $402^2 = 400^2 + \\square \\times 400 + 2^2$，則 $\\square$ 應填入的數字為何？",
            "detailed_solution": "利用和的平方公式 $(a+b)^2 = a^2 + 2ab + b^2$：\n$402^2 = (400+2)^2$\n$= 400^2 + 2 \\times 400 \\times 2 + 2^2$\n$= 400^2 + 4 \\times 400 + 2^2$\n對照題目等式，可知 $\\square = 4$。"
        },
        {
            "category": "國二上-1-1-乘法公式",
            "image_path": "",
            "question_text": "甲 $=\\frac{50^2 - 30^2}{20}$，乙 $=\\frac{100^2 - 20^2}{120}$，試比較甲、乙的大小關係。",
            "detailed_solution": "利用平方差公式分別計算甲、乙的值：\n甲 $= \\frac{(50+30)(50-30)}{20} = \\frac{80 \\times 20}{20} = 80$\n乙 $= \\frac{(100+20)(100-20)}{120} = \\frac{120 \\times 80}{120} = 80$\n因為計算結果皆為 $80$，故甲 $=$ 乙。"
        },
        {
            "category": "國二上-1-1-乘法公式",
            "image_path": "static/images/q18.jpg",
            "question_text": "如圖，大、小正方形的邊長分別為 $299$ 與 $99$，則圖中斜線部分的面積為多少平方單位？",
            "detailed_solution": "斜線部分面積 $=$ 大正方形面積 $-$ 小正方形面積\n$= 299^2 - 99^2$\n利用平方差公式：\n$= (299+99)(299-99)$\n$= 398 \\times 200 = 79600$ 平方單位。"
        },
        {
            "category": "國二上-1-1-乘法公式",
            "image_path": "static/images/q19.jpg",
            "question_text": "如圖，阿土伯有一正方形的土地，邊長為 $202\\frac{1}{2}$ 公尺，他從中間挖去一個邊長為 $197\\frac{1}{2}$ 公尺的正方形作游泳池，則剩下的走道部分（即斜線部分）的面積是多少平方公尺？",
            "detailed_solution": "斜線部分面積 $=$ 土地總面積 $-$ 游泳池面積\n$= (202.5)^2 - (197.5)^2$\n利用平方差公式：\n$= (202.5 + 197.5)(202.5 - 197.5)$\n$= 400 \\times 5 = 2000$ 平方公尺。"
        },
        {
            "category": "國二上-1-1-乘法公式",
            "image_path": "static/images/q20.jpg",
            "question_text": "如圖，已知大圓半徑為 $39$，小圓半徑為 $9$，求灰色部分的面積為多少平方單位？",
            "detailed_solution": "灰色部分面積 $=$ 大圓面積 $-$ 小圓面積\n$= \\pi \\times 39^2 - \\pi \\times 9^2$\n提出公因式 $\\pi$：\n$= \\pi(39^2 - 9^2)$\n利用平方差公式：\n$= \\pi(39+9)(39-9)$\n$= \\pi \\times 48 \\times 30 = 1440\\pi$ 平方單位。"
        },
        {
            "category": "國二上-1-1-乘法公式",
            "image_path": "static/images/q21.jpg",
            "question_text": "如圖，每一個角都是直角，求此 L 型六邊形的面積為多少平方單位？",
            "detailed_solution": "將圖形補齊成一個邊長為 $87$ 的大正方形，再扣除左上角缺少的正方形。\n缺少的正方形邊長為：$87 - 40 = 47$\nL 型面積 $=$ 大正方形面積 $-$ 小正方形面積\n$= 87^2 - 47^2$\n利用平方差公式：\n$= (87+47)(87-47)$\n$= 134 \\times 40 = 5360$ 平方單位。"
        },
        {
            "category": "國二上-1-1-乘法公式",
            "image_path": "",
            "question_text": "試化簡 $(2x-y)^2 + 2(2x-y)(2x+y) + (2x+y)^2$。",
            "detailed_solution": "觀察式子符合和的平方公式 $a^2 + 2ab + b^2 = (a+b)^2$：\n令 $a = (2x-y)$，$b = (2x+y)$\n原式 $= [(2x-y) + (2x+y)]^2$\n$= (2x - y + 2x + y)^2$\n$= (4x)^2 = 16x^2$。"
        },
        {
            "category": "國二上-1-1-乘法公式",
            "image_path": "",
            "question_text": "若 $a-b=5$，$ab=2$，求 $a^2+b^2$ 之值為何？",
            "detailed_solution": "利用差的平方公式變形：$a^2+b^2 = (a-b)^2 + 2ab$\n代入已知數值：\n$a^2+b^2 = 5^2 + 2 \\times 2$\n$= 25 + 4 = 29$。"
        },
        {
            "category": "國二上-1-1-乘法公式",
            "image_path": "",
            "question_text": "求大於 $(99.94)^2$ 的最小整數是多少？",
            "detailed_solution": "利用差的平方公式展開：\n$99.94^2 = (100 - 0.06)^2$\n$= 100^2 - 2 \\times 100 \\times 0.06 + 0.06^2$\n$= 10000 - 12 + 0.0036$\n$= 9988.0036$\n大於 $9988.0036$ 的最小整數為 $9989$。"
        },
        {
            "category": "國二上-1-1-乘法公式",
            "image_path": "static/images/q25.jpg",
            "question_text": "附圖是將兩個邊長分別為 $29$ 公分和 $19$ 公分的等腰直角三角形重疊後的圖形，試求出灰色部分的面積為多少平方公分？",
            "detailed_solution": "灰色部分面積 $=$ 大等腰直角三角形面積 $-$ 小等腰直角三角形面積\n$= \\frac{1}{2} \\times 29^2 - \\frac{1}{2} \\times 19^2$\n提出公因式 $\\frac{1}{2}$，並利用平方差公式：\n$= \\frac{1}{2}(29^2 - 19^2)$\n$= \\frac{1}{2}(29+19)(29-19)$\n$= \\frac{1}{2}(48 \\times 10) = 240$ 平方公分。"
        },
        {
            "category": "國二上-1-1-乘法公式",
            "image_path": "",
            "question_text": "請利用和的平方公式展開 $(a+b+c)^2$。",
            "detailed_solution": "將 $(a+b)$ 視為一項，利用和的平方公式展開：\n$(a+b+c)^2 = ((a+b)+c)^2$\n$= (a+b)^2 + 2(a+b)c + c^2$\n再次展開前方的和的平方，並分配律乘開中間項：\n$= (a^2+2ab+b^2) + (2ac+2bc) + c^2$\n依字母順序重新排列：\n$= a^2+b^2+c^2+2ab+2bc+2ca$。"
        },
        {
            "category": "國二上-1-1-乘法公式",
            "image_path": "",
            "question_text": "已知 $a-b=4$，$ab=5$，則 $a^2+b^2$ 的值為何？",
            "detailed_solution": "利用差的平方公式變形：$a^2+b^2 = (a-b)^2 + 2ab$\n代入已知數值：\n$a^2+b^2 = 4^2 + 2 \\times 5$\n$= 16 + 10 = 26$。"
        },
        {
            "category": "國二上-1-1-乘法公式",
            "image_path": "",
            "question_text": "已知 $a-b=7$，$ab=12$，試求 $a^2+b^2$ 的值為何？",
            "detailed_solution": "利用差的平方公式變形：$a^2+b^2 = (a-b)^2 + 2ab$\n代入已知數值：\n$a^2+b^2 = 7^2 + 2 \\times 12$\n$= 49 + 24 = 73$。"
        },
        {
            "category": "國二上-1-1-乘法公式",
            "image_path": "",
            "question_text": "利用乘法公式計算 $(172\\frac{1}{2})^2-(27\\frac{1}{2})^2$ 的值為何？",
            "detailed_solution": "將帶分數轉換為小數：$172.5^2 - 27.5^2$\n利用平方差公式：\n$= (172.5 + 27.5)(172.5 - 27.5)$\n$= 200 \\times 145 = 29000$。"
        },
        {
            "category": "國二上-1-1-乘法公式",
            "image_path": "static/images/q30.jpg",
            "question_text": "利用乘法公式，求出 $\\frac{388^2 - 232^2}{(388+232)^2}$ 的值為何？",
            "detailed_solution": "先分別計算分子與分母：\n分子利用平方差公式：\n$388^2 - 232^2 = (388+232)(388-232) = 620 \\times 156$\n分母計算底數相加：\n$(388+232)^2 = 620^2 = 620 \\times 620$\n原式 $= \\frac{620 \\times 156}{620 \\times 620}$\n約分消去 $620$：\n$= \\frac{156}{620}$\n分子分母同除以 $4$：\n$= \\frac{39}{155}$。"
        },
        {
            "category": "國二上-1-2-多項式的加減",
            "image_path": "",
            "question_text": "將多項式 $-5x^3 + 9 - 6x^2 + x$ 依降冪排列為何？",
            "detailed_solution": "降冪排列是將多項式各項的次數由大到小重新排列：\n最高次項為 $-5x^3$\n二次項為 $-6x^2$\n一次項為 $+x$\n常數項為 $+9$\n故降冪排列的結果為：$-5x^3 - 6x^2 + x + 9$。"
        },
        {
            "category": "國二上-1-2-多項式的加減",
            "image_path": "",
            "question_text": "將多項式 $-5x^3 + 9 - 6x^2 + x$ 依升冪排列為何？",
            "detailed_solution": "升冪排列是將多項式各項的次數由小到大重新排列：\n常數項為 $9$\n一次項為 $+x$\n二次項為 $-6x^2$\n最高次項為 $-5x^3$\n故升冪排列的結果為：$9 + x - 6x^2 - 5x^3$。"
        },
        {
            "category": "國二上-1-2-多項式的加減",
            "image_path": "",
            "question_text": "若 $ab=a-b$，且 $a$、$b$ 皆不為零，試求 $\\frac{a}{b} + \\frac{b}{a} - ab$ 的值為何？",
            "detailed_solution": "先將前兩項通分：\n$\\frac{a}{b} + \\frac{b}{a} = \\frac{a^2 + b^2}{ab}$\n利用差的平方公式將分子變形：$a^2 + b^2 = (a-b)^2 + 2ab$\n代回原式：$\\frac{(a-b)^2 + 2ab}{ab} - ab$\n因為已知 $a-b = ab$，將其代入分子中的 $(a-b)$：\n$= \\frac{(ab)^2 + 2ab}{ab} - ab$\n將分子提出公因式 $ab$ 約分：\n$= \\frac{ab(ab + 2)}{ab} - ab$\n$= (ab + 2) - ab = 2$。"
        },
        {
            "category": "國二上-1-2-多項式的加減",
            "image_path": "static/images/ch1_2_q4.jpg",
            "question_text": "如圖，請以 $x$ 的多項式表示此 H 型圖形的周長。",
            "detailed_solution": "計算多邊形周長可將所有水平線段與垂直線段加總：\n1. 水平線段總和：\n上方水平線段和 = $(2x-1) + (4x+3) + (2x-1) = 8x+1$\n下方水平線段和亦與上方總寬度相等，但需加上凹槽重複計算的部分。下凹槽水平長度為 $4x+3$，左右兩底水平長度之和為 $(8x+1) - (4x+3) = 4x-2$。\n故下方水平線段總和 = $(4x-2) + (4x+3) = 8x+1$。\n2. 垂直線段總和：\n左側外緣為 $6x-2$，右側外緣亦為 $6x-2$。\n上方凹槽垂直深度為 $3x-1$，共有左右兩段，貢獻 $2(3x-1) = 6x-2$。\n下方凹槽垂直深度為 $4$，共有左右兩段，貢獻 $2 \times 4 = 8$。\n3. 總周長：\n$= 2(8x+1) + 2(6x-2) + 2(3x-1) + 2(4)$\n$= (16x+2) + (12x-4) + (6x-2) + 8$\n$= 34x + 4$。"
        },
        {
            "category": "國二上-1-2-多項式的加減",
            "image_path": "",
            "question_text": "多項式 $3x^3 - 4x^2 + 3$ 的次數為何？並分別寫出 $x^3$ 項係數、$x^2$ 項係數、$x$ 項係數與常數項。",
            "detailed_solution": "1. 最高次方的指數為 $3$，故為「三」次多項式。\n2. $x^3$ 項的係數是 $3$。\n3. $x^2$ 項的係數是 $-4$（注意需包含前面的負號）。\n4. 式子中沒有出現 $x$ 項，代表 $x$ 項的係數是 $0$。\n5. 沒有未知數的項即為常數項，故常數項是 $3$。"
        },
        {
            "category": "國二上-1-2-多項式的加減",
            "image_path": "",
            "question_text": "有一多項式 $Q = 6x^2 + 3x - 7$，則 $Q$ 的各項係數和為何？",
            "detailed_solution": "多項式的各項係數和，即為將所有的係數與常數項相加：\n$x^2$ 項係數為 $6$\n$x$ 項係數為 $3$\n常數項為 $-7$\n各項係數和 $= 6 + 3 + (-7) = 2$。"
        },
        {
            "category": "國二上-1-2-多項式的加減",
            "image_path": "",
            "question_text": "若 $(7-5x) - A = -x^2 - 7x + 7$，試求多項式 $A$ 為何？",
            "detailed_solution": "依據等量公理移項：\n$A = (7-5x) - (-x^2 - 7x + 7)$\n去括號，注意後方括號內各項要變號：\n$A = 7 - 5x + x^2 + 7x - 7$\n合併同類項並依降冪排列：\n$A = x^2 + (-5x + 7x) + (7 - 7)$\n$A = x^2 + 2x$。"
        },
        {
            "category": "國二上-1-2-多項式的加減",
            "image_path": "",
            "question_text": "已知一多項式 $A$ 和另一多項式 $4x^2 - 7x + 4$ 的和為 $-x^2 + 8x - 3$，試求多項式 $A$ 為何？",
            "detailed_solution": "根據題意列式：\n$A + (4x^2 - 7x + 4) = -x^2 + 8x - 3$\n移項求 $A$：\n$A = (-x^2 + 8x - 3) - (4x^2 - 7x + 4)$\n去括號並變號：\n$A = -x^2 + 8x - 3 - 4x^2 + 7x - 4$\n合併同類項：\n$A = (-1 - 4)x^2 + (8 + 7)x + (-3 - 4)$\n$A = -5x^2 + 15x - 7$。"
        },
        {
            "category": "國二上-1-2-多項式的加減",
            "image_path": "",
            "question_text": "計算 $(2x^2 - 5x + 4) + (3x^3 + 3x^2 + 2x - 5)$ 的結果為何？",
            "detailed_solution": "去括號後，將同類項合併並依降冪排列：\n原式 $= 3x^3 + (2x^2 + 3x^2) + (-5x + 2x) + (4 - 5)$\n$= 3x^3 + 5x^2 - 3x - 1$。"
        },
        {
            "category": "國二上-1-2-多項式的加減",
            "image_path": "",
            "question_text": "化簡 $(3x^2 - 5 + 2x) - (4x + 5) + (7 - 2x^2 + 3x)$ 並將結果依升冪排列。",
            "detailed_solution": "先去括號（注意減號後方的項要變號）：\n原式 $= 3x^2 - 5 + 2x - 4x - 5 + 7 - 2x^2 + 3x$\n合併同類項：\n$x^2$ 項：$3x^2 - 2x^2 = x^2$\n$x$ 項：$2x - 4x + 3x = x$\n常數項：$-5 - 5 + 7 = -3$\n合併結果為：$x^2 + x - 3$\n題目要求「依升冪排列」（次方由小到大）：\n故答案為：$-3 + x + x^2$。"
        },
        {
            "category": "國二上-1-2-多項式的加減",
            "image_path": "",
            "question_text": "設 $a$、$b$、$c$ 皆是常數，且 $(a-3)x^2 + (b+5)x + (c-7)$ 是常數多項式，且常數項為 $0$，則 $a+b+c$ 的值為何？",
            "detailed_solution": "因為此多項式為「常數多項式」，代表所有含有 $x$ 的項其係數皆為 $0$：\n$x^2$ 係數為 $0 \\Rightarrow a - 3 = 0 \\Rightarrow a = 3$\n$x$ 係數為 $0 \\Rightarrow b + 5 = 0 \\Rightarrow b = -5$\n又已知常數項為 $0$：\n常數項為 $0 \\Rightarrow c - 7 = 0 \\Rightarrow c = 7$\n計算所求：$a + b + c = 3 + (-5) + 7 = 5$。"
        },
        {
            "category": "國二上-1-2-多項式的加減",
            "image_path": "",
            "question_text": "計算 $6x + (7x-1) - (8x^2+2)$ 的結果並依降冪排列。",
            "detailed_solution": "去括號，減號後方的項需變號：\n原式 $= 6x + 7x - 1 - 8x^2 - 2$\n合併同類項並依降冪（二次 $\\rightarrow$ 一次 $\\rightarrow$ 常數）排列：\n$= -8x^2 + (6x + 7x) + (-1 - 2)$\n$= -8x^2 + 13x - 3$。"
        },
        {
            "category": "國二上-1-2-多項式的加減",
            "image_path": "",
            "question_text": "計算 $-(8x^2-2) - 3x + (6x+1)$ 的結果並依降冪排列。",
            "detailed_solution": "去括號，注意第一個括號前方有負號需變號：\n原式 $= -8x^2 + 2 - 3x + 6x + 1$\n合併同類項並依降冪排列：\n$= -8x^2 + (-3x + 6x) + (2 + 1)$\n$= -8x^2 + 3x + 3$。"
        },
        {
            "category": "國二上-1-2-多項式的加減",
            "image_path": "static/images/ch1_2_q14.jpg",
            "question_text": "如圖，請以 $x$ 的多項式來表示此階梯圖形的周長。",
            "detailed_solution": "計算周長需將外圍所有線段加總。令未知水平段為 $w_1$，未知垂直段為 $v_1$：\n1. 找尋總寬度：最寬處由上方的 $3$ 與 $2x+4$ 構成，故總寬度為 $3 + (2x+4) = 2x+7$。底部的總寬度應等於上方，故 $x + w_1 = 2x+7 \\Rightarrow w_1 = x+7$。\n2. 找尋總高度：右側為 $3x+4$ 且繼續往下走 $2$，故總高度為 $(3x+4) + 2 = 3x+6$。左側總高度應與右側相等，故 $(5x+2) + v_1 = 3x+6 \\Rightarrow v_1 = -2x+4$。\n3. 將所有邊長相加：\n$P = (5x+2) + 3 + (-2x+4) + (2x+4) + (3x+4) + x + 2 + (x+7)$\n合併所有 $x$ 項：$5x - 2x + 2x + 3x + x + x = 10x$\n合併所有常數項：$2 + 3 + 4 + 4 + 4 + 2 + 7 = 26$\n總周長為：$10x + 26$。"
        },
        {
            "category": "國二上-1-2-多項式的加減",
            "image_path": "",
            "question_text": "若 $(7x^2 - 6x + 5) - (5 - 7x) = ax^2 + bx + c$，試求 $cx^2 + ax + b + (x^2 + 2)$ 的多項式為何？",
            "detailed_solution": "先化簡等號左邊的多項式：\n$(7x^2 - 6x + 5) - 5 + 7x$\n$= 7x^2 + (-6x + 7x) + (5 - 5)$\n$= 7x^2 + x + 0$\n對照等號右邊的 $ax^2 + bx + c$，可得：\n$a = 7$, $b = 1$, $c = 0$\n將 $a, b, c$ 的值代入所求式子：\n$cx^2 + ax + b + (x^2 + 2)$\n$= 0 \\cdot x^2 + 7x + 1 + x^2 + 2$\n$= x^2 + 7x + 3$。"
        },
        {
            "category": "國二上-1-2-多項式的加減",
            "image_path": "",
            "question_text": "計算 $(x^2 - 2) - [3x^2 + 2x - 5 - 2(3x^2 - 1)]$ 的結果並依降冪排列。",
            "detailed_solution": "根據四則運算規則，先從中括號內部開始化簡：\n$[3x^2 + 2x - 5 - 6x^2 + 2]$\n$= -3x^2 + 2x - 3$\n將化簡結果代回原式：\n$= (x^2 - 2) - (-3x^2 + 2x - 3)$\n去括號並變號：\n$= x^2 - 2 + 3x^2 - 2x + 3$\n合併同類項：\n$= 4x^2 - 2x + 1$。"
        },
        {
            "category": "國二上-1-2-多項式的加減",
            "image_path": "",
            "question_text": "已知多項式 $A = x^2 + 4x + 3$，且 $A - B = -6x^2 - 5x + 4$，則多項式 $B$ 為何？",
            "detailed_solution": "由 $A - B = -6x^2 - 5x + 4$ 移項可推得：\n$B = A - (-6x^2 - 5x + 4)$\n將多項式 $A$ 代入：\n$B = (x^2 + 4x + 3) + 6x^2 + 5x - 4$\n合併同類項：\n$B = (1+6)x^2 + (4+5)x + (3-4)$\n$B = 7x^2 + 9x - 1$。"
        },
        {
            "category": "國二上-1-2-多項式的加減",
            "image_path": "static/images/ch1_2_q18.jpg",
            "question_text": "有甲、乙、丙、丁四塊積木，其面積分別為甲：$x^2+7$，乙：$4x-2$，丙：$3x^3-2x^2-x$，丁：$9$。翰翰發現這四塊積木恰巧可拼成一個等腰梯形（如圖），則此梯形面積為多少平方單位？",
            "detailed_solution": "梯形面積即為這四塊積木面積的總和：\n總面積 = 甲 + 乙 + 丙 + 丁\n$= (x^2+7) + (4x-2) + (3x^3-2x^2-x) + 9$\n去括號並將同類項合併，依降冪排列：\n最高次為 $3x^3$\n二次項為 $x^2 - 2x^2 = -x^2$\n一次項為 $4x - x = 3x$\n常數項為 $7 - 2 + 9 = 14$\n故梯形總面積為 $3x^3 - x^2 + 3x + 14$ 平方單位。"
        },
        {
            "category": "國二上-1-2-多項式的加減",
            "image_path": "",
            "question_text": "計算 $(5x^2 - 7x - 3) + (-6x^2 + 5x + 6) + (4x^2 - 2x)$ 的結果並依降冪排列。",
            "detailed_solution": "去括號後，將同類項合併：\n原式 $= 5x^2 - 7x - 3 - 6x^2 + 5x + 6 + 4x^2 - 2x$\n$x^2$ 項：$5 - 6 + 4 = 3 \\Rightarrow 3x^2$\n$x$ 項：$-7 + 5 - 2 = -4 \\Rightarrow -4x$\n常數項：$-3 + 6 = 3$\n結果為：$3x^2 - 4x + 3$。"
        },
        {
            "category": "國二上-1-2-多項式的加減",
            "image_path": "",
            "question_text": "大寶作兩個多項式直式加法，已知 $(x^2 + bx - 8) + (ax^2 - 6x + c) = -3x^2 + 7x - 7$，求 $a-b-c$ 的值為何？",
            "detailed_solution": "利用直式加法上下同類項相加等於結果的概念，對照係數：\n$x^2$ 項：$1 + a = -3 \\Rightarrow a = -4$\n$x$ 項：$b + (-6) = 7 \\Rightarrow b = 13$\n常數項：$-8 + c = -7 \\Rightarrow c = 1$\n將 $a, b, c$ 代入所求：\n$a - b - c = -4 - 13 - 1 = -18$。"
        },
        {
            "category": "國二上-1-2-多項式的加減",
            "image_path": "",
            "question_text": "計算 $(x+1)^2 - x^2 + (x-1)^2 - (x-2)^2$ 之值為何？[cite: 60]",
            "detailed_solution": "利用乘法公式將各項展開：\n$(x+1)^2 = x^2+2x+1$\n$(x-1)^2 = x^2-2x+1$\n$(x-2)^2 = x^2-4x+4$\n代回原式並去括號：\n$(x^2+2x+1) - x^2 + (x^2-2x+1) - (x^2-4x+4)$\n$= x^2 + 2x + 1 - x^2 + x^2 - 2x + 1 - x^2 + 4x - 4$\n合併同類項：\n$x^2$ 項：$1 - 1 + 1 - 1 = 0$\n$x$ 項：$2x - 2x + 4x = 4x$\n常數項：$1 + 1 - 4 = -2$\n故計算結果為：$4x - 2$。"
        },
        {
            "category": "國二上-1-2-多項式的加減",
            "image_path": "",
            "question_text": "小薰計算 $A + (3x^2+x-8) = 4x^2$，小寶計算 $(5x^2-6x+2) - B = 7x^2-3x+6$，試求 $A - B$ 的值。[cite: 61]",
            "detailed_solution": "先分別求出多項式 $A$ 與 $B$：\n$A = 4x^2 - (3x^2+x-8)$\n$A = 4x^2 - 3x^2 - x + 8 = x^2 - x + 8$\n\n$B = (5x^2-6x+2) - (7x^2-3x+6)$\n$B = 5x^2 - 6x + 2 - 7x^2 + 3x - 6 = -2x^2 - 3x - 4$\n\n計算 $A - B$：\n$A - B = (x^2 - x + 8) - (-2x^2 - 3x - 4)$\n$= x^2 - x + 8 + 2x^2 + 3x + 4$\n$= 3x^2 + 2x + 12$。"
        },
        {
            "category": "國二上-1-2-多項式的加減",
            "image_path": "static/images/ch1_2_q23.jpg",
            "question_text": "如圖，四邊形 $ABCD$ 和四邊形 $AEFG$ 皆為長方形。已知 $AG=2x+7, GD=10, AE=3x, EB=3x+6$，求矩形 $AEFG$ 的周長？[cite: 62]",
            "detailed_solution": "矩形 $AEFG$ 的長為 $AG = 2x+7$，寬為 $AE = 3x$。\n矩形周長 $= 2 \\times (長 + 寬)$\n$= 2 \\times [(2x+7) + 3x]$\n$= 2 \\times (5x+7)$\n$= 10x + 14$。"
        },
        {
            "category": "國二上-1-2-多項式的加減",
            "image_path": "static/images/ch1_2_q24.jpg",
            "question_text": "承上題，如圖，四邊形 $ABCD$ 和四邊形 $AEFG$ 皆為長方形。已知 $AG=2x+7, GD=10, AE=3x, EB=3x+6$，求斜線區域的周長？[cite: 62]",
            "detailed_solution": "斜線區域周長為包圍斜線部分的六個線段長度總和，即 $\\overline{EB} + \\overline{BC} + \\overline{CD} + \\overline{DG} + \\overline{GF} + \\overline{FE}$。\n先求出大長方形的長與寬：\n$\\overline{AD} = \\overline{AG} + \\overline{GD} = (2x+7) + 10 = 2x+17 = \\overline{BC}$\n$\\overline{AB} = \\overline{AE} + \\overline{EB} = 3x + (3x+6) = 6x+6 = \\overline{CD}$\n再找出內部線段：\n$\\overline{GF} = \\overline{AE} = 3x$（矩形對邊）\n$\\overline{FE} = \\overline{AG} = 2x+7$（矩形對邊）\n將六段相加：\n$(3x+6) + (2x+17) + (6x+6) + 10 + 3x + (2x+7)$\n合併 $x$ 項：$3x + 2x + 6x + 3x + 2x = 16x$\n合併常數項：$6 + 17 + 6 + 10 + 7 = 46$\n故斜線區域周長為：$16x + 46$。"
        },
        {
            "category": "國二上-1-2-多項式的加減",
            "image_path": "",
            "question_text": "若有三個多項式分別為 $A=3x^2+4x-5$，$B=-x^2+6$，$C=x^2-7x+4$，則 $A+B-C = $？[cite: 63]",
            "detailed_solution": "將多項式代入式子中：\n$A+B-C = (3x^2+4x-5) + (-x^2+6) - (x^2-7x+4)$\n去括號並變號：\n$= 3x^2 + 4x - 5 - x^2 + 6 - x^2 + 7x - 4$\n合併同類項：\n$x^2$ 項：$3 - 1 - 1 = 1$\n$x$ 項：$4 + 7 = 11$\n常數項：$-5 + 6 - 4 = -3$\n故結果為：$x^2 + 11x - 3$。"
        },
        {
            "category": "國二上-1-2-多項式的加減",
            "image_path": "",
            "question_text": "若有三個多項式分別為 $A=3x^2+4x-5$，$B=-x^2+6$，$C=x^2-7x+4$，則 $3A-(B-2C) = $？[cite: 63]",
            "detailed_solution": "先將所求式子化簡：\n$3A - (B - 2C) = 3A - B + 2C$\n將多項式代入：\n$= 3(3x^2+4x-5) - (-x^2+6) + 2(x^2-7x+4)$\n展開括號：\n$= (9x^2+12x-15) + x^2 - 6 + (2x^2-14x+8)$\n合併同類項：\n$x^2$ 項：$9 + 1 + 2 = 12$\n$x$ 項：$12 - 14 = -2$\n常數項：$-15 - 6 + 8 = -13$\n故結果為：$12x^2 - 2x - 13$。"
        },
        {
            "category": "國二上-1-2-多項式的加減",
            "image_path": "",
            "question_text": "化簡 $(-5x-9x^2+3) + (6x^2-5+4x) = ax^2+bx+c$，則 $a-b-c = $？[cite: 64]",
            "detailed_solution": "先將左式合併同類項並依降冪排列：\n$(-9x^2 - 5x + 3) + (6x^2 + 4x - 5)$\n$= (-9+6)x^2 + (-5+4)x + (3-5)$\n$= -3x^2 - x - 2$\n對照等號右邊的式子 $ax^2+bx+c$，可得：\n$a = -3$, $b = -1$, $c = -2$\n計算所求：\n$a - b - c = (-3) - (-1) - (-2)$\n$= -3 + 1 + 2 = 0$。"
        },
        {
            "category": "國二上-1-2-多項式的加減",
            "image_path": "",
            "question_text": "計算 $(x^2-1) - [2x^2-x-4+(2x^2-1)] = $？[cite: 65]",
            "detailed_solution": "根據運算法則，先化簡中括號裡面的式子：\n$2x^2 - x - 4 + 2x^2 - 1 = 4x^2 - x - 5$\n將化簡結果代回原式：\n$(x^2-1) - (4x^2 - x - 5)$\n去括號並變號：\n$= x^2 - 1 - 4x^2 + x + 5$\n合併同類項：\n$= -3x^2 + x + 4$。"
        },
        {
            "category": "國二上-1-2-多項式的加減",
            "image_path": "",
            "question_text": "一數學題「兩個多項式 $P$、$Q$，其中 $Q$ 為 $2x^2+x-1$，試求 $P+Q$」，但是小薰在解此題時誤將 $P+Q$ 看成 $P-Q$，除此之外沒有其他計算上的錯誤，算出的答案為 $5x^2-3x-7$，求多項式 $P = $？[cite: 66]",
            "detailed_solution": "根據題意，小薰實際計算的式子為：\n$P - Q = 5x^2 - 3x - 7$\n移項可求得 $P$：\n$P = (5x^2 - 3x - 7) + Q$\n將 $Q = 2x^2+x-1$ 代入：\n$P = (5x^2 - 3x - 7) + (2x^2 + x - 1)$\n合併同類項：\n$P = (5+2)x^2 + (-3+1)x + (-7-1)$\n$P = 7x^2 - 2x - 8$。"
        },
        {
            "category": "國二上-1-2-多項式的加減",
            "image_path": "",
            "question_text": "計算 $(2x^2+3x+6) + (x^2+3x+15) + (-2x+4x^2+1)$ 的結果。[cite: 67]",
            "detailed_solution": "去括號，將所有同類項合併：\n$x^2$ 項：$2x^2 + x^2 + 4x^2 = 7x^2$\n$x$ 項：$3x + 3x - 2x = 4x$\n常數項：$6 + 15 + 1 = 22$\n合併結果為：$7x^2 + 4x + 22$。"
        },
        {
            "category": "國二上-1-2-多項式的加減",
            "image_path": "",
            "question_text": "計算 $(-7x^2+12) - (6x^2+4x-5) = $？[cite: 68]",
            "detailed_solution": "去括號，注意減號後方的所有項都要變號：\n$-7x^2 + 12 - 6x^2 - 4x + 5$\n合併同類項並依降冪排列：\n$= (-7x^2 - 6x^2) - 4x + (12 + 5)$\n$= -13x^2 - 4x + 17$。"
        },
        # ==========================================
        # 1-3 多項式的乘除
        # ==========================================
        {
            "category": "國二上-1-3-多項式的乘除",
            "image_path": "",
            "question_text": "計算 $(x^2-1) - [2x^2-x-4+(2x^2-1)] = $？[cite: 69]",
            "detailed_solution": "先將中括號內的同類項合併：\n$2x^2 - x - 4 + 2x^2 - 1 = 4x^2 - x - 5$\n代回原式並去括號，減號後的項需變號：\n$(x^2-1) - (4x^2 - x - 5)$\n$= x^2 - 1 - 4x^2 + x + 5$\n將同類項合併並依降冪排列：\n$= -3x^2 + x + 4$。"
        },
        {
            "category": "國二上-1-3-多項式的乘除",
            "image_path": "",
            "question_text": "一數學題「兩個多項式 $P$、$Q$，其中 $Q$ 為 $2x^2+x-1$，試求 $P+Q$」，但是小薰在解此題時誤將 $P+Q$ 看成 $P-Q$，除此之外沒有其他計算上的錯誤，算出的答案為 $5x^2-3x-7$，求正確的答案 $P+Q = $？[cite: 70]",
            "detailed_solution": "已知小薰的算式為：$P - Q = 5x^2 - 3x - 7$\n移項求出多項式 $P$：\n$P = (5x^2 - 3x - 7) + Q$\n$P = (5x^2 - 3x - 7) + (2x^2 + x - 1)$\n$P = 7x^2 - 2x - 8$\n接著求正確的答案 $P+Q$：\n$P+Q = (7x^2 - 2x - 8) + (2x^2 + x - 1)$\n$= (7+2)x^2 + (-2+1)x + (-8-1)$\n$= 9x^2 - x - 9$。"
        },
        {
            "category": "國二上-1-3-多項式的乘除",
            "image_path": "",
            "question_text": "計算 $(2x^2+3x+6) + (x^2+3x+15) + (-2x+4x^2+1)$ 的結果。[cite: 71]",
            "detailed_solution": "將括號去掉後，把所有同類項合併並依降冪排列：\n$x^2$ 項：$2x^2 + x^2 + 4x^2 = 7x^2$\n$x$ 項：$3x + 3x - 2x = 4x$\n常數項：$6 + 15 + 1 = 22$\n合併結果為：$7x^2 + 4x + 22$。"
        },
        {
            "category": "國二上-1-3-多項式的乘除",
            "image_path": "",
            "question_text": "計算 $(-7x^2+12) - (6x^2+4x-5) = $？[cite: 72]",
            "detailed_solution": "去括號，注意減號後方的所有項都要變號：\n$-7x^2 + 12 - 6x^2 - 4x + 5$\n合併同類項並依降冪排列：\n$= (-7x^2 - 6x^2) - 4x + (12 + 5)$\n$= -13x^2 - 4x + 17$。"
        },
        {
            "category": "國二上-1-3-多項式的乘除",
            "image_path": "",
            "question_text": "計算 $(7x^2+x-4) \\div (7x-4)$ 的商式和餘式分別為何？[cite: 73]",
            "detailed_solution": "利用長除法進行多項式除法：\n1. 用被除式的首項 $7x^2$ 除以除式的首項 $7x$，得商的首項為 $x$。\n2. 將 $x$ 乘上除式 $(7x-4)$，得到 $7x^2 - 4x$。\n3. 相減：$(7x^2 + x - 4) - (7x^2 - 4x) = 5x - 4$。\n由於餘下的式子次數 ($1$次) 並未小於除式的次數 ($1$次)，繼續除。\n但觀察此處長除法，若繼續除，$\\frac{5x}{7x} = \\frac{5}{7}$。\n重新整理長除法步驟：\n$$ \\require{enclose} \\begin{array}{rll} x + \\frac{5}{7} \\phantom{0000} \\\\[-3pt] 7x-4 \\enclose{longdiv}{ 7x^2 + x - 4 \\phantom{0}} \\\\[-3pt] \\underline{-(7x^2 - 4x) \\phantom{00}} \\\\[-3pt] 5x - 4 \\phantom{0} \\\\[-3pt] \\underline{-(5x - \\frac{20}{7}) } \\\\[-3pt] -\\frac{8}{7} \\phantom{0} \\end{array} $$\n故商式為 $x + \\frac{5}{7}$，餘式為 $-\\frac{8}{7}$。"
        },
        {
            "category": "國二上-1-3-多項式的乘除",
            "image_path": "",
            "question_text": "化簡 $(x-1)(x+2)(x-5) = $？[cite: 75]",
            "detailed_solution": "先將前兩個括號利用分配律展開（或利用公式 $(x+a)(x+b) = x^2+(a+b)x+ab$）：\n$(x-1)(x+2) = x^2 + (2-1)x + (-1)(2) = x^2 + x - 2$\n再將得到的結果與第三個括號相乘：\n$(x^2 + x - 2)(x - 5)$\n$= x^2(x - 5) + x(x - 5) - 2(x - 5)$\n$= x^3 - 5x^2 + x^2 - 5x - 2x + 10$\n合併同類項並依降冪排列：\n$= x^3 - 4x^2 - 7x + 10$。"
        },
        {
            "category": "國二上-1-3-多項式的乘除",
            "image_path": "",
            "question_text": "計算 $(-5x^2+2x+1) \\div (-2x+1)$ 的商式及餘式。[cite: 76]",
            "detailed_solution": "利用長除法進行多項式除法：\n$$ \\require{enclose} \\begin{array}{rll} \\frac{5}{2}x + \\frac{1}{4} \\phantom{0000} \\\\[-3pt] -2x+1 \\enclose{longdiv}{ -5x^2 + 2x + 1 \\phantom{0}} \\\\[-3pt] \\underline{-(-5x^2 + \\frac{5}{2}x) \\phantom{00}} \\\\[-3pt] -\\frac{1}{2}x + 1 \\phantom{0} \\\\[-3pt] \\underline{-(-\\frac{1}{2}x + \\frac{1}{4}) } \\\\[-3pt] \\frac{3}{4} \\phantom{0} \\end{array} $$\n故商式為 $\\frac{5}{2}x + \\frac{1}{4}$，餘式為 $\\frac{3}{4}$。"
        },
        # ==========================================
        # 2-1 平方根的意義 (20題 計算題)
        # ==========================================
        {
            "category": "國二上-2-1-平方根的意義",
            "image_path": "",
            "question_text": "求 $144$ 的平方根為何？",
            "detailed_solution": "因為 $12^2 = 144$ 且 $(-12)^2 = 144$，正數的平方根會有正負兩個，故 $144$ 的平方根為 $\\pm 12$。"
        },
        {
            "category": "國二上-2-1-平方根的意義",
            "image_path": "",
            "question_text": "計算 $\\sqrt{225}$ 的值為何？",
            "detailed_solution": "$\\sqrt{225}$ 代表求 $225$ 的「正」平方根。\n因為 $15^2 = 225$，所以 $\\sqrt{225} = 15$。"
        },
        {
            "category": "國二上-2-1-平方根的意義",
            "image_path": "",
            "question_text": "判斷 $-\\sqrt{49}$ 的值為何？",
            "detailed_solution": "$-\\sqrt{49}$ 代表求 $49$ 的「負」平方根。\n因為 $7^2 = 49$，所以 $-\\sqrt{49} = -7$。"
        },
        {
            "category": "國二上-2-1-平方根的意義",
            "image_path": "",
            "question_text": "若 $x^2 = 81$，求 $x$ 的值為何？",
            "detailed_solution": "由 $x^2 = 81$ 可知 $x$ 為 $81$ 的平方根。\n$81$ 的平方根為 $\\pm 9$，故 $x = \\pm 9$。"
        },
        {
            "category": "國二上-2-1-平方根的意義",
            "image_path": "",
            "question_text": "計算 $\\sqrt{(-13)^2}$ 的值為何？",
            "detailed_solution": "先計算根號內部的平方：$(-13)^2 = 169$。\n再來求 $169$ 的正平方根：$\\sqrt{169} = 13$。\n(觀念：$\\sqrt{a^2} = |a|$)。"
        },
        {
            "category": "國二上-2-1-平方根的意義",
            "image_path": "",
            "question_text": "若 $2x-1$ 的平方根為 $\\pm 5$，求 $x$ 的值為何？",
            "detailed_solution": "已知 $2x-1$ 的平方根是 $\\pm 5$，代表 $2x-1$ 等於 $(\\pm 5)$ 的平方。\n$2x-1 = (\\pm 5)^2$\n$2x-1 = 25$\n$2x = 26$\n$x = 13$。"
        },
        {
            "category": "國二上-2-1-平方根的意義",
            "image_path": "",
            "question_text": "請比較 $\\sqrt{10}$、$3$、$\\sqrt{11}$ 三數的大小關係。",
            "detailed_solution": "為了方便比較，將所有數字都化為根號形式：\n$3 = \\sqrt{3^2} = \\sqrt{9}$。\n因為 $9 < 10 < 11$，所以 $\\sqrt{9} < \\sqrt{10} < \\sqrt{11}$。\n故大小關係為：$3 < \\sqrt{10} < \\sqrt{11}$。"
        },
        {
            "category": "國二上-2-1-平方根的意義",
            "image_path": "",
            "question_text": "若 $a$ 為正整數，且 $a < \\sqrt{50} < a+1$，求 $a$ 的值為何？",
            "detailed_solution": "尋找最接近 $50$ 的完全平方數：\n$7^2 = 49$，$8^2 = 64$。\n因為 $49 < 50 < 64$，所以 $\\sqrt{49} < \\sqrt{50} < \\sqrt{64}$，也就是 $7 < \\sqrt{50} < 8$。\n對照 $a < \\sqrt{50} < a+1$，可得 $a = 7$。"
        },
        {
            "category": "國二上-2-1-平方根的意義",
            "image_path": "",
            "question_text": "滿足 $4 < \\sqrt{x} < 5$ 的整數 $x$ 共有幾個？",
            "detailed_solution": "將不等式各項同時平方：\n$4^2 < (\\sqrt{x})^2 < 5^2$\n$16 < x < 25$\n滿足此條件的整數 $x$ 有：$17, 18, 19, 20, 21, 22, 23, 24$。\n總共有 $24 - 17 + 1 = 8$ 個。"
        },
        {
            "category": "國二上-2-1-平方根的意義",
            "image_path": "",
            "question_text": "若 $\\sqrt{x-3} = 4$，求 $x$ 的值為何？",
            "detailed_solution": "將等式兩邊同時平方：\n$(\\sqrt{x-3})^2 = 4^2$\n$x - 3 = 16$\n移項得 $x = 16 + 3 = 19$。"
        },
        {
            "category": "國二上-2-1-平方根的意義",
            "image_path": "",
            "question_text": "求 $0.0144$ 的平方根為何？",
            "detailed_solution": "將小數化為分數：$0.0144 = \\frac{144}{10000}$。\n求平方根：$\\pm \\sqrt{\\frac{144}{10000}} = \\pm \\frac{12}{100}$。\n化為小數為 $\\pm 0.12$。"
        },
        {
            "category": "國二上-2-1-平方根的意義",
            "image_path": "",
            "question_text": "估算 $\\sqrt{20}$ 的整數部分為何？",
            "detailed_solution": "找尋最接近 $20$ 的完全平方數：\n$4^2 = 16$，$5^2 = 25$。\n因為 $16 < 20 < 25$，所以 $\\sqrt{16} < \\sqrt{20} < \\sqrt{25}$，即 $4 < \\sqrt{20} < 5$。\n故 $\\sqrt{20}$ 的整數部分為 $4$。"
        },
        {
            "category": "國二上-2-1-平方根的意義",
            "image_path": "",
            "question_text": "計算 $\\sqrt{2^4 \\times 3^2}$ 的值為何？",
            "detailed_solution": "利用指數律化簡根號內部的數：\n$\\sqrt{2^4 \\times 3^2} = \\sqrt{(2^2 \\times 3)^2}$\n$= \\sqrt{(4 \\times 3)^2} = \\sqrt{12^2}$\n$= 12$。"
        },
        {
            "category": "國二上-2-1-平方根的意義",
            "image_path": "",
            "question_text": "若 $\\sqrt{2x+5} = 7$，求 $x$ 的值為何？",
            "detailed_solution": "將等式兩邊同時平方以消除根號：\n$(\\sqrt{2x+5})^2 = 7^2$\n$2x + 5 = 49$\n$2x = 44$\n$x = 22$。"
        },
        {
            "category": "國二上-2-1-平方根的意義",
            "image_path": "",
            "question_text": "計算 $-\\sqrt{\\frac{16}{25}}$ 的值為何？",
            "detailed_solution": "根號內為分數時，可分別對分子與分母開根號：\n$-\\sqrt{\\frac{16}{25}} = -\\frac{\\sqrt{16}}{\\sqrt{25}}$\n$= -\\frac{4}{5}$。"
        },
        {
            "category": "國二上-2-1-平方根的意義",
            "image_path": "",
            "question_text": "求帶分數 $1\\frac{9}{16}$ 的平方根為何？",
            "detailed_solution": "先將帶分數化為假分數：$1\\frac{9}{16} = \\frac{25}{16}$。\n求平方根：$\\pm \\sqrt{\\frac{25}{16}} = \\pm \\frac{5}{4}$。"
        },
        {
            "category": "國二上-2-1-平方根的意義",
            "image_path": "",
            "question_text": "滿足 $\\sqrt{30} < x < \\sqrt{80}$ 的正整數 $x$ 有哪些？",
            "detailed_solution": "將不等式各項同時平方：\n$30 < x^2 < 80$\n尋找平方後介於 $30$ 到 $80$ 之間的正整數：\n$5^2 = 25$ (太小)\n$6^2 = 36$ (符合)\n$7^2 = 49$ (符合)\n$8^2 = 64$ (符合)\n$9^2 = 81$ (太大)\n故滿足條件的正整數 $x$ 為 $6, 7, 8$。"
        },
        {
            "category": "國二上-2-1-平方根的意義",
            "image_path": "",
            "question_text": "若 $-3$ 是 $2x+1$ 的其中一個平方根，求 $x$ 的值為何？",
            "detailed_solution": "因為 $-3$ 是 $2x+1$ 的平方根，代表 $(-3)$ 的平方會等於 $2x+1$。\n$(-3)^2 = 2x+1$\n$9 = 2x+1$\n$2x = 8$\n$x = 4$。"
        },
        {
            "category": "國二上-2-1-平方根的意義",
            "image_path": "",
            "question_text": "若 $a$ 的平方根是 $\\pm 8$，求 $a$ 的值為何？",
            "detailed_solution": "已知 $a$ 的平方根為 $\\pm 8$，這代表將平方根平方後就會等於原數 $a$。\n$a = (\\pm 8)^2$\n$a = 64$。"
        },
        {
            "category": "國二上-2-1-平方根的意義",
            "image_path": "",
            "question_text": "請比較 $4$ 與 $\\sqrt{15}$ 的大小關係。",
            "detailed_solution": "為了方便比較，將整數 $4$ 化為根號形式：\n$4 = \\sqrt{4^2} = \\sqrt{16}$。\n因為 $16 > 15$，所以 $\\sqrt{16} > \\sqrt{15}$。\n故大小關係為：$4 > \\sqrt{15}$。"
        },

        # ==========================================
        # 2-2 根式的運算 (20題 計算題)
        # ==========================================
        {
            "category": "國二上-2-2-根式的運算",
            "image_path": "",
            "question_text": "將 $\\sqrt{12}$ 化為最簡根式。",
            "detailed_solution": "利用標準分解式將根號內的數分解：\n$\\sqrt{12} = \\sqrt{4 \\times 3}$\n$= \\sqrt{2^2 \\times 3}$\n將平方數提出根號外：\n$= 2\\sqrt{3}$。"
        },
        {
            "category": "國二上-2-2-根式的運算",
            "image_path": "",
            "question_text": "將 $\\sqrt{72}$ 化為最簡根式。",
            "detailed_solution": "尋找 $72$ 的最大完全平方數因數：\n$\\sqrt{72} = \\sqrt{36 \\times 2}$\n$= \\sqrt{6^2 \\times 2}$\n$= 6\\sqrt{2}$。"
        },
        {
            "category": "國二上-2-2-根式的運算",
            "image_path": "",
            "question_text": "計算 $\\sqrt{2} \\times \\sqrt{3}$ 的值為何？",
            "detailed_solution": "利用根式乘法法則 $\\sqrt{a} \\times \\sqrt{b} = \\sqrt{a \\times b}$：\n$\\sqrt{2} \\times \\sqrt{3} = \\sqrt{2 \\times 3}$\n$= \\sqrt{6}$。"
        },
        {
            "category": "國二上-2-2-根式的運算",
            "image_path": "",
            "question_text": "計算 $\\sqrt{15} \\times \\sqrt{5}$ 的值為何？",
            "detailed_solution": "利用根式乘法法則：\n$\\sqrt{15} \\times \\sqrt{5} = \\sqrt{15 \\times 5} = \\sqrt{75}$\n將 $\\sqrt{75}$ 化為最簡根式：\n$\\sqrt{75} = \\sqrt{25 \\times 3} = 5\\sqrt{3}$。"
        },
        {
            "category": "國二上-2-2-根式的運算",
            "image_path": "",
            "question_text": "計算 $\\frac{\\sqrt{18}}{\\sqrt{2}}$ 的值為何？",
            "detailed_solution": "利用根式除法法則 $\\frac{\\sqrt{a}}{\\sqrt{b}} = \\sqrt{\\frac{a}{b}}$：\n$\\frac{\\sqrt{18}}{\\sqrt{2}} = \\sqrt{\\frac{18}{2}}$\n$= \\sqrt{9}$\n$= 3$。"
        },
        {
            "category": "國二上-2-2-根式的運算",
            "image_path": "",
            "question_text": "將 $\\frac{3}{\\sqrt{3}}$ 進行分母有理化。",
            "detailed_solution": "為了讓分母的根號消失，分子分母同乘 $\\sqrt{3}$：\n$\\frac{3}{\\sqrt{3}} = \\frac{3 \\times \\sqrt{3}}{\\sqrt{3} \\times \\sqrt{3}}$\n$= \\frac{3\\sqrt{3}}{3}$\n約分後得 $\\sqrt{3}$。"
        },
        {
            "category": "國二上-2-2-根式的運算",
            "image_path": "",
            "question_text": "將 $\\frac{1}{\\sqrt{2}}$ 進行分母有理化。",
            "detailed_solution": "分子分母同乘 $\\sqrt{2}$：\n$\\frac{1}{\\sqrt{2}} = \\frac{1 \\times \\sqrt{2}}{\\sqrt{2} \\times \\sqrt{2}}$\n$= \\frac{\\sqrt{2}}{2}$。"
        },
        {
            "category": "國二上-2-2-根式的運算",
            "image_path": "",
            "question_text": "計算 $2\\sqrt{5} + 3\\sqrt{5}$ 的值為何？",
            "detailed_solution": "根號內部的數字相同（同類方根），可以直接相加係數：\n$2\\sqrt{5} + 3\\sqrt{5} = (2+3)\\sqrt{5}$\n$= 5\\sqrt{5}$。"
        },
        {
            "category": "國二上-2-2-根式的運算",
            "image_path": "",
            "question_text": "計算 $5\\sqrt{2} - 2\\sqrt{8}$ 的值為何？",
            "detailed_solution": "先將根式化為最簡方根：\n$\\sqrt{8} = \\sqrt{4 \\times 2} = 2\\sqrt{2}$\n代回原式：\n$5\\sqrt{2} - 2(2\\sqrt{2}) = 5\\sqrt{2} - 4\\sqrt{2}$\n$= (5-4)\\sqrt{2} = \\sqrt{2}$。"
        },
        {
            "category": "國二上-2-2-根式的運算",
            "image_path": "",
            "question_text": "展開並化簡 $\\sqrt{2}(\\sqrt{3} + \\sqrt{2})$。",
            "detailed_solution": "利用分配律將 $\\sqrt{2}$ 乘進括號：\n$= \\sqrt{2} \\times \\sqrt{3} + \\sqrt{2} \\times \\sqrt{2}$\n$= \\sqrt{6} + 2$。"
        },
        {
            "category": "國二上-2-2-根式的運算",
            "image_path": "",
            "question_text": "展開並化簡 $(\\sqrt{3} + 1)(\\sqrt{3} - 1)$。",
            "detailed_solution": "利用平方差公式 $(a+b)(a-b) = a^2 - b^2$：\n$(\\sqrt{3} + 1)(\\sqrt{3} - 1)$\n$= (\\sqrt{3})^2 - 1^2$\n$= 3 - 1$\n$= 2$。"
        },
        {
            "category": "國二上-2-2-根式的運算",
            "image_path": "",
            "question_text": "展開並化簡 $(\\sqrt{5} + \\sqrt{2})^2$。",
            "detailed_solution": "利用和的平方公式 $(a+b)^2 = a^2 + 2ab + b^2$：\n$(\\sqrt{5} + \\sqrt{2})^2$\n$= (\\sqrt{5})^2 + 2 \\times \\sqrt{5} \\times \\sqrt{2} + (\\sqrt{2})^2$\n$= 5 + 2\\sqrt{10} + 2$\n$= 7 + 2\\sqrt{10}$。"
        },
        {
            "category": "國二上-2-2-根式的運算",
            "image_path": "",
            "question_text": "將 $\\frac{2}{\\sqrt{5}-\\sqrt{3}}$ 進行分母有理化。",
            "detailed_solution": "利用平方差公式，分子分母同乘 $(\\sqrt{5}+\\sqrt{3})$：\n$\\frac{2(\\sqrt{5}+\\sqrt{3})}{(\\sqrt{5}-\\sqrt{3})(\\sqrt{5}+\\sqrt{3})}$\n$= \\frac{2(\\sqrt{5}+\\sqrt{3})}{(\\sqrt{5})^2 - (\\sqrt{3})^2}$\n$= \\frac{2(\\sqrt{5}+\\sqrt{3})}{5 - 3}$\n$= \\frac{2(\\sqrt{5}+\\sqrt{3})}{2}$\n約分後得 $\\sqrt{5} + \\sqrt{3}$。"
        },
        {
            "category": "國二上-2-2-根式的運算",
            "image_path": "",
            "question_text": "將 $\\frac{1}{\\sqrt{3}+1}$ 進行分母有理化。",
            "detailed_solution": "分子分母同乘 $(\\sqrt{3}-1)$：\n$\\frac{1 \\times (\\sqrt{3}-1)}{(\\sqrt{3}+1)(\\sqrt{3}-1)}$\n$= \\frac{\\sqrt{3}-1}{(\\sqrt{3})^2 - 1^2}$\n$= \\frac{\\sqrt{3}-1}{3 - 1}$\n$= \\frac{\\sqrt{3}-1}{2}$。"
        },
        {
            "category": "國二上-2-2-根式的運算",
            "image_path": "",
            "question_text": "計算 $\\sqrt{27} + \\sqrt{12} - \\sqrt{75}$ 的值為何？",
            "detailed_solution": "先將所有根式化為最簡：\n$\\sqrt{27} = \\sqrt{9 \\times 3} = 3\\sqrt{3}$\n$\\sqrt{12} = \\sqrt{4 \\times 3} = 2\\sqrt{3}$\n$\\sqrt{75} = \\sqrt{25 \\times 3} = 5\\sqrt{3}$\n代回原式計算：\n$3\\sqrt{3} + 2\\sqrt{3} - 5\\sqrt{3}$\n$= (3+2-5)\\sqrt{3}$\n$= 0\\sqrt{3} = 0$。"
        },
        {
            "category": "國二上-2-2-根式的運算",
            "image_path": "",
            "question_text": "計算 $\\sqrt{45} \\div \\sqrt{5} \\times \\sqrt{2}$ 的值為何？",
            "detailed_solution": "依照由左至右的順序計算，先做除法：\n$\\sqrt{45} \\div \\sqrt{5} = \\sqrt{\\frac{45}{5}} = \\sqrt{9} = 3$\n再乘以後面的 $\\sqrt{2}$：\n$3 \\times \\sqrt{2} = 3\\sqrt{2}$。"
        },
        {
            "category": "國二上-2-2-根式的運算",
            "image_path": "",
            "question_text": "展開並化簡 $(\\sqrt{6} - \\sqrt{2})^2$。",
            "detailed_solution": "利用差的平方公式 $(a-b)^2 = a^2 - 2ab + b^2$：\n$(\\sqrt{6} - \\sqrt{2})^2$\n$= (\\sqrt{6})^2 - 2 \\times \\sqrt{6} \\times \\sqrt{2} + (\\sqrt{2})^2$\n$= 6 - 2\\sqrt{12} + 2$\n其中 $\\sqrt{12} = 2\\sqrt{3}$，代入化簡：\n$= 8 - 2(2\\sqrt{3})$\n$= 8 - 4\\sqrt{3}$。"
        },
        {
            "category": "國二上-2-2-根式的運算",
            "image_path": "",
            "question_text": "計算 $\\sqrt{18} \\times \\sqrt{12} \\div \\sqrt{6}$ 的值為何？",
            "detailed_solution": "可將所有運算放入同一個大根號內：\n$\\sqrt{\\frac{18 \\times 12}{6}}$\n先約分：$\\frac{18}{6} = 3$\n$= \\sqrt{3 \\times 12}$\n$= \\sqrt{36}$\n$= 6$。"
        },
        {
            "category": "國二上-2-2-根式的運算",
            "image_path": "",
            "question_text": "化簡 $\\sqrt{2} \\times (\\sqrt{8} + \\sqrt{18})$。",
            "detailed_solution": "方法一（先化簡括號內）：\n$\\sqrt{8} = 2\\sqrt{2}$，$\\sqrt{18} = 3\\sqrt{2}$\n括號內 $= 2\\sqrt{2} + 3\\sqrt{2} = 5\\sqrt{2}$\n原式 $= \\sqrt{2} \\times 5\\sqrt{2} = 5 \\times 2 = 10$。\n\n方法二（分配律展開）：\n$= \\sqrt{16} + \\sqrt{36}$\n$= 4 + 6 = 10$。"
        },
        {
            "category": "國二上-2-2-根式的運算",
            "image_path": "",
            "question_text": "已知 $\\sqrt{2} \\approx 1.414$，求 $\\frac{2}{\\sqrt{2}}$ 的近似值為何？",
            "detailed_solution": "直接代入小數計算不好除，先將分數進行分母有理化：\n$\\frac{2}{\\sqrt{2}} = \\frac{2 \\times \\sqrt{2}}{\\sqrt{2} \\times \\sqrt{2}} = \\frac{2\\sqrt{2}}{2} = \\sqrt{2}$\n已知 $\\sqrt{2} \\approx 1.414$，故答案即為 $1.414$。"
        },

        # ==========================================
        # 2-3 畢氏定理 (20題 計算題)
        # ==========================================
        {
            "category": "國二上-2-3-畢氏定理",
            "image_path": "",
            "question_text": "一直角三角形的兩股長分別為 $3$ 和 $4$，求其斜邊長為何？",
            "detailed_solution": "設斜邊長為 $c$，依據畢氏定理 $a^2 + b^2 = c^2$：\n$3^2 + 4^2 = c^2$\n$9 + 16 = c^2$\n$c^2 = 25$\n因為邊長必為正數，故 $c = \\sqrt{25} = 5$。"
        },
        {
            "category": "國二上-2-3-畢氏定理",
            "image_path": "",
            "question_text": "已知一直角三角形的斜邊長為 $13$，其中一股長為 $5$，求另一股的長度為何？",
            "detailed_solution": "設另一股長為 $b$，依據畢氏定理：\n$5^2 + b^2 = 13^2$\n$25 + b^2 = 169$\n$b^2 = 169 - 25 = 144$\n故 $b = \\sqrt{144} = 12$。"
        },
        {
            "category": "國二上-2-3-畢氏定理",
            "image_path": "",
            "question_text": "一直角三角形的兩股長分別為 $6$ 和 $8$，求斜邊長為何？",
            "detailed_solution": "設斜邊長為 $c$，依據畢氏定理：\n$6^2 + 8^2 = c^2$\n$36 + 64 = c^2$\n$c^2 = 100$\n故 $c = \\sqrt{100} = 10$。"
        },
        {
            "category": "國二上-2-3-畢氏定理",
            "image_path": "",
            "question_text": "直角三角形的斜邊長為 $25$，一股長為 $7$，求另一股長為何？",
            "detailed_solution": "設另一股長為 $x$，依據畢氏定理：\n$7^2 + x^2 = 25^2$\n$49 + x^2 = 625$\n$x^2 = 625 - 49 = 576$\n故 $x = \\sqrt{576} = 24$。"
        },
        {
            "category": "國二上-2-3-畢氏定理",
            "image_path": "",
            "question_text": "一直角三角形的兩股長分別為 $5$ 和 $12$，求此三角形的面積為何？",
            "detailed_solution": "直角三角形的兩股即為其底與高。\n三角形面積 $= \\frac{1}{2} \\times 底 \\times 高$\n$= \\frac{1}{2} \\times 5 \\times 12$\n$= 30$ 平方單位。"
        },
        {
            "category": "國二上-2-3-畢氏定理",
            "image_path": "",
            "question_text": "一直角三角形的兩股長分別為 $8$ 和 $15$，求其斜邊長為何？",
            "detailed_solution": "設斜邊長為 $c$，依據畢氏定理：\n$8^2 + 15^2 = c^2$\n$64 + 225 = c^2$\n$c^2 = 289$\n故 $c = \\sqrt{289} = 17$。"
        },
        {
            "category": "國二上-2-3-畢氏定理",
            "image_path": "",
            "question_text": "在坐標平面上，求兩點 $A(0,0)$ 與 $B(3,4)$ 的距離為何？",
            "detailed_solution": "利用兩點距離公式 $d = \\sqrt{(x_2-x_1)^2 + (y_2-y_1)^2}$：\n$\\overline{AB} = \\sqrt{(3-0)^2 + (4-0)^2}$\n$= \\sqrt{3^2 + 4^2}$\n$= \\sqrt{9 + 16} = \\sqrt{25} = 5$。"
        },
        {
            "category": "國二上-2-3-畢氏定理",
            "image_path": "",
            "question_text": "在坐標平面上，求兩點 $P(-2, 1)$ 與 $Q(4, 9)$ 的距離為何？",
            "detailed_solution": "利用兩點距離公式：\n$\\overline{PQ} = \\sqrt{(4 - (-2))^2 + (9 - 1)^2}$\n$= \\sqrt{6^2 + 8^2}$\n$= \\sqrt{36 + 64} = \\sqrt{100} = 10$。"
        },
        {
            "category": "國二上-2-3-畢氏定理",
            "image_path": "",
            "question_text": "一矩形的長為 $24$，寬為 $7$，求其對角線長為何？",
            "detailed_solution": "矩形的長、寬與對角線剛好構成一個直角三角形。\n設對角線長為 $d$，依據畢氏定理：\n$24^2 + 7^2 = d^2$\n$576 + 49 = d^2$\n$d^2 = 625$\n故 $d = 25$。"
        },
        {
            "category": "國二上-2-3-畢氏定理",
            "image_path": "",
            "question_text": "已知一正方形的對角線長為 $4\\sqrt{2}$，求其邊長為何？",
            "detailed_solution": "設正方形邊長為 $x$，由畢氏定理可知，兩邊長的平方和等於對角線的平方：\n$x^2 + x^2 = (4\\sqrt{2})^2$\n$2x^2 = 16 \\times 2 = 32$\n$x^2 = 16$\n故邊長 $x = 4$。"
        },
        {
            "category": "國二上-2-3-畢氏定理",
            "image_path": "",
            "question_text": "一等腰直角三角形的斜邊長為 $10$，求其股長為何？",
            "detailed_solution": "設兩股長皆為 $x$，依據畢氏定理：\n$x^2 + x^2 = 10^2$\n$2x^2 = 100$\n$x^2 = 50$\n$x = \\sqrt{50} = 5\\sqrt{2}$。"
        },
        {
            "category": "國二上-2-3-畢氏定理",
            "image_path": "",
            "question_text": "有一把長 $2.5$ 公尺的梯子，斜靠在垂直的牆上。若梯腳距離牆底 $1.5$ 公尺，求梯頂離地面的高度為多少公尺？",
            "detailed_solution": "梯長(斜邊)、梯腳距牆底距離(一股)與牆高(另一股)構成直角三角形。\n設牆高為 $h$，依據畢氏定理：\n$1.5^2 + h^2 = 2.5^2$\n$2.25 + h^2 = 6.25$\n$h^2 = 4.00$\n故 $h = \\sqrt{4} = 2$ 公尺。"
        },
        {
            "category": "國二上-2-3-畢氏定理",
            "image_path": "",
            "question_text": "已知一正三角形的邊長為 $6$，求其高為何？",
            "detailed_solution": "正三角形的高會將底邊平分。畫出高後，可得到一個直角三角形，斜邊為 $6$，底邊的一半為 $3$。\n設高為 $h$，依據畢氏定理：\n$3^2 + h^2 = 6^2$\n$9 + h^2 = 36$\n$h^2 = 27$\n故 $h = \\sqrt{27} = 3\\sqrt{3}$。"
        },
        {
            "category": "國二上-2-3-畢氏定理",
            "image_path": "",
            "question_text": "已知一正三角形的邊長為 $8$，求其面積為何？",
            "detailed_solution": "先求高，高將底邊平分為 $4$。\n設高為 $h$，由畢氏定理：$4^2 + h^2 = 8^2 \\Rightarrow 16 + h^2 = 64 \\Rightarrow h^2 = 48 \\Rightarrow h = \\sqrt{48} = 4\\sqrt{3}$。\n三角形面積 $= \\frac{1}{2} \\times 底 \\times 高$\n$= \\frac{1}{2} \\times 8 \\times 4\\sqrt{3}$\n$= 16\\sqrt{3}$ 平方單位。"
        },
        {
            "category": "國二上-2-3-畢氏定理",
            "image_path": "",
            "question_text": "在坐標平面上，點 $A(-3, -4)$ 到原點 $O(0, 0)$ 的距離為何？",
            "detailed_solution": "利用兩點距離公式：\n$\\overline{AO} = \\sqrt{(-3 - 0)^2 + (-4 - 0)^2}$\n$= \\sqrt{(-3)^2 + (-4)^2}$\n$= \\sqrt{9 + 16} = \\sqrt{25} = 5$。"
        },
        {
            "category": "國二上-2-3-畢氏定理",
            "image_path": "",
            "question_text": "一直角三角形的兩股長分別為 $9$ 和 $12$，求斜邊長為何？",
            "detailed_solution": "設斜邊長為 $c$，依據畢氏定理：\n$9^2 + 12^2 = c^2$\n$81 + 144 = c^2$\n$c^2 = 225$\n故 $c = \\sqrt{225} = 15$。\n（也可觀察其為 $3:4:5$ 直角三角形的 $3$ 倍放大版：$9:12:15$）。"
        },
        {
            "category": "國二上-2-3-畢氏定理",
            "image_path": "",
            "question_text": "已知直角三角形三邊長為 $a, b, c$ 且 $c$ 為斜邊。若 $a=10, c=26$，求 $b$ 的值為何？",
            "detailed_solution": "依據畢氏定理 $a^2 + b^2 = c^2$：\n$10^2 + b^2 = 26^2$\n$100 + b^2 = 676$\n$b^2 = 576$\n故 $b = \\sqrt{576} = 24$。\n（也可觀察其為 $5:12:13$ 直角三角形的 $2$ 倍放大版）。"
        },
        {
            "category": "國二上-2-3-畢氏定理",
            "image_path": "",
            "question_text": "請利用畢氏定理判斷，$5, 12, 13$ 這三個數字是否能構成直角三角形的三邊長？（請回答是或否）",
            "detailed_solution": "判斷最長邊 $13$ 是否滿足畢氏定理：\n較短兩邊的平方和 $= 5^2 + 12^2 = 25 + 144 = 169$。\n最長邊的平方 $= 13^2 = 169$。\n因為 $5^2 + 12^2 = 13^2$，完全符合畢氏定理，故答案為「是」。"
        },
        {
            "category": "國二上-2-3-畢氏定理",
            "image_path": "",
            "question_text": "一菱形的兩對角線長分別為 $12$ 和 $16$，求此菱形的邊長為何？",
            "detailed_solution": "菱形的對角線互相垂直且平分。因此兩條對角線將菱形切分為四個全等的直角三角形。\n直角三角形的兩股長為對角線的一半，分別為 $\\frac{12}{2}=6$ 與 $\\frac{16}{2}=8$。\n設菱形邊長（即直角三角形的斜邊）為 $x$：\n$6^2 + 8^2 = x^2$\n$36 + 64 = 100 = x^2$\n故 $x = \\sqrt{100} = 10$。"
        },
        {
            "category": "國二上-2-3-畢氏定理",
            "image_path": "",
            "question_text": "一長方體的長、寬、高分別為 $3, 4, 12$，求此長方體內部最長對角線的長度為何？",
            "detailed_solution": "長方體內部對角線長度的公式為 $d = \\sqrt{長^2 + 寬^2 + 高^2}$。\n代入數值：\n$d = \\sqrt{3^2 + 4^2 + 12^2}$\n$= \\sqrt{9 + 16 + 144}$\n$= \\sqrt{169}$\n$= 13$。"
        }
    ]
    ]

    for item in problems_data:
        new_prob = Problem(**item)
        db.add(new_prob)
        
    db.commit()
    print(f"✅ 成功匯入 {len(problems_data)} 題「國二上-1-1-乘法公式」測試資料至 SQLite 資料庫！")
    db.close()

if __name__ == "__main__":
    seed_data()
