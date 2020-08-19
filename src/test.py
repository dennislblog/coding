import unittest
import argparse
import importlib
import os
import sys
import glob
import unittest
import json


class TestSolution(unittest.TestCase):

    @classmethod
    def inject(cls, function, test_cases):
        cls.function = function
        cls.test_cases = test_cases

    def testSolution(self):
        for case in self.test_cases:
            try:
                result = self.function(**case["args"])
                expect = case["expected"]
                if isinstance(expect, list):
                    if isinstance(result, list):
                        result = sorted(result)
                    expect = sorted(expect)
                    self.assertListEqual(result, expect)
                elif isinstance(expect, dict):
                    self.assertDictEqual(result, expect)
                else:
                    self.assertEqual(result, expect)

            except AssertionError as e:
                msg = color_print("\n'expect': %s \n'actual': %s" %
                                  (case["expected"], result), BColors.FAIL)
                print("input:", case["args"],  msg)
                # print(e.message)
                raise


class BColors(object):
    HEADER = '\033[95m'
    OK_BLUE = '\033[94m'
    OK_GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    END_COLOR = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def color_print(string, color):
    return color + string + BColors.END_COLOR


def load_json(filename):
    with open(filename) as fp:
        return json.load(fp)


if __name__ == "__main__":
    id = sys.argv[1]
    del sys.argv[1:]
    problem = glob.glob(id + '*.py')
    filename = os.path.splitext(problem[0])[0]
    if not problem:
        sys.stdout.write("problem isn't found")

    ### load the module ###
    module = importlib.import_module(filename)
    solution = getattr(module, 'Solution', None)

    ### load the test case file ###
    testfile = "test_data/%s.json" % filename
    testdata = load_json(testfile)
    method_name, test_cases = testdata["problem"], testdata["test_cases"]
    funcall = getattr(solution(), method_name)

    ### start test ###
    TestSolution.inject(funcall, test_cases)
    unittest.main()
