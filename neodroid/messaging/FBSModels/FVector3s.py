# automatically generated by the FlatBuffers compiler, do not modify

# namespace: FBS

import flatbuffers


class FVector3s(object):
  __slots__ = ['_tab']

  @classmethod
  def GetRootAsFVector3s(cls, buf, offset):
    n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, offset)
    x = FVector3s()
    x.Init(buf, n + offset)
    return x

  # FVector3s
  def Init(self, buf, pos):
    self._tab = flatbuffers.table.Table(buf, pos)

  # FVector3s
  def Values(self, j):
    o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
    if o != 0:
      x = self._tab.Vector(o)
      x += flatbuffers.number_types.UOffsetTFlags.py_type(j) * 24
      from .FVector3 import FVector3
      obj = FVector3()
      obj.Init(self._tab.Bytes, x)
      return obj
    return None

  # FVector3s
  def ValuesLength(self):
    o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
    if o != 0:
      return self._tab.VectorLen(o)
    return 0


def FVector3sStart(builder): builder.StartObject(1)


def FVector3sAddValues(builder, values): builder.PrependUOffsetTRelativeSlot(0,
                                                                             flatbuffers.number_types.UOffsetTFlags.py_type(
                                                                               values), 0)


def FVector3sStartValuesVector(builder, numElems): return builder.StartVector(24, numElems, 8)


def FVector3sEnd(builder): return builder.EndObject()
