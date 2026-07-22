import os

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.responses import JSONResponse

# Import the optimization runner
from src.model.optimizer import run_optimization

app = FastAPI(
    title="UP Agri-Economics Optimization Engine API",
    description="Backend optimization engine for agricultural land allocation."
)

class OptimizationPayload(BaseModel):
    risk_aversion: float
    water_cost: float

@app.get("/")
def health_check():
    """
    Root health-check endpoint. Render (and browsers hitting the bare
    URL) will get a 200 here instead of a 404, and it's a quick way to
    confirm the service is awake.
    """
    return {"status": "ok", "service": "UP Agri-Economics Optimization Engine API"}

@app.post("/optimize")
def optimize_portfolio(payload: OptimizationPayload):
    """
    Receives user parameters, updates the global Pyomo model, 
    runs the GLPK solver, and returns the optimal crop mix.
    """
    try:
        results = run_optimization(payload.risk_aversion, payload.water_cost)
        return JSONResponse(content=results)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn

    # Render (and most cloud hosts) inject the port to bind to via the
    # PORT env var, and require binding to 0.0.0.0 rather than
    # 127.0.0.1/localhost so the service is reachable from outside the
    # container. reload=True is dev-only; disable it for production.
    port = int(os.environ.get("PORT", 8000))
    is_local = os.environ.get("RENDER") is None
    uvicorn.run(
        "src.api.main:app",
        host="127.0.0.1" if is_local else "0.0.0.0",
        port=port,
        reload=is_local,
    )