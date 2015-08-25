import os

def get_html_theme_default():
    return 'opendylan-docs'

def get_html_theme_path():
    return os.path.abspath(os.path.dirname(__file__))

def get_html_theme_options_default():
    return {
        'display_version': False
    }
