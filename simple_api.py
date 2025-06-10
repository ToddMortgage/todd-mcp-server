#!/usr/bin/env python3
import asyncio
import json
import httpx
import subprocess
from datetime import datetime
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from pydantic import BaseModel

# Create FastAPI web server for API endpoints
app = FastAPI(title="Todd's Market Intelligence API")

# Enable CORS for Zapier
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Your database config with hardcoded token
NOTION_TOKEN = "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"

# Request models
class ReportRequest(BaseModel):
    firstName: str
    lastName: str
    email: str
    phone: str
    city: str
    propertyType: str
    minPrice: str = ""
    maxPrice: str = ""
    reportType: str

@app.get("/")
async def root():
    return {"message": "Todd's Market Intelligence API is running!", "status": "healthy"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "Todd's API is running!"}

@app.post("/generate-report")
async def generate_report(request: ReportRequest):
    try:
        # Generate custom market report
       # Call Node.js MLS scraper with form parameters
        try:
            result = subprocess.run([
                'node', 'matrix-scraper.js',
                '--city', request.city,
                '--propertyType', request.propertyType, 
                '--minPrice', request.minPrice,
                '--maxPrice', request.maxPrice
            ], capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                # Parse MLS data from scraper
                mls_data = json.loads(result.stdout)
                
                report_data = {
                    "reportId": f"SFL_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{request.firstName}_{request.lastName}",
                    "client": f"{request.firstName} {request.lastName}",
                    "email": request.email,
                    "city": request.city,
                    "propertyType": request.propertyType,
                    "priceRange": f"${request.minPrice} - ${request.maxPrice}",
                    "reportType": request.reportType,
                    "generated": datetime.now().isoformat(),
                    "mlsData": mls_data,  # Real MLS data here
                    "message": f"MLS data retrieved for {request.city} - {len(mls_data.get('properties', []))} properties found"
                }
            else:
                # Fallback if scraper fails
                report_data = {
                    "reportId": f"SFL_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{request.firstName}_{request.lastName}",
                    "client": f"{request.firstName} {request.lastName}",
                    "email": request.email,
                    "city": request.city,
                    "error": "MLS scraper failed",
                    "message": f"Unable to retrieve MLS data for {request.city}"
                }
                
        except Exception as e:
            # Error handling
            report_data = {
                "reportId": f"SFL_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{request.firstName}_{request.lastName}",
                "error": str(e),
                "message": "MLS scraper error"
            }

@app.get("/test-zapier")
async def test_zapier():
    return {
        "success": True,
        "message": "Zapier connection working!",
        "timestamp": datetime.now().isoformat()
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
