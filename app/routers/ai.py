from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.database import get_session
from app.models.workspace import Workspace
from app.core.ai import ask_gemini

router = APIRouter()

@router.post("/ai/suggest-workspace")
async def suggest_workspace(query: str, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Workspace))
    workspaces = result.scalars().all()

    workspace_list_text = "\n".join(
        [f"id: {w.id}, Name: {w.name}, Type: {w.type}, Capacity: {w.capacity}, description: {w.description}" for w in workspaces]
    )

    prompt = f"""Here is list of workspaces:
{workspace_list_text}

User request: "{query}"Workspace
Choose ONLY ONE most suitable place and reply ONLY with the id number of this place, without any additional words, explanations, or punctuation marks."""

    ai_response = ask_gemini(prompt)
    print(f"DEBUG: Gemini ответил: '{ai_response}'")
    try:
        suggested_id = int(ai_response.strip())
        print(f"DEBUG: ищем workspace с id = {suggested_id}, тип: {type(suggested_id)}")
    except ValueError:
        raise HTTPException(status_code=500, detail="Failed to get AI recommendation")

    query_workspace = select(Workspace).where(Workspace.id == suggested_id)
    result = await session.execute(query_workspace)
    suggested_workspace = result.first()

    if not suggested_workspace:
        raise HTTPException(status_code=404, detail="The AI recommended a place that doesn't exist")

    return suggested_workspace[0]