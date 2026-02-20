import logging

from project.workon.command import Workon
from project.workon.pick.command import Pick

logger = logging.getLogger(__name__)


def handle(command: Workon) -> None:
  logger.debug(f"Handling {command=}")
  result = Pick().execute()
  if result.path:
    print(result.path)
