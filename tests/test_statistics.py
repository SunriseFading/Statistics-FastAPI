import pytest
from fastapi import status

from tests.settings import test_statistic, urls


class TestProducts:
    @pytest.mark.asyncio
    async def test_create_product(self, client):
        response = client.post(urls.create_statistic, json=test_statistic)
        assert response.status_code == status.HTTP_201_CREATED

        response = client.get(urls.get_all_statistics)
        assert response.status_code == status.HTTP_200_OK
        result = response.json()[0]
        assert result.get("date") == test_statistic.get("date")
        assert result.get("views") == test_statistic.get("views")
        assert result.get("clicks") == test_statistic.get("clicks")
        assert result.get("cost") == test_statistic.get("cost")