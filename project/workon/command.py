from dataclasses import dataclass, field


@dataclass
class Workon:
  """Start a dev environment for a project."""

  name: str = field(doc="Project name; auto-selects if exactly one repo matches")
  create: bool = field(
    default=False, doc="Create a new repo in ~/Projects/<name> if no match is found"
  )
