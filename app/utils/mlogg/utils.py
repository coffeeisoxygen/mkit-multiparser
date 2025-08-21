import re
import traceback
from typing import Any

try:
    import stackprinter
except ImportError:
    stackprinter = None


def mask_message(msg: str, mask_regex: dict[str, str], mask_value: str) -> str:
    """Mask sensitive patterns in log message."""
    for pattern in mask_regex.values():
        msg = re.sub(pattern, mask_value, msg)
    return msg


def mask_extra(
    extra: dict[str, Any],
    mask_fields: list,
    mask_regex: dict[str, str],
    mask_value: str,
) -> dict[str, Any]:
    """Mask sensitive fields and patterns in extra dict, including nested dicts."""
    for field in mask_fields:
        if field in extra:
            extra[field] = mask_value
    for key, value in extra.items():
        if key not in mask_fields:
            if isinstance(value, dict):
                extra[key] = mask_extra(value, mask_fields, mask_regex, mask_value)
            elif isinstance(value, str):
                for pattern in mask_regex.values():
                    extra[key] = re.sub(pattern, mask_value, value)
    return extra


def masking_patcher(record: Any, masking: dict[str, Any]) -> None:
    """Apply masking to log record based on config."""
    if masking.get("enabled"):
        mask_value = masking.get("default_mask", "***")
        mask_fields = masking.get("mask_fields", [])
        mask_regex = masking.get("mask_regex", {})
        if masking.get("mask_message", True):
            record["message"] = mask_message(record["message"], mask_regex, mask_value)
        if masking.get("mask_extra", True):
            record["extra"] = mask_extra(
                record["extra"], mask_fields, mask_regex, mask_value
            )


def exception_patcher(record: Any, exception_format: dict[str, Any]) -> None:
    """Apply exception formatting to log record based on config."""
    if exception_format and exception_format.get("enabled"):
        exc = record.get("exception")
        if exc is not None:
            # Ganti style ke default jika diagnose tidak tersedia
            style = "default" if exception_format.get("diagnose") else None
            if exception_format.get("use_stackprinter") and stackprinter:
                record["extra"]["stack"] = stackprinter.format(exc, style=style)
            else:
                record["extra"]["stack"] = "\n" + "".join(
                    traceback.format_exception(type(exc), exc, exc.__traceback__)
                )


def traceback_patcher(record: Any, traceback_format: dict[str, Any]) -> None:
    """Inject traceback only if with_traceback=True in extra (explicit)."""
    # Pastikan extra selalu dict
    if "extra" not in record or not isinstance(record["extra"], dict):
        record["extra"] = {}
    if (
        traceback_format
        and traceback_format.get("enabled")
        and record["extra"].get("with_traceback") is True
    ):
        record["extra"]["traceback"] = "\n" + "".join(traceback.format_stack())
