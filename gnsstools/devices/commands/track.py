import click
import functools
from pathlib import Path
from gnsstools.nmea.parser import Parser
from gnsstools.nmea.frames import GGAFrame
from datetime import datetime


@click.command()
@click.option('-i', '--input', 'source',
              type=click.Path(exists=True, file_okay=True,
                              dir_okay=False, readable=True, path_type=Path),
              help='Input serial device or file contains NMEA data',
              required=True)
def track(source: Path):
  if source.is_char_device():
    from serial import serialposix
    iofactory = serialposix.Serial
  else:
    iofactory = functools.partial(open, mode='rb')

  with iofactory(str(source)) as stream:
    click.echo('Sys time,GPS time,Lon,Lat,Alt MSL,Alt HAE')
    fmt = '{1},{0.utc_time},{0.longitude},{0.latitude},{0.alt_msl},{0.alt_hae}'

    with Parser(stream) as parser:
      try:
        while frame := parser.next_frame():
          if frame.header == GGAFrame.header:
            click.echo(fmt.format(GGAFrame(frame.values), datetime.now().time()))

      except KeyboardInterrupt:
        click.echo('\nNormal finished')
