from cx_Freeze import setup, Executable
import sys

# Dependencies are automatically detected, but it might need
# fine tuning.
all_build_options = {
    'packages': [],
    'excludes': [],
    'include_files': ["Samples/"]
}

mac_options = {
    'custom_info_plist': 'Info-hires.plist'
}

base = 'Win32GUI' if sys.platform == 'win32' else None

executables = [
    Executable('gui.py', base=base, targetName='Automata')
]

setup(name='Automata',
      version='0.1',
      description='Simulates finite automata for CS 422: Automata Theory',
      options={
          'build_exe': all_build_options,
          'bdist_mac': mac_options,
      },
      executables=executables)
