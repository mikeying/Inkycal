"""
inkycal_agenda unittest
"""
import logging
import unittest

from inkycal.modules.inkycal_agenda import Agenda as Module
from inkycal.utils.inky_image import Inkyimage
from tests import Config

merge = Inkyimage.merge

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

sample_url = Config.SAMPLE_ICAL_URL

tests = [
    {
        "name": "Agenda",
        "config": {
            "size": [400, 200],
            "ical_urls": sample_url,
            "ical_files": None,
            "date_format": "ddd D MMM",
            "time_format": "HH:mm",
            "padding_x": 10,
            "padding_y": 10,
            "fontsize": 12,
            "language": "de"
        }
    },
    {
        "name": "Agenda",
        "config": {
            "size": [500, 800],
            "ical_urls": sample_url,
            "ical_files": None,
            "date_format": "DD.MMMM YYYY",
            "time_format": "HH:mm",
            "padding_x": 10,
            "padding_y": 10,
            "fontsize": 12,
            "language": "en"
        }
    },
    {
        "position": 1,
        "name": "Agenda",
        "config": {
            "size": [300, 800],
            "ical_urls": sample_url,
            "ical_files": None,
            "date_format": "ddd D MMM",
            "time_format": "HH:mm",
            "padding_x": 10,
            "padding_y": 10,
            "fontsize": 12,
            "language": "en"
        }
    },
    {
        "name": "Agenda (2 Columns)",
        "config": {
            "size": [800, 600],
            "ical_urls": sample_url,
            "ical_files": None,
            "date_format": "ddd D MMM",
            "time_format": "HH:mm",
            "padding_x": 10,
            "padding_y": 10,
            "fontsize": 12,
            "language": "en",
            "columns": 2
        }
    },
    {
        "name": "Agenda (Wrapping)",
        "config": {
            "size": [200, 600], # Narrow width to force wrapping
            "ical_urls": sample_url,
            "ical_files": None,
            "date_format": "ddd D MMM",
            "time_format": "HH:mm",
            "padding_x": 10,
            "padding_y": 10,
            "fontsize": 12,
            "language": "en",
            "columns": 1
        }
    },
]

invalid_tests = [
    {
        "name": "Agenda (0 Columns)",
        "config": {
            "size": [800, 600],
            "ical_urls": sample_url,
            "ical_files": None,
            "date_format": "ddd D MMM",
            "time_format": "HH:mm",
            "padding_x": 10,
            "padding_y": 10,
            "fontsize": 12,
            "language": "en",
            "columns": 0
        }
    },
    {
        "name": "Agenda (3 Columns)",
        "config": {
            "size": [800, 600],
            "ical_urls": sample_url,
            "ical_files": None,
            "date_format": "ddd D MMM",
            "time_format": "HH:mm",
            "padding_x": 10,
            "padding_y": 10,
            "fontsize": 12,
            "language": "en",
            "columns": 3
        }
    },
]


class TestAgenda(unittest.TestCase):

    def test_generate_image(self):
        for test in tests:
            logger.info(f'test {tests.index(test) + 1} generating image..')
            module = Module(test)
            im_black, im_colour = module.generate_image()
            logger.info('OK')
            if Config.USE_PREVIEW:
                merge(im_black, im_colour).show()

    def test_invalid_columns(self):
        for test in invalid_tests:
            logger.info(f'Testing invalid columns: {test["config"]["columns"]}')
            with self.assertRaises(ValueError):
                Module(test)
            logger.info('Caught expected ValueError')


class TestAgendaDynamicColumnSizing(unittest.TestCase):
    """Test dynamic time column sizing and maximized event title width across screen sizes."""

    def test_dynamic_sizing_with_events(self):
        from unittest.mock import patch, MagicMock
        import arrow

        now = arrow.now()
        mock_events = [
            {
                "begin": now.replace(hour=9, minute=30),
                "end": now.replace(hour=10, minute=30),
                "title": "Team Standup Meeting with Long Project Discussion",
            },
            {
                "begin": now.replace(hour=14, minute=0),
                "end": now.replace(hour=15, minute=0),
                "title": "One-on-One Sync",
            },
            {
                "begin": now.floor("day"),
                "end": now.ceil("day"),
                "title": "Company Holiday",
            },
        ]

        screen_sizes = [
            ([400, 300], 1, 14),
            ([528, 400], 2, 14),
            ([800, 600], 2, 18),
            ([984, 824], 2, 24),
            ([1200, 800], 2, 20),
        ]

        for size, columns, fontsize in screen_sizes:
            config = {
                "name": "Agenda",
                "config": {
                    "size": size,
                    "ical_urls": "https://example.com/calendar.ics",
                    "ical_files": None,
                    "date_format": "dddd MMMM D",
                    "time_format": "h:mm a",
                    "padding_x": 4,
                    "padding_y": 4,
                    "fontsize": fontsize,
                    "language": "en",
                    "columns": columns,
                }
            }

            with patch("inkycal.modules.inkycal_agenda.iCalendar") as mock_ical_class:
                mock_ical = MagicMock()
                mock_ical.get_events.return_value = list(mock_events)
                mock_ical.all_day.side_effect = lambda e: e["title"] == "Company Holiday"
                mock_ical_class.return_value = mock_ical

                module = Module(config)
                im_black, im_colour = module.generate_image()

                expected_w = size[0] - 2 * 4
                expected_h = size[1] - 2 * 4
                self.assertEqual(im_black.size, (expected_w, expected_h))
                self.assertEqual(im_colour.size, (expected_w, expected_h))
