import os
import streamlit as st
import yaml
from streamlit_authenticator import Authenticate
from yaml.loader import SafeLoader
import logging
import shutil
from dotenv import dotenv_values
from pathlib import Path
from detectaicore import (
    set_up_logging,
)


def main(config):
    """
    Main page APP
    """
    st.set_page_config(layout="wide", initial_sidebar_state="expanded")
    if "authentication_status" not in st.session_state:
        st.session_state["authentication_status"] = None
    if "name" not in st.session_state:
        st.session_state["name"] = None
    if "username" not in st.session_state:
        st.session_state["username"] = None
    st.title("NVIDIA and LlamaIndex Developer Contest")
    if "root_dir" not in st.session_state:
        st.session_state["root_dir"] = os.path.dirname(os.path.abspath(__file__))

    authenticator = Authenticate(
        config["credentials"],
        config["cookie"]["name"],
        config["cookie"]["key"],
        config["cookie"]["expiry_days"],
    )

    authenticator.login(key="Login", location="main")

    logging.info(
        f'Name : {st.session_state["name"]}, Autentication Status: {st.session_state["authentication_status"]}, Username: {st.session_state["username"]}'
    )

    if st.session_state["authentication_status"]:
        authenticator.logout("Logout", "main")
        st.write(f'Welcome *{st.session_state["name"]}*')
    elif st.session_state["authentication_status"] == False:
        st.error("Username/password is incorrect")
    elif st.session_state["authentication_status"] == None:
        st.warning("Please enter your username and password")


if __name__ == "__main__":
    # setup environtment
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    OUT_FOLDER = os.path.join(ROOT_DIR, "out")
    TMP_FOLDER = os.path.join(ROOT_DIR, "tmp")
    ANSWERS_FOLDER = os.path.join(ROOT_DIR, "answers")
    SAVE_FOLDER = os.path.join(ROOT_DIR, "saves")
    # logging
    # Set up logging
    LOGS_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")

    Path(LOGS_PATH).mkdir(parents=True, exist_ok=True)
    script_name = os.path.join(LOGS_PATH, "debug.log")
    # create loggers
    if not set_up_logging(
        console_log_output="stdout",
        console_log_level="info",
        console_log_color=True,
        logfile_file=script_name,
        logfile_log_level="info",
        logfile_log_color=False,
        log_line_template="%(color_on)s[%(asctime)s] [%(threadName)s] [%(levelname)-8s] %(message)s%(color_off)s",
    ):
        print("Failed to set up logging, aborting.")
        raise AttributeError("failed to create logging")
    # create folders if they don't exist
    os.makedirs(OUT_FOLDER, exist_ok=True)
    os.makedirs(TMP_FOLDER, exist_ok=True)
    os.makedirs(ANSWERS_FOLDER, exist_ok=True)
    os.makedirs(SAVE_FOLDER, exist_ok=True)
    # read env file
    config = dotenv_values(os.path.join(ROOT_DIR, "keys", ".env"))

    # key access NVIDIA NIM
    if "NVIDIA_API_KEY" not in os.environ:
        os.environ["NVIDIA_API_KEY"] = config.get("NVIDIA_API_KEY")
    with open("keys/config.yaml") as file:
        auth = yaml.load(file, Loader=SafeLoader)

    main(config=auth)
