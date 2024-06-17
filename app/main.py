import uvicorn
from fastapi import FastAPI

from .models import Base
from .database import engine
from .routers import auth, todos, admin, user
from .middleware.request_processtime import AccessMiddleware

app = FastAPI(title="User Service API", openapi_url="/api/v1/openapi.json")

# Create all tables in the database
Base.metadata.create_all(bind=engine)

# Add custom middleware
app.add_middleware(AccessMiddleware)


# Health check endpoint
@app.get("/healthy")
async def health_check():
    return {"status": "healthy"}


# Include routers
app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(user.router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
