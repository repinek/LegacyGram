from collections.abc import Callable, Sequence
from typing import Any, Generic, TypeVar

# --- Primitives ---
class jboolean:
    def __init__(self, value: bool): ...

class jbyte:
    def __init__(self, value: int, truncate: bool = False): ...

class jshort:
    def __init__(self, value: int, truncate: bool = False): ...

class jint:
    def __init__(self, value: int, truncate: bool = False): ...

class jlong:
    def __init__(self, value: int, truncate: bool = False): ...

class jfloat:
    def __init__(self, value: float, truncate: bool = False): ...

class jdouble:
    def __init__(self, value: float, truncate: bool = False): ...

class jchar:
    def __init__(self, value: str): ...

class jvoid:
    """Cannot be instantiated."""

    ...

# --- Classes & Objects ---
def jclass(cls_name: str) -> Any:
    """
    Returns a Python class for a Java class or interface type.
    Example: Calendar = jclass("java.util.Calendar")
    """
    ...

def cast(cls: Any, obj: Any) -> Any:
    """
    Returns a view of the given object as the given class.
    """
    ...

def set_import_enabled(enable: bool) -> None: ...
def detach() -> None: ...

# --- Arrays ---
T = TypeVar("T")

class jarray(Sequence[T], Generic[T]):
    """
    Represents a Java array type or instance.
    Usage:
        IntArray = jarray(jint)
        my_array = IntArray([1, 2, 3])
    """

    def __init__(self, element_type: Any): ...
    def __call__(self, data: list[T] | int) -> jarray[T]: ...

    # Sequence methods
    def __getitem__(self, index: int) -> T: ...
    def __len__(self) -> int: ...
    def __iter__(self) -> Any: ...

    # Java Object methods
    def toString(self) -> str: ...
    def hashCode(self) -> int: ...
    def equals(self, other: Any) -> bool: ...

# --- Proxies & Decorators ---
def dynamic_proxy(*implements: Any) -> Any:
    """Use as first base class: class MyListener(dynamic_proxy(OnClickListener)): ..."""
    ...

def static_proxy(extends: Any | None = None, *implements: Any, package: str | None = None, modifiers: str = "public") -> Any:
    """Use as first base class for static proxy generation."""
    ...

# Decorators
def method(return_type: Any, arg_types: list[Any], *, modifiers: str = "public", throws: list[Any] | None = None) -> Callable: ...
def Override(return_type: Any, arg_types: list[Any], *, modifiers: str = "public", throws: list[Any] | None = None) -> Callable: ...
def constructor(arg_types: list[Any], *, modifiers: str = "public", throws: list[Any] | None = None) -> Callable: ...
