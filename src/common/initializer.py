import inspect
import typing
from typing import Any

T = typing.TypeVar("T")


class Proxy:
    def __init__(self, cls: type[T]):
        self.cls = cls
        self.initialized: Any = None

    def __getattr__(self, name: str):
        if not self.initialized:
            raise RuntimeError(f"{self.cls.__name__} is not initialized")
        return getattr(self.initialized, name)

    def initialize(self, *args: typing.Any, **kwargs: typing.Any) -> Any:
        self.initialized = self.cls(*args, **kwargs)
        return self.initialized

    def reset(self) -> None:
        self.initialized = None

    def run_initialize(self, *args: typing.Any, **kwargs: typing.Any) -> Any:
        if not hasattr(self.cls, "run_initialize"):
            return self.initialize(*args, **kwargs)

        initialized = getattr(self.cls, "run_initialize")(*args, **kwargs)

        if inspect.iscoroutine(initialized):

            async def coro():
                self.initialized = await initialized
                return self.initialized

            return coro()

        self.initialized = initialized
        return self.initialized


class Initialized:
    """Marks child-class as requiring initialization
    Uninitialized class is created via .uninitialized() method
    ```python
      class MyClass(Initialized):
          ...
      my_class = MyClass.uninitialized()
      my_class.my_method() # Attempt to access methods of an uninitialized class will result in RuntimeError
      my_class.initialize(123) # Whatever you have in init goes there
      my_class.my_method() # Yas.. 'V'
    ```
    """

    if typing.TYPE_CHECKING:

        @property
        def initialize(self: T) -> type[T]: ...

        @classmethod
        async def run_initialize(
            cls: type[T],
            *args: typing.Any,
            **kwargs: typing.Any,
        ) -> T: ...

        @classmethod
        def reset(
            cls: type[T],
        ) -> None: ...

    @classmethod
    def uninitialized(cls: type[T]) -> T:
        return Proxy(cls)  # type: ignore
