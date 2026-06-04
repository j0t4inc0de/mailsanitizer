"""
Disposable domain checker — CleanMail by Samod.

Loads a list of known disposable/temporary email domains from
``data/disposable_domains.json`` into a ``frozenset`` at module import time
for O(1) lookups.
"""

import json
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

# Path to the JSON data file (relative to the project root)
_DATA_FILE = Path(__file__).resolve().parent.parent.parent / "data" / "disposable_domains.json"

# Load once at import time
try:
    with open(_DATA_FILE, "r", encoding="utf-8") as fh:
        _DISPOSABLE_DOMAINS: frozenset[str] = frozenset(
            domain.strip().lower() for domain in json.load(fh)
        )
    logger.info("Cargados %d dominios desechables.", len(_DISPOSABLE_DOMAINS))
except FileNotFoundError:
    logger.warning(
        "Archivo de dominios desechables no encontrado: %s — "
        "la verificación de desechables estará desactivada.",
        _DATA_FILE,
    )
    _DISPOSABLE_DOMAINS = frozenset()
except json.JSONDecodeError as exc:
    logger.error("Error al parsear %s: %s", _DATA_FILE, exc)
    _DISPOSABLE_DOMAINS = frozenset()


def is_disposable(domain: str) -> bool:
    """
    Return ``True`` if the given domain is a known disposable email provider.

    Args:
        domain: The email domain to check (e.g. ``"tempmail.com"``).

    Returns:
        ``True`` when the domain appears in the disposable list.
    """
    return domain.strip().lower() in _DISPOSABLE_DOMAINS
