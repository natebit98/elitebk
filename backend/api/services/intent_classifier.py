from dataclasses import dataclass

@dataclass
class IntentResult:
    intent: str
    reason: str

STATS_LOOKUP = {}
COMPARISON = {}
PREDICTION_INFO = {}
BRIEF_SUMMARY = {}
EXPLANATION = {}

def classify_intent(question : str) -> IntentResult: #Return dataclass with appropriate intent classified and reason for next step
    q = question.lower().str()
    
