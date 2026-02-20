import uvicorn
from fastapi import FastAPI, Response
from fastapi.responses import RedirectResponse

# app = FastAPI()
app = FastAPI(title="MinimalCode FastApi")


@app.get("/")
async def redirect() -> Response:
    return RedirectResponse(url="/docs")


@app.get("/{path}")
async def echo_path(path):
    print(path)
    return path

# =====================================================================================================================
if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=80)


# =====================================================================================================================
