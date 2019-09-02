# automatically generated by the FlatBuffers compiler, do not modify

# namespace: Reaction

import flatbuffers


class FMotion(object):
  __slots__ = ['_tab']

  @classmethod
  def GetRootAsFMotion(cls, buf, offset):
    n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, offset)
    x = FMotion()
    x.Init(buf, n + offset)
    return x

  # FMotion
  def Init(self, buf, pos):
    self._tab = flatbuffers.table.Table(buf, pos)

  # FMotion
  def ActorName(self):
    o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
    if o != 0:
      return self._tab.String(o + self._tab.Pos)
    return None

  # FMotion
  def ActuatorName(self):
    o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
    if o != 0:
      return self._tab.String(o + self._tab.Pos)
    return None

  # FMotion
  def Strength(self):
    o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(8))
    if o != 0:
      return self._tab.Get(flatbuffers.number_types.Float64Flags, o + self._tab.Pos)
    return 0.0


def FMotionStart(builder): builder.StartObject(3)


def FMotionAddActorName(builder, actorName): builder.PrependUOffsetTRelativeSlot(0,
                                                                                 flatbuffers.number_types.UOffsetTFlags.py_type(
                                                                                     actorName), 0)


def FMotionAddActuatorName(builder, actuatorName): builder.PrependUOffsetTRelativeSlot(1,
                                                                                       flatbuffers.number_types.UOffsetTFlags.py_type(
                                                                                           actuatorName), 0)


def FMotionAddStrength(builder, strength): builder.PrependFloat64Slot(2, strength, 0.0)


def FMotionEnd(builder): return builder.EndObject()
