#%%

import os
import sys
sys.path.append("..")
import json
from pprint import pprint
from src.container_generator.container_validator import validate_container_structure
import unittest

class TestTemplateStructureValidator(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestTemplateStructureValidator, self).__init__(*args, **kwargs)
        current_directory = os.path.dirname(os.path.abspath(__file__))
        test_data_file_path = os.path.join(current_directory, "test_data.json")
        with open(test_data_file_path, "r", encoding="UTF8") as f:
            self.tests = json.load(f)

    def test_empty(self):
        output = validate_container_structure(self.tests["empty"]["input"])
        self.assertEqual(output, self.tests["empty"]["expected output"], )
    
    def test_minimal(self):
        output = validate_container_structure(self.tests["minimal"]["input"])
        self.assertEqual(output, self.tests["minimal"]["expected output"])
    
    def test_nested_depth_1(self):
        output = validate_container_structure(self.tests["nested-depth: 1"]["input"])
        self.assertEqual(output, self.tests["nested-depth: 1"]["expected output"])

    def test_nested_depth_2(self):
        output = validate_container_structure(self.tests["nested-depth: 2"]["input"])
        self.assertEqual(output, self.tests["nested-depth: 2"]["expected output"])

    def test_nested_depth_3(self):
        output = validate_container_structure(self.tests["nested-depth: 3"]["input"])
        self.assertEqual(output, self.tests["nested-depth: 3"]["expected output"])

    def test_nested_depth_4(self):
        output = validate_container_structure(self.tests["nested-depth: 4"]["input"])
        self.assertEqual(output, self.tests["nested-depth: 4"]["expected output"])
    
    def test_leaf_branch_mixed(self):
        output = validate_container_structure(self.tests["leaf, branch mixed"]["input"])
        self.assertEqual(output, self.tests["leaf, branch mixed"]["expected output"])
    
    def test_leaf_not_None_int(self):
        output = validate_container_structure(self.tests["leaf not None(int)"]["input"])
        self.assertEqual(output, self.tests["leaf not None(int)"]["expected output"])

    def test_leaf_not_None_true(self):
        output = validate_container_structure(self.tests["leaf not None(true)"]["input"])
        self.assertEqual(output, self.tests["leaf not None(true)"]["expected output"])
    
    def test_array(self):
        output = validate_container_structure(self.tests["array"]["input"])
        self.assertEqual(output, self.tests["array"]["expected output"])


if __name__ == "__main__":
    unittest.main()
