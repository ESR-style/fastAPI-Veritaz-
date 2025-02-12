from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from controllers import messages, threads

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(messages.router)
app.include_router(threads.router)

# Startup event
@app.on_event("startup")
async def startup_event():
    # Initialize any required services here
    pass

# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    # Clean up any resources here
    pass