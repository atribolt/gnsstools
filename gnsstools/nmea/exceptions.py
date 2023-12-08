class NmeaError(Exception):
  """The NMEA error"""


class NmeaParseError(NmeaError):
  """The error while parse frame"""


class NmeaCorruptFrame(NmeaParseError):
  """A frame did not pass a check sum process"""
