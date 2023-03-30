from dataclasses import dataclass


@dataclass
class Messages:
    STATISTIC_CREATED = "Statistic created"
    STATISTICS_DELETED = "Statistics deleted"
    STATISTIC_UPDATED = "Statistic updated"


messages = Messages()
