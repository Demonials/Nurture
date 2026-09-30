import sys
from pathlib import Path
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from nurture_lang.runtime import Runtime
from nurture_lang.registry import root_suggestions, member_suggestions

class BasicTests(unittest.TestCase):
    def test_variables_and_comparisons(self):
        out = []
        Runtime(out.append).execute(
            'age = 16\n'
            'if age >= 18:\n'
            '    write("adult")\n'
            'elif age >= 13:\n'
            '    write("teen")\n'
            'else:\n'
            '    write("child")'
        )
        self.assertEqual(out, ["teen"])

    def test_all_comparisons(self):
        out = []
        Runtime(out.append).execute(
            'write(5 == 5)\n'
            'write(5 != 4)\n'
            'write(5 < 6)\n'
            'write(5 <= 5)\n'
            'write(5 > 4)\n'
            'write(5 >= 5)\n'
            'write(5 in [1,5])\n'
            'write(5 not in [1,2])'
        )
        self.assertEqual(out, [True, True, True, True, True, True, True, True])

    def test_loop_old(self):
        out = []
        Runtime(out.append).execute("loop i in 1..3:\n    write(i)")
        self.assertEqual(out, [1, 2, 3])

    def test_loop_new_block(self):
        out = []
        Runtime(out.append).execute("loop(1, 3)->\n    write(i)")
        self.assertEqual(out, [1, 2, 3])

    def test_loop_new_inline(self):
        out = []
        Runtime(out.append).execute('loop(1, 3)->write("x")')
        self.assertEqual(out, ["x", "x", "x"])

    def test_loop_reverse(self):
        out = []
        Runtime(out.append).execute("loop(3, 1)->write(i)")
        self.assertEqual(out, [3, 2, 1])

    def test_function(self):
        out = []
        Runtime(out.append).execute(
            "function add(a, b):\n"
            "    return a + b\n"
            "write(add(2, 3))"
        )
        self.assertEqual(out[-1], 5)

    def test_input(self):
        out = []
        Runtime(out.append, input_fn=lambda prompt: "42").execute(
            'age = int(input("Age: "))\nwrite(age + 1)'
        )
        self.assertEqual(out, [43])

    def test_builtin_helpers(self):
        out = []
        Runtime(out.append).execute(
            'write(str(123))\nwrite(float("2.5"))\nwrite(len("Nurture"))\nwrite(type(1))'
        )
        self.assertEqual(out, ["123", 2.5, 7, "int"])

    def test_boolean_logic(self):
        out = []
        Runtime(out.append).execute('write(true and false)\nwrite(true or false)\nwrite(not false)')
        self.assertEqual(out, [False, True, True])

    def test_try_except(self):
        out = []
        Runtime(out.append).execute(
            'try:\n'
            '    write(unknown_name)\n'
            'except:\n'
            '    write("caught")'
        )
        self.assertEqual(out, ["caught"])

    def test_autocomplete(self):
        self.assertIn("while", root_suggestions("w"))
        self.assertIn("web", root_suggestions("w"))
        self.assertIn("write", root_suggestions("w"))
        self.assertIn("web.get()", member_suggestions("web."))
        self.assertIn("input", root_suggestions("in"))

if __name__ == "__main__":
    unittest.main()
