import inspect
import os

# chatgpt generated lmaolmaolmao
def debugPrint(*args, **kwargs):
    frame = inspect.currentframe().f_back
    filename = frame.f_code.co_filename
    filename_only = os.path.basename(filename)
    line_number = frame.f_lineno

    vscode_link = f"vscode://file/{filename}:{line_number}"
    clickable_link = f"\033[90m\033]8;;{vscode_link}\033\\{filename_only}:{line_number}\033]8;;\033\\\033[0m"
    output = f"{' '.join(map(str, args))}".rstrip()
    print(f"{output:<{100}}{clickable_link}")