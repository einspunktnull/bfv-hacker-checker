import sys

from injector import Injector

from App import App
from GlobalInjectorModule import GlobalInjectorModule
from service.LoggingService import LoggingService

if __name__ == '__main__':
    global_injector: Injector = Injector()
    global_injector.binder.bind(Injector, to=global_injector)
    global_injector.binder.install(GlobalInjectorModule())

    logger: LoggingService = global_injector.get(LoggingService)
    logger.info('Startup App')
    try:
        app: App = global_injector.get(App)
        exit_code: int = app.run()
        sys.exit(exit_code)
    except Exception as ex:
        logger.exception(ex)
        sys.exit(-99999)
