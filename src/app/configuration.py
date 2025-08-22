import os
import tomllib
from pathlib import Path
from typing import Any, Dict


class Configuration:
    def __init__(self, config_file="tests/resources/config.toml") -> None:
        self.config_file: str = config_file
        self.config: Dict[str, Any] = {}
        self._load_config()

    def _load_config(self) -> None:
        config_path = Path(self.config_file)
        if not config_path.exists():
            raise FileNotFoundError(
                f"Configuration file '{self.config_file}' not found."
            )
        try:
            with open(self.config_file, "rb") as f:
                self.config = tomllib.load(f)
        except tomllib.TOMLDecodeError as e:
            raise ValueError(f"Error decoding TOML file: {e}")

    @property
    def token(self) -> str:
        if "github-pat" in self.config.get("github", {}):
            return self.config["github"]["github-pat"]
        else:
            return os.getenv("GITHUB_PAT").strip()

    @property
    def owner(self) -> str:
        return self.config.get("github", {}).get("owner")
