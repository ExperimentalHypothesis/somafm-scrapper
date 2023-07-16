import pytest
from datetime import datetime
from src.playlist_parser import PlaylistParser

from tests import params_test_convert_time, params_test_last_before_midnight


@pytest.mark.parametrize("scraped_times", params_test_convert_time)
def test_convert_time(scraped_times):
    current_date = datetime.now().date()
    scrapped_time = scraped_times
    expected_datetime = datetime.combine(current_date, datetime.strptime(scrapped_time, "%H:%M:%S").time())
    assert PlaylistParser.convert_time(scraped_times) == expected_datetime


@pytest.mark.parametrize("scraped_times, output", params_test_last_before_midnight)
def test_last_before_midnight_is_none(scraped_times, output):
    assert PlaylistParser.last_before_midnight(scraped_times) == output
