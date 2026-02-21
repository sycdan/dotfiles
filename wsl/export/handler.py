import logging
import subprocess
from pathlib import Path

from wsl.export.command import Export

logger = logging.getLogger(__name__)

IMAGES_DIR = Path("C:/wsl-images")


def handle(command: Export) -> Export.Result:
  IMAGES_DIR.mkdir(parents=True, exist_ok=True)
  name = command.name or command.distro
  out_path = IMAGES_DIR / f"{name}.tar"
  logger.info(f"Exporting distro {command.distro!r} → {out_path}")
  subprocess.run(
    ["wsl", "--export", command.distro, str(out_path)],
    check=True,
    capture_output=True,
    timeout=300,
  )
  logger.info(f"Exported to {out_path}")
  return Export.Result(path=out_path.as_posix())
