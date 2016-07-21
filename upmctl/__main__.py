# Copyright (c) 2016, Tobias Schaefer
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
# * Neither the name of upmctl nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import sys
import argparse
import pprint
from client import Client
from plugins import (list_plugins, show_plugin, install_plugin, delete_plugin,
        activate_plugin, deactivate_plugin)
from upm import get_upm_token
from configuration import read_config, get_key_config
from exception import ClientError


def stype(bytestring):
    unicode_string = bytestring.decode(sys.getfilesystemencoding())
    return unicode_string


def parse_options():
    parser = argparse.ArgumentParser(description='upmctl',
                                     epilog='Control the Atlassian Universal \
                                     Plugin Manager from the console.')
    parser.add_argument('--base-url',
                        required=True,
                        type=unicode,
                        help='Confluence URL')
    parser.add_argument('--base-authentication',
                        required=True,
                        type=unicode,
                        help='base authentication USERNAME:PASSWORD')
    parser.add_argument('--configuration-file',
                        type=stype,
                        help='configuration file')
    subparsers = parser.add_subparsers()

    parser_list = subparsers.add_parser('list',
                                        help='list plugins')
    parser_list.set_defaults(list=True)
    parser_list.add_argument('--user',
                             action='store_true',
                             help='list user installed plugins')
    parser_list.add_argument('--system',
                             action='store_true',
                             help='list system plugins')
    parser_list.add_argument('--key',
                             help='list plugins by regex key')
    parser_list.add_argument('--key-configuration-file',
                             help='list plugins by regex key in configuration \
                                  file')

    parser_show = subparsers.add_parser('show',
                                        help='show plugin details')
    parser_show.set_defaults(show=True)
    parser_show.add_argument('key',
                             type=unicode,
                             help='plugin key')

    parser_install = subparsers.add_parser('install',
                                           help='install plugin')
    parser_install.set_defaults(install=True)
    parser_install.add_argument('plugin',
                                type=stype,
                                help='plugin file path')

    parser_delete = subparsers.add_parser('delete',
                                           help='delete plugin')
    parser_delete.set_defaults(delete=True)
    parser_delete.add_argument('key',
                                type=unicode,
                                help='plugin key')

    parser_activate = subparsers.add_parser('activate',
                                            help='activate plugin')
    parser_activate.set_defaults(activate=True)
    parser_activate.add_argument('key',
                                 type=unicode,
                                 help='plugin key')

    parser_deactivate = subparsers.add_parser('deactivate',
                                               help='deactivate plugin')
    parser_deactivate.set_defaults(deactivate=True)
    parser_deactivate.add_argument('key',
                                   type=unicode,
                                   help='plugin key')

    return parser.parse_args()


def run(args):
    client = Client(base_url=args.base_url,
                    base_auth=args.base_authentication)
    pp = pprint.PrettyPrinter()

    try:

        if hasattr(args, 'list'):
            if args.user:
                plugins = list_plugins(client, key='userInstalled',
                                       value='boolean', pattern='true')
            elif args.system:
                plugins = list_plugins(client, key='userInstalled',
                                       value='boolean', pattern='false')
            elif args.key:
                plugins = list_plugins(client, key='key', value='regex',
                                       pattern=args.key)
            elif args.key_configuration_file:
                config = read_config(args.key_configuration_file)
                key = get_key_config(config)
                plugins = list_plugins(client, key='key', value='regex',
                                       pattern=key)
            else:
                plugins = list_plugins(client)
            if plugins is not None:
                pp.pprint(plugins)
        elif hasattr(args, 'show'):
            plugin = show_plugin(client, args.key)
            pp.pprint(plugin)
        elif hasattr(args, 'install'):
            token = get_upm_token(client)
            client.request.url = args.base_url
            install_plugin(client, token, args.plugin)
        elif hasattr(args, 'delete'):
            delete_plugin(client, args.key)
        elif hasattr(args, 'activate'):
            activate_plugin(client, args.key)
        elif hasattr(args, 'deactivate'):
            deactivate_plugin(client, args.key)

    except ClientError as e:
        print >> sys.stderr, "%s: %s" % ('upmctl', e)
        sys.exit(1)

    sys.exit(0)


def main():
    args = parse_options()
    run(args)


if __name__ == '__main__':
    main()
