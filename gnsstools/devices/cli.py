import click

from . import commands


class CommandFactory(click.Group):
	def get_command(self, _, cmd_name: str):
		field = getattr(commands, cmd_name, None)
		return field if isinstance(field, click.Command) else None

	def list_commands(self, _):
		return [
			x for x in dir(commands)
			if not x.startswith('_') and isinstance(getattr(commands, x), click.Command)
		]


@click.group(cls=CommandFactory)
def maincli():
	"""CLI for work with GNSS"""
