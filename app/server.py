from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware

from langserve import add_routes

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://www.bonates.com",
        "https://bonates.com",
        "http://localhost",
        "http://localhost:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

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

# my packages
from einstein import chain as einstein_chain
add_routes(app, einstein_chain, path="/einstein")

# from bonato import chain as bonato_chain
# add_routes(app, bonato_chain, path="/bonato")

# start
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
