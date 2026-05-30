import json
import logging
import os
from pathlib import Path
from typing import Tuple

logger = logging.getLogger("mealie-mcp")

UPLOAD_DIR_ENV = "MEALIE_MCP_UPLOAD_DIR"
UPLOAD_MAX_BYTES_ENV = "MEALIE_MCP_UPLOAD_MAX_BYTES"
DEFAULT_UPLOAD_MAX_BYTES = 50 * 1024 * 1024  # 50 MiB


class UploadPathError(ValueError):
    """Raised when a client-supplied upload path is rejected."""


def _max_upload_bytes() -> int:
    raw = os.getenv(UPLOAD_MAX_BYTES_ENV)
    if not raw:
        return DEFAULT_UPLOAD_MAX_BYTES
    try:
        value = int(raw)
    except ValueError as e:
        raise UploadPathError(
            f"{UPLOAD_MAX_BYTES_ENV} must be an integer byte count, got {raw!r}"
        ) from e
    if value <= 0:
        raise UploadPathError(
            f"{UPLOAD_MAX_BYTES_ENV} must be positive, got {value}"
        )
    return value


def _upload_root() -> Path:
    raw = os.getenv(UPLOAD_DIR_ENV)
    if not raw:
        raise UploadPathError(
            "File-path uploads are disabled. Set "
            f"{UPLOAD_DIR_ENV} to an allowlisted directory on the server "
            "host to enable them. Anything readable from that directory by "
            "the server process becomes reachable via the MCP tool surface."
        )
    root = Path(raw).expanduser().resolve(strict=False)
    if not root.is_dir():
        raise UploadPathError(
            f"{UPLOAD_DIR_ENV}={raw!r} does not exist or is not a directory."
        )
    return root


def read_upload_file(path_str: str) -> Tuple[bytes, str]:
    """Read a client-supplied file path under the configured upload sandbox.

    Returns ``(data, filename)``. Raises ``UploadPathError`` if the path is
    outside the sandbox, traverses a symlink that escapes it, exceeds the
    size limit, or the sandbox is not configured.
    """
    root = _upload_root()
    candidate = Path(path_str).expanduser()
    if not candidate.is_absolute():
        candidate = root / candidate
    # ``resolve(strict=True)`` dereferences symlinks and requires the file to
    # exist; combined with the prefix check below this also blocks symlinks
    # that point outside the sandbox.
    try:
        resolved = candidate.resolve(strict=True)
    except FileNotFoundError as e:
        raise UploadPathError(f"File not found under {root}: {path_str!r}") from e

    try:
        resolved.relative_to(root)
    except ValueError as e:
        raise UploadPathError(
            f"Refusing to read {path_str!r}: resolved path {resolved} is "
            f"outside the upload sandbox {root}."
        ) from e

    if not resolved.is_file():
        raise UploadPathError(f"Not a regular file: {resolved}")

    size = resolved.stat().st_size
    limit = _max_upload_bytes()
    if size > limit:
        raise UploadPathError(
            f"File {resolved.name} is {size} bytes, exceeds limit of {limit} bytes "
            f"(configurable via {UPLOAD_MAX_BYTES_ENV})."
        )

    data = resolved.read_bytes()
    return data, resolved.name


def format_error_response(error_message: str) -> str:
    """Format error responses consistently as JSON strings."""
    error_response = {"success": False, "error": error_message}
    return json.dumps(error_response)


def format_api_params(params: dict) -> dict:
    """Formats list and None values in a dictionary for API parameters."""
    output = {}
    for k, v in params.items():
        if v is None:
            continue
        if isinstance(v, list):
            output[k] = ",".join(v)
        else:
            output[k] = v
    return output
