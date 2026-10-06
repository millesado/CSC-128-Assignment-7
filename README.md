\# Assignment 7: Agent with Tools



\*\*Student:\*\* Michelle Salgado  

\*\*Course:\*\* CSC-128 Chatbot Programming I



\## Project Description



This project is a room reservation agent that can use tools instead of only responding with text. The agent can check room availability, check building hours, and book an available room.



The project includes two read-only tools:



\- `check\_availability` - checks which rooms are available on a weekday.

\- `get\_hours` - checks the building hours for a weekday.



It also includes one state-changing tool:



\- `book\_room` - reserves an available room and removes it from the list of available rooms.



Before `book\_room` can run, the user must confirm the reservation. The Streamlit interface also displays a tool log showing the tool name, arguments, and result for each executed tool call.



\## A Function I Deliberately Did Not Write



I deliberately did not create a `delete\_all\_reservations` function. If the agent had access to this function, it could accidentally delete every room reservation because of a misunderstanding or an incorrect tool call.



Instead of relying only on instructions telling the model not to delete reservations, the function does not exist at all. This makes the agent safer because it cannot perform an action that was never provided as a tool.



\## What Happens If the Model Requests an Unknown Tool



The agent does not automatically execute a tool name provided by the model. The `dispatch\_tool` function first checks whether the requested tool name exists in `AVAILABLE\_TOOLS`.



If the model requests a tool that does not exist, the program returns an "Unknown tool" message instead of trying to execute it. This prevents the model from calling arbitrary functions.



I tested this in `test\_tools.py` by requesting a tool that was intentionally not created:



`delete\_all\_reservations`



The test returned:



`Unknown tool: delete\_all\_reservations`



This proves that an unknown tool is rejected safely instead of being executed.



\## Tool Description Rewrite



While working on the tool schemas, I realized that a description should tell the model when to call a tool, instead of only describing what the function does.



An earlier version of the description for `book\_room` was:



`Books a room.`



This description was too vague because it did not clearly tell the model when a booking should happen.



I changed it to:



`Use this tool only when the user wants to reserve or book a specific available room for a specific weekday.`



The new version is more specific and makes it clear that `book\_room` should be used for an actual reservation request, not just when the user is asking about room availability.



\## Confirmation Before a State-Changing Tool



The `book\_room` tool changes the program's state because it removes a room from the list of available rooms. Because of this, I added a confirmation step before the tool is allowed to run.



When the model requests `book\_room`, the program first displays the room number, weekday, and name. The user must click \*\*Confirm Booking\*\* before the reservation is made. The user can also click \*\*Cancel\*\*, which leaves the availability unchanged.



I tested the confirmation by requesting Room 216 on Thursday and then clicking Cancel. After canceling, I checked Thursday's availability and Rooms 214 and 216 were both still available. This showed that the state-changing tool did not run when the reservation was canceled.



\## Testing and Safety



The project includes `test\_tools.py`, which tests the tools without requiring an API key.



The tests check:



\- Valid room availability.

\- Invalid weekday input.

\- Building hours.

\- The list of allowed tools.

\- A successful state-changing room reservation.

\- Rejection of an unknown tool.

\- Incorrect tool arguments without crashing.

\- Malformed JSON arguments without crashing.



The agent also has a maximum iteration limit of 5. This prevents the tool-calling loop from continuing forever if the model repeatedly requests tools.



Tool arguments are parsed inside a `try/except` block so malformed JSON returns an error message instead of crashing the program. The dispatcher also catches incorrect arguments and other tool errors.



Together, these protections make the agent more reliable and limit what the model is allowed to execute.

