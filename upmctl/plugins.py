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

"""
Performs request to the Universal Plugin Manager (UPM).
"""

import json
import re


def list_plugins(client, key=None, value=None, pattern=None):
    client.request.url = "%s%s" % (client.request.url, '/rest/plugins/1.0/')
    client.get()

    plugins = client.response.json().get('plugins')
    plugins = dict((plugin['name'], plugin) for plugin in plugins).values()

    if value == 'regex':
        regex = re.compile(pattern)
        plugins = [plugin for plugin in plugins
                   if regex.match(plugin.get(key))]
    elif value == 'boolean':
        if pattern == 'true':
            plugins = [plugin for plugin in plugins
                       if plugin.get(key)]
        elif pattern == 'false':
            plugins = [plugin for plugin in plugins
                       if not plugin.get(key)]

    return plugins


def show_plugin(client, key):
    client.request.url = "%s%s%s-key/" % (client.request.url,
                                          '/rest/plugins/1.0/',
                                          key)
    client.get()
    plugin = client.response.json()

    return plugin


def install_plugin(client, token, plugin):
    client.request.url = "%s%s?token=%s" % (client.request.url,
                                            '/rest/plugins/1.0/',
                                            token)

    with open(plugin, 'rb') as filename:
        client.post(files={ 'plugin': filename })


def delete_plugin(client, key):
    client.request.url = "%s%s%s-key" % (client.request.url,
                                         '/rest/plugins/1.0/',
                                         key)
    client.delete()


def activate_plugin(client, key):
    modify_plugin(client, key, True)


def deactivate_plugin(client, key):
    modify_plugin(client, key, False)


def modify_plugin(client, key, status):
    client.request.url = "%s%s%s-key" % (client.request.url,
                                         '/rest/plugins/1.0/',
                                         key)
    client.get()
    raw = client.response.json()
    raw['enabled'] = status
    data = json.dumps(raw)

    client.request.headers['Content-Type'] = \
            'application/vnd.atl.plugins.plugin+json'

    client.put(data=data)
