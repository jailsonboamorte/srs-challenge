import inspect


def get_last_call():
    frame = inspect.trace()[0]
    caller_function_name = frame.function
    caller_line_number = frame.lineno
    caller_file_name = frame.filename

    return "{}:{}:{}".format(caller_function_name, caller_file_name, caller_line_number)
