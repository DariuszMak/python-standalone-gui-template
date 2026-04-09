import logging

import pandas as pd

from weather.client import build_openmeteo_client
from weather.params import API_URL, build_request_params
from weather.parsers import parse_daily_dataframe, parse_hourly_dataframe

logger = logging.getLogger(__name__)


def fetch_weather_response(client, params: dict):
    """Fetch a raw API response from Open-Meteo and return the first location result."""
    responses = client.weather_api(API_URL, params=params)
    return responses[0]


def gather_data() -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Fetch 16-day hourly and daily weather forecast for the configured location.

    Returns:
        A (hourly_dataframe, daily_dataframe) tuple.
    """
    client = build_openmeteo_client()
    params = build_request_params()
    response = fetch_weather_response(client, params)

    utc_offset = response.UtcOffsetSeconds()

    hourly_df = parse_hourly_dataframe(response.Hourly(), utc_offset)
    daily_df = parse_daily_dataframe(response.Daily(), utc_offset)

    logger.info("hourly_dataframe: %s", hourly_df)
    logger.info("daily_dataframe: %s", daily_df)

    return hourly_df, daily_df
