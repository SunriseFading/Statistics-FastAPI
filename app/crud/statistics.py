from datetime import date
from typing import Optional

from app.models.statistics import Statistic
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession


class DBStatistics:
    @staticmethod
    async def create(db: AsyncSession, statistic: Statistic) -> Statistic:
        """
        Creates a new Statistic record in the database.

        Args:
            db (AsyncSession): The database session.
            statistic (Statistic): The Statistic model instance to create.

        Returns:
            Statistic: The created Statistic instance.
        """
        db.add(statistic)
        await db.flush()
        await db.commit()
        return statistic

    @staticmethod
    async def get_by_date(db: AsyncSession, date: date) -> Statistic:
        """
        Retrieves all Statistic records with a given date from the database.

        Args:
            db (AsyncSession): The database session.
            date (date): The date to filter by.

        Returns:
            Statistic: A Statistic instance with the given date.
        """
        query = select(Statistic).where(Statistic.date == date)
        result = await db.execute(query)
        return result.scalars().first()

    @staticmethod
    async def get_all(
        db: AsyncSession,
        sort_by: Optional[str],
        from_date: Optional[date] = None,
        to_date: Optional[date] = None,
    ) -> list[Statistic]:
        """
        Retrieves all Statistic records from the database
        and optionally sorts them by a specified field.

        Args:
            db (AsyncSession): The database session.
            sort_by (str): The name of the field to sort the query set by,
            with an optional "-" prefix for descending order.
            from_date (date): The starting date range for the query.
            to_date (date): The ending date range for the query.

        Returns:
            list[Statistic]: A list of Statistic instances.
        """
        if sort_by is None:
            sort_by = "-date"
        order_by_field = Statistic.date
        if sort_by:
            if sort_by[0] == "-":
                order_by_field = getattr(Statistic, sort_by[1:]).desc()
            else:
                order_by_field = getattr(Statistic, sort_by)

        query = select(Statistic).order_by(order_by_field)
        if from_date:
            query = query.where(Statistic.date >= from_date)
        if to_date:
            query = query.where(Statistic.date <= to_date)
        result = await db.execute(query)
        return result.scalars().all()

    @staticmethod
    async def update(db: AsyncSession, updated_statistic: Statistic):
        """
        Updates an existing Statistic record in the database.

        Args:
            db (AsyncSession): The database session.
            existing_statistic (Statistic): The Statistic model instance to update.
        """
        updated_statistic.cpc = updated_statistic.cost_per_clicks
        updated_statistic.com = updated_statistic.cost_per_views
        await db.merge(updated_statistic)
        await db.commit()

    @staticmethod
    async def delete_all(db: AsyncSession):
        """
        Deletes all Statistic records from the database.

        Args:
            db (AsyncSession): The database session.
        """
        del_statistic = delete(Statistic)
        await db.execute(del_statistic)
        await db.commit()
