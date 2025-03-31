from setuptools import setup

APP = ['src/app.py']
DATA_FILES = []
OPTIONS = {
    'argv_emulation': True,
    'plist': {
        'LSUIElement': True,
    },
    'packages': ['rumps', 'anthropic', 'mss', 'PIL', 'keyring'],
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
    install_requires=[
        'rumps==0.4.0',
        'mss==9.0.1',
        'anthropic==0.21.4',
        'pillow==10.2.0',
    ],
    name="RedLightGreenLight",
    version="0.1.0",
)