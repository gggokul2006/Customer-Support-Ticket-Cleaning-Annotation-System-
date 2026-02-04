# Customer-Support-Ticket-Cleaning-Annotation-System

# 🛠️ Customer Support Ticket Cleaning & Sentiment Analysis System

A Flask-based NLP web application that cleans, analyzes, and classifies customer support tickets.  
The system supports dataset upload, text preprocessing, sentiment analysis, visualization, pagination, and real-time sentiment prediction.

---

## 📌 Features

- 📂 Upload CSV files containing customer support tickets
- 🧹 Text preprocessing (cleaning, tokenization, stopword removal)
- 😊 Sentiment classification (Positive / Negative / Neutral)
- 📊 Word frequency visualization (Top 10 words)
- 📋 Paginated display of processed tickets
- ⚡ Real-time sentiment prediction for user-entered comments
- 🌙 Dark theme UI inspired by LeetCode

---

## 🧠 Technologies Used

- **Backend:** Flask (Python)
- **NLP:** spaCy, TextBlob
- **Data Handling:** Pandas
- **Visualization:** Matplotlib
- **Frontend:** HTML, CSS, JavaScript
- **AJAX:** Fetch API for live prediction

---

## 📁 Project Structure

customer-support-nlp/
│
├── app.py
├── requirements.txt
├── uploads/
├── static/
│ ├── style.css
│ └── plot_*.png
├── templates/
│ ├── index.html
│ └── result.html
└── README.md


##2️⃣ Install dependencies
pip install -r requirements.txt

##3️⃣ Download spaCy model
python -m spacy download en_core_web_sm

##4️⃣ Run the application
python app.py
