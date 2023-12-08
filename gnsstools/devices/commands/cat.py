import io
import sys
import click
from serial import serialposix


@click.command()
@click.option('-d', '--dev',
              type=click.Path(exists=True, file_okay=True,
                              dir_okay=False, readable=True, path_type=str),
              help='Input serial device',
              required=True)
def cat(dev: str, output: io.IOBase):
  """read character device or file"""

  s = serialposix.Serial(dev)

  try:
    while line := s.readline():
      output.write(line.decode('ascii'))
  except KeyboardInterrupt:
    click.echo('\nNormal finished', sys.stderr)

  finally:
    s.close()
