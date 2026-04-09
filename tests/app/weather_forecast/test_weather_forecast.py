from unittest.mock import MagicMock, patch

import numpy as np
import pandas as pd

from src.app.weather_forecast.client import build_openmeteo_client
from src.app.weather_forecast.gather import fetch_weather_response, gather_data
from src.app.weather_forecast.params import FORECAST_DAYS, LATITUDE, LONGITUDE, TIMEZONE, build_request_params
from src.app.weather_forecast.parsers import parse_daily_dataframe, parse_hourly_dataframe

HOURLY_COLUMNS = [
    "date",
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
]

DAILY_COLUMNS = [
    "date",
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
]

N_HOURS = 24
N_DAYS = 3
UTC_OFFSET = 3600

START_TS = int(pd.Timestamp("2024-01-01", tz="UTC").timestamp())
END_TS_HOURLY = START_TS + N_HOURS * 3600
END_TS_DAILY = START_TS + N_DAYS * 86400


def _make_variables_mock(values_list: list[np.ndarray], *, integer: bool = False) -> MagicMock:
    var_mocks = []
    for arr in values_list:
        v = MagicMock()
        if integer:
            v.ValuesInt64AsNumpy.return_value = arr
        else:
            v.ValuesAsNumpy.return_value = arr
        var_mocks.append(v)

    container = MagicMock()
    container.Variables.side_effect = lambda i: var_mocks[i]
    return container


def _make_hourly_mock(n: int = N_HOURS) -> MagicMock:
    arrays = [np.random.rand(n).astype(np.float32) for _ in range(11)]
    mock = _make_variables_mock(arrays)
    mock.Time.return_value = START_TS - UTC_OFFSET
    mock.TimeEnd.return_value = END_TS_HOURLY - UTC_OFFSET
    mock.Interval.return_value = 3600
    return mock


def _make_daily_mock(n: int = N_DAYS) -> MagicMock:
    float_arrays = [np.random.rand(n).astype(np.float32) for _ in range(8)]
    int_arrays = [np.random.randint(0, 86400, n, dtype=np.int64) for _ in range(2)]

    all_arrays = float_arrays[:4] + int_arrays + float_arrays[4:]

    mock = MagicMock()

    var_mocks = []
    for idx, arr in enumerate(all_arrays):
        v = MagicMock()
        if idx in (4, 5):
            v.ValuesInt64AsNumpy.return_value = arr
        else:
            v.ValuesAsNumpy.return_value = arr
        var_mocks.append(v)

    mock.Variables.side_effect = lambda i: var_mocks[i]
    mock.Time.return_value = START_TS - UTC_OFFSET
    mock.TimeEnd.return_value = END_TS_DAILY - UTC_OFFSET
    mock.Interval.return_value = 86400
    return mock


class TestBuildRequestParams:
    def test_returns_required_keys(self):

        params = build_request_params()
        for key in ("latitude", "longitude", "daily", "hourly", "timezone", "forecast_days"):
            assert key in params

    def test_default_coordinates(self):

        params = build_request_params()
        assert params["latitude"] == LATITUDE
        assert params["longitude"] == LONGITUDE

    def test_custom_coordinates(self):

        params = build_request_params(latitude=52.0, longitude=18.0)
        assert params["latitude"] == 52.0
        assert params["longitude"] == 18.0

    def test_daily_and_hourly_are_lists(self):

        params = build_request_params()
        assert isinstance(params["daily"], list)
        assert isinstance(params["hourly"], list)
        assert len(params["daily"]) > 0
        assert len(params["hourly"]) > 0

    def test_forecast_days_default(self):

        assert build_request_params()["forecast_days"] == FORECAST_DAYS

    def test_custom_forecast_days(self):

        assert build_request_params(forecast_days=7)["forecast_days"] == 7

    def test_timezone_default(self):

        assert build_request_params()["timezone"] == TIMEZONE


class TestBuildOpenMeteoClient:
    @patch("src.app.weather_forecast.client.openmeteo_requests.Client")
    @patch("src.app.weather_forecast.client.retry")
    @patch("src.app.weather_forecast.client.requests_cache.CachedSession")
    def test_returns_client(self, mock_session, mock_retry, mock_client_cls):

        client = build_openmeteo_client()
        mock_client_cls.assert_called_once()
        assert client is mock_client_cls.return_value

    @patch("src.app.weather_forecast.client.openmeteo_requests.Client")
    @patch("src.app.weather_forecast.client.retry")
    @patch("src.app.weather_forecast.client.requests_cache.CachedSession")
    def test_cache_params_forwarded(self, mock_session, mock_retry, mock_client_cls):

        build_openmeteo_client(cache_name="custom", expire_after=999)
        mock_session.assert_called_once_with("custom", expire_after=999)

    @patch("src.app.weather_forecast.client.openmeteo_requests.Client")
    @patch("src.app.weather_forecast.client.retry")
    @patch("src.app.weather_forecast.client.requests_cache.CachedSession")
    def test_retry_params_forwarded(self, mock_session, mock_retry, mock_client_cls):

        build_openmeteo_client(retries=3, backoff_factor=0.5)
        mock_retry.assert_called_once_with(mock_session.return_value, retries=3, backoff_factor=0.5)


class TestParseHourlyDataframe:
    def test_returns_dataframe(self):

        df = parse_hourly_dataframe(_make_hourly_mock(), UTC_OFFSET)
        assert isinstance(df, pd.DataFrame)

    def test_has_correct_columns(self):

        df = parse_hourly_dataframe(_make_hourly_mock(), UTC_OFFSET)
        assert list(df.columns) == HOURLY_COLUMNS

    def test_row_count_matches_hours(self):

        df = parse_hourly_dataframe(_make_hourly_mock(N_HOURS), UTC_OFFSET)
        assert len(df) == N_HOURS

    def test_date_column_is_timezone_aware(self):

        df = parse_hourly_dataframe(_make_hourly_mock(), UTC_OFFSET)
        assert df["date"].dt.tz is not None

    def test_no_null_values(self):

        df = parse_hourly_dataframe(_make_hourly_mock(), UTC_OFFSET)
        assert not df.isnull().any().any()

    def test_date_interval_is_one_hour(self):

        df = parse_hourly_dataframe(_make_hourly_mock(), UTC_OFFSET)
        diffs = df["date"].diff().dropna().unique()
        assert len(diffs) == 1
        assert diffs[0] == pd.Timedelta(hours=1)


class TestParseDailyDataframe:
    def test_returns_dataframe(self):

        df = parse_daily_dataframe(_make_daily_mock(), UTC_OFFSET)
        assert isinstance(df, pd.DataFrame)

    def test_has_correct_columns(self):

        df = parse_daily_dataframe(_make_daily_mock(), UTC_OFFSET)
        assert list(df.columns) == DAILY_COLUMNS

    def test_row_count_matches_days(self):

        df = parse_daily_dataframe(_make_daily_mock(N_DAYS), UTC_OFFSET)
        assert len(df) == N_DAYS

    def test_date_column_is_timezone_aware(self):

        df = parse_daily_dataframe(_make_daily_mock(), UTC_OFFSET)
        assert df["date"].dt.tz is not None

    def test_no_null_values(self):

        df = parse_daily_dataframe(_make_daily_mock(), UTC_OFFSET)
        assert not df.isnull().any().any()

    def test_date_interval_is_one_day(self):

        df = parse_daily_dataframe(_make_daily_mock(), UTC_OFFSET)
        diffs = df["date"].diff().dropna().unique()
        assert len(diffs) == 1
        assert diffs[0] == pd.Timedelta(days=1)

    def test_sunrise_sunset_are_integer(self):

        df = parse_daily_dataframe(_make_daily_mock(), UTC_OFFSET)
        assert pd.api.types.is_integer_dtype(df["sunrise"])
        assert pd.api.types.is_integer_dtype(df["sunset"])


class TestFetchWeatherResponse:
    def test_returns_first_element(self):

        sentinel = object()
        mock_client = MagicMock()
        mock_client.weather_api.return_value = [sentinel]
        result = fetch_weather_response(mock_client, {})
        assert result is sentinel

    def test_passes_params_to_api(self):

        mock_client = MagicMock()
        mock_client.weather_api.return_value = [MagicMock()]
        params = {"foo": "bar"}
        fetch_weather_response(mock_client, params)
        mock_client.weather_api.assert_called_once()
        _, call_kwargs = mock_client.weather_api.call_args

        call_args_pos = mock_client.weather_api.call_args[0]
        assert params in call_args_pos or call_kwargs.get("params") == params


class TestGatherData:
    def _make_response_mock(self) -> MagicMock:
        response = MagicMock()
        response.UtcOffsetSeconds.return_value = UTC_OFFSET
        response.Hourly.return_value = _make_hourly_mock()
        response.Daily.return_value = _make_daily_mock()
        return response

    @patch("src.app.weather_forecast.gather.build_openmeteo_client")
    @patch("src.app.weather_forecast.gather.build_request_params")
    @patch("src.app.weather_forecast.gather.fetch_weather_response")
    def test_returns_two_dataframes(self, mock_fetch, mock_params, mock_client):

        mock_fetch.return_value = self._make_response_mock()
        hourly_df, daily_df = gather_data()
        assert isinstance(hourly_df, pd.DataFrame)
        assert isinstance(daily_df, pd.DataFrame)

    @patch("src.app.weather_forecast.gather.build_openmeteo_client")
    @patch("src.app.weather_forecast.gather.build_request_params")
    @patch("src.app.weather_forecast.gather.fetch_weather_response")
    def test_hourly_has_expected_columns(self, mock_fetch, mock_params, mock_client):

        mock_fetch.return_value = self._make_response_mock()
        hourly_df, _ = gather_data()
        for col in HOURLY_COLUMNS:
            assert col in hourly_df.columns

    @patch("src.app.weather_forecast.gather.build_openmeteo_client")
    @patch("src.app.weather_forecast.gather.build_request_params")
    @patch("src.app.weather_forecast.gather.fetch_weather_response")
    def test_daily_has_expected_columns(self, mock_fetch, mock_params, mock_client):

        mock_fetch.return_value = self._make_response_mock()
        _, daily_df = gather_data()
        for col in DAILY_COLUMNS:
            assert col in daily_df.columns

    @patch("src.app.weather_forecast.gather.build_openmeteo_client")
    @patch("src.app.weather_forecast.gather.build_request_params")
    @patch("src.app.weather_forecast.gather.fetch_weather_response")
    def test_uses_utc_offset_from_response(self, mock_fetch, mock_params, mock_client):

        response = self._make_response_mock()
        mock_fetch.return_value = response
        gather_data()
        response.UtcOffsetSeconds.assert_called_once()
