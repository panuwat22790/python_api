import cx_Freeze

executables = [cx_Freeze.Executable("hello.py")]

cx_Freeze.setup(
    name="HelloWorld",
    version="0.1",
    description="A simple Hello World script",
    executables=executables
)