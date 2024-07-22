from cx_Freeze import setup, Executable

setup(

       name="X-ray diagnosis",

       version="1.0",

       description="An application that can diagnose covid and pneumonia from X-ray images",

       executables=[Executable("main.py")],

   )   