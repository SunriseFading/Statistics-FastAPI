from app.crud.statistics import DBStatistics
from app.database import get_session
from app.models.statistics import Statistic as m_Statistic
from app.schemas.statistics import Statistic as s_Statistic
from app.schemas.statistics import StatisticOutput, StatisticParams
from app.utils.messages import messages
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(
    prefix="/statistic",
    tags=["statistic"],
    responses={404: {"description": "Not found"}},
)


@router.get("/get_all", status_code=status.HTTP_200_OK, summary="Get all statistics")
async def get_all(
    params: StatisticParams = Depends(), db: AsyncSession = Depends(get_session)
):
    """
    Retrieves all Statistic records from the database
    and optionally sorts them by a specified field,
    and optionally filters them by a date range.

    Args:
        db (AsyncSession): The database session.
        query (StatisticParams): The query parameters.

    Returns:
        list[Statistic]: A list of Statistic instances.
    """
    statistics = await DBStatistics.get_all(
        from_date=params.from_date,
        to_date=params.to_date,
        sort_by=params.sort_by,
        db=db,
    )
    return (
        [StatisticOutput.from_orm(statistic).dict() for statistic in statistics]
        if statistics
        else None
    )


@router.post("/create", status_code=status.HTTP_201_CREATED, summary="Create statistic")
async def create(statistic: s_Statistic, db: AsyncSession = Depends(get_session)):
    """
    Create or update statistic.

    Args:
        statistic (Statistic): The statistic to create.
        db (AsyncSession): The asynchronous database session.

    Returns:
        Dict[str, str]: A message indicating that the statistic was created or updated.

    """
    existing_statistic = await DBStatistics.get_by_date(db, statistic.date)
    if existing_statistic:
        if statistic.views:
            existing_statistic.views += statistic.views
        if statistic.clicks:
            existing_statistic.clicks += statistic.clicks
        if statistic.cost:
            existing_statistic.cost += statistic.cost
        await DBStatistics.update(db, existing_statistic)
        return {"detail": messages.STATISTIC_UPDATED}

    statistic = m_Statistic(**statistic.dict())
    await DBStatistics.create(db=db, statistic=statistic)
    return {"detail": messages.STATISTIC_CREATED}


@router.delete(
    "/delete_all", status_code=status.HTTP_200_OK, summary="Delete all statistics"
)
async def delete_all(db: AsyncSession = Depends(get_session)):
    """
    Delete all statistics.

    Args:
        db (AsyncSession): The asynchronous database session.

    Returns:
        Dict[str, str]: A message indicating that the statistics were deleted.

    """
    await DBStatistics.delete_all(db=db)
    return {"detail": messages.STATISTICS_DELETED}
