"""
Progressive validation system for Success-Diary application.

This module provides client-side validation rules and server-side validation
functions that work together to provide smooth, helpful user feedback.
"""

from typing import Dict, List, Optional, Union
from dataclasses import dataclass
from app.errors import ValidationError, validation_required, validation_too_long, validation_too_short


@dataclass
class ValidationRule:
    """Configuration for a single validation rule."""
    field_name: str
    rule_type: str  # required, min_length, max_length, range, format
    value: Union[int, str, List]
    message: str
    severity: str = "error"  # error, warning, info
    trigger: str = "blur"  # blur, change, input, submit


@dataclass
class CharacterLimitConfig:
    """Configuration for character counting and limits."""
    max_length: int
    warning_threshold: float = 0.9  # Show counter at 90%
    highlight_threshold: float = 0.95  # Highlight at 95%
    show_counter_at: Optional[int] = None  # Show counter at specific character count


# Daily Entry Form Validation Rules
DAILY_ENTRY_RULES = [
    # Success/Highlights Fields (Priority 1)
    ValidationRule(
        field_name="success_1",
        rule_type="required",
        value=True,
        message="Please share at least one success from today",
        trigger="blur"
    ),
    ValidationRule(
        field_name="success_1",
        rule_type="max_length",
        value=255,
        message="Success highlights should be 255 characters or less",
        trigger="input"
    ),
    ValidationRule(
        field_name="success_2",
        rule_type="max_length",
        value=255,
        message="Success highlights should be 255 characters or less",
        trigger="input"
    ),
    ValidationRule(
        field_name="success_3",
        rule_type="max_length",
        value=255,
        message="Success highlights should be 255 characters or less",
        trigger="input"
    ),
    
    # Gratitude Fields (Priority 1)
    ValidationRule(
        field_name="gratitude_1",
        rule_type="required",
        value=True,
        message="Please share at least one thing you're grateful for",
        trigger="blur"
    ),
    ValidationRule(
        field_name="gratitude_1",
        rule_type="max_length",
        value=255,
        message="Gratitude entries should be 255 characters or less",
        trigger="input"
    ),
    ValidationRule(
        field_name="gratitude_2",
        rule_type="max_length",
        value=255,
        message="Gratitude entries should be 255 characters or less",
        trigger="input"
    ),
    ValidationRule(
        field_name="gratitude_3",
        rule_type="max_length",
        value=255,
        message="Gratitude entries should be 255 characters or less",
        trigger="input"
    ),
    
    # Anxiety/Challenge Fields (Priority 1)
    ValidationRule(
        field_name="anxiety_1",
        rule_type="required",
        value=True,
        message="Please share at least one challenge or worry (this helps with processing)",
        trigger="blur"
    ),
    ValidationRule(
        field_name="anxiety_1",
        rule_type="max_length",
        value=255,
        message="Challenge entries should be 255 characters or less",
        trigger="input"
    ),
    ValidationRule(
        field_name="anxiety_2",
        rule_type="max_length",
        value=255,
        message="Challenge entries should be 255 characters or less",
        trigger="input"
    ),
    ValidationRule(
        field_name="anxiety_3",
        rule_type="max_length",
        value=255,
        message="Challenge entries should be 255 characters or less",
        trigger="input"
    ),
    
    # Daily Journal (Priority 1)
    ValidationRule(
        field_name="journal",
        rule_type="max_length",
        value=8000,
        message="Daily journal should be 8,000 characters or less",
        trigger="input"
    ),
    
    # Overall Rating (Priority 2)
    ValidationRule(
        field_name="score",
        rule_type="range",
        value=[1, 5],
        message="Please rate your day from 1 to 5",
        trigger="change"
    ),
]

# Character Limit Configurations - Clean text counters at 85% threshold
CHARACTER_LIMITS = {
    # Emotion fields: Hide until 85%, show gray at 85%, amber at 90%, red at 95%
    "success_1": CharacterLimitConfig(
        max_length=255,
        show_counter_at=217,  # 85% of 255 (rounded up)
        warning_threshold=0.9,  # 90% - amber
        highlight_threshold=0.95  # 95% - red
    ),
    "success_2": CharacterLimitConfig(
        max_length=255,
        show_counter_at=217,  # 85% of 255
        warning_threshold=0.9,
        highlight_threshold=0.95
    ),
    "success_3": CharacterLimitConfig(
        max_length=255,
        show_counter_at=217,  # 85% of 255
        warning_threshold=0.9,
        highlight_threshold=0.95
    ),
    "gratitude_1": CharacterLimitConfig(
        max_length=255,
        show_counter_at=217,  # 85% of 255
        warning_threshold=0.9,
        highlight_threshold=0.95
    ),
    "gratitude_2": CharacterLimitConfig(
        max_length=255,
        show_counter_at=217,  # 85% of 255
        warning_threshold=0.9,
        highlight_threshold=0.95
    ),
    "gratitude_3": CharacterLimitConfig(
        max_length=255,
        show_counter_at=217,  # 85% of 255
        warning_threshold=0.9,
        highlight_threshold=0.95
    ),
    "anxiety_1": CharacterLimitConfig(
        max_length=255,
        show_counter_at=217,  # 85% of 255
        warning_threshold=0.9,
        highlight_threshold=0.95
    ),
    "anxiety_2": CharacterLimitConfig(
        max_length=255,
        show_counter_at=217,  # 85% of 255
        warning_threshold=0.9,
        highlight_threshold=0.95
    ),
    "anxiety_3": CharacterLimitConfig(
        max_length=255,
        show_counter_at=217,  # 85% of 255
        warning_threshold=0.9,
        highlight_threshold=0.95
    ),
    
    # Journal field: Hide until 85%, show gray at 85%, amber at 90%, red at 95%
    "journal": CharacterLimitConfig(
        max_length=8000,
        show_counter_at=6800,  # 85% of 8000
        warning_threshold=0.9,  # 90% - amber
        highlight_threshold=0.95  # 95% - red
    ),
}

# Authentication Form Validation Rules (Priority 2)
AUTH_FORM_RULES = [
    # Email validation
    ValidationRule(
        field_name="email",
        rule_type="required",
        value=True,
        message="Email address is required",
        trigger="blur"
    ),
    ValidationRule(
        field_name="email",
        rule_type="format",
        value="email",
        message="Please enter a valid email address",
        trigger="blur"
    ),
    
    # Password validation
    ValidationRule(
        field_name="password",
        rule_type="required",
        value=True,
        message="Password is required",
        trigger="blur"
    ),
    ValidationRule(
        field_name="password",
        rule_type="min_length",
        value=8,
        message="Password must be at least 8 characters long",
        trigger="blur"
    ),
]


def get_validation_rules(form_type: str) -> List[ValidationRule]:
    """Get validation rules for a specific form type."""
    if form_type == "daily_entry":
        return DAILY_ENTRY_RULES
    elif form_type == "auth":
        return AUTH_FORM_RULES
    else:
        return []


def get_character_limit_config(field_name: str) -> Optional[CharacterLimitConfig]:
    """Get character limit configuration for a specific field."""
    return CHARACTER_LIMITS.get(field_name)


# Server-side validation functions
def validate_daily_entry_server(form_data: dict) -> List[ValidationError]:
    """Server-side validation for daily entry form."""
    errors = []
    
    # Check required fields
    if not form_data.get('success_1', '').strip():
        errors.append(validation_required('success_1'))
    
    if not form_data.get('gratitude_1', '').strip():
        errors.append(validation_required('gratitude_1'))
    
    if not form_data.get('anxiety_1', '').strip():
        errors.append(validation_required('anxiety_1'))
    
    # Check character limits
    for field_name, config in CHARACTER_LIMITS.items():
        value = form_data.get(field_name, '')
        if len(value) > config.max_length:
            errors.append(validation_too_long(field_name, config.max_length))
    
    # Check score range
    score = form_data.get('score')
    if score is not None:
        try:
            score_int = int(score)
            if score_int < 1 or score_int > 5:
                errors.append(ValidationError(
                    message="Overall rating must be between 1 and 5",
                    field="score"
                ))
        except (ValueError, TypeError):
            errors.append(ValidationError(
                message="Overall rating must be a valid number",
                field="score"
            ))
    
    return errors


def validate_auth_form_server(form_data: dict, form_type: str = "login") -> List[ValidationError]:
    """Server-side validation for authentication forms."""
    errors = []
    
    # Email validation
    email = form_data.get('email', '').strip()
    if not email:
        errors.append(validation_required('email'))
    elif '@' not in email or '.' not in email.split('@')[-1]:
        errors.append(ValidationError(
            message="Please enter a valid email address",
            field="email"
        ))
    
    # Password validation
    password = form_data.get('password', '')
    if not password:
        errors.append(validation_required('password'))
    elif len(password) < 8:
        errors.append(validation_too_short('password', 8))
    
    return errors


# JavaScript configuration export
def get_client_validation_config(form_type: str) -> dict:
    """Get validation configuration for client-side JavaScript."""
    rules = get_validation_rules(form_type)
    
    config = {
        "rules": {},
        "characterLimits": {},
        "debounceMs": 300
    }
    
    # Convert rules to JavaScript-friendly format
    for rule in rules:
        if rule.field_name not in config["rules"]:
            config["rules"][rule.field_name] = []
        
        config["rules"][rule.field_name].append({
            "type": rule.rule_type,
            "value": rule.value,
            "message": rule.message,
            "severity": rule.severity,
            "trigger": rule.trigger
        })
    
    # Add character limit configurations
    for field_name, limit_config in CHARACTER_LIMITS.items():
        config["characterLimits"][field_name] = {
            "maxLength": limit_config.max_length,
            "warningThreshold": limit_config.warning_threshold,
            "highlightThreshold": limit_config.highlight_threshold,
            "showCounterAt": limit_config.show_counter_at
        }
    
    return config