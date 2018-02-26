# -*- coding: utf-8 -*-

import unittest

from pron_dict import tree

class TestSyllabification(unittest.TestCase):

    def test_print_dot(self):
        comptree = tree.BinaryTree()
        comptree.set_data('vaðlaheiðavegavinnu')
        left_tree = tree.BinaryTree()
        left_tree.set_data('vaðlaheiða')
        comptree.set_left(left_tree)
        right_tree = tree.BinaryTree()
        right_tree.set_data('vegavinnu')
        comptree.set_right(right_tree)
        left_left_tree = tree.BinaryTree()
        left_left_tree.set_data('vaðla')
        left_tree.set_left(left_left_tree)
        left_right_tree = tree.BinaryTree()
        left_right_tree.set_data('heiða')
        left_tree.set_right(left_right_tree)
        right_left_tree = tree.BinaryTree()
        right_left_tree.set_data('vega')
        right_tree.set_left(right_left_tree)
        right_right_tree = tree.BinaryTree()
        right_right_tree.set_data('vinnu')
        right_tree.set_right(right_right_tree)


        dot_string = comptree.dot_format()
        print(dot_string)
