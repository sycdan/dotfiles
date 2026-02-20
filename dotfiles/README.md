# Git Config

## Setup

Clone to a central location:

```bash
git clone https://github.com/sycdan/dotfiles.git ~/dotfiles
```

Copy the config template file in your home folder:

```bash
cp ~/dotfiles/git/config_identity-template ~/.gitconfig
```

And set the email applicable to this domain.

## Hooks

To register the hooks for all repos:

```bash
git config --global core.hooksPath ~/dotfiles/git/hooks
```

To register them for only one, run the same command just without the `--global` part, from within a repo folder.

Make the scripts executable:

```bash
chmod +x ~/dotfiles/git/hooks/pre-commit
```

## Formatting

Any staged files will be formatted based on their extension:

- `.cs` - [CSharpier](https://csharpier.com/docs/Configuration)
- `.py` - [Ruff](https://pypi.org/project/ruff/#configuration)

Formatting can be disabled for specific file extensions by adding them to an environment variable:

```bash
export GIT__HOOKS__SKIPFORMAT=cs,py
```
