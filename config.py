import configparser
import os
import yaml

from utils.utils import FancyDict


class Config:
    def __init__(self):
        self.setting = {
            'template_path': os.path.join(os.path.dirname(__file__), 'templates'),
            'static_path': os.path.join(os.path.dirname(__file__), 'static'),
            'debug': True
            }

    def load_configs(self):
        _cp = configparser.ConfigParser()
        current_dir = os.path.dirname(os.path.realpath(__file__))
        config_ini_path = 'config.yml'
        file_path = os.path.join(current_dir, config_ini_path)
        fp = open(file_path, 'r', encoding='utf-8')
        content = fp.read()
        fp.close()

        config_fancy_dict = FancyDict()
        results = yaml.load(content)
        for section, values in results.items():
            f = FancyDict()
            f.update(values)
            config_fancy_dict[section.upper()] = f

        config_fancy_dict['setting'] = self.setting
        return config_fancy_dict


config_info = Config().load_configs()


if __name__ == '__main__':
   print(config_info)

