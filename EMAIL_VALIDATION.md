# Email Validation Feature

## Overview
Comprehensive email validation has been implemented across both frontend and backend to ensure only valid, deliverable email addresses are accepted during registration and login.

## Validation Steps

The email validation process includes the following checks:

### 1. RFC 5322 Syntax Validation
- Verifies the email contains exactly one `@` symbol
- Validates characters in local and domain parts
- Checks local part length (max 64 characters)
- Checks domain length (max 255 characters)
- Ensures domain has a valid TLD (contains at least one dot)
- Validates domain label structure (no leading/trailing hyphens)

### 2. Email Normalization
- Converts domain to lowercase (RFC requires case-insensitive domains)
- Normalizes Unicode characters (NFKC)
- Strips whitespace
- Removes trailing dots from domain

### 3. MX Record Verification (Backend Only)
- Queries DNS for MX (mail exchange) records
- Falls back to A records if no MX records exist
- Verifies the domain can actually receive email
- Gracefully handles DNS timeouts (doesn't reject on timeout)

### 4. Disposable Email Detection
- Checks against a list of known disposable/temporary email providers
- Includes common services like:
  - mailinator.com
  - temp-mail.org
  - guerrillamail.com
  - 10minutemail.com
  - And 20+ more...

### 5. Error Messaging
If validation fails, users receive clear error messages:
- **Generic validation failure**: "Please enter a valid email address that can receive mail."
- **Disposable email detected**: "Please use a permanent email address, not a disposable one."

## Implementation

### Backend (Python/FastAPI)

**Location**: `auth-service/app/utils/email_validator.py`

**Main Functions**:
```python
# Comprehensive validation
validate_email(email: str, check_mx: bool = True, check_disposable: bool = True) 
    -> Tuple[bool, Optional[str], Optional[str]]

# Raises ValueError if invalid
validate_email_or_raise(email: str, check_mx: bool = True, check_disposable: bool = True) 
    -> str
```

**Integration**: 
- Used in `AuthService.register()` with full validation
- Used in `AuthService.login()` with normalization only (no MX/disposable checks)

**Dependencies**:
- `dnspython` - For DNS MX record lookups

### Frontend (JavaScript/React)

**Location**: `frontend/src/utils/emailValidator.js`

**Main Functions**:
```javascript
// Comprehensive validation (client-side only)
validateEmail(email, options = { checkDisposable: true })
    -> { isValid: boolean, normalizedEmail: string|null, error: string|null }

// Throws Error if invalid
validateEmailOrThrow(email, options = {})
    -> string
```

**Integration**:
- Used in `Register.js` with disposable domain checking
- Used in `Login.js` with basic validation only

**Note**: MX record validation is not performed in the browser (requires DNS lookups). This validation happens server-side.

## Usage Examples

### Backend (Python)
```python
from app.utils.email_validator import validate_email_or_raise

# Registration - full validation
try:
    normalized_email = validate_email_or_raise(
        email, 
        check_mx=True, 
        check_disposable=True
    )
    # Use normalized_email for registration
except ValueError as e:
    # Display error message to user
    raise HTTPException(status_code=400, detail=str(e))

# Login - normalization only
normalized_email = validate_email_or_raise(
    email, 
    check_mx=False, 
    check_disposable=False
)
```

### Frontend (JavaScript)
```javascript
import { validateEmail } from '../utils/emailValidator';

// Registration - with disposable check
const { isValid, normalizedEmail, error } = validateEmail(email, { 
    checkDisposable: true 
});

if (!isValid) {
    setError(error);
    return;
}

// Use normalizedEmail for API call
await register(normalizedEmail, password);

// Login - basic validation only
const validation = validateEmail(email, { checkDisposable: false });
```

## Testing

### Backend Tests
Run the test script:
```bash
cd F:\OMNICHAT
python test-email-validation.py
```

This will test:
- RFC 5322 syntax validation
- Email normalization
- Disposable domain detection
- Optionally: MX record verification (requires internet)

### Frontend Tests
You can test in the browser console:
```javascript
import { validateEmail } from './utils/emailValidator';

// Test valid email
validateEmail('test@example.com')
// { isValid: true, normalizedEmail: 'test@example.com', error: null }

// Test disposable domain
validateEmail('test@mailinator.com')
// { isValid: false, normalizedEmail: null, error: '...' }

// Test invalid syntax
validateEmail('notanemail')
// { isValid: false, normalizedEmail: null, error: '...' }
```

## Configuration

### Disable MX Checking (for testing)
In the backend, you can disable MX checking:
```python
# In auth_service.py
normalized_email = validate_email_or_raise(
    email, 
    check_mx=False,  # Disable for testing
    check_disposable=True
)
```

### Add More Disposable Domains
To add more disposable domains to the blocklist:

**Backend**: Edit `auth-service/app/utils/email_validator.py`
```python
DISPOSABLE_DOMAINS = {
    'mailinator.com',
    'your-new-domain.com',  # Add here
    # ...
}
```

**Frontend**: Edit `frontend/src/utils/emailValidator.js`
```javascript
const DISPOSABLE_DOMAINS = new Set([
  'mailinator.com',
  'your-new-domain.com',  // Add here
  // ...
]);
```

## Error Handling

### Backend
All validation errors raise `ValueError` with descriptive messages:
```python
try:
    normalized_email = validate_email_or_raise(email)
except ValueError as e:
    # e.args[0] contains the error message
    raise HTTPException(status_code=400, detail=str(e))
```

### Frontend
Validation returns an object with error information:
```javascript
const { isValid, normalizedEmail, error } = validateEmail(email);
if (!isValid) {
    setError(error);  // Display to user
    return;
}
```

## Performance Considerations

1. **MX Record Lookups**: DNS queries can be slow (100-500ms). The backend:
   - Has a 5-second timeout
   - Gracefully handles timeouts (doesn't reject)
   - Falls back to A records if MX records don't exist

2. **Client-Side First**: The frontend validates before sending to backend, reducing unnecessary API calls.

3. **Login Optimization**: Login only normalizes emails, skipping expensive MX/disposable checks.

## Security Notes

- Email addresses are normalized before storage to prevent duplicate accounts
- Disposable email detection helps prevent spam/fake accounts
- MX record verification ensures email deliverability
- Validation is performed on both client and server (defense in depth)

## Future Enhancements

Potential improvements:
1. Add more disposable domains to the blocklist
2. Integrate with a disposable email API service
3. Add rate limiting to prevent validation abuse
4. Cache MX record lookups to improve performance
5. Add support for internationalized domain names (IDN)
