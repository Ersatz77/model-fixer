import argparse
import logging
import pathlib

from model_fixer.json_model import JsonModel
from model_fixer.logging import setup_logging


def run():
    parser = argparse.ArgumentParser(
        prog="Model Fixer", description="Fixes model paths for Minecraft Java 1.20"
    )

    parser.add_argument(
        "model_folder",
        type=pathlib.Path,
        help="A path to a folder containing Minecraft Java models",
    )

    parser.add_argument(
        "prefix_with",
        type=str,
        choices=("block", "item"),
        help="The folder to prefix texture paths with",
    )

    parser.add_argument(
        "--indent",
        type=int,
        default=4,
        help="Indentation to use when rewriting the model files",
    )

    parser.add_argument("--log", type=str, default="INFO", help="Set the log level")

    args = parser.parse_args()
    setup_logging(args.log)

    model_folder: pathlib.Path = args.model_folder
    path_prefix: str = args.prefix_with
    indent: int = args.indent

    log: logging.Logger = logging.getLogger(name=__name__)

    # Interate over every Json file in the directory and try to fix its texure paths
    for model_file in model_folder.rglob("*.json"):
        try:
            model: JsonModel = JsonModel.from_file(model_file)
            model.try_fix_textures(path_prefix)
            model.to_file(model_file, indent)

            log.info(f"Fixed {model_file.name}")

        except KeyError as ex:
            log.warning(f"Skipped {model_file.name}: '{ex.args[0]}' doesn't exist")

        except Exception as ex:
            log.warning(f"Skipped {model_file.name}: {ex}")
