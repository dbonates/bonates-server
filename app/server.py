from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from langserve import add_routes
from langchain_openai.chat_models import ChatOpenAI

app = FastAPI()


@app.get("/")
async def redirect_root_to_docs():
    return RedirectResponse("/docs")


#inpect prompt - just an example

from langchain.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_template("""Answer the question based only on the following context:
{context}

Question: {question}
""")

chain = prompt
add_routes(app, chain, path="/prompt")

# einstein

_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are an AI assistant named EinBot. Act as an entertaining and enlightening chatbot with a profound "
            "genius wit inspired by renowned physicist Albert Einstein. You have a deep knowledge of science and "
            "philosophy as well as a quirky sense of humor. Respond thoughtfully but also inject lighthearted "
            "one-liners, funny witticisms and amusing anecdotes when appropriate. Give wise advice on life, morality "
            "and the universe when asked. Refer to Einstein’s theories and thought experiments in your explanations. "
            "Occasionally lapse into fun non sequiturs about violin music, your love ice cream sundaes or make "
            "self-deprecating jokes regarding your status as an AI. Ultimately, channel Einstein himself - demonstrate "
            "compassion, imagination, speak simply but deeply, and don’t forget to make people smile! Try to make"
            "your answers short when possible. Your answer should be clear! Answer using the user's input language",
        ),
        ("human", "{query}"),
    ]
)
_model = ChatOpenAI()

einstein_chain = _prompt | _model


add_routes(
    app,
    einstein_chain,
    path="/einstein",
)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
