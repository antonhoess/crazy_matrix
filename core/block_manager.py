from __future__ import annotations
from typing import List, Any, Optional
import os
from enum import Enum

from templates.circuit import CircuitFactory


class BlockFileType(Enum):
    CIRCUIT = "cmc"
    BLACK_BOX = "cmb"
    REPEAT_BOX = "cmr"
# end class


class BlockFileEntry:
    def __init__(self, name: str, path_parts: List[str], block_type: BlockFileType):
        self.name: str = name
        self.path_parts: List[str] = path_parts
        self.type: BlockFileType = block_type
    # end def

    def __str__(self):
        return f"Block(type={self.type.name}, name={self.name}, path='{'.'.join(self.path_parts)}')"
    # end def
# end class


class BlockManager:
    def __init__(self, base_dir: str):
        self.__base_dir = base_dir
        self.__block_entries: List[BlockFileEntry] = list()
    # end def

    @staticmethod
    def _split_all(path):
        all_parts = []
        while True:
            parts = os.path.split(path)
            if parts[0] == path:  # sentinel for absolute paths
                all_parts.insert(0, parts[0])
                break
            elif parts[1] == path:  # sentinel for relative paths
                all_parts.insert(0, parts[1])
                break
            else:
                path = parts[0]
                all_parts.insert(0, parts[1])
            # end if
        return all_parts
    # end def

    def scan_dir(self):
        # Get the list of all files in directory tree at given path
        found_names: List[str] = list()
        file_types = set(item.value for item in BlockFileType)

        for (dir_path, dir_names, file_names) in os.walk(self.__base_dir, followlinks=True):
            for fn in file_names:
                name, ext = os.path.splitext(fn)

                if name not in found_names:
                    found_names.append(name)

                    ext = ext[1:]

                    if ext in file_types:  # Valid file extension
                        file = os.path.join(dir_path, fn)
                        path_parts = self._split_all(file)
                        self.__block_entries.append(BlockFileEntry(name, path_parts[1:-1], BlockFileType(ext)))
                    # end if
                else:
                    print(f"Name '{name}' was found more than once. Only the first occurrence will be available.")
                # end if
            # end for
        # end for
    # end def

    def store(self, box: Any, name: str, overwrite: bool = False) -> None:
        from templates.box import BlackBoxFactory, RepeatBoxFactory

        name_already_exists = name in [entry.name for entry in self.__block_entries]

        if overwrite or not name_already_exists:
            block_type: Optional[BlockFileType] = None

            if type(box) is CircuitFactory:
                block_type = BlockFileType.CIRCUIT

            elif type(box) is BlackBoxFactory:
                block_type = BlockFileType.BLACK_BOX

            elif type(box) is RepeatBoxFactory:
                block_type = BlockFileType.REPEAT_BOX
            # end if

            if block_type is not None:
                box.store(f"{os.path.join(self.__base_dir, name)}.{block_type.value}")

                if overwrite:
                    print(f"Element '{name}'' overwritten.")
                # end if
            # end if
        else:
            print(f"Name '{name}' already exists. Cannot store the element under this name.")
        # end if
    # end def

    def load(self, name: str) -> Any:  # Don't specify a return type since we want to return values of different types
        from templates.box import BlackBoxFactory, RepeatBoxFactory

        for entry in self.__block_entries:
            if entry.name == name:
                fn = f"{os.path.join(self.__base_dir, entry.name)}.{entry.type.value}"

                if entry.type is BlockFileType.CIRCUIT:
                    return CircuitFactory().load(fn)

                elif entry.type is BlockFileType.BLACK_BOX:
                    return BlackBoxFactory().load(fn)

                elif entry.type is BlockFileType.REPEAT_BOX:
                    return RepeatBoxFactory().load(fn)
                # end if
            # end if
        # end for
    # end def
# end class
