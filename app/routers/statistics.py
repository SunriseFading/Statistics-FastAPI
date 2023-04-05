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


@router.get("/all", status_code=status.HTTP_200_OK, summary="Get all statistics")
async def all(
    params: StatisticParams = Depends(), session: AsyncSession = Depends(get_session)
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
    print(params.order_by)
    statistics = await m_Statistic.filter(
        date__gte=params.from_date,
        date__lte=params.to_date,
        order_by=params.order_by,
        session=session,
    )
    return (
        [StatisticOutput.from_orm(statistic).dict() for statistic in statistics]
        if statistics
        else None
    )


@router.post("/create", status_code=status.HTTP_201_CREATED, summary="Create statistic")
async def create(statistic: s_Statistic, session: AsyncSession = Depends(get_session)):
    """
    Create or update statistic.

    Args:
        statistic (Statistic): The statistic to create.
        db (AsyncSession): The asynchronous database session.

    Returns:
        Dict[str, str]: A message indicating that the statistic was created or updated.

    """
    existing_statistic = await m_Statistic.get(date=statistic.date, session=session)
    if existing_statistic:
        existing_statistic.views += statistic.views
        existing_statistic.clicks += statistic.clicks
        existing_statistic.cost += statistic.cost
        existing_statistic.cpc = existing_statistic.cost_per_clicks
        existing_statistic.cpm = existing_statistic.cost_per_views
        await existing_statistic.update(session=session)
        return {"detail": messages.STATISTIC_UPDATED}
    statistic = await m_Statistic(**statistic.dict()).create(session=session)
    return {"detail": messages.STATISTIC_CREATED}


@router.delete(
    "/delete_all", status_code=status.HTTP_200_OK, summary="Delete all statistics"
)
async def delete_all(session: AsyncSession = Depends(get_session)):
    """
    Delete all statistics.

    Args:
        db (AsyncSession): The asynchronous database session.

    Returns:
        Dict[str, str]: A message indicating that the statistics were deleted.

    """
    statistics = await m_Statistic.all(session=session)
    await m_Statistic.delete(instances=statistics, session=session)
    return {"detail": messages.STATISTICS_DELETED}
