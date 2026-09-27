from typing import Any

from fastapi import APIRouter, Query
from sqlmodel import col

from app.api.deps import CurrentUser, SessionDep
from app.crud import get_boss_jobs
from app.models import BossJobDetailsPublic, BossJobsPublic

router = APIRouter(prefix="/boss-jobs", tags=["boss_jobs"])


@router.get("/", response_model=BossJobsPublic)
def read_boss_jobs(
    session: SessionDep,
    current_user: CurrentUser,
    skip: int = 0,
    limit: int = 100,
    created_time: str | None = Query(default=None, description="Filter by creation date (YYYY-MM-DD)"),
    job_name: str | None = Query(default=None, description="Filter by job name (partial match)"),
    city_name: str | None = Query(default=None, description="Filter by city name"),
) -> Any:
    """
    Retrieve boss job listings with optional filters.
    """
    jobs, count = get_boss_jobs(
        session=session,
        skip=skip,
        limit=limit,
        created_time=created_time,
        job_name=job_name,
        city_name=city_name,
    )
    jobs_public = [BossJobDetailsPublic.model_validate(job) for job in jobs]
    return BossJobsPublic(data=jobs_public, count=count)
