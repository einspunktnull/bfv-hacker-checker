from __future__ import annotations

from typing import Any, Type, TypeVar, Generic, Callable, Union

from injector import Injector, NoScope, Provider, Scope, ScopeDecorator

T = TypeVar('T')


class GlobalInjector:
    __instance: GlobalInjector = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            return cls.__instance
        else:
            raise Exception("Can't instantiate directly.")

    def __init__(self):
        self.__injector: Injector = Injector()

    @classmethod
    def __get_instance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    @classmethod
    def get(cls, inj_type: Type[T]) -> T:
        return cls.__get_instance().__injector.get(inj_type)

    @classmethod
    def bind(
            cls,
            interface: Type[T],
            to: Union[None, T, Callable[..., T], Provider[T]] = None,
            scope: Union[None, Type[Scope], ScopeDecorator] = None,
    ) -> None:
        cls.__get_instance().__injector.binder.bind(interface, to=to, scope=scope)
