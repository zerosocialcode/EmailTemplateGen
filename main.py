import os
import sys
import subprocess
from termcolor import colored
import platform
import json

# Clear screen command based on OS
CLEAR = 'cls' if platform.system() == 'Windows' else 'clear'

def clear_screen():
    os.system(CLEAR)

def load_banner():
    """Loads banner from .banner.txt file"""
    try:
        with open('.banner.txt', 'r') as f:
            banner = f.read()
        return colored(banner, 'red', attrs=['bold'])
    except FileNotFoundError:
        # Default banner if file not found
        default_banner = """               _.------.
           _.-`   (ðŸ§¿).-`\"\"\"-.
 '.__.---'`       _'`   _ .--.)
        -'         '-.-';`
        ' -      _.'  ``'--.                                      '---`    .-'\"\"`\"\"
                   /`
"""
        return colored(default_banner, 'red', attrs=['bold'])

def load_config():
    """Loads configuration from config.json"""
    try:
        with open('.dev.json', 'r') as f:
            config = json.load(f)
        return config
    except (FileNotFoundError, json.JSONDecodeError):
        # Default config if file not found or invalid
        return {
            "tool_name": "TemplateFusion",
            "developer": "Zerosocialcode"
        }

def print_banner():
    """Prints the banner and header information"""
    config = load_config()
    print(load_banner())
    print(colored(f"\n{config['tool_name']}", 'red', attrs=['bold']))
    print(colored(f"developer: {config['developer']}\n", 'red', attrs=['bold']))
    print("-" * os.get_terminal_size().columns)

def refresh_screen(tools=None, current_selection=None):
    """Clears and re-renders the screen with banner"""
    clear_screen()
    print_banner()
    
    if tools:
        list_tools(tools)
    if current_selection:
        print("\n" + colored(f"Running: {current_selection}", 'cyan'))

def scan_tools(base_path):
    tools = {}
    for entry in os.listdir(base_path):
        tool_path = os.path.join(base_path, entry)
        if os.path.isdir(tool_path):
            for main_file in ["__main__.py", "main.py"]:
                main_path = os.path.join(tool_path, main_file)
                if os.path.isfile(main_path):
                    tools[entry] = main_path
    return tools

def list_tools(tools):
    for idx, name in enumerate(tools.keys(), 1):
        print(colored(f"{idx}. {name}", 'cyan'))

def select_tool(tools):
    while True:
        try:
            refresh_screen(tools)
            choice = input(colored("\ntemplatefusion> ", 'yellow'))
            if not choice:
                continue
            choice = int(choice)
            if 1 <= choice <= len(tools):
                tool_name = list(tools.keys())[choice-1]
                return tool_name, tools[tool_name]
            print(colored("Invalid number. Try again.", 'red'))
        except ValueError:
            print(colored("Please enter a number.", 'red'))
        except KeyboardInterrupt:
            graceful_exit()

def run_tool(tool_main_path, tool_dir, tool_name):
    refresh_screen(current_selection=tool_name)
    step(f"Launching '{tool_name}' ...")
    cmd = [sys.executable, os.path.basename(tool_main_path)]
    try:
        # Run tool in a new process group to better handle signals
        subprocess.run(cmd, cwd=tool_dir, check=True)
    except KeyboardInterrupt:
        pass  # Let the tool handle its own interrupt
    except subprocess.CalledProcessError as e:
        print(colored(f"Tool error: {e}", 'red'))
    finally:
        input(colored("\nPress Enter to return to menu...", 'yellow'))

def step(msg):
    print(colored(f"[•] {msg}", 'magenta'))

def graceful_exit():
    clear_screen()
    print(colored("\nThank you for using TemplateFusion. Goodbye!", 'red', attrs=['bold']))
    sys.exit(0)

def main():
    try:
        base_path = os.getcwd()
        tools = scan_tools(base_path)
        if not tools:
            print(colored("No tools detected in this directory.", 'red'))
            sys.exit(1)

        while True:
            tool_name, tool_main_path = select_tool(tools)
            tool_dir = os.path.dirname(tool_main_path)
            run_tool(tool_main_path, tool_dir, tool_name)
            
    except KeyboardInterrupt:
        graceful_exit()

if __name__ == "__main__":
    main()
