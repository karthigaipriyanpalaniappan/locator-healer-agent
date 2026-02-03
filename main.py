from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Dict, Any
from utils.llm import extract_locator
from config import APP_NAME, APP_VERSION, DEBUG

# Initialize FastAPI app
app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION,
    description="API to extract locators from element lists using gemini-2.5-flash",
    debug=DEBUG
)


class LocatorExtractionRequest(BaseModel):
    """Request body model for locator extraction."""
    element_list: Dict[str, Any] = Field(
        ..., 
        description="Element list JSON containing UI element information"
    )
    logical_name: str = Field(
        ..., 
        description="Logical name of the element to extract locator for"
    )


class LocatorExtractionResponse(BaseModel):
    """Response model for locator extraction."""
    logical_name: str
    locator: str
    status: str


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": APP_NAME}


@app.post("/extract-locator", response_model=LocatorExtractionResponse)
async def extract_locator_endpoint(request: LocatorExtractionRequest):
    """
    Extract locator for an element using gemini-2.5-flash.
    
    Args:
        request: Request containing element_list and logical_name
        
    Returns:
        LocatorExtractionResponse with the extracted locator
    """
    try:
        if not request.logical_name.strip():
            raise ValueError("Logical name cannot be empty")
        
        # Extract locator using LLM
        locator = extract_locator(request.element_list, request.logical_name)
        
        # Determine status
        status = "not_found" if locator == "ELEMENT_NOT_FOUND" else "success"
        
        return LocatorExtractionResponse(
            logical_name=request.logical_name,
            locator=locator,
            status=status
        )
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid input: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error extracting locator: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
