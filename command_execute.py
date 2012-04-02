import re
import os
import subprocess

VALID_COMMANDS = {
    "sed": {"params": True},
    "ls":  {"params": False},
    "cat": {"params": True},
    #"echo": {"params": True},
    "pwd": {"params": False},
    "grep": {"params": True},
}

alphanum_regex = re.compile("^[$\w\d_/-]+$")

class CommandException(Exception):
    def __init__(self, value):
        self.parameter = value

    def __str__(self):
        return str(self.parameter)

class InvalidCommand(CommandException):
    pass

class SingleCommandOnly(CommandException):
    pass

class InStringError(CommandException):
    pass

class RunError(CommandException):
    pass

def parse(command):
    in_string = False
    string_char = None

    commands = []
    current_command = []
    current_subsection = ""

    for char in command:
        if not in_string:
            if char == '"' or char == "'":
                in_string = True
                string_char = char
                current_subsection += char
            elif char == ";":
                raise SingleCommandOnly("Cannot use ;")
            elif char == " ":
                if current_subsection != "":
                    current_command.append(current_subsection)
                current_subsection = ""
            elif char == "|":
                if current_command:
                    commands.append(current_command)
                current_command = []
            else:
                if not alphanum_regex.match(char):
                    raise InvalidCommand("Invalid character: %s" %char)
                current_subsection += char
        else:
            if char == string_char:
                in_string = False
            current_subsection += char
    if current_subsection != "":
        current_command.append(current_subsection)
    if current_command:
        commands.append(current_command)

    if in_string:
        raise InStringError("Unended string")

    for command in commands:
        if command[0] not in VALID_COMMANDS:
            raise InvalidCommand("Invalid command: %s" %command[0])
        command_dict = VALID_COMMANDS[command[0]]
        if command_dict["params"] and len(command) < 2:
            raise InvalidCommand("'%s' requires a parameter" %command[0])
    return commands

def execute(command):
    commands = parse(command)
    os.chdir("/home/divineslayer")
    #Using shell=True allows you to execute as a string
    #rather than as a list. This seems riskier.
    cmdout = open("/dev/null", "r")
    for command in commands:
        command = " ".join(command)
        handler = subprocess.Popen(command, shell=True, stdin=cmdout, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        error = handler.stderr.read()
        if error:
            raise RunError("Error running command: %s" %error)
        cmdout = handler.stdout
    return cmdout.read()
