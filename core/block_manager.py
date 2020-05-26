from __future__ import annotations
from typing import List, Any, Optional
import os
from enum import Enum
import pykwalify.core

from templates.block import BlockType
from templates.circuit import CircuitFactory
from templates.box import BlackBoxFactory, RepeatBoxFactory


# Overwrite the original implementation, since it doesn't support other filename extension. This problem was solved by pykwalifire, but I didn't succeed to install it.
class MyCore(pykwalify.core.Core):
    def __init__(self, source_file=None, schema_files=None, source_data=None, schema_data=None, extensions=None, strict_rule_validation=False,
                 fix_ruby_style_regex=False, allow_assertions=False,):
        """
        :param extensions:
            List of paths to python files that should be imported and available via 'func' keywork.
            This list of extensions can be set manually or they should be provided by the `--extension`
            flag from the cli. This list should not contain files specified by the `extensions` list keyword
            that can be defined at the top level of the schema.
        """
        import yaml
        from pykwalify.errors import CoreError
        import logging
        log = logging.getLogger(__name__)
        logging.disable(logging.CRITICAL)

        if schema_files is None:
            schema_files = []
        if extensions is None:
            extensions = []

        log.debug(u"source_file: %s", source_file)
        log.debug(u"schema_file: %s", schema_files)
        log.debug(u"source_data: %s", source_data)
        log.debug(u"schema_data: %s", schema_data)
        log.debug(u"extension files: %s", extensions)

        self.source = None
        self.schema = None
        self.validation_errors = None
        self.validation_errors_exceptions = None
        self.root_rule = None
        self.extensions = extensions
        self.errors = []
        self.strict_rule_validation = strict_rule_validation
        self.fix_ruby_style_regex = fix_ruby_style_regex
        self.allow_assertions = allow_assertions

        if source_file is not None:
            if not os.path.exists(source_file):
                raise CoreError(u"Provided source_file do not exists on disk: {0}".format(source_file))

            with open(source_file, "r") as stream:
                self.source = yaml.safe_load(stream)

        if not isinstance(schema_files, list):
            raise CoreError(u"schema_files must be of list type")

        # Merge all schema files into one single file for easy parsing
        if len(schema_files) > 0:
            schema_data = {}
            for f in schema_files:
                if not os.path.exists(f):
                    raise CoreError(u"Provided source_file do not exists on disk : {0}".format(f))

                with open(f, "r") as stream:
                    data = yaml.safe_load(stream)
                    if not data:
                        raise CoreError(u"No data loaded from file : {0}".format(f))

                    for key in data.keys():
                        if key in schema_data.keys():
                            raise CoreError(u"Parsed key : {0} : two times in schema files...".format(key))

                    schema_data = dict(schema_data, **data)

            self.schema = schema_data

        # Nothing was loaded so try the source_data variable
        if self.source is None:
            log.debug(u"No source file loaded, trying source data variable")
            self.source = source_data
        if self.schema is None:
            log.debug(u"No schema file loaded, trying schema data variable")
            self.schema = schema_data

        # Test if anything was loaded
        if self.source is None:
            raise CoreError(u"No source file/data was loaded")
        if self.schema is None:
            raise CoreError(u"No schema file/data was loaded")

        # Merge any extensions defined in the schema with the provided list of extensions from the cli
        for f in self.schema.get('extensions', []):
            self.extensions.append(f)

        if not isinstance(self.extensions, list) and all(isinstance(e, str) for e in self.extensions):
            raise CoreError(u"Specified extensions must be a list of file paths")

        self._load_extensions()

        if self.strict_rule_validation:
            log.info("Using strict rule keywords validation...")
# end class


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
    def __init__(self, base_dir: str, schema_filename: str = None):
        self.__base_dir = base_dir
        self.__block_entries: List[BlockFileEntry] = list()
        self.__schema_filename: Optional[str] = schema_filename
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

        name_already_exists = False  # name in [entry.name for entry in self.__block_entries]
        entry_: BlockFileEntry = None

        for entry in self.__block_entries:
            if entry.name == name:
                name_already_exists = True
                entry_ = entry
                break
            # end if
        # end for

        if overwrite or not name_already_exists:
            box_type: Optional[BlockFileType] = None

            if type(box) is CircuitFactory:
                box_type = BlockFileType.CIRCUITf

            elif type(box) is BlackBoxFactory:
                box_type = BlockFileType.BLACK_BOX

            elif type(box) is RepeatBoxFactory:
                box_type = BlockFileType.REPEAT_BOX
            # end if

            if box_type is not None:
                if not name_already_exists:
                    # Store to base directory
                    box.store(f"{os.path.join(self.__base_dir, name)}.{box_type.value}")

                else:
                    # Overwrite file in original location (of course)
                    box.store(f"{os.path.join(self.__base_dir, *entry_.path_parts, name)}.{box_type.value}")

                    if overwrite:
                        print(f"Element '{name}' overwritten.")
                    # end if
                # end if
            # end if
        else:
            print(f"Name '{name}' already exists. Cannot store the element under this name.")
        # end if
    # end def

    def get_filename_from_name(self, name: str) -> Optional[str]:
        for entry in self.__block_entries:
            if entry.name == name:
                fn = f"{os.path.join(self.__base_dir, *entry.path_parts, entry.name)}.{entry.type.value}"
                return fn
            # end if
        # end for

        return None
    # end def

    def load(self, name: str) -> Any:  # Don't specify a return type since we want to return values of different types
        from templates.box import BlackBoxFactory, RepeatBoxFactory

        box: Optional[Any] = None

        for entry in self.__block_entries:
            if entry.name == name:
                file_okay = True
                fn = f"{os.path.join(self.__base_dir, *entry.path_parts, entry.name)}.{entry.type.value}"

                if self.__schema_filename is not None:
                    c = MyCore(source_file=fn, schema_files=[self.__schema_filename])

                    try:
                        c.validate(raise_exception=True)

                    except RuntimeError as e:
                        file_okay = False
                        print(e)
                    # end try
                # end if

                if file_okay:
                    if entry.type is BlockFileType.CIRCUIT:
                        box = CircuitFactory().load(fn)

                    elif entry.type is BlockFileType.BLACK_BOX:
                        box = BlackBoxFactory().load(fn, name=name)

                    elif entry.type is BlockFileType.REPEAT_BOX:
                        box = RepeatBoxFactory().load(fn, name=name)
                    # end if

                    if not self.cross_check(box):
                        box = None
                    # end if
                # end if

                break
            # end if
        # end for

        return box
    # end def

    @staticmethod
    def cross_check(box: Any) -> bool:
        # General checks
        for b, block in enumerate(box.blocks):
            if block.type is BlockType.VAL_CONST:
                if not hasattr(block, "value"):
                    print(f"'blocks[{b}].value' needs to be set.")
                    return False
                # end if
            # end if

            elif block.type is BlockType.BOX:
                if not hasattr(block, "box_name"):
                    print(f"'blocks[{b}].box_name' needs to be set.")
                    return False
                # end if
            # end if
        # end for

        # Special checks
        if type(box) is CircuitFactory:
            if not hasattr(box, "conns"):
                print(f"'conns' needs to exist.")
                return False
            else:
                if len(box.conns) < 1:
                    print(f"length('conns') needs to be >= 1 (at least 1 connection to the drawer).")
                    return False
                # end if
            # end if

        elif type(box) is BlackBoxFactory or type(box) is RepeatBoxFactory:
            if box.n_in is None:
                print(f"'box.n_in' needs to be set.")
                return False
            # end if

            if box.n_out is None:
                print(f"'box.n_out' needs to be set.")
                return False
            # end if

            if not hasattr(box, "bonds"):
                print(f"'bonds' needs to exist.")
                return False
            else:
                if len(box.bonds) < 2:
                    print(f"length('bonds') needs to be >= 2 (at least 1 in and 1 out).")
                    return False
                # end if
            # end if
        # end if

        return True
    # end def
# end class
