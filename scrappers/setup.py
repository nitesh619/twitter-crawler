from cx_Freeze import setup, Executable

setup(name='Crawler',
      version='1.0',
      description='Twitter search',
      executables=[Executable("Twitter_Search.py")])
