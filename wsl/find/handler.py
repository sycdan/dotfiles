import logging
import shlex
import subprocess

from wsl.find.command import Find
from wsl.list.command import List

logger = logging.getLogger(__name__)

_PATH = "export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"


def _distro_has_origin(distro: str, wsl_path: str) -> bool:
  # Pass the script via stdin (bash -s) to avoid Windows command-line
  # argument quoting: wsl.exe mangles $(...) substitutions in -c scripts.
  # Use find | while (no process substitution) for portability.
  script = f"""\
{_PATH}
find "$HOME/projects" -maxdepth 1 -mindepth 1 -type d 2>/dev/null | while IFS= read -r d; do
  git -C "$d" remote -v 2>/dev/null | grep -qF {shlex.quote(wsl_path)} && echo found && break
done
"""
  try:
    result = subprocess.run(
      ["wsl", "-d", distro, "--", "bash", "-s"],
      input=script.encode("utf-8"),  # binary: avoids Windows \n→\r\n conversion
      capture_output=True,
      timeout=15,
    )
    stdout = result.stdout.decode("utf-8")
    stderr = result.stderr.decode("utf-8")
    logger.debug(f"{distro}: stdout={stdout.strip()!r} stderr={stderr.strip()!r}")
    return stdout.strip() == "found"
  except Exception as e:
    logger.debug(f"{distro}: check failed: {e}")
    return False


def handle(command: Find) -> Find.Result:
  logger.debug(f"Searching for origin {command.origin!r}")
  from wsl.path.get.query import Get

  wsl_path = Get(win_path=command.origin).execute().wsl_path
  if not wsl_path:
    logger.warning(f"Could not convert {command.origin!r} to a WSL path")
    return Find.Result()
  logger.debug(f"WSL path: {wsl_path!r}")

  distros = List().execute().distros
  logger.info(f"Checking {len(distros)} distros: {distros}")
  for distro in distros:
    logger.debug(f"Checking {distro}")
    if _distro_has_origin(distro, wsl_path):
      logger.info(f"Found match: {distro}")
      return Find.Result(distro=distro)
  logger.info("No matching distro found")
  return Find.Result()
