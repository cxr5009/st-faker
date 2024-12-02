# ./utilities/display_debug.py

import streamlit as st

def display_debug(display: bool = False) -> None:
    """
    Display the debug information where called.

    Args:
        display (bool): Whether to display the debug information.
    """
    if st.session_state.get("mode", None) == "DEBUG" or display:
        with st.expander("Debug", expanded=True):
            st.json(st.session_state)
            