from setuptools import setup

APP = ['src/app.py']
DATA_FILES = []
OPTIONS = {
    'argv_emulation': True,
    'plist': {
        'LSUIElement': True,  # Make it a background app
        'CFBundleName': 'Red Light Green Light',
        'CFBundleDisplayName': 'Red Light Green Light',
        'CFBundleIdentifier': 'com.dannytayara.redlightgreenlight',
        'CFBundleVersion': '0.1.0',
        'CFBundleShortVersionString': '0.1.0',
        'NSHumanReadableCopyright': '© 2025 Danny Tayara',
    },
    'packages': ['rumps', 'anthropic', 'mss', 'PIL', 'keyring', 'PyQt6'],
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
    install_requires=[
        'rumps==0.4.0',
        'mss==9.0.1',
        'anthropic==0.49.0',
        'pillow==10.2.0',
        'keyring==24.3.0',
        'PyQt6==6.5.0',
    ],
    name="red-light-green-light",
    version="0.1.0",
)