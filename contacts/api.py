from abc import ABC
from typing import *
from wefram import api
from .models import Contact


@api.register
class Team(api.EntityAPI):
    async def read(
            self,
            *keys: Union[str, int],
            count: bool = False,
            offset: Optional[int] = None,
            limit: Optional[int] = None,
            order: Optional[Union[str, List[str]]] = None,
            deep: bool = False,
            like: Optional[str] = None,
            ilike: Optional[str] = None,
            **filters: Any
    ) -> Any:
        return await Contact.team(
            search_term=ilike,
            for_json=True
        )

    async def create(cls, return_key: bool = False, **with_values) -> Any:
        raise NotImplementedError

    async def delete(self, *keys: Optional[Sequence[Union[str, int]]]) -> None:
        raise NotImplementedError

    async def options(
            self,
            *keys: Union[str, int],
            like: Optional[str] = None,
            ilike: Optional[str] = None
    ) -> dict:
        raise NotImplementedError

    async def update(self, *keys: Optional[Sequence[Union[str, int]]], **values) -> None:
        raise NotImplementedError


