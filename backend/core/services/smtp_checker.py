"""
SMTP mailbox checker — CleanMail by Samod.

Performs an SMTP handshake against the mail server of a domain to verify
whether a specific mailbox exists, WITHOUT sending any real email.

The check simulates the first steps of the SMTP protocol:
    1. Connect to the MX server on port 25 (or 587 as fallback).
    2. Send EHLO to identify the client.
    3. Send MAIL FROM with a neutral probe address.
    4. Send RCPT TO with the target address.
    5. Interpret the server's 250/251 response as "mailbox exists".

Important policy decisions
--------------------------
- If the server refuses connection, times out, or actively blocks probing
  (many large providers do), the function returns ``True`` (we do NOT mark
  the email as invalid — it's "unverifiable", not "bad").
- A hard ``550``/``551``/``552``/``553`` SMTP rejection is the only signal
  treated as a definitive "mailbox does not exist".
- Results are cached for 30 minutes per full email address to avoid hammering
  the same server during bulk validation runs.

Dependencies
------------
- ``smtplib`` — Python standard library, no extra install required.
- ``dns.resolver`` — already a dependency via ``dnspython``.
"""

import logging
import smtplib
import socket
import threading
import time

import dns.resolver

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Cache: email → (exists: bool, expires_at: float)
# ---------------------------------------------------------------------------
_smtp_cache: dict[str, tuple[bool, float]] = {}
_smtp_cache_lock = threading.Lock()
_SMTP_CACHE_TTL = 1800  # 30 minutes

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
_SMTP_TIMEOUT = 10          # seconds per socket operation
_PROBE_FROM = "probe@cleanmail-verify.com"
_SMTP_PORTS = [25, 587]     # try both in order

# SMTP reply codes that definitively mean "mailbox does not exist"
_HARD_REJECT_CODES = {550, 551, 552, 553, 554}


# ---------------------------------------------------------------------------
# Cache helpers
# ---------------------------------------------------------------------------

def _cache_get(email: str) -> tuple[bool, bool]:
    """
    Return ``(hit, result)``.

    ``hit`` is True when a valid cached entry is present; ``result`` is the
    stored boolean.
    """
    with _smtp_cache_lock:
        entry = _smtp_cache.get(email)
        if entry is not None:
            value, expires_at = entry
            if time.monotonic() < expires_at:
                return True, value
            del _smtp_cache[email]
    return False, False


def _cache_set(email: str, value: bool) -> None:
    """Store a result in the cache."""
    with _smtp_cache_lock:
        _smtp_cache[email] = (value, time.monotonic() + _SMTP_CACHE_TTL)


# ---------------------------------------------------------------------------
# MX resolution helper (reuses dnspython already in the project)
# ---------------------------------------------------------------------------

def _get_mx_hosts(domain: str) -> list[str]:
    """
    Return a list of MX hostnames for ``domain``, sorted by priority.

    Returns an empty list if the domain has no MX records or the lookup fails.
    """
    try:
        resolver = dns.resolver.Resolver()
        resolver.lifetime = 5.0
        resolver.timeout = 5.0
        answers = resolver.resolve(domain, "MX")
        # Sort by preference (lower = higher priority)
        sorted_answers = sorted(answers, key=lambda r: r.preference)
        return [str(r.exchange).rstrip(".") for r in sorted_answers]
    except Exception:
        return []


# ---------------------------------------------------------------------------
# Core SMTP probe
# ---------------------------------------------------------------------------

def check_smtp_mailbox(email: str, domain: str) -> bool:
    """
    Verify whether ``email`` is accepted by the domain's mail server.

    Performs a lightweight SMTP handshake (EHLO → MAIL FROM → RCPT TO) and
    interprets the server's response to the ``RCPT TO`` command.

    Returns
    -------
    ``True``  → Mailbox likely exists OR server is unverifiable (safe default).
    ``False`` → Server returned a hard rejection (5xx) for this specific address.

    Args:
        email:  The full email address to verify (e.g. ``"user@example.com"``).
        domain: The domain portion of the email (e.g. ``"example.com"``).
    """
    # 1. Check cache
    hit, cached = _cache_get(email)
    if hit:
        return cached

    # 2. Resolve MX records
    mx_hosts = _get_mx_hosts(domain)
    if not mx_hosts:
        # No MX hosts found at this stage means has_mx_record() already caught
        # this — but guard here anyway. Treat as unverifiable → safe default.
        _cache_set(email, True)
        return True

    # 3. Try each MX host on each port
    result = _probe_smtp(email, mx_hosts)

    # 4. Store in cache and return
    _cache_set(email, result)
    return result


def _probe_smtp(email: str, mx_hosts: list[str]) -> bool:
    """
    Attempt an SMTP handshake against the provided MX hosts.

    Tries each host/port combination in order.  Returns ``True`` (safe default)
    unless at least one host gives a hard 5xx rejection for the RCPT TO.
    """
    for host in mx_hosts[:3]:           # limit to top 3 MX hosts
        for port in _SMTP_PORTS:
            try:
                with smtplib.SMTP(timeout=_SMTP_TIMEOUT) as smtp:
                    smtp.connect(host, port)
                    smtp.ehlo_or_helo_if_needed()
                    smtp.mail(_PROBE_FROM)
                    code, _ = smtp.rcpt(email)

                    if code in _HARD_REJECT_CODES:
                        logger.debug(
                            "SMTP hard reject %d for %s via %s:%d",
                            code, email, host, port,
                        )
                        return False

                    # 250 or 251 → exists; 4xx → temporary, treat as unverifiable
                    return True

            except smtplib.SMTPConnectError:
                logger.debug("SMTP connect error to %s:%d", host, port)
                continue
            except smtplib.SMTPServerDisconnected:
                logger.debug("SMTP server disconnected: %s:%d", host, port)
                continue
            except smtplib.SMTPException as exc:
                logger.debug("SMTP exception for %s via %s:%d — %s", email, host, port, exc)
                continue
            except (socket.timeout, OSError) as exc:
                logger.debug("Socket error for %s via %s:%d — %s", email, host, port, exc)
                continue
            except Exception as exc:
                logger.debug("Unexpected error for %s via %s:%d — %s", email, host, port, exc)
                continue

    # All attempts failed → server is unverifiable, return safe default
    return True
