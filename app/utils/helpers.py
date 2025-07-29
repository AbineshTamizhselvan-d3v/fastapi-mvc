from typing import Optional, Dict, Any
from datetime import datetime, timedelta
import re
import secrets
import string

def generate_random_string(length: int = 10) -> str:
    """Generate a random string of specified length."""
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))

def generate_sku() -> str:
    """Generate a random SKU."""
    prefix = "SKU"
    random_part = generate_random_string(8).upper()
    return f"{prefix}-{random_part}"

def validate_email(email: str) -> bool:
    """Validate email format."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def format_currency(amount: float, currency: str = "USD") -> str:
    """Format amount as currency string."""
    return f"${amount:.2f}"

def calculate_pagination_info(total: int, page: int, size: int) -> Dict[str, Any]:
    """Calculate pagination information."""
    total_pages = (total + size - 1) // size  # Ceiling division
    has_next = page < total_pages
    has_prev = page > 1
    
    return {
        "total": total,
        "page": page,
        "size": size,
        "total_pages": total_pages,
        "has_next": has_next,
        "has_prev": has_prev
    }

def format_phone_number(phone: str) -> str:
    """Format phone number to standard format."""
    # Remove all non-digit characters
    digits = re.sub(r'\D', '', phone)
    
    # Format as (XXX) XXX-XXXX if US format
    if len(digits) == 10:
        return f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"
    elif len(digits) == 11 and digits[0] == '1':
        return f"+1 ({digits[1:4]}) {digits[4:7]}-{digits[7:]}"
    else:
        return phone  # Return original if not standard format

def slugify(text: str) -> str:
    """Convert text to URL-friendly slug."""
    # Convert to lowercase and replace spaces with hyphens
    slug = re.sub(r'[^\w\s-]', '', text.lower())
    slug = re.sub(r'[-\s]+', '-', slug)
    return slug.strip('-')

def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """Truncate text to specified length."""
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix

def calculate_percentage(part: float, whole: float) -> float:
    """Calculate percentage."""
    if whole == 0:
        return 0.0
    return round((part / whole) * 100, 2)

def time_ago(dt: datetime) -> str:
    """Return human-readable time difference."""
    now = datetime.utcnow()
    diff = now - dt
    
    if diff.days > 0:
        return f"{diff.days} day{'s' if diff.days > 1 else ''} ago"
    elif diff.seconds > 3600:
        hours = diff.seconds // 3600
        return f"{hours} hour{'s' if hours > 1 else ''} ago"
    elif diff.seconds > 60:
        minutes = diff.seconds // 60
        return f"{minutes} minute{'s' if minutes > 1 else ''} ago"
    else:
        return "Just now"

def mask_email(email: str) -> str:
    """Mask email for privacy (e.g., j***@example.com)."""
    if '@' not in email:
        return email
    
    local, domain = email.split('@', 1)
    if len(local) <= 2:
        masked_local = local[0] + '*'
    else:
        masked_local = local[0] + '*' * (len(local) - 2) + local[-1]
    
    return f"{masked_local}@{domain}"

def validate_password_strength(password: str) -> Dict[str, Any]:
    """Validate password strength and return feedback."""
    criteria = {
        "length": len(password) >= 8,
        "uppercase": bool(re.search(r'[A-Z]', password)),
        "lowercase": bool(re.search(r'[a-z]', password)),
        "digit": bool(re.search(r'\d', password)),
        "special": bool(re.search(r'[!@#$%^&*(),.?":{}|<>]', password))
    }
    
    score = sum(criteria.values())
    
    if score == 5:
        strength = "Very Strong"
    elif score == 4:
        strength = "Strong"
    elif score == 3:
        strength = "Medium"
    elif score == 2:
        strength = "Weak"
    else:
        strength = "Very Weak"
    
    return {
        "strength": strength,
        "score": score,
        "criteria": criteria,
        "suggestions": _get_password_suggestions(criteria)
    }

def _get_password_suggestions(criteria: Dict[str, bool]) -> list:
    """Get password improvement suggestions."""
    suggestions = []
    
    if not criteria["length"]:
        suggestions.append("Use at least 8 characters")
    if not criteria["uppercase"]:
        suggestions.append("Include at least one uppercase letter")
    if not criteria["lowercase"]:
        suggestions.append("Include at least one lowercase letter")
    if not criteria["digit"]:
        suggestions.append("Include at least one number")
    if not criteria["special"]:
        suggestions.append("Include at least one special character")
    
    return suggestions
