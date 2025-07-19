"""
Timezone Utility Functions

Handles timezone resolution, date calculations, and user timezone preferences.
Based on ADR-0005: User Timezone Handling Strategy.
"""

from datetime import date, datetime, time
from typing import Optional
import pytz
from app.models import User


def get_user_effective_timezone(user: User) -> str:
    """
    Get user's effective timezone using priority chain:
    Manual setting → Auto-detection → UTC fallback
    
    Args:
        user: User model instance
        
    Returns:
        str: Timezone string (e.g., 'America/New_York')
    """
    # Priority chain implementation
    if user.user_timezone:
        return user.user_timezone
    
    if user.timezone_auto_detect and user.last_detected_timezone:
        return user.last_detected_timezone
    
    # Legacy fallback
    if user.timezone:
        return user.timezone
        
    # Final fallback
    return 'UTC'


def get_user_local_date(user: User) -> date:
    """
    Get current date in user's timezone.
    
    Args:
        user: User model instance
        
    Returns:
        date: Current date in user's local timezone
    """
    user_timezone = get_user_effective_timezone(user)
    
    try:
        user_tz = pytz.timezone(user_timezone)
        return datetime.now(user_tz).date()
    except pytz.exceptions.UnknownTimeZoneError:
        # Fallback to UTC if timezone is invalid
        return datetime.utcnow().date()


def get_user_date_range(user: User, target_date: date) -> tuple[datetime, datetime]:
    """
    Get UTC datetime range for a specific date in user's timezone.
    Useful for querying entries that fall within a user's local day.
    
    Args:
        user: User model instance
        target_date: The date in user's local timezone
        
    Returns:
        tuple: (start_utc, end_utc) as UTC datetime objects
    """
    user_timezone = get_user_effective_timezone(user)
    
    try:
        user_tz = pytz.timezone(user_timezone)
        
        # Start of day in user's timezone
        start_local = user_tz.localize(datetime.combine(target_date, time.min))
        # End of day in user's timezone  
        end_local = user_tz.localize(datetime.combine(target_date, time.max))
        
        # Convert to UTC for database queries
        start_utc = start_local.astimezone(pytz.UTC)
        end_utc = end_local.astimezone(pytz.UTC)
        
        return (start_utc, end_utc)
        
    except pytz.exceptions.UnknownTimeZoneError:
        # Fallback: treat as UTC
        start_utc = datetime.combine(target_date, time.min).replace(tzinfo=pytz.UTC)
        end_utc = datetime.combine(target_date, time.max).replace(tzinfo=pytz.UTC)
        return (start_utc, end_utc)


def format_user_date(user: User, target_date: date, format_type: str = 'full') -> str:
    """
    Format date for display in user's locale/timezone.
    
    Args:
        user: User model instance
        target_date: Date to format
        format_type: 'full', 'short', or 'iso'
        
    Returns:
        str: Formatted date string
    """
    if format_type == 'iso':
        return target_date.isoformat()
    elif format_type == 'short':
        return target_date.strftime('%m/%d/%Y')
    else:  # full
        return target_date.strftime('%A, %B %d, %Y')


def validate_timezone(timezone_str: str) -> bool:
    """
    Validate if a timezone string is valid.
    
    Args:
        timezone_str: Timezone string to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    try:
        pytz.timezone(timezone_str)
        return True
    except pytz.exceptions.UnknownTimeZoneError:
        return False


def get_common_timezones() -> list[dict]:
    """
    Get list of common timezone choices for UI dropdowns.
    
    Returns:
        list: List of timezone dictionaries with 'value' and 'label'
    """
    common_zones = [
        ('UTC', 'UTC (Coordinated Universal Time)'),
        ('America/New_York', 'Eastern Time (New York)'),
        ('America/Chicago', 'Central Time (Chicago)'),
        ('America/Denver', 'Mountain Time (Denver)'),
        ('America/Los_Angeles', 'Pacific Time (Los Angeles)'),
        ('America/Toronto', 'Eastern Time (Toronto)'),
        ('America/Vancouver', 'Pacific Time (Vancouver)'),
        ('Europe/London', 'Greenwich Mean Time (London)'),
        ('Europe/Paris', 'Central European Time (Paris)'),
        ('Europe/Berlin', 'Central European Time (Berlin)'),
        ('Europe/Rome', 'Central European Time (Rome)'),
        ('Asia/Tokyo', 'Japan Standard Time (Tokyo)'),
        ('Asia/Shanghai', 'China Standard Time (Shanghai)'),
        ('Asia/Hong_Kong', 'Hong Kong Time'),
        ('Asia/Singapore', 'Singapore Time'),
        ('Asia/Kolkata', 'India Standard Time (Mumbai)'),
        ('Australia/Sydney', 'Australian Eastern Time (Sydney)'),
        ('Australia/Melbourne', 'Australian Eastern Time (Melbourne)'),
        ('Pacific/Auckland', 'New Zealand Time (Auckland)'),
    ]
    
    return [
        {'value': tz, 'label': label}
        for tz, label in common_zones
    ]


def get_timezone_offset_display(timezone_str: str) -> str:
    """
    Get human-readable timezone offset display.
    
    Args:
        timezone_str: Timezone string
        
    Returns:
        str: Formatted offset (e.g., 'UTC-5' or 'UTC+9')
    """
    try:
        tz = pytz.timezone(timezone_str)
        now = datetime.now(tz)
        offset = now.strftime('%z')
        
        if offset:
            # Convert from +0500 to UTC+5 format
            hours = int(offset[1:3])
            minutes = int(offset[3:5])
            sign = '+' if offset[0] == '+' else '-'
            
            if minutes == 0:
                return f'UTC{sign}{hours}'
            else:
                return f'UTC{sign}{hours}:{minutes:02d}'
        else:
            return 'UTC+0'
            
    except (pytz.exceptions.UnknownTimeZoneError, ValueError):
        return 'UTC+0'