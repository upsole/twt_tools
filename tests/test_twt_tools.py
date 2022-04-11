from twt_tools import __version__
from twt_tools.thread import Thread
import os 


def test_version():
    assert __version__ == '0.1.0'

def test_thread_finishes():
    name = '1513515770361397253'
    thread = Thread(url=name, thread_name=name)
    thread.build_markdown()
    thread.build_pdf()
    thread.cleanup()
    os.remove(f'{name}.pdf')
    assert True
