from pathlib import Path

import yaml
from app.utils.mlogg.utils import masking_patcher
from loguru import logger
from loguru_config import LoguruConfig

logconfigpath = Path(__file__).parent.parent.parent.parent / "logconfig.yaml"

with open(logconfigpath, encoding="utf-8") as file:
    config_dict = yaml.safe_load(file)

dict_maskingsetup = config_dict.pop("masking", {})


def patcher_wrapper(record):
    """Wrapper agar masking config bisa diakses oleh patcher."""
    masking_patcher(record, dict_maskingsetup)


LoguruConfig.load(config_or_file=config_dict)
LoguruConfig(extra={"env": "test masking"}, patcher=patcher_wrapper).configure()


def main():
    logger.info("test with credit card pattern in meesage 4532-1234-5678-9012")
    logger.info("test with email card pattern in message john.doe@example.com")
    logger.info("test with password pattern in message password: 123456")
    logger.info("test with token pattern in message token: 1903907190712")
    # sampling jika ada di field extra
    logger.bind(
        extra={
            "user_id": "12345",
            "email": "john.doe@example.com",
            "card": "4532-1234-5678-9012",
            "token": "1903907190712",
            "password": "Password123456",
        }
    ).info("Payment processed successfully.")


if __name__ == "__main__":
    main()
