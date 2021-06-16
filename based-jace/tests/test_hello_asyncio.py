import pytest  # Note: pytest-asyncio does not require a separate import
import asyncio
from typing import Any

from .hello_asyncio import say_hello


@pytest.mark.parametrize('name', [
    'Robert Paulson',
    'Seven of Nine',
    'x Æ a-12'
])
@pytest.mark.asyncio
async def test_say_hello(name: Any):
    await say_hello(name)


class TestSayHelloThrowsExceptions:
    @pytest.mark.parametrize('name', [
        '',
    ])
    @pytest.mark.asyncio
    async def test_say_hello_value_error(self, name: Any):
        with pytest.raises(ValueError):
            await say_hello(name)

    @pytest.mark.parametrize('name', [
        19,
        {'name', 'Diane'},
        []
    ])
    @pytest.mark.asyncio
    async def test_say_hello_type_error(self, name: Any):
        with pytest.raises(TypeError):
            await say_hello(name)
