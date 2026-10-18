from agent.shell_runner import ShellRunner

_shell=ShellRunner(timeout=30)

_RAW_TOOLS = [
    _shell.run, read_file, write_file, list_directory, search_files, move_file,
    open_app, open_url, open_path, get_clipboard, set_clipboard,
]