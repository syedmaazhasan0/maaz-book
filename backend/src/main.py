"""
Main application entry point for the Integrated RAG Chatbot API.
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from src.api.query_api import router as query_router
import traceback


# Initialize the FastAPI application
app = FastAPI(title="Integrated RAG Chatbot API")

# Add CORS middleware
try:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*","http://localhost:3000","http://maaz-book.vercel.app"],
        allow_credentials=True,
        allow_methods=["Get", "POST", "PUT", "DELETE", "OPTIONS"],
        allow_headers=["X-API-KEY", "Content-Type","Authorization"],
    )
except Exception as e:
    print(f"Error adding middleware: {e}")

# Include the query API router
app.include_router(query_router, prefix="", tags=["query"])


# Removed custom exception handler to use FastAPI defaults
# v3

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "API is running"}


@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "Physical AI and Humanoid Robotics Chatbot API"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)