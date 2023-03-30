import uuid

from app.database import Base
from sqlalchemy import Column, Date, Float, Integer
from sqlalchemy_utils import UUIDType


class Statistic(Base):
    __tablename__ = "statistics"

    id = Column(
        UUIDType(binary=False), primary_key=True, index=True, default=uuid.uuid4
    )
    date = Column(Date, unique=True, index=True)
    views = Column(Integer, default=0)
    clicks = Column(Integer, default=0)
    cost = Column(Float, default=0)
    cpc = Column(Float, nullable=True)
    cpm = Column(Float, nullable=True)

    def __init__(self, *args, **kwargs):
        """
        Initializes a new instance of the Statistic model.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        """
        super().__init__(*args, **kwargs)
        self.cpc = self.cost_per_clicks
        self.cpm = self.cost_per_views

    @property
    def cost_per_clicks(self) -> float:
        """
        Calculates the cost per click.

        Returns:
            float: The cost per click value.
        """
        return self.cost / self.clicks if self.cost and self.clicks else None

    @property
    def cost_per_views(self) -> float:
        """
        Calculates the cost per thousand views.

        Returns:
            float: The cost per thousand views value.
        """
        return ((self.cost / self.views) * 1000) if self.cost and self.views else None


fields = [column.name for column in Statistic.__table__.columns if column.name != "id"]
