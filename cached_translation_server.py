from concurrent import futures
import time
import grpc

from collections import namedtuple

from google_translation import GoogleTranslation
from redis_cache import RedisCache

import cached_translation_pb2
import cached_translation_pb2_grpc
import logging

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

TranslationRequest = namedtuple("TranslationRequest", "text targetLanguage sourceLanguage")


def find_translation(translations, text):
    if text in translations:
        tmp = translations[text]
        translation = {"translatedText": tmp[0],
                       "detectedSourceLanguage": tmp[1],
                       "input": text}
        return translation
    return False


class CachedTranslation(cached_translation_pb2_grpc.CachedTranslationServicer):

    def __init__(self):
        self.cloud_translation = GoogleTranslation()
        self.cache = RedisCache()
        self.bad_translation = {"translatedText": "",
                                "detectedSourceLanguage": "",
                                "input": "BAD ARGUMENT"}

    def GetTranslations(self, request, context):

        cached_translations, not_translated_texts = self.cache.get_from_cache(
            request.texts,
            request.sourceLanguage,
            request.targetLanguage)

        cloud_translations = self.get_cloud_translations_and_save_to_cache(request, not_translated_texts)

        result_translations = self.merge_translations(request, cached_translations, cloud_translations)

        return cached_translation_pb2.TranslationReply(translations=result_translations)

    def get_cloud_translations_and_save_to_cache(self, request, not_translated_texts):

        translation_request = TranslationRequest(
            text=[],
            targetLanguage=request.targetLanguage,
            sourceLanguage=request.sourceLanguage)

        translation_request.text.extend(not_translated_texts)

        if len(translation_request.text):
            cloud_translations = self.handle_request_to_cloud(request, translation_request)
        else:
            cloud_translations = []

        return cloud_translations

    def handle_request_to_cloud(self, request, translation_request):
        cloud_translations = {}
        try:
            cloud_responses = self.cloud_translation.get_translation(translation_request)
            self.cache.save_to_cache(cloud_responses, request.sourceLanguage, request.targetLanguage)
            for cloud_response in cloud_responses:
                if request.sourceLanguage:
                    cloud_translations[cloud_response["input"]] = (cloud_response["translatedText"], "")
                else:
                    cloud_translations[cloud_response["input"]] = (cloud_response["translatedText"],
                                                                   cloud_response["detectedSourceLanguage"])
        except:
            cloud_translations[self.bad_translation["input"]] = ("", "")

        return cloud_translations

    def merge_translations(self, request, cached_translations, cloud_translations):

        result_translations = []

        for text in request.texts:
            translation = find_translation(cached_translations, text)
            if translation:
                result_translations.append(translation)
                continue
            result_translations.append(find_translation(cloud_translations, text))

        if not len(result_translations) or not result_translations[0]:
            result_translations = [self.bad_translation]

        return result_translations


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    cached_translation_pb2_grpc.add_CachedTranslationServicer_to_server(CachedTranslation(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    logging.basicConfig()
    serve()
