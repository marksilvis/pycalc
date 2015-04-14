import unittest
import math, sys
from calc import Calculator

class CalcTests(unittest.TestCase):

    def setUp(self):
        """Create calculator class"""
        self.calc = Calculator()

    def tearDown(self):
        """Destroy calculator class"""
        del self.calc

    def testGetCommands(self):
        """Ensures command list is returned correctly"""
        expected = ("constants: display mathematical constants\n"
                    "exit: close calculator\n"
                    "help: show help\n"
                    "history: input history\n"
                    "prev: previous input\n"
                    "var: save variable\n"
                    "variables: display saved variables")
        commands = self.calc.get_commands()
        self.assertEqual(commands, expected)

    def testAddtoHistoryKey(self):
        """Ensures history is correctly added to"""
        line = "1+2"
        ans = "3"
        self.calc.add_to_history(line, ans)
        self.assertIn(line, self.calc._history)

    def testAddToHistoryValue(self):
        """Ensures answer is correctly added to history"""
        line= "1+2"
        ans = "3"
        self.calc.add_to_history(line, ans)
        self.assertEqual(ans, self.calc._history[line])

    def testGetHistoryNoHistory(self):
        """Ensures history is clear when no calculations have been input"""
        expected = ""
        history = self.calc.get_history()
        self.assertEqual(history, expected)

    def testGetHistoryWithHistory(self):
        """Ensures history returns correct values when calculations have been input"""
        expected = ("1+2 = None\n"
                    "2 * 2 = None")
        self.calc.add_to_history("1+2", "None")
        self.calc.add_to_history("2 * 2", "None")
        history = self.calc.get_history()
        self.assertEqual(history, expected)

    def testGetPrevious(self):
        """Ensures get_previous returns last calculation"""
        self.calc.add_to_history('1+2', '3')
        self.calc.add_to_history('2 * 2', '4')
        self.calc.add_to_history('10/5', '2')
        prev = self.calc.get_previous()
        self.assertEqual('10/5', prev)

    def testGetPreviousWithAnswer(self):
        """Ensures get_previous returns the answer to the last calculation when requested"""
        self.calc.add_to_history('1+2', '3')
        self.calc.add_to_history('2 * 2', '4')
        self.calc.add_to_history('10/5', '2')
        prev, ans = self.calc.get_previous(True)
        self.assertEqual('2', ans)

    def testSetAnswer(self):
        """Ensures previous answer constant gets set"""
        self.calc.set_answer('5')
        self.assertEqual(self.calc._constants['ans'], '5')

    def testSetVariable(self):
        """Ensures that variables can be set correctly"""
        expected = "five set to 5"
        actual = self.calc.set_variable('five', '5')
        self.assertEqual(actual, expected)

    def testSetVariableKeyInVariablesDict(self):
        """Ensures setting variable adds key to variables dict"""
        self.calc.set_variable('five', '5')
        self.assertIn('five', self.calc._variables)

    def testSetVariableValueInVariablesDict(self):
        """Ensures setting variable addes value to variables dict"""
        self.calc.set_variable('five', '5')
        self.assertEqual(self.calc._variables['five'], '5')

    def testSetVariableInvalidKey(self):
        """Ensures only a valid variable may be added (an identifier)"""
        expected = "Error: Variable must begin with a letter"
        actual = self.calc.set_variable('5', '5')
        self.assertEqual(actual, expected)

    def testSetVariableInvalidValue(self):
        """Ensures only a valid value may be added (a number, integer or decimal)"""
        expected = "Error: Value must be an integer or decimal"
        actual = self.calc.set_variable('five', 'X')
        self.assertEqual(actual, expected)

    def testSetVariableInvalidValueLong(self):
        """Ensures only a valid value may be added (integer or decimal)
        Tests for previous error of allowing very long strings
        """
        expected = "Error: Value must be an integer or decimal"
        actual = self.calc.set_variable('t', '9324u2389423723742384')
        self.assertEqual(actual, expected)

    def testSetVariableNoCommandOverride(self):
        """Ensures set_variable does not override commands"""
        self.calc.set_variable('help', '5')
        self.assertNotEqual(self.calc._commands['help'], '5')

    def testSetVariableNoConstantOverride(self):
        """Ensures set_variable does not override constants"""
        self.calc.set_variable('pi', '3.14')
        self.assertNotEqual(self.calc._constants['pi'], '3.14')

    def testGetVariablesNoVariables(self):
        """Ensures no variables are returned by get_variables if none have been added"""
        expected = ""
        variables = self.calc.get_variables()
        self.assertEqual(expected, variables)

    def testGetVariablesWithVariables(self):
        """Ensures all variables are returned by get_variables after variables have been added"""
        expected = ("five = 5\n"
                    "ten = 10")
        self.calc.set_variable('ten', '10')
        self.calc.set_variable('five', '5')
        variables = self.calc.get_variables()
        self.assertEqual(variables, expected)

    def testGetConstants(self):
        """Ensures all constants are returned by get_constants"""
        expected = ("ans = None\n"
                    "e = {0}\n"
                    "pi = {1}".format(math.e, math.pi))
        constants = self.calc.get_constants()
        self.assertEqual(constants, expected)

    def testCheckForVariablesDoesNotExist(self):
        """If input contains a variable or constant, it replaces it with its value
        Ensures that, if the variable doesn't exist, it fails
        """
        eval = "hello"
        expected = None
        actual = self.calc.check_for_variables(eval)
        self.assertEqual(actual, expected)

    def testCheckForVariablesValidVariable(self):
        """If input contains a variable, it should be replaced with its value
        Ensures that, if the variable exists, it is replaced
        """
        var = "x"
        self.calc.set_variable(var, '5')
        result = self.calc.check_for_variables(var)
        self.assertEqual(result, '5')

    def testCheckForVariableValidConstant(self):
        """Ensures that constants are replaced with their appropriate value"""
        eval = 'pi'
        result = self.calc.check_for_variables(eval)
        self.assertEqual(result, str(math.pi))

    def testCheckForVariableValidAnswer(self):
        """Ensures the previous answer constant is added"""
        self.calc.set_answer('5')
        result = self.calc.check_for_variables('ans')
        self.assertEqual(result, '5')

    def testCheckEqualParensEqual(self):
        """Ensures method returns true when input has equal number of left and right parentheses"""
        eval = '((2))'
        result = self.calc.check_equal_parens(eval)
        self.assertTrue(result)

    def testCheckEqualParensNotEqual(self):
        """Ensures method returns false when input has inequal number of left and right parentheses"""
        eval = '(((2))'
        result = self.calc.check_equal_parens(eval)
        self.assertFalse(result)

    def testCalculateReturnsCorrectAdd(self):
        """Ensures calculation is correct for addition"""
        eval = "2+2"
        expected = 4.0
        answer = self.calc.calculate(eval)
        self.assertEqual(answer, expected)

    def testCalculateReturnsCorrectSub(self):
        """Ensures calculation is correct for subtraction"""
        eval = '2-2'
        expected = 0.0
        answer = self.calc.calculate(eval)
        self.assertEqual(answer, expected)

    def testCalculateReturnsCorrectMult(self):
        """Ensures calculation is correct for multiplication"""
        eval = '2*2'
        expected = 4.0
        answer = self.calc.calculate(eval)
        self.assertEqual(answer, expected)

    def testCalculateReturnsCorrectDiv(self):
        """Ensures calculation is correct for division"""
        eval = '2/2'
        expected = 1.0
        answer = self.calc.calculate(eval)
        self.assertEqual(answer, expected)

    def testCalculateReturnsCorrectModulo(self):
        """Ensures calculation is correct for modulus"""
        eval = '10%2'
        expected = 0.0
        answer = self.calc.calculate(eval)
        self.assertEqual(answer, expected)

    def testCalculateReturnsCorrectPower(self):
        """Ensures calculation is correct for eponentiation"""
        eval = '2^2'
        expected = 4.0
        answer = self.calc.calculate(eval)
        self.assertEqual(answer, expected)

    def testCalculateReturnsCorrectComplex(self):
        """Ensures calculation is correct for a more complex calculation"""
        eval = '((10^2/2)*5)-300'
        expected = -50.0
        answer = self.calc.calculate(eval)
        self.assertEqual(answer, expected)

    def testCalculateReturnsCorrectConstant(self):
        """Ensures calculation is correct with constant"""
        eval = '2*pi'
        eval = self.calc.verify(eval)
        expected = 2*math.pi
        answer = self.calc.calculate(eval)
        self.assertEqual(answer, expected)

    def testCalculateReturnsCorrectVariable(self):
        """Ensures calculation is correct with variable"""
        self.calc.set_variable('five', '5')
        eval = 'five^2'
        eval = self.calc.verify(eval)
        expected = 25.0
        answer = self.calc.calculate(eval)
        self.assertEqual(answer, expected)

if __name__ == '__main__':
    unittest.main()
