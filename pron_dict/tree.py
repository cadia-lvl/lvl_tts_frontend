#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class BinaryTree:
    def __init__(self):
        self.data = None
        self.left = None
        self.right = None

    def set_left(self, tree):
        self.left = tree

    def set_right(self, tree):
        self.right = tree

    def set_data(self, content):
        self.data = content

    def get_direct_child_data(self):
        return self.left.data, self.right.data

    def traverse_tree(self, dot_string):
        dot_string += self.data + ' -> ' + self.left.data + '\n'
        dot_string += self.data + ' -> ' + self.right.data + '\n'
        return dot_string

    def dot_format(self):
        dot_string = 'digraph G {\n'
        root = self
        right = None
        while root.left:
            dot_string = root.traverse_tree(dot_string)
            if right:
                dot_string = right.traverse_tree(dot_string)
            right = root.right
            root = root.left

        dot_string += '}'

        return dot_string

