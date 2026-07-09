from pydantic import BaseModel, Field
from typing import List, Optional

class HCPInteractionSchema(BaseModel):
    hcpName: str = ""
    specialty: str = ""
    organization: str = ""
    interactionType: str = ""
    interactionDate: str = ""
    interactionTime: str = ""
    location: str = ""
    duration: str = ""
    productsDiscussed: List[str] = Field(default_factory=list)
    topicsDiscussed: List[str] = Field(default_factory=list)
    materialsShared: List[str] = Field(default_factory=list)
    samplesDistributed: List[str] = Field(default_factory=list)
    questionsRaised: List[str] = Field(default_factory=list)
    objections: List[str] = Field(default_factory=list)
    followUpDate: str = ""
    sentiment: str = ""
    interactionOutcome: str = ""
    summary: str = ""

    class Config:
        from_attributes = True

class ChatRequest(BaseModel):
    message: str
    history: List[dict] = []
