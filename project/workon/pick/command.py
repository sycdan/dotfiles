from dataclasses import dataclass, field


@dataclass
class Pick:
  """Interactively select a git repo from ~/Projects."""

  @dataclass
  class Result:
    path: str = field(
      default="", doc="Full path to the chosen repo, or empty if cancelled"
    )

  def execute(self) -> "Pick.Result":
    from project.workon.pick.handler import handle

    return handle(self)
