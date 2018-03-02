# -*- coding: utf-8 -*-

import unittest

from pron_dict import tree
from pron_dict import tree_builder
from pron_dict import entry
from pron_dict import syllabification

class TestSyllabification(unittest.TestCase):

    def test_tree_builder(self):
        comp_tree = tree_builder.build_compound_tree(entry.PronDictEntry('ljósvakamiðlar', 'l j ou: s v a k a m I D l a r'))
        syllables = []
        syllabification.syllabify_tree(comp_tree, syllables)
        print(syllables)
        comp_tree.preorder()

    def test_preorder(self):
        comptree = tree.CompoundTree('ljósvakamiðlar')
        comptree.left = tree.CompoundTree('ljósvaka')
        comptree.right = tree.CompoundTree('miðlar')
        comptree.left.left = tree.CompoundTree('ljós')
        comptree.left.right = tree.CompoundTree('vaka')

        comptree.preorder()

        comptree = tree.CompoundTree('atvinnuleysistryggingasjóður')
        comptree.left = tree.CompoundTree('atvinnuleysis')
        comptree.right = tree.CompoundTree('tryggingasjóður')
        comptree.left.left = tree.CompoundTree('atvinnu')
        comptree.left.right = tree.CompoundTree('leysis')
        comptree.right.left = tree.CompoundTree('trygginga')
        comptree.right.right = tree.CompoundTree('sjóður')

        comptree.preorder()

    @unittest.skip('skip this')
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
