import responses
import pytest 
from src.guardian import get_guardian_article

API_KEY = "523c0511-988f-42cb-a5e5-79790a206bd3"

@responses.activate
def test_retrieve_guardian_aritcle():
    mock_response = {"response": {
            "results": [
                {
                    "webPublicationDate": "2025-04-11T04:52:41Z",
                    "webTitle": "Dutton tight-lipped over how many voluntary redundancies would be offered in public service cuts plan",
                    "webUrl": "https://www.theguardian.com/some-article-url"
                }
            ]
        }
    }
    responses.add(
        responses.GET,
        "https://content.guardianapis.com/search",
        json=mock_response,
        status=200
    )

    articles = get_guardian_article("climate", api_key=API_KEY)

    assert len(articles) == 1
    assert articles[0]['webTitle'] == "Dutton tight-lipped over how many voluntary redundancies would be offered in public service cuts plan"
    assert articles[0]['webUrl'] == "https://www.theguardian.com/some-article-url"

@responses.activate
def test_get_guardian_article_not_found():
    responses.add(
        responses.GET,
        "https://content.guardianapis.com/search",
        status=404,
        body="Not Found"
    )

    try:
        articles = get_guardian_article("climate", api_key=API_KEY)

        assert False, "Expected an exception but got results"
    except Exception as e:
        assert str(e) == "API returned 404: Not Found"


@responses.activate
def test_get_guardian_article_missing_api_key():
    responses.add(
        responses.GET,
        "https://content.guardianapis.com/search",
        status=400,
        body="API key missing"
    )

    try:
        articles = get_guardian_article("climate")
        assert False, "Expected an exception but got results"
    except Exception as e:
        assert str(e) == "API key missing"
