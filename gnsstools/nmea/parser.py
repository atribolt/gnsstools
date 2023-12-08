import io
import itertools
import operator
from typing import NamedTuple
from .frame import Frame
from .exceptions import NmeaParseError, NmeaCorruptFrame


class NmeaLine(NamedTuple):
  start: int
  message: bytes
  checksum: int


class Parser:
  buffer: bytes = None

  @staticmethod
  def _test_xor_sum(data: bytes, expected: int):
    hashsum = list(itertools.accumulate(data, operator.xor, initial=0))
    return hashsum[-1] == expected

  @staticmethod
  def _unpack_line(line: bytes):
    if len(line) < 6:
      raise NmeaParseError(f'Line is very short: {line}')

    return NmeaLine(
      start=line[0],
      message=line[1:-5],
      checksum=int(line[-4:-2], 16) if line.endswith(b'\r\n') else int(line[-3:-1], 16)
    )

  def __init__(self, stream: io.IOBase):
    """
    :param stream: is the opened stream for read NMEA data
    """

    if not stream.readable():
      raise ValueError('The stream invalid. It should be readable IO')

    self.stream = stream
    self.buffer = b''

  def __enter__(self):
    self.buffer = b''
    return self

  def __exit__(self, exc_type, exc_val, exc_tb):
    return

  def next_frame(self) -> Frame | None:
    line = self.stream.readline()
    if not line:
      return None

    line = self._unpack_line(line)

    if line.start not in b'$!':
      raise NmeaParseError(f'Unknown the line start symbol: {line.start}')

    if not self._test_xor_sum(line.message, line.checksum):
      raise NmeaCorruptFrame(f'The message {line.message} is corrupted. {hex(line.checksum)}')

    return Frame(line.message)


# ---

def test_parse():
  data = b'$GPGGA,,,,,,0,00,99.99,,,,,,*48\r\n'

  stream = io.BytesIO(data)

  parser = Parser(stream)
  frame = parser.next_frame()

  assert frame.source == 'GP', 'Source parse invalid'
  assert frame.header == 'GGA', 'Header parse invalid'


def test_parse_corrupt_frame():
  data = b'$GPGGA,,,,,,0,00,99.99,,,,,,*49\r\n'

  stream = io.BytesIO(data)
  parser = Parser(stream)

  try:
    parser.next_frame()
  except NmeaCorruptFrame:
    pass
  else:
    raise AssertionError('expected NmeaCorruptFrame exception')
