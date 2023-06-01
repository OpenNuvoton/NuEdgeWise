@ ECHO OFF
set MODEL_SRC_DIR=C:\ProgramData\Anaconda3
call %MODEL_SRC_DIR%\Scripts\activate.bat
call cd c:\
::call cd %~dp0
call conda activate NuEdgeWise_env
call jupyter lab