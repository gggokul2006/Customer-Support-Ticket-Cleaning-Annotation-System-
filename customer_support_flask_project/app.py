from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import re
import spacy
import matplotlib.pyplot as plt
from collections import Counter
from textblob import TextBlob
import os, time

# ======================
# APP INIT
# ======================
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

nlp = spacy.load("en_core_web_sm")

# ======================
# NLP FUNCTIONS
# ======================
def clean_text(text):
    text = str(text).lower()
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"[^a-zA-Z\s]", "", text)
    return text.strip()

def tokenize(text):
    text = str(text)
    doc = nlp(text)
    return [t.text for t in doc if t.is_alpha and not t.is_stop]

def sentiment(text):
    text = str(text)
    polarity = TextBlob(text).sentiment.polarity
    if polarity > 0:
        return "Positive"
    elif polarity < 0:
        return "Negative"
    else:
        return "Neutral"

# ======================
# ROUTES
# ======================
@app.route('/')
def index():
    return render_template("index.html")

# 🔥 SAFETY: if someone opens /process directly
@app.route('/process', methods=['GET'])
def process_get():
    return redirect(url_for('index'))

@app.route('/process', methods=['POST'])
def process():
    # ---------- File Upload ----------
    file = request.files['dataset']
    path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(path)

    # ---------- Read CSV ----------
    df = pd.read_csv(path)

    # Remove duplicate columns
    df = df.loc[:, ~df.columns.duplicated()]
    df = df.reset_index(drop=True)

    # Find text column safely
    possible_cols = ["text", "tweet", "message", "content", "description"]
    text_col = None
    for col in possible_cols:
        if col in df.columns:
            text_col = col
            break
    if text_col is None:
        text_col = df.columns[0]

    df = df[[text_col]].rename(columns={text_col: "text"}).dropna()


    df["text"] = df["text"].astype(str)

    # ---------- NLP ----------
    df["cleaned_text"] = df["text"].apply(clean_text)
    df["tokens"] = df["cleaned_text"].apply(tokenize)
    df["sentiment"] = df["text"].apply(sentiment)

    # ---------- Plot ----------
    if not os.path.exists("static"):
        os.makedirs("static")

    # delete old plots
    for f in os.listdir("static"):
        if f.startswith("plot_") and f.endswith(".png"):
            os.remove(os.path.join("static", f))

    all_words = []
    for t in df["tokens"]:
        all_words.extend(t)

    freq = Counter(all_words).most_common(10)
    words = [w for w, _ in freq]
    counts = [c for _, c in freq]

    plot_name = f"plot_{int(time.time())}.png"
    plot_path = os.path.join("static", plot_name)

    plt.figure(figsize=(8, 4))
    plt.bar(words, counts)
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.savefig(plot_path)
    plt.close()

   
    df.index = df.index + 1  


    # ---------- Render Result ----------
    return render_template(
        "result.html",
        tables=df.to_html(classes="table"),
        positive=(df["sentiment"] == "Positive").sum(),
        negative=(df["sentiment"] == "Negative").sum(),
        neutral=(df["sentiment"] == "Neutral").sum(),
        plot_file=plot_name
    )


from flask import jsonify

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    text = str(data.get("text", ""))

    polarity = TextBlob(text).sentiment.polarity
    if polarity > 0:
        result = "Positive"
    elif polarity < 0:
        result = "Negative"
    else:
        result = "Neutral"

    return jsonify({"sentiment": result})

# ======================
# RUN SERVER
# ======================
if __name__ == "__main__":
    os.makedirs("uploads", exist_ok=True)
    app.run(debug=True)


