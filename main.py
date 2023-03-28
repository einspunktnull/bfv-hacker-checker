import os
import sys
from configparser import ConfigParser

from lib.App import App

if __name__ == '__main__':
    config: ConfigParser = ConfigParser()
    config.read('config.ini')

    data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
    print(data_dir)
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    app: App = App(
        name='Battlefield V Hacker Checker',
        icon_path="res/icon.png",
        url=config.get('app', 'url'),
        key=config.get('user', 'key'),
        default_player=config.get('user', 'default_player'),
        data_dir=data_dir
    )

    sys.exit(app.run())
