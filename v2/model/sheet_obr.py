from typing import TypedDict


class ColumnSheetObr(TypedDict):
    perfil: str
    mapa: str
    skin: str
    skin_local: str
    replay: str
    done: bool
    posted: bool
    approved: bool
    o_que_seria: str
    sliderbreaks: int | None