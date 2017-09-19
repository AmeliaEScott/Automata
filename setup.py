from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
buildOptions = dict(packages = [], excludes = [])

import sys
base = 'Win32GUI' if sys.platform=='win32' else None

executables = [
    Executable('gui.py', base=base, targetName = 'Automata')
]

setup(name='Automata',
      version = '0.1',
      description = 'Simulates finite automata for CS 422: Automata Theory',
      options = dict(build_exe = buildOptions),
      executables = executables)
