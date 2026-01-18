import re
import unicodedata
import socket
from typing import Tuple, Optional
import dns.resolver
import logging

logger = logging.getLogger(__name__)

# Common disposable email domains
DISPOSABLE_DOMAINS = {
    'mailinator.com', 'temp-mail.org', 'guerrillamail.com', 'tempmail.com',
    '10minutemail.com', 'throwaway.email', 'maildrop.cc', 'trashmail.com',
    'yopmail.com', 'fakeinbox.com', 'getnada.com', 'anonbox.net',
    'dispostable.com', 'emailondeck.com', 'spam4.me', 'temp-mail.io',
    'mohmal.com', 'mailnesia.com', 'sharklasers.com', 'guerrillamailblock.com',
    'getairmail.com', 'mytemp.email', 'tmpmail.net', 'fakemail.net',
    'throwawaymail.com', 'mintemail.com', 'tempinbox.com', 'jetable.org'
}

# RFC 5322 email regex (simplified but comprehensive)
EMAIL_REGEX = re.compile(
    r'^[a-zA-Z0-9.!#$%&\'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$'
)


def normalize_email(email: str) -> str:
    """
    Normalize email address:
    - Convert domain to lowercase
    - Remove unnecessary Unicode characters
    - Strip whitespace
    """
    email = email.strip()
    
    # Normalize Unicode characters
    email = unicodedata.normalize('NFKC', email)
    
    # Split local and domain parts
    if '@' not in email:
        return email.lower()
    
    local, domain = email.rsplit('@', 1)
    
    # Lowercase the domain part (RFC requires case-insensitive domain)
    # Keep local part as-is (technically case-sensitive, though most servers ignore case)
    domain = domain.lower()
    
    # Remove trailing dots from domain
    domain = domain.rstrip('.')
    
    return f"{local}@{domain}"


def check_rfc5322_syntax(email: str) -> bool:
    """
    Check if email follows RFC 5322 syntax rules:
    - Contains exactly one '@'
    - Valid characters in local and domain parts
    - Proper domain structure
    """
    # Check for exactly one @
    if email.count('@') != 1:
        return False
    
    # Check overall format
    if not EMAIL_REGEX.match(email):
        return False
    
    local, domain = email.rsplit('@', 1)
    
    # Check local part length (max 64 characters per RFC 5321)
    if len(local) > 64 or len(local) == 0:
        return False
    
    # Check domain length (max 255 characters per RFC 5321)
    if len(domain) > 255 or len(domain) == 0:
        return False
    
    # Check domain has at least one dot (valid TLD)
    if '.' not in domain:
        return False
    
    # Check each label in domain
    labels = domain.split('.')
    for label in labels:
        if len(label) == 0 or len(label) > 63:
            return False
        # Labels can't start or end with hyphen
        if label.startswith('-') or label.endswith('-'):
            return False
    
    return True


def check_mx_records(domain: str, timeout: float = 5.0) -> bool:
    """
    Verify that the domain has valid MX records (mail servers).
    Returns True if MX records exist, False otherwise.
    """
    try:
        # Configure resolver with timeout
        resolver = dns.resolver.Resolver()
        resolver.timeout = timeout
        resolver.lifetime = timeout
        
        # Try to get MX records
        mx_records = resolver.resolve(domain, 'MX')
        return len(mx_records) > 0
    except dns.resolver.NXDOMAIN:
        # Domain does not exist
        logger.warning(f"Domain does not exist: {domain}")
        return False
    except dns.resolver.NoAnswer:
        # Domain exists but has no MX records
        # Try A record as fallback (some domains use A records for mail)
        try:
            a_records = resolver.resolve(domain, 'A')
            return len(a_records) > 0
        except:
            logger.warning(f"No MX or A records for domain: {domain}")
            return False
    except dns.exception.Timeout:
        # DNS timeout - we'll be lenient and allow it
        logger.warning(f"DNS timeout for domain: {domain}")
        return True  # Don't reject on timeout
    except Exception as e:
        # Other DNS errors - log and be lenient
        logger.error(f"DNS error for domain {domain}: {str(e)}")
        return True  # Don't reject on DNS errors


def is_disposable_domain(domain: str) -> bool:
    """
    Check if the domain is a known disposable/temporary email provider.
    """
    domain_lower = domain.lower()
    return domain_lower in DISPOSABLE_DOMAINS


def validate_email(email: str, check_mx: bool = True, check_disposable: bool = True) -> Tuple[bool, Optional[str], Optional[str]]:
    """
    Comprehensive email validation.
    
    Args:
        email: Email address to validate
        check_mx: Whether to check MX records (can be disabled for testing)
        check_disposable: Whether to check for disposable domains
    
    Returns:
        Tuple of (is_valid, normalized_email or None, error_message or None)
    """
    error_msg = "Please enter a valid email address that can receive mail."
    
    # Step 1: Basic cleanup
    email = email.strip()
    if not email:
        return False, None, error_msg
    
    # Step 2: Normalize the email
    try:
        normalized = normalize_email(email)
    except Exception as e:
        logger.error(f"Error normalizing email: {str(e)}")
        return False, None, error_msg
    
    # Step 3: Check RFC 5322 syntax
    if not check_rfc5322_syntax(normalized):
        return False, None, error_msg
    
    # Extract domain
    _, domain = normalized.rsplit('@', 1)
    
    # Step 4: Check for disposable domains
    if check_disposable and is_disposable_domain(domain):
        return False, None, "Please use a permanent email address, not a disposable one."
    
    # Step 5: Verify MX records
    if check_mx and not check_mx_records(domain):
        return False, None, error_msg
    
    # All checks passed
    return True, normalized, None


def validate_email_or_raise(email: str, check_mx: bool = True, check_disposable: bool = True) -> str:
    """
    Validate email and return normalized version, or raise ValueError.
    
    Args:
        email: Email address to validate
        check_mx: Whether to check MX records
        check_disposable: Whether to check for disposable domains
    
    Returns:
        Normalized email string
    
    Raises:
        ValueError: If validation fails
    """
    is_valid, normalized, error = validate_email(email, check_mx, check_disposable)
    
    if not is_valid:
        raise ValueError(error or "Invalid email address")
    
    return normalized
