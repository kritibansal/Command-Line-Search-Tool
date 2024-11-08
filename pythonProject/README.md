# Command-Line Search Tool

This tool allows users to search for words in text files using a command-line interface. It supports multiple commands, including searching for words, displaying help, and exiting the application with a summary of statistics. The tool also provides real-time highlighting of search terms within the messages and tracks the most frequently searched terms.

## Features

**Search for Words:** Perform case-insensitive searches for one or more words across multiple messages.

**Help:** View a list of available commands and their usage.

**Summary on Exit:** Display the total number of searches, word matches, and frequently searched terms when exiting.

**Graceful Exit on Ctrl+C:** Exits gracefully, displaying summary statistics even if interrupted by Ctrl+C.

### Requirements

Python 3.x

### Usage

**Run the Tool**

Execute the tool from the command line, specifying one or more text files as input:

```python main.py input1.txt input2.txt ...```

Once the tool is running, you can use the following commands:

**help:** Displays usage information for all available commands.
Usage: help

**search word1,word2 :** Searches for the specified words in the messages. Words should be separated by commas. Matching words in messages are displayed in uppercase.

Usage: search word1,word2

Example: search hello,world

**-1:** Exits the program, displaying a summary of all searches and matches.

Usage: -1

