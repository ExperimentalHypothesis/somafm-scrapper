from unittest.mock import Mock, patch

import pytest
from datetime import datetime, date

import pytz
from bs4 import BeautifulSoup

from src.playlist_parser import PlaylistParser

from tests import params_test_convert_time, params_test_last_before_midnight, params_test_delete_break_station


def test_init():
    with patch("src.playlist_parser.requests.get") as mocked_get:
        mocked_resp = Mock()
        mocked_resp.text = "<html>..</html>"
        mocked_get.return_value = mocked_resp

        url = "https://somafm.com/dronezone/songhistory.html"
        scrapper = PlaylistParser(url)

    assert scrapper.page is not None
    assert isinstance(scrapper.soup, BeautifulSoup)
    assert scrapper.parsed == []


def test_artists_property(mocked_scrapper_over_midnight):
    artists = mocked_scrapper_over_midnight.artists
    assert isinstance(artists, list)
    assert artists[0] == "The Green Kingdom"
    assert artists[1] == "Blue Is Nine"
    assert artists[len(artists) - 1] == "jarguna"


def test_songs_property(mocked_scrapper_over_midnight):
    songs = mocked_scrapper_over_midnight.songs
    assert isinstance(songs, list)
    print(songs)
    assert songs[0] == "Atmosphere 1"
    assert songs[1] == "Isle Of Skye"
    assert songs[len(songs) - 1] == "Tricks in the Clouds"


def test_albums_property(mocked_scrapper_over_midnight):
    albums = mocked_scrapper_over_midnight.albums
    assert isinstance(albums, list)
    assert albums[0] == "Solaria"
    assert albums[1] == "A Pool Appears"
    assert albums[len(albums) - 1] == "Pareidolia"


def test_played_at_property(mocked_scrapper_over_midnight, mocked_scrapper):
    played_at = mocked_scrapper_over_midnight.played_at
    assert isinstance(played_at, list)
    assert played_at[0] == datetime(2023, 7, 26, 2, 28, 9)
    assert played_at[1] == datetime(2023, 7, 26, 2, 23, 14)
    assert played_at[len(played_at) - 1] == datetime(2023, 7, 25, 23, 56, 34)

    played_at = mocked_scrapper.played_at
    assert isinstance(played_at, list)
    assert played_at[0] == datetime(2023, 7, 26, 11, 47, 31)
    assert played_at[len(played_at) - 1] == datetime(2023, 7, 26, 9, 31, 48)


def test_url_property(mocked_scrapper_over_midnight):
    urls = mocked_scrapper_over_midnight.urls
    assert isinstance(urls, list)
    assert urls[0] == "/buy/multibuy.cgi?mode=amazon&title=Atmosphere%201&album=Solaria&artist=The%20Green%20Kingdom"
    assert urls[1] == "https://blueisnine.bandcamp.com"
    assert urls[len(urls) - 1] == "/buy/multibuy.cgi?mode=amazon&title=Tricks%20in%20the%20Clouds&album=Pareidolia&artist=jarguna"


def test_channel_property(mocked_scrapper_over_midnight):
    assert "Drone Zone" == mocked_scrapper_over_midnight.channel


@pytest.mark.parametrize("scraped_times", params_test_convert_time)
def test_convert_str_to_datetime(scraped_times):
    current_date = datetime.now().date()
    scrapped_time = scraped_times
    expected_datetime = datetime.combine(current_date, datetime.strptime(scrapped_time, "%H:%M:%S").time())

    assert PlaylistParser.convert_str_to_datetime(scraped_times) == expected_datetime


@pytest.mark.parametrize("scraped_times, output", params_test_last_before_midnight)
def test_last_before_midnight_is_none(scraped_times, output):
    assert PlaylistParser.last_before_midnight(scraped_times) == output


#
@pytest.mark.parametrize("played_at_in, artists_in, played_at_out, artists_out", params_test_delete_break_station)
def test_delete_break_station(played_at_in, artists_in, played_at_out, artists_out):
    PlaylistParser.delete_break_station(played_at_in, artists_in)

    assert played_at_in == played_at_out
    assert artists_in == artists_out


def test_get_current_date_in_la_timezone():
    utc_now = datetime.utcnow()
    given = PlaylistParser.get_current_date_in_la_timezone()
    expected = utc_now.replace(tzinfo=pytz.utc).astimezone(pytz.timezone("America/Los_Angeles")).date()

    assert given == expected
    assert isinstance(given, date)
    assert not isinstance(given, datetime)
