@ ECHO On
set MODEL_SRC_DIR=C:\ProgramData\miniforge3
call %MODEL_SRC_DIR%\Scripts\activate.bat
::call cd c:\
call cd %~dp0
call conda create --name NuEdgeWise_env_test  python=3.8.13
call conda activate NuEdgeWise_env_test
call pip install -r requirements.txt
::call jupyter lab
pause