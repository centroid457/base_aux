from typing import Optional, Dict, List, Any
from pydantic import BaseModel
from enum import Enum
from datetime import datetime

class TestStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    PASSED = "passed"
    FAILED = "failed"
    SKIPPED = "skipped"
    PAUSED = "paused"

class TestNode(BaseModel):
    id: str
    name: str
    type: str  # "class" or "function"
    status: TestStatus = TestStatus.PENDING
    duration: Optional[float] = None
    error: Optional[str] = None
    children: List['TestNode'] = []
    
class TestPlan(BaseModel):
    name: str
    path: str
    tests: List[TestNode] = []

class RunState(BaseModel):
    status: str  # "idle", "running", "paused", "stopping"
    current_test: Optional[str] = None
    testplan: Optional[str] = None
    results: Dict[str, Any] = {}
    started_at: Optional[datetime] = None