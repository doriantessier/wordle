from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import random

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MOTS = ["pomme", "tigre", "terre", "melon", "chien", "colle", "plage", "table", "lampe", "maths", "piano", "stylo", "nuage"]
current_word = {"secret": random.choice(MOTS)}

@app.get("/api/v1/wordle/new")
def new_game():
    current_word["secret"] = random.choice(MOTS)
    return {"message": "Trouve mon mot ! Il fait 5 lettres"}

@app.get("/api/v1/wordle/guess")
def guess(mot: str = Query(...)):
    mot = mot.lower()
    secret = current_word["secret"]

    if len(mot) != len(secret):
        return {"error": "Je t'ai dit que mon mot fait 5 lettres"}

    correct = []
    used = [False] * len(secret)

    #Lettres bien placées
    for i in range(len(secret)):
        if mot[i] == secret[i]:
            correct.append({"letter": mot[i], "color": "green"})
            used[i] = True
        else:
            correct.append(None)

    #Lettres mal placées
    for i in range(len(secret)):
        if correct[i] is None:
            if mot[i] in secret and any(secret[j] == mot[i] and not used[j] for j in range(len(secret))):
                correct[i] = {"letter": mot[i], "color": "orange"}
                j = next(j for j in range(len(secret)) if secret[j] == mot[i] and not used[j])
                used[j] = True
            else:
                correct[i] = {"letter": mot[i], "color": "black"}

    return {"correct": correct}
