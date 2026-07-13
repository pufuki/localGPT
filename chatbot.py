# Introduction
#   LocalGPT Chatbot with Memory
#   Tools  : Python + LangChain + Ollama 
#
#   1. Install Ollama:  https://ollama.com/download
#   2. Open terminal :  ollama serve
#   3. Pull a model  :  ollama pull llama3
#   4. Install libs  :  pip install -r requirements.txt
#   5. Run the bot   :  python chatbot.py

from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

# Settings
MODEL       = "llama3"   # swap to any models
MEMORY_SIZE = 10         # how many past messages the bot remembers
TEMPERATURE = 0.7        # 0 = very focused answers | 1 = more creative

# The bot's personality, edit this to change how it behaves
SYSTEM_PROMPT = """
You are a helpful and friendly AI assistant running locally.
You remember the conversation and refer back to it naturally.
Keep answers short and clear unless the user asks for more detail.
"""

# MEMORY  (a plain Python list of messages)
memory = []   # holds HumanMessage and AIMessage objects

def save_message(role, text):
    """
    Save a message to memory.
    If memory is full, the oldest message is removed automatically.
    """
    if role == "human":
        memory.append(HumanMessage(content=text))
    else:
        memory.append(AIMessage(content=text))

    # Keep memory from growing too large
    if len(memory) > MEMORY_SIZE:
        memory.pop(0)   # remove the oldest message


# CHAT  (this function does the actual talking)
def chat(user_text):
    """
    How it works:
      Step 1 → save what the user said
      Step 2 → send [system prompt + full memory] to the model
      Step 3 → save the AI reply, then return it
    """
    save_message("human", user_text)

    # Build the full message list the model will read
    all_messages = [SystemMessage(content=SYSTEM_PROMPT)] + memory

    # Send to the local Ollama model
    response = bot.invoke(all_messages)
    reply    = response.content

    save_message("ai", reply)
    return reply


# HELPER FUNCTIONS  (for commands like history/help)
def show_history():
    """Print the full conversation stored in memory."""
    if not memory:
        print("\n  (no history yet — start chatting!)\n")
        return

    print("\n  ┌─ Conversation History ───────────────")
    for msg in memory:
        speaker = "  │  You" if isinstance(msg, HumanMessage) else "  │   AI"
        print(f"{speaker}: {msg.content}")
    print("  └──────────────────────────────────────\n")


def show_help():
    """Print all available commands."""
    print("""
  ┌─ Commands ──────────────────────────────┐
  │  quit  /  exit   -> close the chatbot   │
  │  clear           -> wipe memory         │
  │  history         -> see past messages   │
  │  help            -> show this list      │
  └─────────────────────────────────────────┘
    """)


# MAIN LOOP  (keeps the chat going until you quit)

def run_chatbot():
    # Welcome banner
    print("Welcome to")
    print("""
██╗      ██████╗  ██████╗ █████╗ ██╗      ██████╗ ██████╗ ████████╗
██║     ██╔═══██╗██╔════╝██╔══██╗██║     ██╔════╝ ██╔══██╗╚══██╔══╝
██║     ██║   ██║██║     ███████║██║     ██║  ███╗██████╔╝   ██║   
██║     ██║   ██║██║     ██╔══██║██║     ██║   ██║██╔═══╝    ██║   
███████╗╚██████╔╝╚██████╗██║  ██║███████╗╚██████╔╝██║        ██║   
╚══════╝ ╚═════╝  ╚═════╝╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═╝        ╚═╝   
                                                               """)
    print(f"model: {MODEL}")
    print("-" * 50)
    print("Type a message and press Enter to chat.")
    print("Type  help  to see all commands.")
    print("-" * 50 + "\n")

    while True:

        # Read user input
        try:
            user_input = input("You: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n\nGoodbye!\n")
            break

        # Ignore blank lines
        if not user_input:
            continue

        command = user_input.lower()

        #Built-in commands
        if command in ("quit", "exit"):
            print("\nGoodbye!\n")
            break

        elif command == "clear":
            memory.clear()
            print("Memory wiped — starting fresh!\n")

        elif command == "history":
            show_history()

        elif command == "help":
            show_help()

        #Regular chat message 
        else:
            try:
                reply = chat(user_input)
                print(f"\nAI: {reply}\n")

            except Exception as error:
                print(f"\nError: {error}")
                print("Is Ollama running?  Try: ollama serve\n")



# START THE BOT

if __name__ == "__main__":

    # Connect to the local Ollama model
    bot = ChatOllama(model=MODEL, temperature=TEMPERATURE)

    # Launch the chat loop
    run_chatbot()
