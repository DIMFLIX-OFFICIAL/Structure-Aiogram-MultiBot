from aiogram.dispatcher.filters import BoundFilter
from aiogram.types import CallbackQuery
from typing import Union, List


class CData(BoundFilter):
    key = 'cdata'

    def __init__(self, cdata: Union[str, List[str]]):
        self.cdata = cdata

    async def check(self, obj: CallbackQuery):
        if type(self.cdata) == str:
            return obj.data == self.cdata

        elif type(self.cdata) == list:
            for i in self.cdata:
                if obj.data == i:
                    return True

            return False


class CDataStart(BoundFilter):
    key = 'cdata_start'

    def __init__(self, cdata_start: Union[str, List[str]]):
        self.cdata_start = cdata_start

    async def check(self, obj: CallbackQuery):
        if type(self.cdata_start) == str:
            return obj.data.endswith(self.cdata_start)

        elif type(self.cdata_start) == list:
            for i in self.cdata_start:
                if obj.data.startswith(i):
                    return True

            return False


class CDataEnd(BoundFilter):
    key = 'cdata_end'

    def __init__(self, cdata_end: Union[str, List[str]]):
        self.cdata_end = cdata_end

    async def check(self, obj: CallbackQuery):
        if type(self.cdata_end) == str:
            return obj.data.endswith(self.cdata_end)

        elif type(self.cdata_end) == list:
            for i in self.cdata_end:
                if obj.data.endswith(i):
                    return True

            return False

