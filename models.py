from pydantic import BaseModel


class Version(BaseModel):
    version: str
    revision: str


class KnownGoodVersions(BaseModel):
    timestamp: str
    versions: list[Version]
