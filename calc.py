""" Python Calculator
A simple Python shell application that evaluates calculator input.

author - Mark Silvis
"""

import sys, math, re
from collections import OrderedDict


class Calculator():
    """Calculator"""
    def __init__(self):
        super(Calculator, self).__init__()
        self._commands = {'exit': 'close calculator',
                         'history': 'input history',
                         'prev': 'previous input',
                         'help': 'show help',
                         'var': 'save variable',
                         'variables': 'display saved variables',
                         'constants': 'display mathematical constants'}
        self._constants = {'pi': math.pi,
                          'e': math.e,
                          'ans': None}
        self._variables = {}
        self._history = OrderedDict()

    def calculate(self, evalute):
        pass

    """ Helper methods """
    # setters
    def set_answer(self, answer):
        """Set answer to that of previous calculation

        args:
        answer -- answer to most recent calculation
        """
        self._constants['ans'] = answer

    def set_variable(self, key, value):
        """Save a variable

        args:
        key -- variable name
        value -- variable value
        """
        if not key.isidentifier():
            return "Error: Variable must begin with a letter"
        elif not re.match("[/^\d*\.?\d*$/]", value):    # variable value may be integer or decimal
            return "Error: Value must be an integer or decimal"
        elif key in self._commands:
            return "Error: Cannot overwrite command"
        elif key in self._constants:
            return "Error: Cannot overwrite constant"
        else:
            self._variables[key] = value
            return "{0} set to {1}".format(key, value)

    def add_to_history(self, line, ans):
        """Add evaluation to history in last position
        
        args:
        line -- user input
        ans  -- answer to calculation
        """
        self._history[line] = ans

    # getters
    def get_previous(self, ans=False):
        """Return last calculation

        args:
        ans -- also return answer to previous input
        """
        # return input and answer
        if ans and len(self._history) != 0:
            prev = next(reversed(self._history))
            out = self._history[prev]
            return prev, out
        # return just input
        elif len(self._history) != 0:
            prev = next(reversed(self._history))
            return prev

        return ""

    def get_history(self):
        """Get calculator's history"""
        history = "\n".join("{0} = {1}".format(i, self._history[i]) for i in self._history)
        return history

    def get_variables(self):
        """Get variables saved in calculator"""
        variables = "\n".join("{0} = {1}".format(i, self._variables[i]) for i in sorted(self._variables))
        return variables

    def get_constants(self):
        """Get all available mathematical constants"""
        constants = "\n".join("{0} = {1}".format(i, self._constants[i]) for i in sorted(self._constants))
        return constants

    def get_commands(self):
        """Get all calculator commands"""
        commands = "\n".join("{0}: {1}".format(i, self._commands[i]) for i in sorted(self._commands))
        return commands            


def main():    
    calc = Calculator()
    print(calc.get_commands() + "\n")

    # calculator repl
    while True:
        # get user input
        try:
            string = input("> ")
            evaluate = string.split()
        except EOFError:
            sys.exit(-1)
        except KeyboardInterrupt:
            print()
            break

        # blank command, do nothing
        if evaluate == []:
            pass

        # else, determine command
        else:
            command = evaluate[0].lower()

        # exit command
        if command == "exit":
            break

        # print input history
        elif command == "history":
            history = calc.get_history()
            print(history)
            if len(history) > 0:
                print()

        # print previous input
        elif command == "prev":
            prev = calc.get_previous()
            print("{0}\n".format(prev)) if len(prev) != 0 else print()

        # print saved variables
        elif command == "variables":
            variables = calc.get_variables()
            print(variables)
            if len(variables) > 0:
                print()

        # print mathematical consants
        elif command == "constants":
            constants = calc.get_constants()
            print(constants)
            if len(constants) > 0:
                print()

        # print commands
        elif command == "help":
            help = calc.get_commands()
            print(help)
            print()

        # save a variable
        elif command == "var":
            if len(evaluate) == 4 and evaluate[2] == "=":
                key = evaluate[1]
                value = evaluate[3]
                store = calc.set_variable(key, value)
                print("{0}\n".format(store))
            elif len(evaluate) > 4:
                print("Error: Invalid var command\nToo many arguments\n")
            else:
                print("Error: Invalid var command\nUsage: var 'variable name' = 'value'\n")

        # calculate
        else:
            answer = calc.calculate(evaluate)
            print("= {0}".format(answer))
            print()

            # save answer and add to history
            calc.add_to_history(string, answer)
            calc.set_answer(answer)

    sys.exit()

if __name__ == '__main__':
    main()