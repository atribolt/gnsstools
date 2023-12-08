import enum
from datetime import time
from gnsstools.nmea.exceptions import NmeaParseError


class Solution(enum.IntEnum):
  No = 0
  StandAlone = 1
  DGPS = 2
  PPS = 3
  FixedRTK = 4
  RTK = 5
  InertialSystem = 6
  Manual = 7
  ManualSimulate = 8


class GGAFrame:
  """
  The show a Frame as a GGA frame.
  The data about fixed solution.
  """

  header = 'GGA'

  def __init__(self, values: list[str]):
    if len(values) != 14:
      raise NmeaParseError('The incorrect GGA frame')

    self.values = values

  @property
  def longitude(self) -> float:
    pos = 3
    if lon := self.values[pos]:
      try:
        degrees = int(lon[:3])
        minutes = float(lon[3:])
      except (ValueError, IndexError):
        raise NmeaParseError('Invalid longitude value: %s' % lon)
      return degrees + minutes / 60
    return 0.0

  @property
  def latitude(self) -> float:
    pos = 1
    if lat := self.values[pos]:
      try:
        degrees = int(lat[:2])
        minutes = float(lat[2:])
      except (ValueError, IndexError):
        raise NmeaParseError('Invalid latitude value: %s' % lat)
      return degrees + minutes / 60
    return 0.0

  @property
  def alt_msl(self) -> float:
    pos = 8
    if alt := self.values[pos]:
      try:
        return float(alt)
      except (ValueError, IndexError):
        raise NmeaParseError('Invalid altitude MSL value: %s' % alt)
    return 0.0

  @property
  def alt_hae(self) -> float:
    pos = 10
    if alt := self.values[pos]:
      try:
        return float(alt)
      except (ValueError, IndexError):
        raise NmeaParseError('Invalid altitude HAE value: %s' % alt)
    return 0.0

  @property
  def utc_time(self) -> time:
    pos = 0
    if tm := self.values[pos]:
      try:
        return time(
          hour=int(tm[:2]),
          minute=int(tm[2:4]),
          second=int(tm[4:6])
        )
      except (ValueError, IndexError):
        raise NmeaParseError('Invalid time value: %s' % tm)
    return time()

  @property
  def solution(self) -> Solution:
    pos = 5
    if sln := self.values[pos]:
      try:
        code = int(sln)
        return Solution(code)
      except (ValueError, IndexError):
        raise NmeaParseError('Invalid solution value: %s' % sln)
      except TypeError:
        raise NmeaParseError('Unknown solution: %s' % sln)
    return Solution.No

  @property
  def sattelites(self) -> int:
    pos = 6
    if sln := self.values[pos]:
      try:
        code = int(sln)
        return Solution(code)
      except (ValueError, IndexError):
        raise NmeaParseError('Invalid solution value: %s' % sln)
      except TypeError:
        raise NmeaParseError('Unknown solution: %s' % sln)
    return Solution.No


# ---

def test_interface():
  values = [
    '134801',  # time
    '4812.000', 'N',  # lat
    '01130.000', 'E',  # lon
    '7', '08', '',
    '545.2', 'M',  # alt MSL
    '46.9', 'M',  # alt HAE
    '', ''
  ]

  frame = GGAFrame(values)

  assert frame.longitude == 11.5, 'Longitude load incorrect'
  assert frame.latitude == 48.2, 'Latitude load incorrect'
  assert frame.utc_time == time(13, 48, 1), 'Time load incorrect'
  assert frame.solution == Solution.Manual, 'Solution load incorrect'
  assert frame.alt_msl == 545.2, 'Altitude MSL load invalid'
  assert frame.alt_hae == 46.9, 'Altitude HAE load invalid'


def test_less_values():
  values = []

  try:
    GGAFrame(values)
  except NmeaParseError:
    pass
  else:
    raise AssertionError('expected NmeaParseError exception')
