import sys

from injector import Injector, singleton

from lib.App import App
from lib.Config import Config
from lib.GlobalInjector import GlobalInjector
from lib.Logger import Logger

if __name__ == '__main__':

    GlobalInjector.bind(Config, to=Config, scope=singleton)
    GlobalInjector.bind(Logger, to=Logger, scope=singleton)
    logger: Logger = GlobalInjector.get(Logger)
    logger.info('Startup App')
    app: App = GlobalInjector.get(App)
    try:
        exit_code: int = app.run()
        sys.exit(exit_code)
    except Exception as ex:
        logger.exception(ex)
        sys.exit(-99999)
