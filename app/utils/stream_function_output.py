from fastapi import FastAPI
from starlette.responses import StreamingResponse
import contextlib, io, sys, threading, time, re


def remove_ansi_escape_sequences(text):
    # Updated regex pattern for ANSI escape sequences
    ansi_escape = re.compile(r"\x1B\[[0-?]*[ -/]*[@-~]")
    return ansi_escape.sub("", text)


@contextlib.contextmanager
def capture_output():
    new_out = io.StringIO()
    old_out = sys.stdout
    try:
        sys.stdout = new_out
        yield new_out
    finally:
        sys.stdout = old_out


def stream_function_output(func):
    with capture_output() as captured:

        def run_func():
            func()  # Call the passed-in function
            print("<<EOF>>")  # Signal end of function

        thread = threading.Thread(target=run_func)
        thread.start()
        # Process and yield lines as they are captured
        partial_output = ""
        while True:
            captured.seek(0)
            new_output = captured.read()
            if new_output:
                cleaned_output = remove_ansi_escape_sequences(new_output)
                partial_output += cleaned_output
                while "\n" in partial_output:
                    line, partial_output = partial_output.split("\n", 1)
                    yield f"data: {line}\n\n"
                captured.truncate(0)
                captured.seek(0)
            if "<<EOF>>" in new_output:
                break
            time.sleep(0.1)
    yield "event: close\ndata: bye\n\n"
