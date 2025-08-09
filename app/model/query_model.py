from pydantic import BaseModel, Field
from typing import List, Optional

# New nested model for structured search terms in both languages
class SearchTerms(BaseModel):
    english_product: str
    english_attributes: List[str]
    french_product: str
    french_attributes: List[str]

class QueryRequest(BaseModel):
    query: str

class FinalResponse(BaseModel):
    original_query: str
    # The search_terms field will now contain everything we need
    search_terms: Optional[SearchTerms] = None