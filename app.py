from flask import Flask, render_template_string, request
import jieba
from collections import Counter

app = Flask(__name__)

# ===================== 你的信息 =====================
STUDENT_ID = "423830112"
STUDENT_NAME = "杜彦苇"
# ===================================================

# ===================== 可调整参数 =====================
TOP_K = 5  # 提取几个关键词（可调）
MIN_WORD_LEN = 2  # 最短词长度（可调）
# ======================================================

# 停用词（可优化）
STOP_WORDS = {"的", "了", "是", "我", "有", "在", "和", "就", "都", "很", "非常", "今天"}

# 提取关键词
def extract_keywords(text):
    words = [w for w in jieba.lcut(text) if len(w) >= MIN_WORD_LEN and w not in STOP_WORDS]
    counter = Counter(words)
    return counter.most_common(TOP_K)

# 简单情绪分类
def simple_classify(text):
    positive = ["开心", "好", "顺利", "棒", "喜欢", "满意", "成功"]
    negative = ["难过", "坏", "糟糕", "烦", "生气", "失败"]
    score = sum(1 for w in positive if w in text) - sum(1 for w in negative if w in text)
    if score > 0:
        return "积极正面"
    elif score < 0:
        return "消极负面"
    else:
        return "中性"

# 前端页面
HTML = '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>AI文本智能分析</title>
    <style>
        .box{max-width:650px;margin:40px auto;padding:20px;}
        .info{font-size:18px;color:#0066cc;margin:20px 0;}
        textarea{width:100%;height:120px;padding:10px;font-size:15px;}
        button{padding:10px 25px;background:#0066cc;color:white;border:none;border-radius:6px;}
        .res{margin-top:20px;padding:15px;background:#f5f5f5;border-radius:8px;}
    </style>
</head>
<body>
    <div class="box">
        <h1>AI文本关键词提取与情绪分类</h1>
        <div class="info">
            学号：{{ sid }} &nbsp;&nbsp; 姓名：{{ name }}
        </div>
        <form method="post">
            <textarea name="text" placeholder="输入一段中文文本..."></textarea>
            <br><br>
            <button type="submit">开始分析</button>
        </form>
        {% if res %}
        <div class="res">
            <p>输入文本：{{ res.text }}</p>
            <p>情绪分类：{{ res.label }}</p>
            <p>关键词：{{ res.keywords | safe }}</p>
        </div>
        {% endif %}
    </div>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    res = None
    if request.method == 'POST':
        text = request.form['text']
        keywords = extract_keywords(text)
        label = simple_classify(text)
        kw_str = "，".join([f"{w}({c})" for w, c in keywords])
        res = {"text": text, "label": label, "keywords": kw_str}
    return render_template_string(HTML, sid=STUDENT_ID, name=STUDENT_NAME, res=res)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
