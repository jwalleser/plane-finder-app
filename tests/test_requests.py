import requests


def test_request_get_trade_a_plane_home():
    response = requests.get("https://www.trade-a-plane.com")
    html = response.text
    assert len(html) > 0
    assert html.lower().startswith("<!doctype html>")
