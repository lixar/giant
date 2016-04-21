#!/usr/bin/env python

from cookiecutter.main import cookiecutter
from yapsy.PluginManager import PluginManager
import os
import logging
from .giant_base import BaseGiantClient, BaseGiantServer

logging.basicConfig()

if os.name == "nt":
    def symlink_ms(source, link_name):
        import ctypes
        csl = ctypes.windll.kernel32.CreateSymbolicLinkW
        csl.argtypes = (ctypes.c_wchar_p, ctypes.c_wchar_p, ctypes.c_uint32)
        csl.restype = ctypes.c_ubyte
        flags = 1 if os.path.isdir(source) else 0
        try:
            if csl(link_name, source.replace('/', '\\'), flags) == 0:
                raise ctypes.WinError()
        except:
            pass
    os.symlink = symlink_ms

class GiantCommands(object):

    _client_category = 'Client'
    _server_category = 'Server'

    def __init__(self):
        self.client_plugins = None
        self.server_plugins = None
        
        self._plugin_manager = PluginManager(plugin_info_ext='giant')
        self._plugin_manager.setCategoriesFilter({
           GiantCommands._client_category : BaseGiantClient,
           GiantCommands._server_category: BaseGiantServer,
           })
        path = os.path.dirname(os.path.realpath(__file__))
        self._plugin_manager.setPluginPlaces([path + '/plugins'])
        self._plugin_manager.collectPlugins()
        self.plugin_infos = self._plugin_manager.getAllPlugins()
    
    def new_plugin(self, args):
        import getpass
        username = getpass.getuser()
        safe_language = (args.language
            .replace('#', 'Sharp')
            .replace('+', 'Plus')
            .replace(' ', '')
            .replace('!', 'Exclamation')
            .replace('/', 'Slash')
            .replace('*', 'Star'))
        repo_name = safe_language.lower()+'_'+args.framework.lower()
        cookiecutter('gh:lixar/giant-plugin', extra_context={
            'full_name': username,
            'project_language': args.language,
            'project_framework': args.framework,
            'project_type': args.type,
            'repo_name': repo_name,
            'command': repo_name.replace('_', '-')
        })
        
    def install_plugin(self, args):
        import glob
        input_path = args.input_plugin
        plugin_file = glob.glob(input_path + '/*.giant')
        with open(plugin_file[0], 'r') as plugin:
            for line in plugin.readlines():
                if line.startswith('Name'):
                    plugin_name = line.split(' = ')[1].strip()
                if line.startswith('Type'):
                    plugin_type = line.split(' = ')[1].strip()
        
        path = os.path.dirname(os.path.abspath(__file__))
        plugins_dir = os.path.join(path, 'plugins')
        plugins_dir = os.path.join(plugins_dir, plugin_type.lower())
        try:
            os.makedirs(plugins_dir)
        except: 
            pass
        plugins_dir = os.path.join(plugins_dir, plugin_name)
        if args.symlink:
            try:
                import pdb; pdb.set_trace()
                os.symlink(os.path.abspath(args.input_plugin), plugins_dir)
            except:
                logging.error('Plugin with this name already exists.')
        else:
            import shutil
            shutil.copytree(os.path.abspath(args.input_plugin), plugins_dir)
            # TODO Update giant-1.0.0.dist-info/RECORD to have new files added.
        
    def uninstall_plugin(self, args):
        import shutil
        plugin = self._get_plugin(args.command_name)
        path = plugin.path
        while not path.endswith('client') and not path.endswith('server'):
            path, plugin_dirname = os.path.split(path)
        shutil.rmtree(os.path.join(path, plugin_dirname))
        
    def get_client_plugins(self):
        if self.client_plugins == None:
            self.client_plugins = self._plugin_manager.getPluginsOfCategory(GiantCommands._client_category)
        return self.client_plugins
        
    def get_server_plugins(self):
        if self.server_plugins == None:
            self.server_plugins = self._plugin_manager.getPluginsOfCategory(GiantCommands._server_category)
        return self.server_plugins
        
    def get_all_plugins(self):
        return self.get_client_plugins() + self.get_server_plugins()
        
    def _get_plugin(self, command_name):
        return next(plugin for plugin in self.get_all_plugins() if plugin.details.get('Details', 'Command') == command_name)
        
    def generate_client(self, args, name):
        plugin_info = next(plugin_info for plugin_info in self.client_plugins if plugin_info.details.get('Details', 'Command') == name)
        self._plugin_manager.activatePluginByName(plugin_info.name)
        self._generate_project(args, plugin_info.plugin_object)
        
    def generate_server(self, args, name):
        plugin_info = next(plugin_info for plugin_info in self.server_plugins if plugin_info.details.get('Details', 'Command') == name)
        plugin = self._plugin_manager.activatePluginByName(plugin_info.name)
        self._generate_project(args, plugin_info.plugin_object)
        
    def _generate_project(self, args, plugin):
        if args.swagger_files == None:
            import requests
            response = requests.get(args.swagger_url)
            try:
                swagger = response.json()
            except:
                import yaml
                try:
                    swagger = yaml.load(response.text)
                except:
                    logging.critical("Failed to parse server response to JSON or YAML.")
                    exit(1)
        else:
            swagger = {}
            for f in args.swagger_files:
                if os.path.isdir(f):
                    files = os.listdir(f)
                else:
                    files = [f]
                for swagger_file_path in files:
                    with open(swagger_file_path, 'r') as swagger_file:
                        try:
                            api = json.load(swagger_file)
                        except:
                            swagger_file.seek(0)
                            import yaml
                            api = yaml.load(swagger_file)
                    paths = {}
                    
                    for path_name, path in api['paths'].iteritems():
                        if len(args.swagger_files) > 1:
                            paths[api['host'] + path_name] = path
                        else:
                            paths[path_name] = path
                    api['paths'] = paths
                    
                    tag = f.split('.')[0]
                    self.mergedicts(swagger, api, conflicts=['paths', 'definitions'], conflict_tag=tag)
                
        plugin.setup(swagger, args.output_dir)
        print('Generating Project...')
        plugin.generate()
        
    def mergedicts(self, a, b, path=None, conflicts=[], conflict_tag=None):
        "merges b into a"
        if path is None: path = []
        for key in b:
            if key in a:
                if isinstance(a[key], dict) and isinstance(b[key], dict):
                    self.mergedicts(a[key], b[key], path + [str(key)], conflicts=conflicts, conflict_tag=conflict_tag)
                elif a[key] == b[key]:
                    pass # same leaf value
                else:
                    conflict_path = '.'.join(path + [str(key)])
                    if any(conflict in conflicts for conflict in conflict_path.split('.')):
                        if conflict_tag is not None and key + conflict_tag not in a.keys():
                            a[key + conflict_tag] = b[key]
                            continue # resolve conflict using tag.
                        raise Exception('Conflict at ' + '.'.join(path + [str(key)]))
                    else:
                        print('Ignoring conflict ' + conflict_path)
            else:
                a[key] = b[key]
        return a
    
giant = GiantCommands()
