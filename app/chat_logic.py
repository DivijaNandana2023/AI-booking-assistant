"""
Chat logic - Booking state + memory
"""

from typing import Dict, List
from datetime import datetime
from config import REQUIRED_BOOKING_FIELDS


class ConversationMemory:
    def __init__(self, max_length=25):
        self.max_length = max_length
        self.messages = []

    def add_message(self, role, content):
        self.messages.append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        })
        if len(self.messages) > self.max_length:
            self.messages = self.messages[-self.max_length:]

    def clear(self):
        self.messages = []

    def get_length(self):
        return len(self.messages)


class ChatLogic:
    """Main booking state manager"""

    def __init__(self):
        self.current_booking_state = {}
        self._booking_in_progress = False

    # ================= BOOKING STATE =================

    def start_booking_flow(self):
        self._booking_in_progress = True
        self.current_booking_state = {}

    def is_booking_in_progress(self) -> bool:
        return self._booking_in_progress

    def reset_booking_context(self):
        self._booking_in_progress = False
        self.current_booking_state = {}

    # ================= FIELDS =================

    def set_booking_field(self, field: str, value: str):
        self.current_booking_state[field] = value

    def get_booking_state(self) -> Dict:
        return self.current_booking_state.copy()

    def get_missing_fields(self) -> List[str]:
        missing = []
        for field in REQUIRED_BOOKING_FIELDS:
            if field not in self.current_booking_state or not self.current_booking_state[field]:
                missing.append(field)
        return missing
