"""
CSC-128 Assignment 7: Agent with Tools
Michelle Salgado

Agent loop for the room reservation assistant.
"""

import json
from groq import Groq

from tools import TOOL_SCHEMAS, dispatch_tool

MAX_ITERATIONS = 5

SYSTEM_PROMPT = """
You are a room reservation assistant.

Use the available tools whenever the user asks about room availability,
building hours, or wants to reserve a room.

Never claim that a room was booked unless the book_room tool successfully
completed the reservation.

Do not invent tools or capabilities that are not available.
"""


def parse_tool_arguments(argument_string):
    """Safely parse tool arguments from a JSON string."""
    try:
        return json.loads(argument_string)
    except json.JSONDecodeError as error:
        return f"Invalid tool arguments: {error}"


def run_agent(client, messages, confirmed=False, tool_log=None):
    """Run the agent loop until the model gives a final answer."""

    if tool_log is None:
        tool_log = []

    for iteration in range(MAX_ITERATIONS):
        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=messages,
            tools=TOOL_SCHEMAS,
            tool_choice="auto"
        )

        message = response.choices[0].message
        messages.append(message)

        # If the model does not request a tool, the agent is finished.
        if not message.tool_calls:
            return message.content

        # Process each tool call requested by the model.
        for tool_call in message.tool_calls:
            tool_name = tool_call.function.name

            # Tool arguments arrive as a JSON string and may be malformed.
            arguments = parse_tool_arguments(
                tool_call.function.arguments
            )

            if isinstance(arguments, str):
                tool_result = arguments
            else:
                # State-changing tools require explicit confirmation.
                if tool_name == "book_room" and not confirmed:
                    day = arguments.get("day", "")
                    room = arguments.get("room", "")
                    name = arguments.get("name", "")

                    return {
                        "confirmation_required": True,
                        "message": (
                            f"Please confirm: book room {room} on {day} "
                            f"for {name}?"
                        ),
                        "arguments": arguments
                    }

                tool_result = dispatch_tool(tool_name, arguments)

                tool_log.append(
                    {
                        "tool": tool_name,
                        "arguments": arguments.copy(),
                        "result": tool_result
                    }
                )

            # Send the tool result back to the model.
            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": str(tool_result)
                }
            )

    return (
        "The agent stopped because it reached the maximum "
        "number of tool calls."
    )