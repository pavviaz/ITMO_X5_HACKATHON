from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from src.dao import search_by_embedding, get_text_embedding
from src.contracts import ChatHistory
# from dao import search_by_embedding, get_text_embedding
# from contracts import ChatHistory

router = APIRouter(prefix="/api/v1", tags=["x5_api"])


@router.post("/get_answer")
async def search(
    request: Request,
    text: ChatHistory,
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
    # query rewriting - to make last user message contextualized
    req = text.history[-1].content

    # TODO
    # domen classifier - to decide wether to lauch main pipeline 
    # or ask to specify request

    q_emb = await get_text_embedding(req)

    result = await search_by_embedding(
        embedding=q_emb,
        session=request.state.db,
        f_index=request.state.fd,
    )

    return JSONResponse(content={"res": result} | {"success": True})
