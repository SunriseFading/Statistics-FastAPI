from dataclasses import dataclass
from datetime import date


@dataclass
class Urls:
    create_statistic = "/statistic/create/"
    get_all_statistics = "/statistic/get_all/?from_date=2023-03-25&to_date=2023-03-30"
    delete_all_statistics = "/statistic/delete_all/"


urls = Urls()


test_statistic = {
    "date": "2023-03-30",
    "views": 1000,
    "clicks": 100,
    "cost": 1000,
}
