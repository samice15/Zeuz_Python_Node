# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: execution_report_request_message.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import test_case_message_pb2 as test__case__message__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n&execution_report_request_message.proto\x12\tprotos.v1\x1a\x17test_case_message.proto\"P\n\x16\x45xecutionReportRequest\x12\x0e\n\x06run_id\x18\x01 \x01(\t\x12&\n\ttest_case\x18\x02 \x01(\x0b\x32\x13.protos.v1.TestCaseB\x07Z\x05pb/v1b\x06proto3')



_EXECUTIONREPORTREQUEST = DESCRIPTOR.message_types_by_name['ExecutionReportRequest']
ExecutionReportRequest = _reflection.GeneratedProtocolMessageType('ExecutionReportRequest', (_message.Message,), {
  'DESCRIPTOR' : _EXECUTIONREPORTREQUEST,
  '__module__' : 'execution_report_request_message_pb2'
  # @@protoc_insertion_point(class_scope:protos.v1.ExecutionReportRequest)
  })
_sym_db.RegisterMessage(ExecutionReportRequest)

if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'Z\005pb/v1'
  _EXECUTIONREPORTREQUEST._serialized_start=78
  _EXECUTIONREPORTREQUEST._serialized_end=158
# @@protoc_insertion_point(module_scope)
