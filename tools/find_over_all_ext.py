import importlib.util
import config


class FindOverAllExtensions:
    """
        Подгрузка расширений без привязки к наименованию папки.
    """
    dict_of_extensions = {}

    def __init__(self, extension_type):
        self.list_of_extensions = []
        self.path = '/code/external_modules/'
        self.extension_type = extension_type
        d = config.NLAB_EXTENSION_PRIORITY.get(self.extension_type)
        if d:
            self.dict_of_extensions = dict(sorted(d.items(), key=lambda kv: kv[1]))

    def load_extension(self, extension_path):
        spec = importlib.util.spec_from_file_location(self.extension_type, extension_path)
        m = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(m)
        self.list_of_extensions.append(m)

    def run(self):
        for extension_name in self.dict_of_extensions.keys():
            extension_path = f'{self.path}{extension_name}/main.py'
            self.load_extension(extension_path)
        return self.list_of_extensions

    def get_store_extension(self):
        for extension_name in self.dict_of_extensions.keys():
            extension_path = f'{self.path}{extension_name}/store.py'
            self.load_extension(extension_path)
        return self.list_of_extensions
