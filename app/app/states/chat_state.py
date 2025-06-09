import reflex as rx
from typing import TypedDict, List
import asyncio
import uuid
import httpx
import json
import time

# --- Constants for API (Ideally from .env) ---
API_BASE_URL = "http://localhost:8119"
AGENT_ID_PARAM = "team_agent"
# ---

class Message(TypedDict):
    text: str
    is_ai: bool

class Chat(TypedDict):
    messages: List[Message]
    title: str
    id: str

class ChatState(rx.State):
    conversations: dict[str, Chat] = {}
    current_chat_id: str = ""
    is_typing: bool = False # True while API is fetching AND during simulated typing
    editing_chat_id: str = ""
    current_message: str = "" # Bound to the input field

    # Simulated typing speed
    SIMULATED_TYPING_SPEED_CPS: float = 300.0  # Characters per second (adjust for desired speed)

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     if not self.conversations:
    #         self._create_and_select_new_chat("Intros")

    def _generate_chat_id(self) -> str:
        return f"{time.time()}-{uuid.uuid4()}"

    def _create_and_select_new_chat(self, title: str) -> str:
        import traceback
        print("=== DEBUG: _create_and_select_new_chat called ===")
        print(f"Title: {title}")
        print("Stack trace:")
        traceback.print_stack()
        print("=== End stack trace ===")
        
        new_id = self._generate_chat_id()
        self.conversations[new_id] = {"id": new_id, "title": title, "messages": []}
        self.current_chat_id = new_id
        print(f"DEBUG: Created and selected chat: ID={new_id}, Title='{title}'")
        return new_id

    @rx.var
    def messages(self) -> List[Message]:
        if not self.current_chat_id or self.current_chat_id not in self.conversations:
            return []
        return self.conversations[self.current_chat_id]["messages"]

    def get_latest_timestamp(self, chat_id: str) -> float:
        try:
            return float(chat_id.split("-")[0])
        except (ValueError, IndexError, TypeError): return 0.0

    @rx.var
    def sorted_chat_titles(self) -> List[dict[str, str]]:
        if not self.conversations: return []
        sorted_chats = sorted(
            self.conversations.values(),
            key=lambda chat: self.get_latest_timestamp(chat.get("id", "")),
            reverse=True,
        )
        return [{"id": chat["id"], "title": chat.get("title", "Untitled")} for chat in sorted_chats]

    def _ensure_chat_exists_and_is_selected(self):
        if not self.current_chat_id or self.current_chat_id not in self.conversations:
            if self.conversations:
                self.current_chat_id = self.sorted_chat_titles[0]["id"] if self.sorted_chat_titles else self._create_and_select_new_chat("Intros")
            else:
                self._create_and_select_new_chat("Intros")  # This will only run when actually needed

    @rx.event
    def select_chat(self, chat_id: str):
        if chat_id in self.conversations:
            self.current_chat_id = chat_id
            self.is_typing = False # Reset typing if user switches chat during AI response
            self.editing_chat_id = ""
        else:
            self._ensure_chat_exists_and_is_selected()

    @rx.event
    def new_chat(self):
        existing_titles = {chat['title'] for chat in self.conversations.values()}
        chat_num = 1; new_title = f"Chat {chat_num}"
        while new_title in existing_titles: chat_num += 1; new_title = f"Chat {chat_num}"
        self._create_and_select_new_chat(new_title)
        self.is_typing = False
        self.editing_chat_id = ""

    @rx.event
    def set_current_message(self, message: str):
        self.current_message = message

    @rx.event
    async def send_message(self):
        message_to_send = self.current_message.strip()
        if not message_to_send or self.is_typing: # Prevent sending if already processing
            self.current_message = ""
            return

        self._ensure_chat_exists_and_is_selected()
        current_convo = self.conversations[self.current_chat_id]
        if not current_convo["messages"] and current_convo["title"].startswith("Chat "):
            title = (message_to_send[:20] + "..." if len(message_to_send) > 20 else message_to_send)
            current_convo["title"] = title
        
        current_convo["messages"].append({"text": message_to_send, "is_ai": False})
        current_convo["messages"].append({"text": "", "is_ai": True}) # AI placeholder
        
        self.is_typing = True # Start "thinking" indication
        self.current_message = ""
        yield # Update UI: show user message, AI placeholder with "Thinking...", set button to loading
        
        # Call the method that gets the full response and then simulates typing
        yield ChatState.fetch_and_simulate_typing_ai_response

    @rx.event(background=True)
    async def fetch_and_simulate_typing_ai_response(self): # Renamed for clarity
        print("DEBUG: fetch_and_simulate_typing_ai_response called")
        if not self.current_chat_id or self.current_chat_id not in self.conversations:
            print(f"DEBUG: fetch_and_simulate - Invalid current_chat_id: {self.current_chat_id}")
            async with self: self.is_typing = False
            return

        chat = self.conversations[self.current_chat_id]
        user_message_text = ""
        # The user message is the one before the last AI placeholder
        if chat["messages"] and len(chat["messages"]) >= 2 and not chat["messages"][-2]["is_ai"]:
            user_message_text = chat["messages"][-2]["text"]
        
        if not user_message_text:
            print("DEBUG: fetch_and_simulate - Could not find user_message_text.")
            async with self:
                if chat["messages"] and chat["messages"][-1]["is_ai"] and chat["messages"][-1]["text"] == "":
                    chat["messages"].pop() # Remove empty AI placeholder
                self.is_typing = False
            return
        
        print(f"DEBUG: Getting full API response for: '{user_message_text}'")
        url = f"{API_BASE_URL}/runs"
        params = {"agent_id": AGENT_ID_PARAM} # No "stream=true"
        form_data_payload = {"message": user_message_text}
        full_ai_reply_text = ""

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    url, params=params, data=form_data_payload, timeout=60.0
                )
                print(f"DEBUG: Full API Response Status: {response.status_code}")
                response.raise_for_status()
                response_data = response.json()
                print(f"DEBUG: Full API Response JSON: {response_data}")
                full_ai_reply_text = response_data.get("content")

                if full_ai_reply_text is None or not isinstance(full_ai_reply_text, str):
                    full_ai_reply_text = "Error: AI response format incorrect (content missing or not string)."
                    print(f"DEBUG: Invalid AI reply. Data: {response_data}")

        except httpx.HTTPStatusError as e:
            full_ai_reply_text = f"API Error ({e.response.status_code}): {e.response.text}"
            print(f"DEBUG: HTTPStatusError: {full_ai_reply_text}")
        except Exception as e:
            full_ai_reply_text = f"An error occurred: {str(e)}"
            print(f"DEBUG: General Exception: {full_ai_reply_text}")
        
        # --- Start Simulated Typing Animation ---
        # The `is_typing` state is still True.
        # Clear the AI placeholder text before starting the animation.
        async with self:
            if self.current_chat_id in self.conversations and \
               self.conversations[self.current_chat_id]["messages"] and \
               self.conversations[self.current_chat_id]["messages"][-1]["is_ai"]:
                 self.conversations[self.current_chat_id]["messages"][-1]["text"] = ""
        yield # Update UI to clear any "Thinking..." before character simulation

        if full_ai_reply_text:
            delay_per_char = 1.0 / self.SIMULATED_TYPING_SPEED_CPS
            current_displayed_text_in_sim = ""
            for char_index in range(len(full_ai_reply_text)):
                # Safety check: if user switched chat or is_typing became false, stop simulation
                if not self.is_typing or self.current_chat_id not in self.conversations or \
                   not self.conversations[self.current_chat_id]["messages"] or \
                   not self.conversations[self.current_chat_id]["messages"][-1]["is_ai"]:
                    print("DEBUG: Typing simulation interrupted (chat changed or typing stopped).")
                    break 

                current_displayed_text_in_sim += full_ai_reply_text[char_index]
                async with self:
                    # Re-check context before state update inside loop
                    if self.current_chat_id in self.conversations and \
                       self.conversations[self.current_chat_id]["messages"] and \
                       self.conversations[self.current_chat_id]["messages"][-1]["is_ai"]:
                        self.conversations[self.current_chat_id]["messages"][-1]["text"] = current_displayed_text_in_sim
                yield # Update UI with new character
                await asyncio.sleep(delay_per_char)
        else: # If full_ai_reply_text was empty or became an error message
             async with self:
                if self.current_chat_id in self.conversations and \
                   self.conversations[self.current_chat_id]["messages"] and \
                   self.conversations[self.current_chat_id]["messages"][-1]["is_ai"]:
                    self.conversations[self.current_chat_id]["messages"][-1]["text"] = full_ai_reply_text if full_ai_reply_text else "No response."

        async with self:
            self.is_typing = False # Typing simulation finished
        print("DEBUG: Simulated typing finished.")
        # yield # Final update for is_typing (often implicit with state change)

    @rx.event
    def set_editing_chat(self, chat_id: str):
        self.editing_chat_id = chat_id

    @rx.event
    def rename_chat_from_form(
        self, form_data: dict[str, str]
    ):
        new_title = form_data.get("new_title", "").strip()
        chat_id = self.editing_chat_id
        if chat_id in self.conversations and new_title:
            self.conversations[chat_id]["title"] = new_title
        self.editing_chat_id = ""

    @rx.event
    def rename_chat_from_input(self):
        self.editing_chat_id = ""

    @rx.event
    def delete_chat(self, chat_id: str):
        if chat_id in self.conversations:
            del self.conversations[chat_id]
        if self.current_chat_id == chat_id:
            self.current_chat_id = ""
            self.editing_chat_id = ""
            self.is_typing = False
    
    @rx.var
    def display_messages(self) -> List[Message]:
        # if not self.conversations:
        #     self._ensure_chat_exists_and_is_selected()  # Only create when UI needs it
        return self.messages