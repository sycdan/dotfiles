import logging
from pathlib import Path

from project.workon.command import Workon

logger = logging.getLogger(__name__)

ACTION_DIR = Path(__file__).parent


def handle(command: Workon) -> Workon.Result:
  logger.debug(f"Handling {command=}")
  logger.error(f"Logic for the Workon command must be defined in {ACTION_DIR.as_posix()}/{Path(__file__).name}")
  # TODO
  """
   wsl --import projectname C:\wsl\projectname C:\wsl-images\ubuntu24_2026-02-19.tar
  """
  return Workon.Result()
