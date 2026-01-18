"""
Test script for email validation functionality
Run this from the auth-service directory
"""
import sys
sys.path.insert(0, 'auth-service')

from app.utils.email_validator import validate_email, validate_email_or_raise

def test_email_validation():
    """Test various email validation scenarios"""
    
    test_cases = [
        # (email, should_pass, description)
        ("test@example.com", True, "Valid email"),
        ("user.name@example.com", True, "Valid email with dot in local part"),
        ("user+tag@example.com", True, "Valid email with plus"),
        ("Test@Example.COM", True, "Mixed case (should normalize)"),
        ("test@EXAMPLE.com", True, "Mixed case domain (should normalize)"),
        
        # Invalid syntax
        ("notanemail", False, "No @ symbol"),
        ("@example.com", False, "Missing local part"),
        ("test@", False, "Missing domain"),
        ("test@@example.com", False, "Double @@"),
        ("test@example", False, "Missing TLD"),
        ("test @example.com", False, "Space in email"),
        
        # Disposable domains
        ("test@mailinator.com", False, "Disposable domain - mailinator"),
        ("user@temp-mail.org", False, "Disposable domain - temp-mail"),
        ("test@10minutemail.com", False, "Disposable domain - 10minutemail"),
        
        # Edge cases
        ("a@b.co", True, "Short but valid"),
        ("very.long.local.part.name@subdomain.example.com", True, "Long but valid"),
        ("test@ex-ample.com", True, "Hyphen in domain"),
    ]
    
    print("=" * 80)
    print("EMAIL VALIDATION TESTS")
    print("=" * 80)
    print()
    
    passed = 0
    failed = 0
    
    for email, should_pass, description in test_cases:
        # Test without MX check for speed
        is_valid, normalized, error = validate_email(
            email, 
            check_mx=False, 
            check_disposable=True
        )
        
        test_passed = (is_valid == should_pass)
        status = "✓ PASS" if test_passed else "✗ FAIL"
        
        if test_passed:
            passed += 1
        else:
            failed += 1
        
        print(f"{status} | {description}")
        print(f"       Input: {email}")
        print(f"       Expected: {'Valid' if should_pass else 'Invalid'}")
        print(f"       Got: {'Valid' if is_valid else 'Invalid'}")
        if normalized:
            print(f"       Normalized: {normalized}")
        if error:
            print(f"       Error: {error}")
        print()
    
    print("=" * 80)
    print(f"RESULTS: {passed} passed, {failed} failed")
    print("=" * 80)
    
    return failed == 0

def test_mx_records():
    """Test MX record validation (slower, tests real DNS)"""
    print("\n" + "=" * 80)
    print("MX RECORD TESTS (with real DNS lookups)")
    print("=" * 80)
    print()
    
    test_cases = [
        ("test@gmail.com", True, "Gmail (should have MX records)"),
        ("test@example.com", True, "Example.com (should have MX records)"),
        ("test@thisdoesnotexist12345.com", False, "Non-existent domain"),
    ]
    
    for email, should_pass, description in test_cases:
        print(f"Testing: {description}")
        print(f"  Email: {email}")
        
        is_valid, normalized, error = validate_email(
            email, 
            check_mx=True, 
            check_disposable=False
        )
        
        status = "✓" if (is_valid == should_pass) else "✗"
        print(f"  Result: {status} {'Valid' if is_valid else 'Invalid'}")
        if error:
            print(f"  Error: {error}")
        print()

if __name__ == "__main__":
    print("Testing email validation functionality...\n")
    
    # Run syntax tests
    syntax_ok = test_email_validation()
    
    # Ask before running MX tests (they're slower)
    response = input("\nRun MX record tests? (requires internet, slower) [y/N]: ")
    if response.lower() in ['y', 'yes']:
        test_mx_records()
    
    if syntax_ok:
        print("\n✓ All syntax validation tests passed!")
    else:
        print("\n✗ Some syntax validation tests failed!")
