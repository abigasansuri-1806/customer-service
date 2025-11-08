from fastapi import FastAPI
from app.routes_customer import router as customer_router
from app.database import init_db
from utils.kafka_producer import start_producer, stop_producer

app = FastAPI(
    title="Customer Service API",
    description="Microservice for managing customers and KYC status.",
    version="1.0.0"
)

app.include_router(customer_router)

@app.on_event("startup")
async def startup_event():
    await start_producer()
    init_db()
    print("App startup complete!")

@app.on_event("shutdown")
async def shutdown_event():
    await stop_producer()

@app.get("/")
def read_root():
    return {"message": "Customer Service is running!"}
