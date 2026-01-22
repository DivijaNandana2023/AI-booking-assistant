"""
Booking flow - Slot filling and confirmation dialog
"""
from typing import Dict, List, Tuple
from datetime import datetime
from config import REQUIRED_BOOKING_FIELDS, SERVICE_TYPES


class BookingFlow:
    """Manages the booking flow - slot filling and confirmation"""

    def __init__(self, chat_logic):
        self.chat_logic = chat_logic

    def get_next_required_field(self) -> str:
        """Get the next field to ask for"""
        missing = self.chat_logic.get_missing_fields()
        if not missing:
            return None

        # Priority order for asking fields
        priority = ["name", "email", "phone", "booking_type", "date", "time"]
        for field in priority:
            if field in missing:
                return field

        return missing[0]

    def get_field_prompt(self, field: str) -> str:
        """Get friendly prompt for a specific field"""
        prompts = {
            "name": "What is your name?",
            "email": "What is your email address?",
            "phone": "What is your phone number?",
            "booking_type": f"What service would you like to book? (Options: {', '.join(SERVICE_TYPES)})",
            "date": "What date would you prefer? (Format: YYYY-MM-DD)",
            "time": "What time would you prefer? (Format: HH:MM, e.g., 14:30 for 2:30 PM)",
        }
        return prompts.get(field, f"Please provide {field}")

    def validate_field(self, field: str, value: str) -> Tuple[bool, str]:
        """Validate a field value"""
        if not value or not value.strip():
            return False, f"{field} cannot be empty"

        if field == "email":
            import re
            pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
            if not re.match(pattern, value):
                return False, "Please enter a valid email address"

        elif field == "phone":
            import re
            clean = re.sub(r"[^\d+\-]", "", value)
            if len(clean) < 10:
                return False, "Please enter a valid phone number"

        elif field == "date":
            try:
                datetime.strptime(value.strip(), "%Y-%m-%d")
            except ValueError:
                return False, "Please use date format: YYYY-MM-DD (e.g., 2024-12-25)"

        elif field == "time":
            try:
                datetime.strptime(value.strip(), "%H:%M")
            except ValueError:
                return False, "Please use time format: HH:MM (e.g., 14:30)"

        elif field == "booking_type":
            if value.strip() not in SERVICE_TYPES:
                return False, f"Please choose from: {', '.join(SERVICE_TYPES)}"

        return True, ""

    def process_field_response(self, field: str, value: str) -> Tuple[bool, str]:
        """
        Process and validate a field response
        
        Returns:
            (success: bool, message: str)
        """
        is_valid, error_msg = self.validate_field(field, value)

        if not is_valid:
            return False, error_msg

        # Set the field
        self.chat_logic.set_booking_field(field, value.strip())
        return True, f"Got it! {field}: {value}"

    def is_booking_complete(self) -> bool:
        """Check if all required fields are collected"""
        return len(self.chat_logic.get_missing_fields()) == 0

    def get_booking_summary(self) -> str:
        """Generate booking summary for confirmation"""
        state = self.chat_logic.get_booking_state()

        summary = "\n📋 **Booking Summary:**\n"
        summary += f"- **Name:** {state.get('name', 'N/A')}\n"
        summary += f"- **Email:** {state.get('email', 'N/A')}\n"
        summary += f"- **Phone:** {state.get('phone', 'N/A')}\n"
        summary += f"- **Service Type:** {state.get('booking_type', 'N/A')}\n"
        summary += f"- **Date:** {state.get('date', 'N/A')}\n"
        summary += f"- **Time:** {state.get('time', 'N/A')}\n"

        return summary

    def get_confirmation_message(self) -> str:
        """Get confirmation prompt"""
        summary = self.get_booking_summary()
        return (
            f"{summary}\n\n"
            "**Please confirm these details. Reply with 'yes' to confirm or 'no' to modify.**"
        )

    def extract_fields_from_message(self, message: str) -> Dict[str, str]:
        """
        Try to extract multiple fields from a single message
        Useful for handling natural language input
        """
        extracted = {}
        from chat_logic import IntentDetector

        detector = IntentDetector()
        entities = detector.extract_entities(message)

        # Map detected entities to booking fields
        field_mapping = {
            "email": "email",
            "phone": "phone",
            "date": "date",
            "time": "time",
            "name": "name"
        }

        for entity_key, field_name in field_mapping.items():
            if entity_key in entities:
                extracted[field_name] = entities[entity_key]

        # Try to detect booking type from message
        for service_type in SERVICE_TYPES:
            if service_type.lower() in message.lower():
                extracted["booking_type"] = service_type
                break

        return extracted

    def handle_modification(self, field: str, new_value: str) -> Tuple[bool, str]:
        """Handle modification of a previously entered field"""
        is_valid, error_msg = self.validate_field(field, new_value)

        if not is_valid:
            return False, error_msg

        self.chat_logic.set_booking_field(field, new_value.strip())
        return True, f"Updated {field} to: {new_value}"

    def reset(self):
        """Reset the booking flow"""
        self.chat_logic.reset_booking_state()
