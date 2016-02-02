from requests import Session, Request


PLUGINS = {
    'all': 'all',
    'user': 'user',
    'system': 'system'
}


class ConfluenceCtl(object):


    def __init__(self, base_url=None, base_auth=None, method='GET'):
        self.base_url = base_url
        self.base_auth = base_auth
        self.method = method
        self.request = Request(method, base_url)
        if self.method is not None:
            user, password = self.base_auth.split(':')
            self.request.auth = (user, password)
        self.session = Session()
        self.response = None


    def __send(self):
        prep = self.request.prepare()
        self.response = self.session.send(prep)


    def __append(self, plugin, installed_by):
        user_installed = plugin.get('userInstalled')
        if installed_by == 'user' and not user_installed:
            return False
        elif installed_by != 'user' and user_installed:
            return False
        return True


    def __exists(self, plugin, plugin_list):
        any(_plugin['name'] == plugin.get('name') for _plugin in plugin_list)


    def plugin_list(self, installed_by='all'):
        self.request.url = "%s%s" % (self.request.url, 'rest/plugins/1.0/')
        self.__send()
        plugin_list = list()
        for plugin in self.response.json().get('plugins'):
            item = {
                'name': plugin.get('name'),
                'version': plugin.get('version'),
                'enabled': plugin.get('enabled')
            }
            if not self.__exists(plugin, plugin_list)  and \
                self.__append(plugin, installed_by):
                plugin_list.append(item)
        return plugin_list

