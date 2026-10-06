"""
CSC-128 Assignment 7: Tool Tests
Michelle Salgado

Tests the room reservation tools and dispatch guard.
No API key is required for these tests.
"""

from tools import (
    AVAILABILITY,
    AVAILABLE_TOOLS,
    check_availability,
    get_hours,
    book_room,
    dispatch_tool
)
from agent import parse_tool_arguments

print("TEST 1: Check availability")
print(check_availability("Monday"))

print("\nTEST 2: Invalid weekday")
print(check_availability("Saturday"))

print("\nTEST 3: Check building hours")
print(get_hours("Wednesday"))

print("\nTEST 4: Available tool names")
print(list(AVAILABLE_TOOLS.keys()))

print("\nTEST 5: Book a room and change state")
print(check_availability("Friday"))
print(book_room("Friday", "214", "Michelle"))
print(check_availability("Friday"))

print("\nTEST 6: Unknown tool is rejected")
print(dispatch_tool("delete_all_reservations", {}))

print("\nTEST 7: Bad tool arguments do not crash")
print(dispatch_tool("book_room", {"day": "Monday"}))

print("\nTEST 8: Malformed JSON does not crash")
print(parse_tool_arguments('{"day": "Monday"'))