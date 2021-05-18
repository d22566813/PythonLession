# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: track.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='track.proto',
  package='',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x0btrack.proto\"^\n\x0cTrackRequest\x12\r\n\x05image\x18\x01 \x01(\x0c\x12\r\n\x05label\x18\x02 \x03(\t\x12\x13\n\x0b\x64\x65tect_type\x18\x03 \x01(\t\x12\x1b\n\x0bpoint_array\x18\x04 \x03(\x0b\x32\x06.Point\"\x1d\n\x05Point\x12\t\n\x01x\x18\x01 \x01(\x03\x12\t\n\x01y\x18\x02 \x01(\x03\"(\n\rTrackResponse\x12\x17\n\x0f\x61lgorithm_image\x18\x01 \x01(\x0c\x32\x31\n\x05Track\x12(\n\x05Track\x12\r.TrackRequest\x1a\x0e.TrackResponse\"\x00\x62\x06proto3'
)




_TRACKREQUEST = _descriptor.Descriptor(
  name='TrackRequest',
  full_name='TrackRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='image', full_name='TrackRequest.image', index=0,
      number=1, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='label', full_name='TrackRequest.label', index=1,
      number=2, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='detect_type', full_name='TrackRequest.detect_type', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='point_array', full_name='TrackRequest.point_array', index=3,
      number=4, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=15,
  serialized_end=109,
)


_POINT = _descriptor.Descriptor(
  name='Point',
  full_name='Point',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='x', full_name='Point.x', index=0,
      number=1, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='y', full_name='Point.y', index=1,
      number=2, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=111,
  serialized_end=140,
)


_TRACKRESPONSE = _descriptor.Descriptor(
  name='TrackResponse',
  full_name='TrackResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='algorithm_image', full_name='TrackResponse.algorithm_image', index=0,
      number=1, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=142,
  serialized_end=182,
)

_TRACKREQUEST.fields_by_name['point_array'].message_type = _POINT
DESCRIPTOR.message_types_by_name['TrackRequest'] = _TRACKREQUEST
DESCRIPTOR.message_types_by_name['Point'] = _POINT
DESCRIPTOR.message_types_by_name['TrackResponse'] = _TRACKRESPONSE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

TrackRequest = _reflection.GeneratedProtocolMessageType('TrackRequest', (_message.Message,), {
  'DESCRIPTOR' : _TRACKREQUEST,
  '__module__' : 'track_pb2'
  # @@protoc_insertion_point(class_scope:TrackRequest)
  })
_sym_db.RegisterMessage(TrackRequest)

Point = _reflection.GeneratedProtocolMessageType('Point', (_message.Message,), {
  'DESCRIPTOR' : _POINT,
  '__module__' : 'track_pb2'
  # @@protoc_insertion_point(class_scope:Point)
  })
_sym_db.RegisterMessage(Point)

TrackResponse = _reflection.GeneratedProtocolMessageType('TrackResponse', (_message.Message,), {
  'DESCRIPTOR' : _TRACKRESPONSE,
  '__module__' : 'track_pb2'
  # @@protoc_insertion_point(class_scope:TrackResponse)
  })
_sym_db.RegisterMessage(TrackResponse)



_TRACK = _descriptor.ServiceDescriptor(
  name='Track',
  full_name='Track',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=184,
  serialized_end=233,
  methods=[
  _descriptor.MethodDescriptor(
    name='Track',
    full_name='Track.Track',
    index=0,
    containing_service=None,
    input_type=_TRACKREQUEST,
    output_type=_TRACKRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_TRACK)

DESCRIPTOR.services_by_name['Track'] = _TRACK

# @@protoc_insertion_point(module_scope)
