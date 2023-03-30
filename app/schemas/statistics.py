from datetime import date
from typing import Optional

from app.models.statistics import fields
from pydantic import BaseModel, validator


class Statistic(BaseModel):
    date: date
    views: Optional[int]
    clicks: Optional[int]
    cost: Optional[float]

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
    sort_by: Optional[str]

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

    @validator("sort_by")
    def validate_sort_by(cls, v):
        """
        Validates that the Statistic model has a field specified by sort_by.

        Args:
            v (str): The sort_by value to validate.

        Raises:
            ValueError: If the Statistic model has not field specified by sort_by.

        Returns:
            str: The valid sort_by
        """
        if v is not None:
            if v[0] == "-":
                v = v[1:]
            print(v)
            if v not in fields:
                raise ValueError("statistic model didn't have this field")
        return v
