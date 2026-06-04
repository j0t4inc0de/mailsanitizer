"""
MX record checker — CleanMail by Samod.

Uses ``dnspython`` to resolve MX records for a domain with a 5-second
timeout.  Results are cached in-memory for 1 hour to avoid redundant
DNS queries during bulk validation runs.
"""

import logging
import threading
import time

import dns.resolver

logger = logging.getLogger(__name__)

# In-memory cache: domain → (has_mx: bool, expires_at: float)
_mx_cache: dict[str, tuple[bool, float]] = {}
_cache_lock = threading.Lock()

# Cache TTL in seconds (1 hour)
_CACHE_TTL = 3600

# DNS query timeout in seconds
_DNS_TIMEOUT = 5.0


def _is_cache_valid(domain: str) -> tuple[bool, bool]:
    """
    Check if a cached entry exists and is still valid.

    Returns:
        (hit, result) — ``hit`` is True when a valid cache entry exists;
        ``result`` is the cached boolean value.
    """
    with _cache_lock:
        entry = _mx_cache.get(domain)
        if entry is not None:
            value, expires_at = entry
            if time.monotonic() < expires_at:
                return True, value
            # Expired — remove stale entry
            del _mx_cache[domain]
    return False, False


def _set_cache(domain: str, value: bool) -> None:
    """Store a result in the cache with the configured TTL."""
    with _cache_lock:
        _mx_cache[domain] = (value, time.monotonic() + _CACHE_TTL)


def has_mx_record(domain: str) -> bool:
    """
    Return ``True`` if the domain has at least one MX record.

    Performs a DNS MX query with a 5-second timeout.  Results are cached
    for 1 hour so repeated checks for the same domain are free.

    Args:
        domain: The domain to query (e.g. ``"gmail.com"``).

    Returns:
        ``True`` when the domain has valid MX records.
    """
    domain = domain.strip().lower()

    # 1. Check cache
    hit, cached_value = _is_cache_valid(domain)
    if hit:
        return cached_value

    # 2. Perform DNS lookup
    try:
        resolver = dns.resolver.Resolver()
        resolver.lifetime = _DNS_TIMEOUT
        resolver.timeout = _DNS_TIMEOUT
        answers = resolver.resolve(domain, "MX")
        result = len(answers) > 0
    except (
        dns.resolver.NoAnswer,
        dns.resolver.NXDOMAIN,
        dns.resolver.NoNameservers,
        dns.resolver.Timeout,
        dns.exception.DNSException,
    ):
        result = False
    except Exception:
        logger.exception("Error inesperado al verificar MX para %s", domain)
        result = False

    # 3. Cache and return
    _set_cache(domain, result)
    return result
