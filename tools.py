"""
CSC-128 Assignment 7 starter: the tools and their schemas
Michelle Salgado
"""

AVAILABILITY = {
    "Monday": ["214", "216", "220"],
    "Tuesday": ["214", "220"],
    "Wednesday": ["216", "220"],
    "Thursday": ["214", "216"],
    "Friday": ["214", "216", "220"]
}

def check_availability(day):
    """TODO 2: return which rooms are free. Handle a bad day name."""
    day = day.strip().title()

    if day not in AVAILABILITY:
        return f"Sorry, {day} is not a valid weekday."

    rooms = AVAILABILITY[day]

    if not rooms:
        return f"There are no rooms available on {day}."

    return f"Available rooms on {day}: {', '.join(rooms)}"

def get_hours(day):
    """TODO 3: return the opening hours for a weekday."""
    day = day.strip().title()

    if day not in AVAILABILITY:
        return f"Sorry, {day} is not a valid weekday."

    return f"The building is open from 8:00 AM to 5:00 PM on {day}."

def book_room(day, room, name):
    """
    TODO 4: reserve a room and remove it from availability.

    Think about what this function should NOT be able to do before you
    write it. Do not add a delete function.
    """
    day = day.strip().title()
    room = str(room).strip()
    name = name.strip()

    if day not in AVAILABILITY:
        return f"Sorry, {day} is not a valid weekday."

    if room not in AVAILABILITY[day]:
        return f"Room {room} is not available on {day}."

    if not name:
        return "A name is required to book a room."

    AVAILABILITY[day].remove(room)

    return f"Room {room} has been booked for {name} on {day}."

AVAILABLE_TOOLS = {
    # TODO 5: map every tool name to its function
    "check_availability": check_availability,
    "get_hours": get_hours,
    "book_room": book_room
}

def dispatch_tool(tool_name, arguments):
    """Safely run a tool only if its name is allowed."""
    if tool_name not in AVAILABLE_TOOLS:
        return f"Unknown tool: {tool_name}"

    try:
        return AVAILABLE_TOOLS[tool_name](**arguments)
    except TypeError as error:
        return f"Tool argument error: {error}"
    except Exception as error:
        return f"Tool failed: {error}"


TOOL_SCHEMAS = [
    {
        "type": "function",
        "function": {
            "name": "check_availability",
            "description": (
                "Use this tool when the user asks which rooms are available "
                "or free on a specific weekday."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "day": {
                        "type": "string",
                        "description": "The weekday to check."
                    }
                },
                "required": ["day"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_hours",
            "description": (
                "Use this tool when the user asks what time the building "
                "opens, closes, or is open on a specific weekday."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "day": {
                        "type": "string",
                        "description": "The weekday to check."
                    }
                },
                "required": ["day"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "book_room",
            "description": (
                "Use this tool only when the user wants to reserve or book "
                "a specific available room for a specific weekday."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "day": {
                        "type": "string",
                        "description": "The weekday for the reservation."
                    },
                    "room": {
                        "type": "string",
                        "description": "The room number to reserve."
                    },
                    "name": {
                        "type": "string",
                        "description": "The name of the person making the reservation."
                    }
                },
                "required": ["day", "room", "name"]
            }
        }
    }
]