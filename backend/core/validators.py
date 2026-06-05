"""
Email validation pipeline — CleanMail by Samod.

Four-stage pipeline:
  1. Syntax check (RFC 5322 regex)
  2. Disposable domain check (in-memory set)
  3. DNS MX record lookup (5-second timeout, cached 1 hour)
  4. SMTP mailbox probe (EHLO/RCPT TO handshake, cached 30 min)

Public API:
    validate_email(email: str) -> dict
"""

import re

from core.services.disposable_checker import is_disposable
from core.services.mx_checker import has_mx_record
from core.services.smtp_checker import check_smtp_mailbox

# ---------------------------------------------------------------------------
# RFC 5322 simplified regex for email syntax validation
# ---------------------------------------------------------------------------
_EMAIL_REGEX = re.compile(
    r"^(?!\.)(?!.*\.\.)"                          # no leading dot, no consecutive dots
    r"[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+"         # local part
    r"@"
    r"[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}"          # domain label start
    r"[a-zA-Z0-9])?"                               # domain label end
    r"(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}"      # sub-domain labels
    r"[a-zA-Z0-9])?)*"
    r"\.[a-zA-Z]{2,}$",                            # TLD (>=2 chars)
    re.IGNORECASE,
)


def validate_email(email: str) -> dict:
    """
    Run the full validation pipeline on a single email address.

    Returns a dictionary with two keys:

    - ``estado``: one of ``"valido"``, ``"invalido"``, ``"desechable"``.
    - ``motivo``: a short machine-readable reason when the email is not
      valid (``None`` when ``estado == "valido"``).

    Stages
    ------
    1. **Syntax** — checks against an RFC 5322-derived regex.
    2. **Disposable** — checks the domain against a known list.
    3. **MX** — verifies that the domain publishes at least one MX record.
    4. **SMTP** — performs an EHLO/RCPT TO handshake to confirm the mailbox
       exists on the server. Providers that block SMTP probing are treated
       as "unverifiable" and the email is returned as valid (safe default).

    Args:
        email: The raw email string to validate.

    Returns:
        ``{"estado": str, "motivo": str | None}``
    """
    email = email.strip().lower()

    # Stage 1: Syntax
    if not email or not _EMAIL_REGEX.match(email):
        return {"estado": "invalido", "motivo": "sintaxis"}

    # Extract domain
    try:
        domain = email.rsplit("@", 1)[1]
    except IndexError:
        return {"estado": "invalido", "motivo": "formato_invalido"}

    # Stage 2: Disposable domain
    if is_disposable(domain):
        return {"estado": "desechable", "motivo": "dominio_temporal"}

    # Stage 3: MX record
    if not has_mx_record(domain):
        return {"estado": "invalido", "motivo": "sin_mx"}

    # Stage 4: SMTP mailbox probe
    if not check_smtp_mailbox(email, domain):
        return {"estado": "invalido", "motivo": "buzon_inexistente"}

    return {"estado": "valido", "motivo": None}
