import sys
import re
import signal
from collections import deque, Counter

# Define global variables for summary tracking
search_count = 0
total_matches = 0
search_terms = Counter()

# Define constants for command-line options
HELP = "help"
SEARCH = "search"
EXIT = "-1"

permissibleCommands = {
    HELP: {"expectedInputs": [], "usage": "Usage: help"},
    SEARCH: {"expectedInputs": [], "usage": "Usage: search <word1>,<word2> - Searches words in messages"},
    EXIT: {"expectedInputs": [], "usage": "exits the application and provides the stats"}
}

# Store all messages
messages = []

def read_messages_from_files(file_paths):
    """Reads all lines from given input files and stores them"""
    global messages
    for file_path in file_paths:
        try:
            with open(file_path, 'r') as file:
                file_messages = file.readlines()
                if file_messages:
                    messages.extend([msg.strip() for msg in file_messages])
                else:
                    print(f"Warning: {file_path} is empty, continuing without error.")
        except FileNotFoundError:
            print(f"Error: File {file_path} not found.")
        except Exception as e:
            print(f"Error reading {file_path}: {e}")


def searchREPL():
    """The main Read-Evaluate-Print-Loop for command-line interaction."""
    print("\nWelcome to the search tool...")
    while True:
        userInput = input(">>> ").strip()
        parsedInput = parseAndValidateCommand(userInput)
        if parsedInput["command"] == "NoOp":
            continue
        processCommand(parsedInput)


def processCommand(parsedInput):
    """Processes commands based on the parsed input."""
    command = parsedInput["command"]
    if command == HELP:
        processHelp()
    elif command == SEARCH:
        processSearch(parsedInput["inputs"])
    elif command == EXIT:
        processExit()


def parseAndValidateCommand(userInput):
    """Validates the user command and arguments."""
    inputArr = deque(userInput.split(' '))
    command = inputArr.popleft().lower()
    if command in permissibleCommands:
        return {"command": command, "inputs": inputArr}
    else:
        print("Invalid command. Type 'help' for available commands.")
        return {"command": "NoOp"}


def processHelp():
    """Displays usage information for available commands."""
    print("\nAvailable commands:")
    for cmd, details in permissibleCommands.items():
        print(f"{cmd}: {details['usage']}")
    print()

def processSearch(inputs):
    """Handles the search functionality."""
    global search_count, total_matches, search_terms
    search_count += 1

    if not inputs:
        print("Error: No search terms provided.")
        return

    search_words = ' '.join(inputs).split(',')
    mostFrequentTerms(search_words)
    matches_found = False
    matches_in_search = 0

    for msg in messages:
        highlighted_msg = msg
        msg_match_count = 0
        for word in search_words:
            pattern = re.compile(re.escape(word), re.IGNORECASE)
            if re.search(pattern, msg):
                highlighted_msg = pattern.sub(lambda m: m.group(0).upper(), highlighted_msg)
                matches_found = True
                msg_match_count += len(re.findall(pattern, msg))

        if msg_match_count > 0:
            total_matches += msg_match_count
            matches_in_search += msg_match_count
            print(highlighted_msg)

    if not matches_found:
        print("No matches found.")
    else:
        print(f"Total matches in this search: {matches_in_search}\n")


def processExit():
    """Displays summary information and exits the program."""
    print("\nExiting the program...")
    print("Summary:")
    print(f"Total searches performed: {search_count}")
    print(f"Total words matched across all input files: {total_matches}")
    if search_terms:
        print("Most frequent search terms:")
        for term, count in search_terms.most_common():
            print(f"{term}: {count} times")
    sys.exit(0)

def mostFrequentTerms(search_words):
    for word in search_words:
        search_terms[word.lower()] += 1

def handleCtrlC(sig, frame):
    """Handles Ctrl+C to provide a graceful exit."""
    print("\nReceived interrupt signal. Exiting gracefully...")
    processExit()


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python main.py input1.txt input2.txt ...")
        sys.exit(1)

    signal.signal(signal.SIGINT, handleCtrlC)
    read_messages_from_files(sys.argv[1:])
    searchREPL()
