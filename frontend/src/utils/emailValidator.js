// Common disposable email domains
const DISPOSABLE_DOMAINS = new Set([
  'mailinator.com', 'temp-mail.org', 'guerrillamail.com', 'tempmail.com',
  '10minutemail.com', 'throwaway.email', 'maildrop.cc', 'trashmail.com',
  'yopmail.com', 'fakeinbox.com', 'getnada.com', 'anonbox.net',
  'dispostable.com', 'emailondeck.com', 'spam4.me', 'temp-mail.io',
  'mohmal.com', 'mailnesia.com', 'sharklasers.com', 'guerrillamailblock.com',
  'getairmail.com', 'mytemp.email', 'tmpmail.net', 'fakemail.net',
  'throwawaymail.com', 'mintemail.com', 'tempinbox.com', 'jetable.org'
]);

// RFC 5322 email regex (simplified but comprehensive)
const EMAIL_REGEX = /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$/;

/**
 * Normalize email address:
 * - Convert domain to lowercase
 * - Strip whitespace
 * - Remove trailing dots from domain
 */
export function normalizeEmail(email) {
  email = email.trim();
  
  // Normalize Unicode characters if available
  if (email.normalize) {
    email = email.normalize('NFKC');
  }
  
  // Split local and domain parts
  const atIndex = email.lastIndexOf('@');
  if (atIndex === -1) {
    return email.toLowerCase();
  }
  
  const local = email.substring(0, atIndex);
  let domain = email.substring(atIndex + 1);
  
  // Lowercase the domain part (RFC requires case-insensitive domain)
  domain = domain.toLowerCase();
  
  // Remove trailing dots from domain
  domain = domain.replace(/\.+$/, '');
  
  return `${local}@${domain}`;
}

/**
 * Check if email follows RFC 5322 syntax rules:
 * - Contains exactly one '@'
 * - Valid characters in local and domain parts
 * - Proper domain structure
 */
export function checkRFC5322Syntax(email) {
  // Check for exactly one @
  const atCount = (email.match(/@/g) || []).length;
  if (atCount !== 1) {
    return false;
  }
  
  // Check overall format
  if (!EMAIL_REGEX.test(email)) {
    return false;
  }
  
  const [local, domain] = email.split('@');
  
  // Check local part length (max 64 characters per RFC 5321)
  if (local.length > 64 || local.length === 0) {
    return false;
  }
  
  // Check domain length (max 255 characters per RFC 5321)
  if (domain.length > 255 || domain.length === 0) {
    return false;
  }
  
  // Check domain has at least one dot (valid TLD)
  if (!domain.includes('.')) {
    return false;
  }
  
  // Check each label in domain
  const labels = domain.split('.');
  for (const label of labels) {
    if (label.length === 0 || label.length > 63) {
      return false;
    }
    // Labels can't start or end with hyphen
    if (label.startsWith('-') || label.endsWith('-')) {
      return false;
    }
  }
  
  return true;
}

/**
 * Check if the domain is a known disposable/temporary email provider.
 */
export function isDisposableDomain(domain) {
  return DISPOSABLE_DOMAINS.has(domain.toLowerCase());
}

/**
 * Comprehensive email validation (client-side checks only).
 * 
 * Note: MX record validation is done server-side as it requires DNS lookups
 * which are not available in the browser.
 * 
 * @param {string} email - Email address to validate
 * @param {Object} options - Validation options
 * @param {boolean} options.checkDisposable - Whether to check for disposable domains
 * @returns {Object} - { isValid: boolean, normalizedEmail: string|null, error: string|null }
 */
export function validateEmail(email, options = {}) {
  const { checkDisposable = true } = options;
  
  const errorMsg = "Please enter a valid email address that can receive mail.";
  
  // Step 1: Basic cleanup
  email = email.trim();
  if (!email) {
    return { isValid: false, normalizedEmail: null, error: errorMsg };
  }
  
  // Step 2: Normalize the email
  let normalized;
  try {
    normalized = normalizeEmail(email);
  } catch (e) {
    console.error('Error normalizing email:', e);
    return { isValid: false, normalizedEmail: null, error: errorMsg };
  }
  
  // Step 3: Check RFC 5322 syntax
  if (!checkRFC5322Syntax(normalized)) {
    return { isValid: false, normalizedEmail: null, error: errorMsg };
  }
  
  // Extract domain
  const domain = normalized.split('@')[1];
  
  // Step 4: Check for disposable domains
  if (checkDisposable && isDisposableDomain(domain)) {
    return { 
      isValid: false, 
      normalizedEmail: null, 
      error: "Please use a permanent email address, not a disposable one." 
    };
  }
  
  // Client-side checks passed
  // Note: MX record validation will happen server-side
  return { isValid: true, normalizedEmail: normalized, error: null };
}

/**
 * Validate email and return normalized version, or throw error.
 * 
 * @param {string} email - Email address to validate
 * @param {Object} options - Validation options
 * @returns {string} - Normalized email string
 * @throws {Error} - If validation fails
 */
export function validateEmailOrThrow(email, options = {}) {
  const { isValid, normalizedEmail, error } = validateEmail(email, options);
  
  if (!isValid) {
    throw new Error(error || "Invalid email address");
  }
  
  return normalizedEmail;
}
