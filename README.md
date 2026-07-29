# TickDroid 🤖

A multi-purpose, asynchronous Discord bot built with Python, featuring AI integrations powered by Google Gemini. 

## 🚀 Features

* **Direct AI Chat:** Talk directly to Gemini using the `!g <message>` command for conversational, friendly, and context-aware responses.
* **AI Magic 8-Ball:** Ask your questions and get witty, Gemini-powered 8-ball answers.
* **PDF Summarization:** Upload any PDF file to instantly generate text summaries.
* **To-Do List:** A built-in task manager to keep your server organized and track your goals.

## 🛠️ Architecture

TickDroid is built using the `discord.py` framework and utilizes a modular "Cogs" architecture to keep features separated and highly maintainable. 

* **`/cogs`:** Contains modular feature logic (e.g., `8ball.py`, `toDoList.py`, `gemini_response.py`, `fileLogic.py`).
* **`/json`:** Directory designated for local JSON data and configuration storage.
* **`main.py`:** The primary entry point to launch the bot.

## ⚙️ Setup & Installation

1. Clone this repository to your local machine.
2. Install the required dependencies using `pip install -r requirements.txt`.
3. Run `python setup.py` to configure the bot and set up your necessary environment variables.
4. Start the bot by executing `python main.py` in your terminal.
