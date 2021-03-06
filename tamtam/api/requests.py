import logging
import typing

import aiohttp
import pydantic
import yarl

from ..helpers.ctx import ContextInstanceMixin
from .exceptions import BaseWrapperError, JsonParsingError, tt_explanation

logger = logging.getLogger(__name__)

UrlType = typing.Union[str, yarl.URL]
QueryVariable = typing.Union[str, int]
Query = typing.Union[
    None,
    str,
    typing.Mapping[str, QueryVariable],
    typing.Sequence[typing.Tuple[str, QueryVariable]],
]


def is_error(response_json: dict):
    return all(k in response_json for k in ("code", "message"))


def params_filter(dictionary: Query):
    """
    Pop NoneType values and convert everything to str, designed?for=params
    :param dictionary: source dict
    :return: filtered dict
    """
    return (
        {k: str(v) for k, v in dictionary.items() if v is not None}
        if dictionary
        else {}
    )


class Requester(ContextInstanceMixin):
    def __init__(self, session: aiohttp.ClientSession, default_params: dict = None):
        self.session = session
        self.params = params_filter(default_params or {})

    async def __call__(
        self,
        http_method: str,
        url: UrlType,
        *,
        params: Query = None,
        json: str = None,
        model=None,
        models_in_list: bool = None,
        model_from_key: str = None,
        extra_key: str = None,
        **aiohttp_request_kwargs,
    ):
        if "data" in aiohttp_request_kwargs:
            json = aiohttp_request_kwargs.pop("data")

        async with self.session.request(
            http_method,
            url.__str__(),
            params={**self.params, **params_filter(params)},
            data=json,
            **aiohttp_request_kwargs,
        ) as response:

            tt_exp = tt_explanation.get(response.status)
            try:
                response_json = await response.json()
                logger.info(
                    f"Sent [{http_method}] to {url!s} [model: {model!r}|data: {json!s}]\t"
                    f"Got  {response_json} | exp: {tt_exp!s}"
                )

            except ValueError as exc:
                logger.error(exc, exc_info=True)
                raise JsonParsingError()

            if is_error(response_json):
                logger.error(response_json)
                raise BaseWrapperError(response_json, tt_exp or "unknown")

            if model:
                try:
                    if model_from_key:
                        if models_in_list:
                            ret = [
                                model(**rjs)
                                for rjs in response_json.get(model_from_key)
                            ]
                        else:
                            ret = model(**(response_json.get(model_from_key)))
                    elif models_in_list:
                        ret = [model(**rjs) for rjs in response_json]
                    else:
                        ret = model(**response_json)

                except pydantic.ValidationError as exc:
                    logger.error(exc, exc_info=True)
                    raise JsonParsingError()

                if extra_key:
                    return ret, response_json.get(extra_key)
                return ret

            return response_json

    async def get(self, url: UrlType, params: dict = None, **kwargs):
        return await self("GET", url, params=params, **kwargs)

    async def post(self, url: UrlType, params: dict = None, json: str = None, **kwargs):
        return await self("POST", url, params=params, json=json, **kwargs)

    async def close(self):
        await self.session.close()
