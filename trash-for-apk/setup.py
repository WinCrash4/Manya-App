from cx_Freeze import setup, Executable

base = None    

executables = [Executable("main.py", base=base)]

packages = ["idna","kivy","kivymd","re","wikipedia","os","random","psutil","datetime","json","googletrans","requests", "pyaudio"]
options = {
    'build_exe': {    
        'packages':packages,
    },    
}

setup(
    name = "Manya",
    options = options,
    version = "0.1.2",
    description = 'Manya demo-version',
    executables = executables
)