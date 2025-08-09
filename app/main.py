import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.model.query_model import QueryRequest, FinalResponse, SearchTerms
from app.service.nlp_pipeline import process_query_with_groq_llm

# Create FastAPI app
app = FastAPI(
    title="Agro-Food NLP Microservice",
    description="A robust microservice that processes multilingual user queries into English and French structured data.",
    version="15.0.0"  # THE DUAL-LANGUAGE BUILD
)

# Allow CORS so your frontend or other services can call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to your frontend domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root health-check endpoint
@app.get("/")
async def root():
    return {"message": "NLP Microservice is running!"}

# Main processing endpoint
@app.post("/process-query", response_model=FinalResponse)
async def process_query_endpoint(request: QueryRequest):
    """
    Receives a user query and processes it using the Llama 3 Groq API
    to get structured output in both English and French.
    """
    result_dict = process_query_with_groq_llm(request.query)

    search_terms_data = SearchTerms(
        english_product=result_dict.get('english_product', 'N/A'),
        english_attributes=result_dict.get('english_attributes', []),
        french_product=result_dict.get('french_product', 'N/A'),
        french_attributes=result_dict.get('french_attributes', [])
    ) if result_dict and result_dict.get('english_product') != "Error" else None

    return FinalResponse(
        original_query=request.query,
        search_terms=search_terms_data
    )

# Only for local testing
if __name__ == "_main_":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))  # Render sets PORT env var
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)