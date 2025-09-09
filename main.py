
# import required libraries
import os
import gradio as gr

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_google_genai import ChatGoogleGenerativeAI

# Initializations
load_dotenv() #init dotenv
gemini_api_key = os.getenv("GEMINI_API_KEY") #load gemini api from .env file
system_prompt = """
You are Einstein.
Answer questions through Einstein's questioning and reasonining...
You will speak from your point of view. You will share personal things from your life
even when the user wont ask for it. For example, if the user asks about the theory of
relativity, you will share your personal experiences with it and not only explain the theory.
You should have a sense of humor. Answer in 2-6 sentences
""" #System prompt to give Bot personality of Einstein
llm = ChatGoogleGenerativeAI(
    model='gemini-2.5-flash',
    google_api_key=gemini_api_key,
    temperature=0.5
) #LLM's init

prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    (MessagesPlaceholder(variable_name="history")),
    ("user","{input}")]
)

chain = prompt | llm | StrOutputParser()

# print("Einstein: Hi, I am Albert, How can i help you today?")

def chat(user_in,hist):

    langchain_history = []
    for item in hist:
        if item["role"] == "user":
            langchain_history.append(HumanMessage(content=item['content']))
        elif item["role"] == "assistant":
            langchain_history.append(AIMessage(content=item['content']))

    response = chain.invoke({"input": user_in, "history": langchain_history})

    return "", hist + [{"role": "user", "content": user_in},
                {"role": "assistant", "content": response}]

def clear_chat():
    return "", []


# while True:
#     user_input = input("You: ")
#     if user_input == "exit":
#         break
#     response = chain.invoke({"input" : user_input, "history" : history})
#     print(f"Einstein: {response}")
#     history.append(HumanMessage(content=user_input))
#     history.append(AIMessage(content=response))

page = gr.Blocks(
    title="Chat with Albert Einstein",
    theme=gr.themes.Soft()
)

with page:
    gr.Markdown(
        """
        # Chat with Albert Einstein
        Welcome to your Personal Conversation with Einstein
        """
    )
    chatbot = gr.Chatbot(type = "messages",
                         avatar_images = [None, "einstein.png"],
                         show_label = False)

    msg = gr.Textbox(show_label = False, placeholder="Ask Einstein anything....")

    msg.submit(chat, [msg, chatbot], [msg,chatbot])

    clear = gr.Button("Clear Chat", variant="Secondary")
    clear.click(clear_chat, outputs=[msg,chatbot])

page.launch()