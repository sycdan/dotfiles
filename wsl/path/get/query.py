from dataclasses import dataclass, field


@dataclass
class Get:
  """Convert a Windows path to its WSL equivalent using wslpath."""

  win_path: str = field(doc="Windows path to convert (e.g. C:/Users/foo/bar)")
  distro: str = field(
    default="", doc="WSL distro to run wslpath in; defaults to the default WSL distro"
  )

  @dataclass
  class Result:
    success: bool = field(default=False, doc="Whether the conversion was successful")
    wsl_path: str = field(
      default="",
      doc="Converted WSL path (e.g. /mnt/c/Users/foo/bar), or empty on failure",
    )

  def execute(self) -> "Get.Result":
    from wsl.path.get.handler import handle

    return handle(self)
