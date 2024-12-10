@echo off

call variables_no_vela.bat

set model_argu= --tflite_path %MODEL_SRC_DIR%\%MODEL_SRC_FILE% --output_dir %GEN_SRC_DIR% --template_dir %TEMPLATES_DIR%

@echo on

Tool\tflite2cpp\gen_model_cpp.exe %model_argu%

pause
