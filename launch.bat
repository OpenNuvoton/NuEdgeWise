@ECHO ON
:: Update this path if Miniforge is installed elsewhere.
set MODEL_SRC_DIR=C:\ProgramData\miniforge3
call "%MODEL_SRC_DIR%\Scripts\activate.bat"
cd /d "%~dp0"
call conda create --name NuEdgeWise_env python=3.9.13 -y
call conda activate NuEdgeWise_env
call python -m pip install -r requirements.txt
::call jupyter lab
pause