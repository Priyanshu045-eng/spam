from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict
import re

class TextClassifier:
    def __init__(self):
        self.spam_keywords = [
            "win", "won", "free", "offer", "click", "subscribe", "buy now", "lottery", "claim", "discount",
            "money", "deal", "sale", "limited time", "urgent", "act now", "gift", "bonus", "credit card",
            "loan", "investment", "earn", "bitcoin", "crypto", "forex", "guaranteed", "reward", "signup",
            "follow back", "followers", "promote", "sponsor", "giveaway", "link in bio", "order now"
        ]
        self.abusive_words = [
            "stupid", "idiot", "fool", "dumb", "trash", "hate", "moron", "useless", "loser", "crap",
            "bastard", "ugly", "nonsense", "shut up", "kill", "disgusting", "suck", "jerk", "annoying",
            "hate you", "die", "f off", "worthless", "terrible", "worst", "clown", "lame","fuck", "fucking", "shit", "bitch", "bastard", "asshole", "dick", "pussy",
            "motherfucker", "mf", "slut", "whore", "dumb", "stupid", "idiot", "retard","hoe", "cunt", "fag", "gay insult","kill you", "i will kill", "go die", "suicide", "shoot you","madarchod", "madharchod", "bhosdike", "bsdk", "chutiya", "chutiye",
            "mc", "bc", "rand", "randwa", "gaand", "gand", "bhosda", "lavde", "randi","launde", "kutte", "suar", "kamine", "harami", "nalayak", "bewakoof", "sex", "lust", "boobs", "nude", "b0obs", "n00d", "xxx", "porn", "suck","ugly", "fat", "loser", "no one likes you"



        ]

        self.normal_chat_words = [
            "hello", "hi", "hey", "good morning", "good night", "good evening", "how are you", "what's up",
            "thank you", "thanks", "please", "ok", "sure", "yes", "no", "fine", "great", "awesome",
            "cool", "nice", "amazing", "superb", "wonderful", "perfect", "wow", "good job", "well done",
            "congrats", "congratulations", "bro", "sis", "buddy", "dude", "mate", "friend", "bhai",
            "lol", "lmao", "rofl", "haha", "hehe", "funny", "nice pic", "cool photo", "love this", "omg",
            "btw", "brb", "idk", "ikr", "tbh", "smh", "ok bro", "np", "no problem", "sounds good",
            "see you", "take care", "talk later", "let’s go", "hangout", "mood", "vibes", "chill",
            "nice post", "great work", "keep it up", "beautiful", "awesome post", "good one", "well said",
            "so true", "facts", "agreed", "amazing shot", "love this pic", "looking good", "cute", "wow amazing",
            "project", "assignment", "exam", "study", "lecture", "class", "teacher", "college", "event",
            "presentation", "notes", "discussion", "group", "app", "feature", "meeting", "plan", "deadline",
            "topic", "friendship", "community", "feedback", "suggestion", "recommend", "party", "fun", "weekend"
        ]

    def clean_text(self, text: str) -> str:
        return re.sub(r'[^a-zA-Z\s]', '', text.lower())

    def predict(self, text: str) -> Dict[str, any]:
        cleaned = self.clean_text(text)
        spam_score = sum(1 for word in self.spam_keywords if word in cleaned)
        abuse_score = sum(1 for word in self.abusive_words if word in cleaned)
        normal_score = sum(1 for word in self.normal_chat_words if word in cleaned)

        if abuse_score > 0:
            label = "Abusive"
        elif spam_score > 1 and spam_score > normal_score:
            label = "Spam"
        else:
            label = "Normal"

        return {
            "text": text,
            "label": label,
            "spam_score": spam_score,
            "abuse_score": abuse_score,
            "normal_score": normal_score
        }


app = FastAPI(title="Chat Text Classifier API", version="1.0")

classifier = TextClassifier()

class TextInput(BaseModel):
    text: str


@app.get("/")
def root():
    return {"message": "Welcome to the Chat Text Classifier API 🚀"}


@app.post("/predict")
def predict_text(input_data: TextInput):
    """Predict whether text is Normal, Spam, or Abusive."""
    result = classifier.predict(input_data.text)
    return result

