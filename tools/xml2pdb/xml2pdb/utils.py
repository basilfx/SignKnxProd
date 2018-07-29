import argparse
import os


class VerboseAction(argparse.Action):
    """
    Argparse action to count the verbose level (e.g. -v, -vv, etc).
    """

    def __call__(self, parser, args, value, option_string=None):
        try:
            value = int(value or "1")
        except ValueError:
            value = value.count("v") + 1

        setattr(args, self.dest, value)


class NewPathAction(argparse.Action):
    """
    Argparse action that resolves a given path to absolute path.
    """

    def __call__(self, parser, args, values, option_string=None):
        setattr(args, self.dest, os.path.abspath(values))


class PathAction(argparse.Action):
    """
    Argparse action that resolves a given path, and ensures it exists.
    """

    def __call__(self, parser, args, values, option_string=None):
        path = os.path.abspath(values)

        if not os.path.exists(path):
            parser.error("Path doesn't exist for '%s': %s" % (
                option_string, path))

        setattr(args, self.dest, path)
