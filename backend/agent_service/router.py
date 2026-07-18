from fastapi import APIRouter, HTTPException
from agent_service.orchestrator import generate_report

router= APIRouter()

@router.get("/report/{symbol}")
def report(symbol:str):
	result= generate_report(symbol)
	if "error" in result:
		raise HTTPException(400,result["error"])
	return result