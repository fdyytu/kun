from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from config.settings.app import APP_NAME, APP_VERSION, API_PREFIX, HOST, PORT
from routes.v1 import admin_router, auth_router
import uvicorn

# Create FastAPI instance
app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION,
    description="API Service with Admin Panel"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers with API prefix
app.include_router(admin_router, prefix=f"{API_PREFIX}/admin", tags=["admin"])
app.include_router(auth_router, prefix=f"{API_PREFIX}/admin/auth", tags=["auth"])

@app.get("/")
async def root():
    return {"message": f"Welcome to {APP_NAME} v{APP_VERSION}"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": APP_VERSION}

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=HOST,
        port=PORT,
        reload=True
    )
