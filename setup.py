import sys
import os.path
from cx_Freeze import setup, Executable

os.environ['TCL_LIBRARY'] = r'C:\Python36\tcl\tcl8.6'
os.environ['TK_LIBRARY'] = r'C:\Python36\tcl\tk8.6'

setup(
    name = "Better Call Test",
    version = "1.0.0",
    description = "Better Call Test - Test Engineering Manager",
    executables = [Executable("mainwindow.pyw", base="Win32GUI")])
