import inspect
import logging
import re
from pathlib import Path

import yaml
from loguru import logger
from loguru_config import LoguruConfig

from app.config.core import get_settings


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
regex_patterns = config_dict.pop("regex_patterns", {})

# Sekarang, inisialisasi LoguruConfig HANYA dengan bagian konfigurasi Loguru yang valid
logconfig = LoguruConfig.load(config_dict)
# --- Akhir Bagian yang diperbarui ---


def hide_sensitive_data(record) -> None:
    """Prevent from leaking sensitive data using dynamic regex."""
    # Gunakan pola regex yang dimuat dari kamus regex_patterns
    record["message"] = re.sub(
        regex_patterns.get(
            "credit_card", r""
        ),  # Gunakan .get() untuk keamanan jika kunci tidak ada
        "XXXX-XXXX-XXXX-XXXX",
        record["message"],
    )
    record["message"] = re.sub(
        regex_patterns.get("email", r""),  # Gunakan .get() untuk keamanan
        "***@***.***",
        record["message"],
    )


overenv = get_settings().APP_ENV.value
logger.configure(extra={"env": overenv}, patcher=hide_sensitive_data)
