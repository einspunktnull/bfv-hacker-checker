from injector import Module, singleton, Binder

from App import App
from QApplicationWrap import QApplicationWrap
from service.ConfigService import ConfigService
from service.DetectPlayerNameService import DetectPlayerNameService
from service.LoggingService import LoggingService
from service.PrepareService import PrepareService
from ui.AboutDialog import AboutDialog
from ui.AppWindow import AppWindow
from ui.DebugWindow import DebugWindow


class GlobalInjectorModule(Module):

    def configure(self, binder: Binder):
        binder.bind(ConfigService, to=ConfigService, scope=singleton)
        binder.bind(LoggingService, to=LoggingService, scope=singleton)
        binder.bind(PrepareService, to=PrepareService, scope=singleton)
        binder.bind(DetectPlayerNameService, to=DetectPlayerNameService, scope=singleton)
        binder.bind(App, to=App)
        binder.bind(QApplicationWrap, to=QApplicationWrap)
        binder.bind(AppWindow, to=AppWindow)
        binder.bind(DebugWindow, to=DebugWindow)
        binder.bind(AboutDialog, to=AboutDialog)
