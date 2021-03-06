from ..redis_cache import RedisCache
import pytest


class TestCache:

    @pytest.fixture()
    def cache(self):
        cache = RedisCache()
        cache.flushall()
        return cache

    def test_save_get_value(self, cache):
        translation = {"translatedText": "text Translated",
                       "input": "text"}

        cache.save_to_cache([translation], "en", "ru")

        test_value, tmp = cache.get_from_cache(["text"], "en", "ru")

        print(test_value)

        assert test_value["text"][0] == "text Translated"
        assert test_value["text"][1] == "en"

    def test_save_get_value_without_source(self, cache):
        translation = {"translatedText": "text Translated",
                       "detectedSourceLanguage": "en",
                       "input": "text"}

        cache.save_to_cache([translation], "", "ru")

        test_value, tmp = cache.get_from_cache(["text"], "", "ru")

        print(test_value)

        assert test_value["text"][0] == "text Translated"
        assert test_value["text"][1] == "en"
