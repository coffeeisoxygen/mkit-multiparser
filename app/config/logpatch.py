def redact_password(record):
    if "password" in record["extra"]:
        record["extra"]["password"] = "***MASKED***"
