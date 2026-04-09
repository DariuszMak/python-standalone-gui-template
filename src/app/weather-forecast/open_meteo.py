import logging

import openmeteo_requests
import pandas as pd
import requests_cache
from retry_requests import retry  # type: ignore

logger = logging.getLogger(__name__)


def gather_data() -> tuple[pd.DataFrame, pd.DataFrame]:
    cache_session = requests_cache.CachedSession(".cache", expire_after=3600)
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
    openmeteo = openmeteo_requests.Client(session=retry_session)

    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": 51.9727,
        "longitude": 17.5026,
        "daily": [
            "sunshine_duration",
            "uv_index_max",
            "apparent_temperature_max",
            "apparent_temperature_min",
            "sunrise",
            "sunset",
            "daylight_duration",
            "rain_sum",
            "temperature_2m_max",
            "temperature_2m_min",
        ],
        "hourly": [
            "temperature_2m",
            "cloud_cover",
            "precipitation",
            "apparent_temperature",
            "soil_temperature_6cm",
            "relative_humidity_2m",
            "surface_pressure",
            "wind_speed_10m",
            "wind_direction_10m",
            "wind_gusts_10m",
            "soil_moisture_0_to_1cm",
        ],
        "timezone": "Europe/Berlin",
        "forecast_days": 16,
    }
    responses = openmeteo.weather_api(url, params=params)

    response = responses[0]

    hourly = response.Hourly()
    hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
    hourly_cloud_cover = hourly.Variables(1).ValuesAsNumpy()
    hourly_precipitation = hourly.Variables(2).ValuesAsNumpy()
    hourly_apparent_temperature = hourly.Variables(3).ValuesAsNumpy()
    hourly_soil_temperature_6cm = hourly.Variables(4).ValuesAsNumpy()
    hourly_relative_humidity_2m = hourly.Variables(5).ValuesAsNumpy()
    hourly_surface_pressure = hourly.Variables(6).ValuesAsNumpy()
    hourly_wind_speed_10m = hourly.Variables(7).ValuesAsNumpy()
    hourly_wind_direction_10m = hourly.Variables(8).ValuesAsNumpy()
    hourly_wind_gusts_10m = hourly.Variables(9).ValuesAsNumpy()
    hourly_soil_moisture_0_to_1cm = hourly.Variables(10).ValuesAsNumpy()

    hourly_data = {
        "date": pd.date_range(
            start=pd.to_datetime(hourly.Time() + response.UtcOffsetSeconds(), unit="s", utc=True),
            end=pd.to_datetime(hourly.TimeEnd() + response.UtcOffsetSeconds(), unit="s", utc=True),
            freq=pd.Timedelta(seconds=hourly.Interval()),
            inclusive="left",
        )
    }

    hourly_data["temperature_2m"] = hourly_temperature_2m
    hourly_data["cloud_cover"] = hourly_cloud_cover
    hourly_data["precipitation"] = hourly_precipitation
    hourly_data["apparent_temperature"] = hourly_apparent_temperature
    hourly_data["soil_temperature_6cm"] = hourly_soil_temperature_6cm
    hourly_data["relative_humidity_2m"] = hourly_relative_humidity_2m
    hourly_data["surface_pressure"] = hourly_surface_pressure
    hourly_data["wind_speed_10m"] = hourly_wind_speed_10m
    hourly_data["wind_direction_10m"] = hourly_wind_direction_10m
    hourly_data["wind_gusts_10m"] = hourly_wind_gusts_10m
    hourly_data["soil_moisture_0_to_1cm"] = hourly_soil_moisture_0_to_1cm

    hourly_dataframe = pd.DataFrame(data=hourly_data)

    daily = response.Daily()
    daily_sunshine_duration = daily.Variables(0).ValuesAsNumpy()
    daily_uv_index_max = daily.Variables(1).ValuesAsNumpy()
    daily_apparent_temperature_max = daily.Variables(2).ValuesAsNumpy()
    daily_apparent_temperature_min = daily.Variables(3).ValuesAsNumpy()
    daily_sunrise = daily.Variables(4).ValuesInt64AsNumpy()
    daily_sunset = daily.Variables(5).ValuesInt64AsNumpy()
    daily_daylight_duration = daily.Variables(6).ValuesAsNumpy()
    daily_rain_sum = daily.Variables(7).ValuesAsNumpy()
    daily_temperature_2m_max = daily.Variables(8).ValuesAsNumpy()
    daily_temperature_2m_min = daily.Variables(9).ValuesAsNumpy()

    daily_data = {
        "date": pd.date_range(
            start=pd.to_datetime(daily.Time() + response.UtcOffsetSeconds(), unit="s", utc=True),
            end=pd.to_datetime(daily.TimeEnd() + response.UtcOffsetSeconds(), unit="s", utc=True),
            freq=pd.Timedelta(seconds=daily.Interval()),
            inclusive="left",
        )
    }

    daily_data["sunshine_duration"] = daily_sunshine_duration
    daily_data["uv_index_max"] = daily_uv_index_max
    daily_data["apparent_temperature_max"] = daily_apparent_temperature_max
    daily_data["apparent_temperature_min"] = daily_apparent_temperature_min
    daily_data["sunrise"] = daily_sunrise
    daily_data["sunset"] = daily_sunset
    daily_data["daylight_duration"] = daily_daylight_duration
    daily_data["rain_sum"] = daily_rain_sum
    daily_data["temperature_2m_max"] = daily_temperature_2m_max
    daily_data["temperature_2m_min"] = daily_temperature_2m_min

    daily_dataframe = pd.DataFrame(data=daily_data)

    logger.info("hourly_dataframe: %s", hourly_dataframe)
    logger.info("daily_dataframe: %s", daily_dataframe)

    return hourly_dataframe, daily_dataframe
