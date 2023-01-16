from multiprocessing import Process

import pytest
from webapp.app import app
from flask import Flask

server = None


def start_local_server():
    global server
    server = Process(target=app.run, args=("localhost", 5000))
    server.start()


def stop_local_server():
    global server
    server.terminate()


@pytest.fixture()
def webapp() -> Flask:
    # Start server
    start_local_server()

    # Provide app for testing
    yield app

    stop_local_server()

