import logging
import subprocess

from wsl.path.get.query import Get

logger = logging.getLogger(__name__)


def handle(command: Get) -> Get.Result:
  logger.info(f"Converting {command.win_path!r} to WSL path")
  cmd = ["wsl"]
  if command.distro:
    cmd += ["-d", command.distro]
  cmd += ["--", "wslpath", command.win_path]
  result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
  if result.returncode != 0:
    logger.warning(f"wslpath failed: {result.stderr.strip()!r}")
    return Get.Result()
  wsl_path = result.stdout.strip()
  logger.debug(f"Result: {wsl_path!r}")
  return Get.Result(success=True, wsl_path=wsl_path)
