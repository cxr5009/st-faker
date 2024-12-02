# ./mapper_playground.py

# Third-party imports
import streamlit as st
from faker import Faker
import json

# Local imports
from utilities.display_debug import display_debug
from utilities.flash import FlashMessage, flash

st.set_page_config(
    page_title="Mapper",
    page_icon=":material/map:",
    layout="wide",
    menu_items={
        "Get help": None,
        "Report a bug": None,
        "About": None,
    },
)

def get_providers_from_json(path_to_json):
    """
    Get all available providers from the JSON file.
    """
    with open(path_to_json) as f:
        data = json.load(f)
    return data

def get_faker_providers(module):
    """
    Get all available providers from the faker module.
    """
    providers = []
    for provider in dir(module):
        if not provider.startswith("_"):
            providers.append(provider)
    return providers

def generate_provider_group_layout(provider_group):
    """
    Generate the layout for a group of providers and return the selected providers.
    """
    toggle_settings = provider_group["group"]["toggle"]
    popover_settings = provider_group["group"]["popover"]
    pills_data = provider_group["group"]["popover"]["pills"]
    
    with st.container():
        col1, col2 = st.columns([1, 3])
        with col1:
            is_enabled = st.toggle(
                label=toggle_settings["label"],
                value=toggle_settings["value"],
                key=toggle_settings["key"],
                help=toggle_settings["help"],
                on_change=toggle_settings["on_change"],
                args=toggle_settings["args"],
                kwargs=toggle_settings["kwargs"],
                disabled=toggle_settings["disabled"],
                label_visibility=toggle_settings["label_visibility"],
            )

        with col2:
            with st.popover(
                label=popover_settings["label"],
                help=popover_settings["help"],
                icon=popover_settings["icon"],
                disabled=not is_enabled,
                use_container_width=popover_settings["use_container_width"],
            ):
                st.pills(
                    label=pills_data["label"],
                    options=pills_data["options"],
                    selection_mode=pills_data["selection_mode"],
                    default=pills_data["default"],
                    format_func=pills_data["format_func"],
                    key=pills_data["key"],
                    help=pills_data["help"],
                    on_change=pills_data["on_change"],
                    args=pills_data["args"],
                    kwargs=pills_data["kwargs"],
                    disabled=pills_data["disabled"],
                    label_visibility=pills_data["label_visibility"],
                )

def build_faker_config():
    """
    Build and set the faker configuration based on the selected providers.
    st.session_state stores the status of each *_toggle and assoicated *_pills based on the toggle key name and pills key name.
    """
    selected_providers = []
    for key, value in st.session_state.items():
        if key.endswith("_toggle") and value:
            for provider in st.session_state[key.replace("_toggle", "_pills")]:
                selected_providers.append(provider)
    
    if selected_providers:
        st.session_state["providers"] = selected_providers
    
def fake_json_preview(config = None, faker = None) -> None:
    """
    Display the JSON faker preview based off the configuration.
    """
    try:
        if config:
            if not faker:
                fake = Faker()
            fake_json = st.json(fake.json(config))
            return fake_json
    except Exception as e:
        flash(f"An error occurred: {e}", FlashMessage.ERROR)
        return None

PATH_TO_PROVIDERS_JSON = "./providers.json"

st.logo("images/logo.svg", size="large")
st.title("Streamlit Faker Playground")


with st.container():

    FlashMessage.flash()
    col_config, col_preview = st.columns([6, 5])
    with col_config:
        st.header("Configuration Wizard")
        wizard_providers, wizard_options, wizard_generate = st.tabs(["Providers", "Options", "Generate"])
        with wizard_providers:
            st.subheader("Select Providers")
            providers = get_providers_from_json(PATH_TO_PROVIDERS_JSON)
            # loop through each provider group and generate the layout and update session state with each selected pill (provider):
            for provider_group in providers:
                generate_provider_group_layout(provider_group)
                
        with wizard_options:
            st.subheader("Options")
            st.write("Options go here")

        with wizard_generate:
            st.subheader("Generate")
            st.write("Generate goes here")

    with col_preview:
        st.header("Preview")
        faker_config=build_faker_config()
        output_json, output_csv = st.tabs(["JSON", "CSV"])
        with output_json:
            st.subheader("JSON")
            
            # To-Do: Add the JSON preview here
            # if st.session_state.config:
            #     fake_json = fake_json_preview(st.session_state.config)
            # if fake_json:
            #     st.code(fake_json, language="json", line_numbers=True, wrap_lines=True)

            st.code("{foo: 'bar'}", language="json", line_numbers=True, wrap_lines=True)

        with output_csv:
            st.subheader("CSV")
            st.write("CSV goes here")

display_debug(display=True)