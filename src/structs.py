import msgspec


class RawData(msgspec.Struct, kw_only=True):
    to: str | None = None
    from_: str | None = None
    text: str


class FsLetter(msgspec.Struct, kw_only=True):
    id: str
    raw: RawData
