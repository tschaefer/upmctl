import sys
import os
import argparse
from core import ConfluenceCtl, PLUGINS


def stype(bytestring):
    unicode_string = bytestring.decode(sys.getfilesystemencoding())
    return unicode_string


def parse_options():
    parser = argparse.ArgumentParser(description='vagrantctl')
    parser.add_argument('-u', '--base-url',
                        type=unicode,
                        help='Confluence URL')
    parser.add_argument('-a', '--base-authentication',
                        type=unicode,
                        help='base authentication credentials')
    parser.add_argument('-c', '--configuration-file',
                        type=stype,
                        help='configuration file')
    subparsers = parser.add_subparsers()

    parser_plugin = subparsers.add_parser('plugin')
    parser_plugin.set_defaults(plugin=True)
    parser_plugin.add_argument('-l', '--list',
                               type=unicode,
                               choices=PLUGINS.keys(),
                               help='list installed plugins')


    return parser.parse_args()


def run(args):
    confluencectl = ConfluenceCtl(base_url=args.base_url,
                                  base_auth=args.base_authentication)
    if hasattr(args, 'plugin'):
        if hasattr(args, 'list'):
            for plugin in confluencectl.plugin_list(installed_by=args.list):
                print plugin


def main():
    args = parse_options()
    run(args)


if __name__ == '__main__':
    main()
