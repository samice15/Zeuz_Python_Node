# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: deploy_request_message.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import deploy_info_message_pb2 as deploy__info__message__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1c\x64\x65ploy_request_message.proto\x12\tprotos.v1\x1a\x19\x64\x65ploy_info_message.proto\"L\n\rDeployRequest\x12\x0f\n\x07user_id\x18\x01 \x01(\x05\x12*\n\x0b\x64\x65ploy_info\x18\x02 \x01(\x0b\x32\x15.protos.v1.DeployInfoB\x07Z\x05pb/v1b\x06proto3')



_DEPLOYREQUEST = DESCRIPTOR.message_types_by_name['DeployRequest']
DeployRequest = _reflection.GeneratedProtocolMessageType('DeployRequest', (_message.Message,), {
  'DESCRIPTOR' : _DEPLOYREQUEST,
  '__module__' : 'deploy_request_message_pb2'
  # @@protoc_insertion_point(class_scope:protos.v1.DeployRequest)
  })
_sym_db.RegisterMessage(DeployRequest)

if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'Z\005pb/v1'
  _DEPLOYREQUEST._serialized_start=70
  _DEPLOYREQUEST._serialized_end=146
# @@protoc_insertion_point(module_scope)
