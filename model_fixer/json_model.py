import json
import pathlib

from model_fixer.types import JsonObject


class JsonModel:
    """
    A wrapper around a dictionary that represents a Json model from Minecraft Java
    """

    def __init__(self, model: JsonObject):
        self._data: JsonObject = model

    @classmethod
    def from_file(cls, path: pathlib.Path) -> "JsonModel":
        """
        Create a `JsonModel` from a file
        """
        with open(path, "r") as file:
            return cls(json.load(file))

    def to_file(self, path: pathlib.Path, indent: int):
        """
        Write a `JsonModel` to a file
        """
        with open(path, "w") as file:
            file.write(self.to_json_str(indent))

    def try_fix_textures(self, path_prefix: str):
        """
        Fixes textures by adding `path_prefix` to the beginning of the path portion of the resource location
        """
        # Loop through every texture and fix the resource location if necessary
        textures: JsonObject = self._data["textures"]
        for key, resource_location in textures.items():
            # Require the resource location to be a string
            if not isinstance(resource_location, str):
                raise TypeError(f"The resource location for '{key}' must be a string")

            # Fix resource location if necessary
            parts: list[str] = resource_location.split(":")
            new_resource_location: str = ""
            match len(parts):
                case 1:
                    new_resource_location = self._format_resource_location(
                        namespace="minecraft", path=parts[0], path_prefix=path_prefix
                    )
                case 2:
                    new_resource_location = self._format_resource_location(
                        namespace=parts[0], path=parts[1], path_prefix=path_prefix
                    )
                case _:
                    raise ValueError(
                        f"'{resource_location}' is not a valid resource location"
                    )

            textures[key] = new_resource_location

    def _format_resource_location(
        self, *, namespace: str, path: str, path_prefix: str
    ) -> str:
        """
        Creates a resource location string out of the different parts

        Paths starting with `#` will be retured as is without a namespace
        """
        if path.startswith("#"):
            return path

        new_path: str = (
            path if path.startswith(("block/", "item/")) else f"{path_prefix}/{path}"
        )
        return f"{namespace}:{new_path}"

    def to_json_str(self, indent: int) -> str:
        """
        Return the model as a Json string
        """
        return json.dumps(self._data, indent=indent)
