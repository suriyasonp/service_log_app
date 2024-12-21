from fastapi import FastAPI
from routers import user_router  # Import your routers

app = FastAPI()

# Include routers
app.include_router(user_router.router, prefix="/users", tags=["Users"])

@app.get("/")
def read_root():
    return {"message": "Service Log API is running!"}