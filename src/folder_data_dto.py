import dataclasses
import pathlib
import typing


@dataclasses.dataclass
class FolderDataDTO:
    folder_path: pathlib.Path
    internal_items: typing.Set[pathlib.Path]

