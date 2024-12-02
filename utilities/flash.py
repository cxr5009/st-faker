# ./utilities/flash.py

import streamlit as st
from typing import Optional

class FlashMessage:
    """
    A utility class for managing flash messages in Streamlit applications.
    
    This class allows setting and displaying messages that persist across 
    Streamlit reruns, ensuring users have time to read important notifications.
    """
    
    # Class-level constants for message types
    SUCCESS = "success"
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"
    EXCEPTION = "exception"
    
    @staticmethod
    def _ensure_session_state():
        """
        Ensure the necessary session state keys are initialized.
        """
        if 'flash_messages' not in st.session_state:
            st.session_state.flash_messages = []
    
    @classmethod
    def flash(cls, 
              message: Optional[str] = None, 
              message_type: str = SUCCESS) -> None:
        """
        Set or display flash messages.
        
        Args:
            message (Optional[str]): The message to flash. 
                                     If None, displays existing messages.
            message_type (str): Type of message (success, error, warning, info).
                                Defaults to success.
        
        Usage:
            # Set a message to be displayed
            FlashMessage.flash("Operation successful!", FlashMessage.SUCCESS)
            
            # Display any existing messages
            FlashMessage.flash()
        Returns:
            bool: True if a message was added or displayed, False otherwise
        """
        cls._ensure_session_state()
        
        # If a new message is provided, add it to the queue
        if message:
            st.session_state.flash_messages.append({
                'message': message,
                'type': message_type
            })
            return True
        
        # Display all queued messages
        displayed = False
        if st.session_state.flash_messages:
            messages_to_display = st.session_state.flash_messages.copy()
            st.session_state.flash_messages.clear()
        
            # Display messages based on their type
            for msg in messages_to_display:
                if msg['type'] == cls.SUCCESS:
                    st.success(msg['message'])
                elif msg['type'] == cls.ERROR:
                    st.error(msg['message'])
                elif msg['type'] == cls.WARNING:
                    st.warning(msg['message'])
                elif msg['type'] == cls.INFO:
                    st.info(msg['message'])
                displayed = True

        return displayed
    
    @classmethod
    def success(cls, message: str) -> None:
        """
        Shortcut method to flash a success message.
        
        Args:
            message (str): The success message to display.
        """
        cls.flash(message, cls.SUCCESS)
    
    @classmethod
    def error(cls, message: str) -> bool:
        """
        Shortcut method to flash an error message.
        
        Args:
            message (str): The error message to display.

        Returns:
            bool: True if message was added
        """
        cls.flash(message, cls.ERROR)
    
    @classmethod
    def warning(cls, message: str) -> bool:
        """
        Shortcut method to flash a warning message.
        
        Args:
            message (str): The warning message to display.

        Returns:
            bool: True if message was added
        """
        cls.flash(message, cls.WARNING)
    
    @classmethod
    def info(cls, message: str) -> bool:
        """
        Shortcut method to flash an info message.
        
        Args:
            message (str): The info message to display.

        Returns:
            bool: True if message was added
        """
        cls.flash(message, cls.INFO)

    @classmethod
    def exception(cls, message: str) -> bool:
        """
        Shortcut method to flash an exception message.
        
        Args:
            message (str): The exception message to display.

        Returns:
            bool: True if message was added
        """
        cls.flash(message, cls.EXCEPTION)

# Convenience import to allow direct use
flash = FlashMessage.flash
