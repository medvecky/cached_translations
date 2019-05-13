# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

import cached_translation_pb2 as cached__translation__pb2


class CachedTranslationStub(object):
  # missing associated documentation comment in .proto file
  pass

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.GetTranslation = channel.unary_unary(
        '/CachedTranslation/GetTranslation',
        request_serializer=cached__translation__pb2.TranslationRequest.SerializeToString,
        response_deserializer=cached__translation__pb2.TranslationReply.FromString,
        )
    self.GetTranslationWithSource = channel.unary_unary(
        '/CachedTranslation/GetTranslationWithSource',
        request_serializer=cached__translation__pb2.TranslationWithSourceRequest.SerializeToString,
        response_deserializer=cached__translation__pb2.TranslationWithSourceReply.FromString,
        )


class CachedTranslationServicer(object):
  # missing associated documentation comment in .proto file
  pass

  def GetTranslation(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def GetTranslationWithSource(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_CachedTranslationServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'GetTranslation': grpc.unary_unary_rpc_method_handler(
          servicer.GetTranslation,
          request_deserializer=cached__translation__pb2.TranslationRequest.FromString,
          response_serializer=cached__translation__pb2.TranslationReply.SerializeToString,
      ),
      'GetTranslationWithSource': grpc.unary_unary_rpc_method_handler(
          servicer.GetTranslationWithSource,
          request_deserializer=cached__translation__pb2.TranslationWithSourceRequest.FromString,
          response_serializer=cached__translation__pb2.TranslationWithSourceReply.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'CachedTranslation', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))
