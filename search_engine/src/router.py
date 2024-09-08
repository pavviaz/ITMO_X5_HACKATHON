from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from src.dao import search_by_embedding, get_text_embedding, rewrite_query, qa_stuff
from src.contracts import ChatHistory
# from dao import search_by_embedding, get_text_embedding, rewrite_query, qa_stuff
# from contracts import ChatHistory

router = APIRouter(prefix="/api/v1", tags=["x5_api"])


@router.post("/get_answer")
async def search(
    request: Request,
    chat_history: ChatHistory,
):
    """
    Search for nearest neighbors in
    the database on the given text.

    Args:
        request (Request): The FastAPI request object.
        text (str): The resume text for which to search for nearest neighbors.

    Returns:
        JSONResponse: The search results as a JSON response,
        including the metadata information retrieved
        from the database and the "success" key with the value True.
    """
    # TODO
    # if user's last content is similar to any of popular - return
    # use llm? train some model?

    # TODO
    # query rewriting - to make last user message contextualized
    rewrited = await rewrite_query(chat_history.history)

    # TODO
    # domen classifier - to decide wether to lauch main pipeline
    # or ask to specify request

    q_emb = await get_text_embedding(rewrited)

    result = await search_by_embedding(
        embedding=q_emb,
        session=request.state.db,
        f_index=request.state.fd,
    )

    qa = await qa_stuff(rewrited, result)

    return JSONResponse(
        content={"qa_answer": qa, "sources": result} | {"success": True}
    )
