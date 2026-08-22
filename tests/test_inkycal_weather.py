"""
inkycal_weather unittest
"""
import logging
import unittest

from inkycal.modules.inkycal_weather import Weather as Module
from inkycal.utils.inky_image import Inkyimage
from tests import Config

merge = Inkyimage.merge

owm_api_key = Config.OPENWEATHERMAP_API_KEY
location = '2825297'

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

tests = [
    {
        "position": 1,
        "name": "Weather",
        "config": {
            "size": [500, 100],
            "api_key": owm_api_key,
            "location": location,
            "round_temperature": True,
            "round_windspeed": True,
            "forecast_interval": "daily",
            "units": "metric",
            "hour_format": "12",
            "use_beaufort": False,
            "padding_x": 10,
            "padding_y": 10,
            "fontsize": 12,
            "language": "de"
        }
    },
    {
        "position": 1,
        "name": "Weather",
        "config": {
            "size": [500, 150],
            "api_key": owm_api_key,
            "location": "2643123",
            "round_temperature": True,
            "round_windspeed": True,
            "forecast_interval": "daily",
            "units": "metric",
            "hour_format": "12",
            "use_beaufort": True,
            "padding_x": 10,
            "padding_y": 10,
            "fontsize": 12,
            "language": "en"
        }
    },
    {
        "position": 1,
        "name": "Weather",
        "config": {
            "size": [500, 200],
            "api_key": owm_api_key,
            "location": location,
            "round_temperature": False,
            "round_windspeed": True,
            "forecast_interval": "daily",
            "units": "metric",
            "hour_format": "12",
            "use_beaufort": True,
            "padding_x": 10,
            "padding_y": 10,
            "fontsize": 12,
            "language": "en"
        }
    },
    {
        "position": 1,
        "name": "Weather",
        "config": {
            "size": [500, 100],
            "api_key": owm_api_key,
            "location": location,
            "round_temperature": True,
            "round_windspeed": False,
            "forecast_interval": "daily",
            "units": "metric",
            "hour_format": "12",
            "use_beaufort": True,
            "padding_x": 10,
            "padding_y": 10,
            "fontsize": 12,
            "language": "en"
        }
    },
    {
        "position": 1,
        "name": "Weather",
        "config": {
            "size": [500, 150],
            "api_key": owm_api_key,
            "location": location,
            "round_temperature": True,
            "round_windspeed": True,
            "forecast_interval": "hourly",
            "units": "metric",
            "hour_format": "12",
            "use_beaufort": True,
            "padding_x": 10,
            "padding_y": 10,
            "fontsize": 12,
            "language": "en"
        }
    },
    {
        "position": 1,
        "name": "Weather",
        "config": {
            "size": [500, 150],
            "api_key": owm_api_key,
            "location": location,
            "round_temperature": True,
            "round_windspeed": True,
            "forecast_interval": "daily",
            "units": "imperial",
            "hour_format": "12",
            "use_beaufort": True,
            "padding_x": 10,
            "padding_y": 10,
            "fontsize": 12,
            "language": "en"
        }
    },
    {
        "position": 1,
        "name": "Weather",
        "config": {
            "size": [500, 100],
            "api_key": owm_api_key,
            "location": location,
            "round_temperature": True,
            "round_windspeed": True,
            "forecast_interval": "daily",
            "units": "metric",
            "hour_format": "24",
            "use_beaufort": True,
            "padding_x": 10,
            "padding_y": 10,
            "fontsize": 12,
            "language": "en"
        }
    },
    {
        "position": 1,
        "name": "Weather",
        "config": {
            "size": [500, 100],
            "api_key": owm_api_key,
            "location": location,
            "round_temperature": True,
            "round_windspeed": True,
            "forecast_interval": "daily",
            "units": "metric",
            "hour_format": "12",
            "use_beaufort": False,
            "padding_x": 10,
            "padding_y": 10,
            "fontsize": 12,
            "language": "en"
        }
    },
    {
        "position": 1,
        "name": "Weather",
        "config": {
            "size": [500, 150],
            "api_key": owm_api_key,
            "location": location,
            "round_temperature": True,
            "round_windspeed": True,
            "forecast_interval": "daily",
            "units": "imperial",
            "hour_format": "12",
            "use_beaufort": False,
            "show_today_high_and_low": True,
            "padding_x": 10,
            "padding_y": 10,
            "fontsize": 12,
            "language": "en"
        }
    },
    {
        "position": 1,
        "name": "Weather",
        "config": {
            "size": [500, 150],
            "api_key": owm_api_key,
            "location": location,
            "round_temperature": True,
            "round_windspeed": True,
            "forecast_interval": "daily",
            "units": "imperial",
            "hour_format": "12",
            "use_beaufort": False,
            "show_today_high_and_low": False,
            "show_location": True,
            "padding_x": 10,
            "padding_y": 10,
            "fontsize": 12,
            "language": "en"
        }
    },
]


class TestWeather(unittest.TestCase):

    @unittest.skipUnless(owm_api_key, "OpenWeatherMap API key not configured")
    def test_generate_image(self):
        for test in tests:
            logger.info(f'test {tests.index(test) + 1} generating image..')
            module = Module(test)
            im_black, im_colour = module.generate_image()
            logger.info('OK')
            if Config.USE_PREVIEW:
                merge(im_black, im_colour).show()


class TestWeatherMultiScreenSizes(unittest.TestCase):
    """Deterministic multi-screen size testing with mocked OpenWeatherMap responses."""

    def setUp(self):
        import arrow
        self.now = arrow.utcnow()
        self.mock_current = {
            "detailed_status": "clear sky",
            "weather_icon_name": "01d",
            "temp": 68.0,
            "temp_feels_like": 68.0,
            "min_temp": 55.0,
            "max_temp": 75.0,
            "humidity": 65,
            "wind": 10.0,
            "wind_gust": 10.0,
            "uvi": 5.0,
            "sunrise": self.now.datetime,
            "sunset": self.now.datetime,
            "location_name": "San Francisco",
        }
        self.mock_forecasts = [
            {
                "temp": 65.0 + i,
                "min_temp": 55.0,
                "max_temp": 75.0,
                "precip_3h_mm": 0.0,
                "wind": 10.0,
                "wind_gust": 10.0,
                "pressure": 1013,
                "humidity": 60,
                "precip_probability": 0.0,
                "icon": "01d",
                "datetime": self.now.shift(hours=+3 * i).datetime,
            }
            for i in range(8)
        ]

    def _mock_daily_forecast(self, day: int):
        return {
            "datetime": self.now.shift(days=+day).datetime,
            "icon": "01d",
            "temp_min": 52.0 + day,
            "temp_max": 74.0 + day,
            "precip_mm": 0.0,
        }

    def test_screen_sizes_and_settings_matrix(self):
        from unittest.mock import patch
        from inkycal.utils.openweathermap_wrapper import OpenWeatherMap

        screen_sizes = [
            [400, 100],   # Small / compact (4.2")
            [500, 100],   # Low-height (5.83")
            [528, 140],   # Standard compact (7.5")
            [500, 200],   # Medium / square aspect ratio (< 4)
            [600, 250],   # Tall aspect ratio
            [984, 160],   # Large / wide (12.48")
            [1200, 300],  # High resolution (9.7")
        ]

        configs = [
            {"show_location": True, "show_today_high_and_low": True, "forecast_interval": "daily", "units": "imperial"},
            {"show_location": True, "show_today_high_and_low": False, "forecast_interval": "hourly", "units": "imperial"},
            {"show_location": False, "show_today_high_and_low": True, "forecast_interval": "daily", "units": "metric"},
            {"show_location": True, "show_today_high_and_low": True, "forecast_interval": "hourly", "units": "metric"},
        ]

        with patch.object(OpenWeatherMap, "get_current_weather", return_value=self.mock_current), \
             patch.object(OpenWeatherMap, "get_weather_forecast", return_value=self.mock_forecasts), \
             patch.object(OpenWeatherMap, "get_forecast_for_day", side_effect=self._mock_daily_forecast), \
             patch("inkycal.modules.inkycal_weather.internet_available", return_value=True):

            for size in screen_sizes:
                for conf in configs:
                    full_config = {
                        "position": 1,
                        "name": "Weather",
                        "config": {
                            "size": size,
                            "api_key": "mock_api_key",
                            "location": "5391959",
                            "round_temperature": True,
                            "round_windspeed": True,
                            "hour_format": "12",
                            "use_beaufort": False,
                            "padding_x": 4,
                            "padding_y": 4,
                            "fontsize": 14,
                            "language": "en",
                            **conf,
                        }
                    }
                    module = Module(full_config)
                    im_black, im_colour = module.generate_image()

                    expected_w = size[0] - 2 * 4
                    expected_h = size[1] - 2 * 4
                    self.assertEqual(im_black.size, (expected_w, expected_h))
                    self.assertEqual(im_colour.size, (expected_w, expected_h))