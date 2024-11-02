from fastapi import APIRouter, HTTPException
from backend.models.debate import DebateConfig, DebateState
from backend.services.debate import DebateService

router = APIRouter()
debate_service = DebateService()

@router.post("/start", response_model=DebateState)
async def start_debate(config: DebateConfig):
    return await debate_service.create_debate(config)

@router.post("/{debate_id}/turn", response_model=DebateState)
async def make_turn(debate_id: str, content: str):
    try:
        return await debate_service.process_turn(debate_id, content)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/{debate_id}", response_model=DebateState)
async def get_debate(debate_id: str):
    debate = debate_service.active_debates.get(debate_id)
    if not debate:
        raise HTTPException(status_code=404, detail="Debate not found")
    return debate