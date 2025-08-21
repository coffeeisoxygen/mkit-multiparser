import inspect
import logging
import re
from pathlib import Path

import yaml
from app.config.core import get_settings
from loguru import logger
from loguru_config import LoguruConfig


class InterceptHandler(logging.Handler):
    def emit(self, record: logging.LogRecord) -> None:
        level: str | int
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        frame, depth = inspect.currentframe(), 0
        while frame and (depth == 0 or frame.f_code.co_filename == logging.__file__):
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )


logging.basicConfig(handlers=[InterceptHandler()], level=0, force=True)


logyamlpath = Path(__file__).parent.parent.parent / "logconfig.yaml"

# --- Bagian yang diperbarui ---
# Baca file YAML sebagai string
yaml_content = logyamlpath.read_text()
# Uraikan string YAML menjadi kamus Python
config_dict = yaml.safe_load(yaml_content)

# Dapatkan pola regex dan hapus dari kamus konfigurasi utama
# Gunakan .pop() untuk mengambil kunci dan menghapusnya, mencegah TypeError pada LoguruConfig
masking_setup = config_dict.pop("masking", {})

# Sekarang, inisialisasi LoguruConfig HANYA dengan bagian konfigurasi Loguru yang valid
logconfig = LoguruConfig.load(config_dict)
# --- Akhir Bagian yang diperbarui ---

overenv = get_settings().APP_ENV.value
masking_enabled = overenv == "PRODUCTION"


def hide_sensitive_data(record) -> None:
    """Prevent leaking sensitive data using dynamic regex and mask_fields in PRODUCTION."""
    if masking_enabled:
        mask_regex = masking_setup.get("mask_regex", {})
        default_mask = masking_setup.get("default_mask", "XXXX-XXXX-XXXX-XXXX")
        mask_fields = masking_setup.get("mask_fields", [])

        # Mask message by regex
        record["message"] = re.sub(
            mask_regex.get("credit_card", r""),
            default_mask,
            record["message"],
        )
        record["message"] = re.sub(
            mask_regex.get("email", r""),
            default_mask,
            record["message"],
        )

        # Mask sensitive fields in extra
        if "extra" in record and isinstance(record["extra"], dict):
            for field in mask_fields:
                if field in record["extra"]:
                    record["extra"][field] = default_mask


# ini adalah Main config nya
logger.configure(extra={"env": overenv}, patcher=hide_sensitive_data)
