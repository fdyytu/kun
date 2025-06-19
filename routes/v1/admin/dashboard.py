from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import Dict, Any, List
import jwt
from datetime import datetime, timedelta
import random

router = APIRouter()
security = HTTPBearer()

# Secret key for JWT (should match the one in login.py)
SECRET_KEY = "your-secret-key-here"
ALGORITHM = "HS256"

class DashboardStats(BaseModel):
    total_users: int
    active_users: int
    total_transactions: int
    total_revenue: float
    pending_orders: int
    system_status: str
    last_updated: str

class SystemMetrics(BaseModel):
    cpu_usage: float
    memory_usage: float
    disk_usage: float
    active_connections: int

class RecentActivity(BaseModel):
    id: str
    type: str
    description: str
    timestamp: str
    user: str

def verify_admin_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Verify admin token and return user info
    """
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        role: str = payload.get("role")
        
        if username is None or role != "admin":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid admin token"
            )
        
        return {"username": username, "role": role}
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )

def generate_mock_stats() -> DashboardStats:
    """
    Generate mock dashboard statistics
    In production, this would fetch real data from database
    """
    return DashboardStats(
        total_users=random.randint(1000, 5000),
        active_users=random.randint(100, 500),
        total_transactions=random.randint(10000, 50000),
        total_revenue=round(random.uniform(100000, 500000), 2),
        pending_orders=random.randint(10, 100),
        system_status="healthy",
        last_updated=datetime.now().isoformat()
    )

def generate_system_metrics() -> SystemMetrics:
    """
    Generate mock system metrics
    """
    return SystemMetrics(
        cpu_usage=round(random.uniform(10, 80), 2),
        memory_usage=round(random.uniform(30, 90), 2),
        disk_usage=round(random.uniform(20, 70), 2),
        active_connections=random.randint(50, 200)
    )

def generate_recent_activities() -> List[RecentActivity]:
    """
    Generate mock recent activities
    """
    activities = [
        RecentActivity(
            id="1",
            type="user_registration",
            description="New user registered",
            timestamp=(datetime.now() - timedelta(minutes=5)).isoformat(),
            user="user123"
        ),
        RecentActivity(
            id="2",
            type="transaction",
            description="Payment processed successfully",
            timestamp=(datetime.now() - timedelta(minutes=15)).isoformat(),
            user="user456"
        ),
        RecentActivity(
            id="3",
            type="system",
            description="System backup completed",
            timestamp=(datetime.now() - timedelta(hours=1)).isoformat(),
            user="system"
        )
    ]
    return activities

@router.get("/dashboard/stats", response_model=DashboardStats)
async def get_dashboard_stats(current_user: dict = Depends(verify_admin_token)):
    """
    Get dashboard statistics for admin panel
    """
    try:
        stats = generate_mock_stats()
        return stats
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch dashboard stats: {str(e)}"
        )

@router.get("/dashboard/metrics", response_model=SystemMetrics)
async def get_system_metrics(current_user: dict = Depends(verify_admin_token)):
    """
    Get system metrics for admin dashboard
    """
    try:
        metrics = generate_system_metrics()
        return metrics
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch system metrics: {str(e)}"
        )

@router.get("/dashboard/activities")
async def get_recent_activities(current_user: dict = Depends(verify_admin_token)):
    """
    Get recent activities for admin dashboard
    """
    try:
        activities = generate_recent_activities()
        return {
            "activities": activities,
            "total": len(activities),
            "last_updated": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch recent activities: {str(e)}"
        )

@router.get("/dashboard/overview")
async def get_dashboard_overview(current_user: dict = Depends(verify_admin_token)):
    """
    Get complete dashboard overview
    """
    try:
        stats = generate_mock_stats()
        metrics = generate_system_metrics()
        activities = generate_recent_activities()
        
        return {
            "stats": stats,
            "metrics": metrics,
            "recent_activities": activities[:5],  # Last 5 activities
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch dashboard overview: {str(e)}"
        )
