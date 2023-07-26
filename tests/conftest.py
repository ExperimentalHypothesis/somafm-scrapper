from unittest.mock import Mock, patch

import pytest

from src.playlist_parser import PlaylistParser


@pytest.fixture
def mocked_scrapper_over_midnight():
    with patch("src.playlist_parser.requests.get") as mocked_get:
        print("in patch mocked_scrapper")
        mocked_resp = Mock()
        with open("tests/mocked_data/mocked_page_over_midnight.txt") as f:
            mocked_resp.text = f.read()
            mocked_get.return_value = mocked_resp

        url = "https://somafm.com/dronezone/songhistory.html"
        scrapper = PlaylistParser(url)

    return scrapper


@pytest.fixture
def mocked_scrapper():
    with patch("src.playlist_parser.requests.get") as mocked_get:
        print("in patch mocked_scrapper")
        mocked_resp = Mock()
        with open("tests/mocked_data/mocked_page.txt") as f:
            mocked_resp.text = f.read()
            mocked_get.return_value = mocked_resp

        url = "https://somafm.com/dronezone/songhistory.html"
        scrapper = PlaylistParser(url)

    return scrapper
