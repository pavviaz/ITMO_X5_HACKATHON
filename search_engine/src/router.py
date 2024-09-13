from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from src.dao import (
    search_by_embedding,
    get_text_embedding,
    rewrite_query,
    check_popularity,
    check_domain,
    qa_stuff
)
from src.contracts import ChatHistory
from src.config import popular_answers
# from dao import (
#     search_by_embedding,
#     get_text_embedding,
#     rewrite_query,
#     check_popularity,
#     check_domain,
#     qa_stuff
# )
# from contracts import ChatHistory
# from config import popular_answers


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
    popularity = await check_popularity(chat_history.history[-1].content)

    if popularity != "ordinary":
        popular_answer = popular_answers[popularity]
        return JSONResponse(
            content={"qa_answer": popular_answer, "sources": [], "exit": "POP_FILTER"}
            | {"success": True}
        )

    if len(chat_history.history) > 1:
        rewrited = await rewrite_query(chat_history.history)
    else:
        rewrited = chat_history.history[0].content

    domain = await check_domain(rewrited)
    if domain == "multi":
        return JSONResponse(
            content={
                "qa_answer": "Пожалуйста, уточните ваш запрос",
                "sources": [],
                "exit": f"DOMEN: {domain}"
            }
            | {"success": True}
        )
    elif domain == "trash":
        return JSONResponse(
            content={
                "qa_answer": popular_answers["popular_angry"],
                "sources": [],
                "exit": f"DOMEN: {domain}"
            }
            | {"success": True}
        )
    q_emb = await get_text_embedding(rewrited)

    result = await search_by_embedding(
        embedding=q_emb,
        session=request.state.db,
        f_index=request.state.fd,
    )

    qa = await qa_stuff(rewrited, result)

    return JSONResponse(
        content={"qa_answer": qa, "sources": result, "exit": f"QA"} | {"success": True}
    )
