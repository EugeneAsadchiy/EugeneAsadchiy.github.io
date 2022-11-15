from flask import Flask, request, render_template
from datetime import datetime
import json

app = Flask(__name__)
DATA_FILE = "data.json"


# Загрузка сообщений
def load_messages():
    with open(DATA_FILE, "r") as json_file:
        data = json.load(json_file)
        return data["all_messages"]


all_messages = load_messages()


# Сохраняем сообщения
def save_messages():
    with open(DATA_FILE, "w") as json_file:
        data = {"all_messages": all_messages}
        json.dump(data, json_file, indent=3)


@app.route("/")
def hello_world():
    return "<p> Hello, welcome to my acc </p>"


# API ДЛЯ ПОЛУЧЕНИЯ СООБЩЕНИЙ
@app.route("/get_messages")
def get_messages():
    # after = int(request.args.get("after", 0))
    # return {"messages": all_messages[after-1:]}
    return {"messages": all_messages}


def add_message(sender, text):
    new_message = {
        "sender": sender,
        "text": text,
        "time": datetime.now().strftime("%H:%M")
    }
    all_messages.append(new_message)
    save_messages()


add_message("Mike", "hello")
add_message("Zhenya", "hi")


# API ДЛЯ ОТПРАВКИ СООБЩЕНИЙ
@app.route("/send_message")
def send_message():
    sender = request.args["sender"]
    text = request.args["text"]

    add_message(sender, text)


@app.route("/chat")
def chat_page():
    return render_template("form.html")


app.run(host="0.0.0.0", port=80)
