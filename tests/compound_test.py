import unittest

from pron_dict_quality_assurance import compound_analysis

class TestCompound(unittest.TestCase):

    def test_compound_analysis(self):
        comp_tree = compound_analysis.build_compound_tree('framhaldsskólanemendur')
        elem_arr = []
        comp_tree.preorder(elem_arr)
        print(str(elem_arr))
