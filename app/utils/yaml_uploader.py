from pathlib import Path
from typing import Any

import yaml

from app.exception import FileIndexInUseError, FileNotFoundError, FormatFileError


class YamlDataUploader:
    def __init__(self, key_name: str, id_field: str, model: type, logger: Any):
        self.key_name = key_name
        self.id_field = id_field
        self.model = model
        self.logger = logger

    def check_duplicates(self, items: list[dict]) -> list[str]:
        seen = set()
        duplicates = []
        for item in items:
            item_id = item.get(self.id_field)
            if item_id in seen:
                duplicates.append(item_id)
            else:
                seen.add(item_id)
        return duplicates

    def load_and_validate(self, yaml_path: Path) -> list[Any]:
        with self.logger.contextualize(path=yaml_path, operation="load_yaml"):
            if not yaml_path.exists():
                self.logger.error("YAML file not found", path=str(yaml_path))
                raise FileNotFoundError(f"YAML file not found: {yaml_path}")

            try:
                with yaml_path.open("r", encoding="utf-8") as f:
                    data = yaml.safe_load(f)
            except yaml.YAMLError as e:
                self.logger.exception(
                    "Failed to parse YAML file", error=str(e), path=str(yaml_path)
                )
                raise FormatFileError("Failed to parse YAML file") from e

            if not isinstance(data, dict) or self.key_name not in data:
                self.logger.error(
                    f"YAML must contain '{self.key_name}' key", path=str(yaml_path)
                )
                raise FileIndexInUseError(f"YAML must contain '{self.key_name}' key")

            items = data[self.key_name]
            if not isinstance(items, list):
                self.logger.error(
                    f"'{self.key_name}' must be a list", path=str(yaml_path)
                )
                raise FileIndexInUseError(f"'{self.key_name}' must be a list")

            duplicates = self.check_duplicates(items)
            if duplicates:
                self.logger.error(
                    "Duplicate IDs found", duplicates=duplicates, path=str(yaml_path)
                )
                raise ValueError(f"Duplicate {self.id_field}s found: {duplicates}")

            validated_items = []
            for i, item in enumerate(items):
                try:
                    validated = self.model(**item)
                    validated_items.append(validated)
                except FileIndexInUseError as e:
                    self.logger.exception(
                        "Validation failed", index=i, item=item, error=str(e)
                    )
                    raise ValueError(f"Validation failed at index {i}: {e}") from e

            return validated_items
