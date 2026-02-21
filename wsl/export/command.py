from dataclasses import dataclass, field

from scaf.rules import values_must_fit


@dataclass
class Export:
  """Export a WSL distro to a .tar image in C:/wsl-images/."""

  distro: str = field(doc="Distro name to export")
  name: str = field(default="", doc="Output filename (without .tar); defaults to the distro name")

  def __post_init__(self):
    values_must_fit(self)

  @dataclass
  class Result:
    path: str = field(default="", doc="Absolute path to the exported .tar file")

  def execute(self) -> "Export.Result":
    from wsl.export.handler import handle

    return handle(self)
