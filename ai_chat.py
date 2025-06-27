from langdetect import detect

# 🧠 Detect language
def detect_language(text: str) -> str:
    try:
        return detect(text)
    except:
        return "en"

# 📚 Common static replies for keywords
COMMON_QUESTIONS = {
    "rules": "📜 Group Rules:\n1. Give Respect Everyone\n2. Spam or Scammer not Allowed\n3. Koi Promotion Ya irrelevent link nahi bhejna\n3. Ya Group Ma Jo Kuch Bhi Diya Jata Hai Totally Free Hain Kisi Ko Paisa Nahi Dena.",
    "admin": "👨‍💼 Admin: @mbshustler\nAap kisi bhi maslay ke liye contact kar sakte hain.",
    "contact": "📩 Contact: mbsbusinesses1@gmail.com (or @mbshustler on Telegram)",
    "youtube": "📺 Hamara YouTube channel: https://www.youtube.com/@MBSKnowledgeHub"
}

# ❓ Response function (without AI)
def get_ai_response(user_message: str) -> str:
    lang = detect_language(user_message)
    msg = user_message.lower()

    for keyword in COMMON_QUESTIONS:
        if keyword in msg:
            return COMMON_QUESTIONS[keyword]

    # Fallback manual response
    if lang in ["ur", "hi"]:
        return "Aap kya poochhna chahte hain? Main madad karne ke liye hoon!"
    elif lang == "en":
        return "I'm here to help! Please ask your question."
    else:
        return "❓ Mujhe aapka sawaal samajh nahi aaya. Kripya dobara bhejein."
