import pytest
import asyncio
from asyncio.events import AbstractEventLoop
from .hello_asyncio import say_hello
from typing import Any, Generator, Callable


@pytest.fixture
def event_loop() -> Generator[AbstractEventLoop, None, None]:
    loop: AbstractEventLoop = asyncio.get_event_loop()
    yield loop


@pytest.mark.parametrize('name', [
    'Robert Paulson',
    'Seven of Nine',
    'x Æ a-12'
])
def test_say_hello(event_loop: AbstractEventLoop, name: Any):
    event_loop.run_until_complete(say_hello(name))


class TestSayHelloThrowsExceptions:
    @pytest.mark.parametrize('name', [
        '',
    ])
    def test_say_hello_value_error(self, event_loop: Callable[[None], Generator], name: Any):
        with pytest.raises(ValueError):
            event_loop.run_until_complete(say_hello(name))

    @pytest.mark.parametrize('name', [
        19,
        {'name', 'Diane'},
        []
    ])
    def test_say_hello_type_error(self, event_loop: Callable[[None], Generator], name: Any):
        with pytest.raises(TypeError):
            event_loop.run_until_complete(say_hello(name))
