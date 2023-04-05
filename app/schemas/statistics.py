from datetime import date

from app.models.statistics import fields
from pydantic import BaseModel, validator


class Statistic(BaseModel):
    date: date
    views: int = 0
    clicks: int = 0
    cost: float = 0

    @validator("date")
    def validate_date(cls, v):
        """
        Validates that the date is not in the future.

        Args:
            v (date): The date to validate.

        Raises:
            ValueError: If the date is in the future.

        Returns:
            date: The valid date.
        """
        today = date.today()
        if v > today:
            raise ValueError("date cannot be a future date")
        return v

    @validator("views", "clicks", "cost")
    def validate_number(cls, v):
        """
        Validates that the number is at least 0.

        Args:
            v (int): The number to validate.

        Raises:
            ValueError: If the number of views is less than 0.

        Returns:
            int: The valid number.
        """
        if v is not None:
            if v < 0:
                raise ValueError("views, clicks, cost must be at least 0")
        return v


class StatisticOutput(BaseModel):
    date: date
    views: int
    clicks: int
    cost: int
    cpc: float
    cpm: float

    class Config:
        orm_mode = True


class StatisticParams(BaseModel):
    from_date: date
    to_date: date
    order_by: str = "-date"

    @validator("from_date", "to_date")
    def validate_date(cls, v):
        """
        Validates that the date is not in the future.

        Args:
            v (date): The date to validate.

        Raises:
            ValueError: If the date is in the future.

        Returns:
            date: The valid date.
        """
        today = date.today()
        if v > today:
            raise ValueError("date cannot be a future date")
        return v

    @validator("order_by")
    def validate_order_by(cls, v):
        """
        Validates that the Statistic model has a field specified by order_by.

        Args:
            v (str): The order_by value to validate.

        Raises:
            ValueError: If the Statistic model has not field specified by order_by.

        Returns:
            str: The valid order_by
        """
        if v is not None:
            if v[1:] not in fields and v not in fields:
                raise ValueError("statistic model didn't have this field")
        return v
