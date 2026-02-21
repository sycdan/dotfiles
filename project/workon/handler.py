import logging
import subprocess
from pathlib import Path

from project.workon.command import Workon
from project.workon.pick.command import Pick
from wsl.activate.command import Activate
from wsl.create.command import Create
from wsl.find.command import Find
from wsl.list.command import List

logger = logging.getLogger(__name__)

PROJECTS_DIR = Path.home() / "Projects"


def handle(command: Workon, *wsl_args: str) -> None:
  logger.debug(f"Handling {command=}")

  pick_result = Pick(query=command.name).execute()
  if not pick_result.path:
    if not command.create:
      raise RuntimeError(f"No repos match {command.name!r}")

    new_repo = PROJECTS_DIR / command.name
    logger.info(f"Creating new repo at {new_repo}")
    new_repo.mkdir(parents=True)  # fail if it already exists somehow
    subprocess.run(["git", "init", str(new_repo)], check=True)
    pick_result = Pick.Result(path=new_repo.as_posix())

  repo = Path(pick_result.path)
  # Pass the Windows path as-is; wsl/find and wsl/create convert it via wslpath inside WSL
  win_path = repo.as_posix()
  logger.debug(f"Windows path for {repo.name!r}: {win_path!r}")

  distro = Find(origin=win_path).execute().distro
  if not distro:
    if repo.name in List().execute().distros:
      logger.warning(f"Distro {repo.name!r} exists but origin didn't match — using it anyway")
      distro = repo.name
    else:
      logger.info(f"No existing distro found, creating {repo.name!r}")
      distro = Create(name=repo.name, origin=win_path).execute().distro

  Activate(name=distro, project=repo.name).execute(*wsl_args)
