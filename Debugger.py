import inspect
import os

# chatgpt generated lmaolmaolmao
def debugPrint(*args, **kwargs):
    frame = inspect.currentframe().f_back
    filename = frame.f_code.co_filename
    filename = os.path.basename(filename)
    line_number = frame.f_lineno
    clickable_link = f"\033[90m\033]8;;file:///{filename}:{line_number}\033\\{filename}:{line_number}\033]8;;\033\\\033[0m"
    
    output = f"{' '.join(map(str, args))}".rstrip()
    print(f"{output:<{80}}{clickable_link}")