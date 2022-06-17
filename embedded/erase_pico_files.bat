:: Use your COM port as an argument while calling this script (ex: copy_files_to_pico.bat COM5)

@rshell -p %1 --buffer-size 512 rm -r /pyboard/
@echo Pico cleaned
