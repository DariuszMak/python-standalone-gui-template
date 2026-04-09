import logging

import pandas as pd

from src.app.weather_forecast.client import build_openmeteo_client
from src.app.weather_forecast.params import API_URL, build_request_params
from src.app.weather_forecast.parsers import parse_daily_dataframe, parse_hourly_dataframe

logger = logging.getLogger(__name__)


def fetch_weather_response(client, params: dict):
    responses = client.weather_api(API_URL, params=params)
    return responses[0]


def gather_data() -> tuple[pd.DataFrame, pd.DataFrame]:
    client = build_openmeteo_client()
    params = build_request_params()
    response = fetch_weather_response(client, params)

    utc_offset = response.UtcOffsetSeconds()

    hourly_df = parse_hourly_dataframe(response.Hourly(), utc_offset)
    daily_df = parse_daily_dataframe(response.Daily(), utc_offset)

    logger.info("hourly_dataframe: %s", hourly_df)
    logger.info("daily_dataframe: %s", daily_df)

    return hourly_df, daily_df
