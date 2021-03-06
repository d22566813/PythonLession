# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import track_pb2 as track__pb2


class TrackStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Track = channel.unary_unary(
                '/Track/Track',
                request_serializer=track__pb2.TrackRequest.SerializeToString,
                response_deserializer=track__pb2.TrackResponse.FromString,
                )


class TrackServicer(object):
    """Missing associated documentation comment in .proto file."""

    def Track(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_TrackServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'Track': grpc.unary_unary_rpc_method_handler(
                    servicer.Track,
                    request_deserializer=track__pb2.TrackRequest.FromString,
                    response_serializer=track__pb2.TrackResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'Track', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Track(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def Track(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Track/Track',
            track__pb2.TrackRequest.SerializeToString,
            track__pb2.TrackResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
