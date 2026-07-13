# 🤖 LocalGPT Chatbot with Memory

A simple, fully offline AI chatbot that runs on your own machine.
No API keys. No internet required. No cloud. Just local AI!

**Built with:** Python · LangChain · Ollama

---

## 📁 Project Files

```
localgpt-chatbot/
 ├── chatbot.py        ← All the chatbot code (start here)
 ├── requirements.txt  ← Python packages to install
 └── README.md         ← Setup guide (this file)
```

---

## ⚙️ One-Time Setup

### 1 · Install Ollama
Go to https://ollama.com/download and install it for your OS.

### 2 · Start Ollama (keep this terminal open)
```bash
ollama serve
```

### 3 · Download an AI model (pick one)
```bash
ollama pull llama3      # best quality  (~4 GB)
ollama pull mistral     # also great    (~4 GB)
ollama pull phi3        # smaller/fast  (~2 GB)
```

### 4 · Install Python packages
```bash
pip install -r requirements.txt
```

---

## ▶️ Run the Chatbot

Open a **second terminal** (keep `ollama serve` running) and type:
```bash
python chatbot.py
```

---

## 💬 Example Chat

```
══════════════════════════════════════════════════
  🤖  LocalGPT Chatbot   |   model: llama3
══════════════════════════════════════════════════
  Type a message and press Enter to chat.
  Type  help  to see all commands.
══════════════════════════════════════════════════

You: Hi! What can you do?
AI: I can answer questions, help you think through problems,
    write text, and more — all running locally on your machine!

You: Remember my name is Arjun
AI: Got it, Arjun! I'll remember that for our conversation.

You: What's my name?
AI: Your name is Arjun, as you mentioned earlier!

You: clear
🗑️  Memory wiped — starting fresh!

You: exit
Goodbye! 👋
```

---

## ⌨️ Commands

| Type this  | What happens                          |
|------------|---------------------------------------|
| `quit`     | Close the chatbot                     |
| `exit`     | Close the chatbot                     |
| `clear`    | Wipe memory, start a fresh chat       |
| `history`  | Print the conversation so far         |
| `help`     | Show the command list                 |

---

## 🎛️ Customize the Bot

Open `chatbot.py` and edit the settings at the top:

```python
MODEL       = "llama3"   # change to "mistral" or "phi3"
MEMORY_SIZE = 10         # raise this to remember more messages
TEMPERATURE = 0.7        # 0 = precise | 1 = creative/random

SYSTEM_PROMPT = """
You are a helpful assistant...   ← change the personality here
"""
```

---

## 🧠 How Memory Works (simple explanation)

```
User says something
        ↓
  Saved to memory list
        ↓
  [system prompt + full memory] sent to model
        ↓
  Model replies using context from past messages
        ↓
  Reply saved to memory list
        ↓
  If memory > MEMORY_SIZE → oldest message removed
```

That's it! No database, no embeddings — just a list of messages
passed along with every request so the model knows what was said.

---

## 🛠️ Troubleshooting

| Problem                  | Fix                                         |
|--------------------------|---------------------------------------------|
| `Connection refused`     | Run `ollama serve` in another terminal      |
| `Model not found`        | Run `ollama pull llama3` first              |
| Very slow responses      | Try `ollama pull phi3` (smaller model)      |
| Package not found error  | Run `pip install -r requirements.txt` again |
