import os
import unittest
import shutil

import pytest
from hypothesis import given
from hypothesis.strategies import integers

from tm_trees import TMTree, FileSystemTree
EXAMPLE_PATH = os.path.join(os.getcwd(), 'example-directory', 'workshop')


class SampleTests(unittest.TestCase):


    def test_file_system_tree_nonexistent_path(self) -> None:
        """This test checks that FileSystemTree's initializer raises an error
        for a nonexistent path.
        """
        with self.assertRaises(FileNotFoundError):
            FileSystemTree('nonexistent')

    def test_file_system_tree_zero_size_file(self) -> None:
        """This test checks that FileSystemTree's initializer works correctly
        for a file of data size 0.
        """
        temp_file_path = 'empty.py'
        with open(temp_file_path, 'w') as temp_file:
            pass

        sample_file = FileSystemTree(temp_file_path)
        assert sample_file.data_size == 0
        os.remove(temp_file_path)

    def test_file_system_tree_special_characters(self) -> None:
        """This test checks that FileSystemTree's initializer works correctly
        for a file with special characters in the name.
        """
        temp_file_path = '@#$%.txt'
        with open(temp_file_path, 'w') as temp_file:
            temp_file.write('Special characters!')

        sample_file = FileSystemTree(temp_file_path)
        assert sample_file._name == '@#$%.txt'
        assert sample_file.data_size == os.path.getsize(temp_file_path)

        os.remove(temp_file_path)

    def test_file_system_tree_nested(self) -> None:
        """This test checks that FileSystemTree's initializer works correctly
        for directories that are nested.
        """
        os.makedirs('nested/nested-again/final')

        sample_directory = FileSystemTree('nested')
        assert sample_directory.data_size == 0

        os.rmdir('nested/nested-again/final')
        os.rmdir('nested/nested-again')
        os.rmdir('nested')

    def test_file_system_tree_large_number_of_files(self) -> None:
        """This test checks that FileSystemTree's initializer works correctly
        for a directory with a large number of files. In this test, create 10000
        files in the directory.
        """
        os.mkdir('large-directory')
        for i in range(1000):
            with open(f'large-directory/file_{i}.txt', 'w') as temp_file:
                temp_file.write(f'File {i}')

        sample_large_directory = FileSystemTree('large-directory')
        assert len(sample_large_directory._subtrees) == 1000
        assert sample_large_directory.data_size > 0

        for i in range(1000):
            os.remove(f'large-directory/file_{i}.txt')

        os.rmdir('large-directory')

    def test_name_none_with_data(self) -> None:
        """Test that the initializer does not override the data size of a file
        whose name is None and whose data size is greater than 0
        """
        leaf = TMTree(None, [], 10)
        assert leaf._name is None
        assert leaf._subtrees == []
        assert leaf.is_empty()
        assert leaf.data_size != 0
        assert leaf.data_size == 10


class TestTMTreeRectangles(unittest.TestCase):

    def test_single_leaf_update_rectangles(self) -> None:
        """This test checks that update_rectangles correctly sets the rectangle
        for a single leaf node, ensuring it occupies the entire given space.
        """
        leaf = TMTree('single leaf', [], 5)
        leaf.update_rectangles((0, 0, 100, 200))
        assert leaf.rect == (0, 0, 100, 200)

    def test_zero_data_size_update_rectangles(self) -> None:
        """This test checks that update_rectangles handles nodes with zero data
        size correctly, ensuring they don't occupy any space in the
        visualization.
        """
        leaf = TMTree('nodata', [], 0)
        leaf.update_rectangles((0, 0, 100, 100))
        assert leaf.rect == (0, 0, 0, 0)

    def test_get_rectangles_empty_tree(self) -> None:
        """This test checks that get_rectangles returns an empty list for an
        empty tree, ensuring no rectangles are generated.
        """
        empty_tree = TMTree('', [], 0)
        assert empty_tree.get_rectangles() == []

    def test_division_by_zero(self) -> None:
        """Test that update_rectangles does not cause a division by zero error
        in a simple tree with a single file with zero data size.
        """
        leaf = TMTree("leaf", [], 0)
        root = TMTree("root", [leaf], 0)

        rect = (0, 0, 100, 100)
        root.update_rectangles(rect)

        self.assertEqual(root.rect, (0, 0, 0, 0))
        self.assertEqual(leaf.rect, (0, 0, 0, 0))

    def test_division_by_zero_complex(self) -> None:
        """Test that update_rectangles does not cause a division by zero error
        in a complex tree structure with multiple nested folders and files,
        all with zero data size.
        """
        leaf1 = TMTree("leaf1", [], 0)
        leaf2 = TMTree("leaf2", [], 0)
        folder1 = TMTree("folderA", [leaf1, leaf2], 0)

        leaf3 = TMTree("leaf3", [], 0)
        leaf4 = TMTree("leaf4", [], 0)
        folder2 = TMTree("folderB", [leaf3, leaf4], 0)

        root = TMTree("root", [folder1, folder2], 0)

        rect = (0, 0, 100, 100)
        root.update_rectangles(rect)

        self.assertEqual(root.rect, (0, 0, 0, 0))
        self.assertEqual(folder1.rect, (0, 0, 0, 0))
        self.assertEqual(folder2.rect, (0, 0, 0, 0))
        self.assertEqual(leaf1.rect, (0, 0, 0, 0))
        self.assertEqual(leaf2.rect, (0, 0, 0, 0))
        self.assertEqual(leaf3.rect, (0, 0, 0, 0))
        self.assertEqual(leaf4.rect, (0, 0, 0, 0))

    def test_division_by_zero_complex_2(self) -> None:
        """Test that update_rectangles does not cause a division by zero error
        in a complex tree structure with multiple nested folders and files,
        all with zero data size.
        """
        leaf1 = TMTree("leaf1", [], 0)
        leaf2 = TMTree("leaf2", [], 0)
        folder1 = TMTree("folder1", [leaf1, leaf2], 0)

        leaf3 = TMTree("leaf3", [], 0)
        leaf4 = TMTree("leaf4", [], 0)
        folder2 = TMTree("folder2", [leaf3, leaf4], 0)

        leaf5 = TMTree("leaf5", [], 0)
        leaf6 = TMTree("leaf6", [], 0)
        folder3 = TMTree("folder3", [leaf5, leaf6], 0)

        root = TMTree("root", [folder1, folder2, folder3], 0)

        rect = (0, 0, 100, 100)
        root.update_rectangles(rect)

        self.assertEqual(root.rect, (0, 0, 0, 0))
        self.assertEqual(folder1.rect, (0, 0, 0, 0))
        self.assertEqual(folder2.rect, (0, 0, 0, 0))
        self.assertEqual(folder3.rect, (0, 0, 0, 0))
        self.assertEqual(leaf1.rect, (0, 0, 0, 0))
        self.assertEqual(leaf2.rect, (0, 0, 0, 0))
        self.assertEqual(leaf3.rect, (0, 0, 0, 0))
        self.assertEqual(leaf4.rect, (0, 0, 0, 0))
        self.assertEqual(leaf5.rect, (0, 0, 0, 0))
        self.assertEqual(leaf6.rect, (0, 0, 0, 0))

    def test_negative_heights(self) -> None:
        """Test the update_rectangles method with negative heights.
        """
        leaf1 = TMTree("leaf1", [], 20)
        leaf2 = TMTree("leaf2", [], 30)
        leaf3 = TMTree("leaf3", [], 50)
        child1 = TMTree("child1", [leaf1, leaf2], 50)
        child2 = TMTree("child2", [leaf3], 50)
        root = TMTree("root", [child1, child2], 100)
        root.update_rectangles((0, 0, 200, -100))
        root.expand_all()

        assert root.rect == (0, 0, 200, -100)
        assert child1.rect == (0, 0, 100, -100)
        assert leaf1.rect == (0, 0, 40, -100)
        assert leaf2.rect == (40, 0, 60, -100)
        assert child2.rect == (100, 0, 100, -100)
        assert leaf3.rect == (100, 0, 100, -100)

        rects = root.get_rectangles()
        expected = [(0, 0, 40, -100), (40, 0, 60, -100), (100, 0, 100, -100)]
        for i in range(len(rects)):
            assert rects[i][0] == expected[i]


class TestGetTreeAtPosition(unittest.TestCase):
    def setUp(self) -> None:
        """Set up a sample tree for testing.
        """
        self.leaf1 = TMTree('leaf1', [], 2)
        self.leaf2 = TMTree('leaf2', [], 3)
        self.child = TMTree('child', [self.leaf1, self.leaf2], 5)
        self.root = TMTree('root', [self.child], 5)
        self.root.update_rectangles((0, 0, 100, 100))

    def test_position_outside_tree(self) -> None:
        """Test that the method returns None when the position is outside the
        tree's rectangle.
        """
        assert self.root.get_tree_at_position((-10, -10)) is None
        assert self.root.get_tree_at_position((150, 150)) is None

    def test_empty_tree(self) -> None:
        """Test that the method returns None for an empty tree.
        """
        empty_tree = TMTree('', [], 0)
        assert empty_tree.get_tree_at_position((10, 10)) is None

    def test_position_out_of_bounds(self) -> None:
        """Test that get_tree_at_position returns None when the position is outside
        the bounds of the tree's rectangle."""
        leaf = TMTree("leaf", [], 100)
        root = TMTree("root", [leaf], 0)
        root.update_rectangles((0, 0, 100, 100))
        self.assertIsNone(root.get_tree_at_position((150, 150)))

    def test_multiple_leaves_expanded(self) -> None:
        """Test that a single expanded leaf returns None when its position is
        queried, as it should not be considered a tree at that position.
        """
        leaf1 = TMTree("leaf1", [], 20)
        leaf2 = TMTree("leaf2", [], 30)
        leaf3 = TMTree("leaf3", [], 50)
        root = TMTree("root", [leaf1, leaf2, leaf3], 0)
        root.update_rectangles((0, 0, 100, 100))
        root.expand()
        self.assertEqual(root.get_tree_at_position((10, 10)), leaf1)
        self.assertEqual(root.get_tree_at_position((40, 40)), leaf2)
        self.assertEqual(root.get_tree_at_position((80, 80)), leaf3)

    def test_corner_case_top_left(self) -> None:
        """Test that the correct leaf is returned when querying the top-left
        corner of the rectangle, ensuring that boundary conditions are
        handled correctly.
        """
        leaf1 = TMTree("leaf1", [], 40)
        leaf2 = TMTree("leaf2", [], 60)
        root = TMTree("root", [leaf1, leaf2], 0)
        root.update_rectangles((0, 0, 100, 100))
        root.expand()
        self.assertEqual(root.get_tree_at_position((0, 0)), leaf1)

    def test_corner_case_bottom_right(self) -> None:
        """Test that the correct leaf is returned when querying the
        bottom-right corner of the rectangle, ensuring that boundary conditions
        are handled correctly.
        """
        leaf1 = TMTree("leaf1", [], 50)
        leaf2 = TMTree("leaf2", [], 50)
        root = TMTree("root", [leaf1, leaf2], 0)
        root.update_rectangles((0, 0, 100, 100))
        root.expand()
        self.assertEqual(root.get_tree_at_position((99, 99)), leaf2)


class TestUpdateSize(unittest.TestCase):
    def test_leaf_increase_size(self) -> None:
        """Test increasing the size of a leaf and updating its data size.
        """
        leaf = TMTree("leaf", [], 50)
        leaf.change_size(0.2)
        leaf.update_data_sizes()
        self.assertEqual(leaf.data_size, 60)

    def test_leaf_decrease_size(self) -> None:
        """Test decreasing the size of a leaf and updating its data size.
        """
        leaf = TMTree("leaf", [], 50)
        leaf.change_size(-0.2)
        leaf.update_data_sizes()
        self.assertEqual(leaf.data_size, 40)

    def test_folder_single_leaf(self) -> None:
        """Test updating the data size of a folder containing a single leaf.
        """
        leaf = TMTree("leaf", [], 50)
        folder = TMTree("folder", [leaf], 0)
        leaf.change_size(0.1)
        folder.update_data_sizes()
        self.assertEqual(folder.data_size, 55)

    def test_folder_multiple_leaves(self) -> None:
        """Test updating the data size of a folder containing multiple leaves.
        """
        leaf1 = TMTree("leaf1", [], 50)
        leaf2 = TMTree("leaf2", [], 60)
        folder = TMTree("folder", [leaf1, leaf2], 0)
        leaf1.change_size(0.2)
        leaf2.change_size(-0.1)
        folder.update_data_sizes()
        self.assertEqual(folder.data_size, 114)

    def test_nested_folders(self) -> None:
        """Test updating the data size of nested folders.
        """
        leaf1 = TMTree("leaf1", [], 50)
        leaf2 = TMTree("leaf2", [], 60)
        subfolder = TMTree("subfolder", [leaf1, leaf2], 0)
        leaf3 = TMTree("leaf3", [], 70)
        folder = TMTree("folder", [subfolder, leaf3], 0)
        leaf1.change_size(0.1)
        leaf2.change_size(-0.1)
        leaf3.change_size(0.2)
        folder.update_data_sizes()
        self.assertEqual(folder.data_size, 193)
        self.assertEqual(subfolder.data_size, 109)

    def test_empty_folder(self) -> None:
        """Test updating the data size of an empty folder.
        """
        folder = TMTree("folder", [], 0)
        folder.update_data_sizes()
        self.assertEqual(folder.data_size, 0)

    def test_folder_with_empty_subfolders(self) -> None:
        """Test updating the data size of a folder with empty subfolders.
        """
        subfolder1 = TMTree("subfolder1", [], 0)
        subfolder2 = TMTree("subfolder2", [], 0)
        folder = TMTree("folder", [subfolder1, subfolder2], 0)
        folder.update_data_sizes()
        self.assertEqual(folder.data_size, 0)

    def test_multi_nested_folders(self) -> None:
        """Test updating the data size of multi-nested folders.
        """
        leaf = TMTree("leaf", [], 10)
        level1 = TMTree("level1", [leaf], 0)
        level2 = TMTree("level2", [level1], 0)
        level3 = TMTree("level3", [level2], 0)
        level3.update_data_sizes()
        self.assertEqual(level3.data_size, 10)
        self.assertEqual(level2.data_size, 10)
        self.assertEqual(level1.data_size, 10)

    def test_uneven_subtrees(self) -> None:
        """Test updating the data size of a folder with unevenly sized subtrees.
        """
        small_leaf = TMTree("small_leaf", [], 1)
        large_leaf = TMTree("large_leaf", [], 1000)
        folder = TMTree("folder", [small_leaf, large_leaf], 0)
        small_leaf.change_size(0.5)
        large_leaf.change_size(-0.2)
        folder.update_data_sizes()
        self.assertEqual(folder.data_size, 802)

    def test_subtrees_of_size_zero(self) -> None:
        """Test updating the data size of a folder with subtrees whose data size
        is zero.
        """
        zero_leaf = TMTree("zero_leaf", [], 0)
        non_zero_leaf = TMTree("non_zero_leaf", [], 50)
        folder = TMTree("folder", [zero_leaf, non_zero_leaf], 0)
        non_zero_leaf.change_size(-0.2)
        folder.update_data_sizes()
        self.assertEqual(folder.data_size, 40)


class TestChangeSize(unittest.TestCase):
    def test_increase_leaf_size(self) -> None:
        """Test increasing the size of a leaf.
        """
        leaf = TMTree("leaf", [], 50)
        leaf.change_size(0.1)
        leaf.update_data_sizes()
        self.assertEqual(leaf.data_size, 55)

    def test_decrease_leaf_size(self) -> None:
        """Test decreasing the size of a leaf.
        """
        leaf = TMTree("leaf", [], 50)
        leaf.change_size(-0.1)
        leaf.update_data_sizes()
        self.assertEqual(leaf.data_size, 45)

    def test_zero_change_leaf_size(self) -> None:
        """Test changing the size of a leaf by zero percent.
        """
        leaf = TMTree("leaf", [], 50)
        leaf.change_size(0)
        leaf.update_data_sizes()
        self.assertEqual(leaf.data_size, 50)

    def test_increase_leaf_size_boundary(self) -> None:
        """Test increasing the size of a leaf by the maximum allowed factor.
        """
        leaf = TMTree("leaf", [], 50)
        leaf.change_size(0.99)
        leaf.update_data_sizes()
        self.assertEqual(leaf.data_size, 100)

    def test_decrease_leaf_size_boundary(self) -> None:
        """Test decreasing the size of a leaf by the maximum allowed factor.
        """
        leaf = TMTree("leaf", [], 50)
        leaf.change_size(-0.99)
        leaf.update_data_sizes()
        self.assertEqual(leaf.data_size, 1)

    def test_change_size_on_folder(self) -> None:
        """Test changing the size of a folder, which should have no effect.
        """
        leaf = TMTree("leaf", [], 50)
        folder = TMTree("folder", [leaf], 0)
        folder.change_size(0.1)
        folder.update_data_sizes()
        self.assertEqual(folder.data_size, 50)
        self.assertEqual(leaf.data_size, 50)

    def test_change_size_on_nested_folders(self) -> None:
        """Test changing the size of a leaf in a nested folder structure.
        """
        leaf1 = TMTree("leaf1", [], 50)
        leaf2 = TMTree("leaf2", [], 60)
        folder1 = TMTree("folder1", [leaf1], 0)
        folder2 = TMTree("folder2", [leaf2], 0)
        root = TMTree("root", [folder1, folder2], 0)
        leaf1.change_size(0.1)
        leaf2.change_size(-0.1)
        root.update_data_sizes()
        self.assertEqual(leaf1.data_size, 55)
        self.assertEqual(leaf2.data_size, 54)
        self.assertEqual(folder1.data_size, 55)
        self.assertEqual(folder2.data_size, 54)
        self.assertEqual(root.data_size, 109)

    def test_change_size_on_nested_folders_complex(self) -> None:
        """Test changing the size of leaves in a multi-nested folder structure.
        """
        leaf1 = TMTree("leaf1", [], 50)
        leaf2 = TMTree("leaf2", [], 60)
        leaf3 = TMTree("leaf3", [], 70)
        leaf4 = TMTree("leaf4", [], 80)

        subfolder1 = TMTree("subfolder1", [leaf1, leaf2], 0)
        subfolder2 = TMTree("subfolder2", [leaf3], 0)
        folder1 = TMTree("folder1", [subfolder1], 0)
        folder2 = TMTree("folder2", [subfolder2, leaf4], 0)
        root = TMTree("root", [folder1, folder2], 0)

        leaf1.change_size(0.1)
        leaf2.change_size(-0.1)
        leaf3.change_size(0.2)
        leaf4.change_size(-0.2)

        root.update_data_sizes()

        self.assertEqual(leaf1.data_size, 55)
        self.assertEqual(leaf2.data_size, 54)
        self.assertEqual(leaf3.data_size, 84)
        self.assertEqual(leaf4.data_size, 64)
        self.assertEqual(subfolder1.data_size, 109)
        self.assertEqual(subfolder2.data_size, 84)
        self.assertEqual(folder1.data_size, 109)
        self.assertEqual(folder2.data_size, 148)
        self.assertEqual(root.data_size, 257)

    def test_change_size_empty_folder(self) -> None:
        """Test changing the size of an empty folder.
        """
        folder = TMTree("folder", [], 0)
        folder.change_size(0.1)
        folder.update_data_sizes()
        self.assertEqual(folder.data_size, 0)

    def test_reduce_size_below_zero(self) -> None:
        """Test reducing the size of a node to zero or negative.
        """
        leaf = TMTree('leaf', [], 2)
        leaf.change_size(-100)
        leaf.update_data_sizes()
        self.assertEqual(leaf.data_size, 1)

    def test_change_size_multi_nested_folder(self) -> None:
        """Test changing the size of a leaf in a multi-nested folder.
        """
        leaf = TMTree('leaf', [], 10)
        child = TMTree('child', [leaf], 10)
        parent = TMTree('parent', [child], 10)
        root = TMTree('root', [parent], 10)
        leaf.change_size(0.5)
        root.update_data_sizes()
        self.assertEqual(leaf.data_size, 15)
        self.assertEqual(child.data_size, 15)
        self.assertEqual(parent.data_size, 15)
        self.assertEqual(root.data_size, 15)


class TestMove(unittest.TestCase):
    def setUp(self) -> None:
        """Set up a sample tree for testing.
        """
        self.leaf1 = TMTree('leaf1', [], 2)
        self.leaf2 = TMTree('leaf2', [], 3)
        self.child1 = TMTree('child1', [self.leaf1], 2)
        self.child2 = TMTree('child2', [self.leaf2], 3)
        self.root = TMTree('root', [self.child1, self.child2], 5)

    def test_move_leaf(self) -> None:
        """Test moving a leaf from one node to another.
        """
        self.leaf1.move(self.child2)
        assert self.leaf1 in self.child2._subtrees
        assert self.leaf1 not in self.child1._subtrees

    def test_move_updates_sizes(self) -> None:
        """Test that moving a leaf updates the data sizes correctly.
        """
        self.leaf1.move(self.child2)
        assert self.child1.data_size == 0
        assert self.child2.data_size == 5
        assert self.root.data_size == 5

    def test_move_leaf_to_another_folder(self) -> None:
        """Test moving a leaf from one folder to another.
        """
        leaf1 = TMTree("leaf1", [], 30)
        leaf2 = TMTree("leaf2", [], 40)
        folder1 = TMTree("folder1", [leaf1], 0)
        folder2 = TMTree("folder2", [leaf2], 0)
        root = TMTree("root", [folder1, folder2], 0)

        leaf1.move(folder2)
        root.update_data_sizes()

        self.assertEqual(leaf1._parent_tree, folder2)
        self.assertIn(leaf1, folder2._subtrees)
        self.assertNotIn(leaf1, folder1._subtrees)
        self.assertEqual(folder2.data_size, 70)
        self.assertEqual(folder1.data_size, 0)

    def test_move_folder_to_root(self) -> None:
        """Test moving a folder to the root of the tree.
        """
        leaf1 = TMTree("leaf1", [], 30)
        folder1 = TMTree("folder1", [leaf1], 0)
        root = TMTree("root", [folder1], 0)

        folder1.move(root)
        root.update_data_sizes()

        self.assertEqual(folder1._parent_tree, root)
        self.assertIn(folder1, root._subtrees)
        self.assertEqual(root.data_size, 30)

    def test_move_folder_to_itself(self) -> None:
        """Test attempting to move a folder to itself (should do nothing).
        """
        leaf1 = TMTree("leaf1", [], 30)
        folder1 = TMTree("folder1", [leaf1], 0)

        original_folder1 = folder1
        folder1.move(folder1)

        self.assertEqual(folder1, original_folder1)
        self.assertIn(leaf1, folder1._subtrees)
        self.assertEqual(folder1.data_size, 30)

    def test_move_subtree_to_leaf(self) -> None:
        """Test attempting to move a subtree to a leaf (should do nothing).
        """
        self.leaf1 = TMTree('leaf1', [], 2)
        self.leaf2 = TMTree('leaf2', [], 3)
        self.leaf3 = TMTree('leaf3', [], 5)
        self.child1 = TMTree('child1', [self.leaf1, self.leaf2], 5)
        self.child2 = TMTree('child2', [self.leaf3], 5)
        self.root = TMTree('root', [self.child1, self.child2], 10)
        original_child1 = self.child1
        self.child1.move(self.leaf3)
        assert self.child1 == original_child1
        assert self.leaf3._subtrees == []

    def test_move_empty_folder_into_nested_folder(self) -> None:
        """Test moving an empty folder into a nested folder structure.
        """
        empty_folder = TMTree('empty_folder', [])
        leaf = TMTree('leaf', [], 10)
        nested_folder1 = TMTree('nested_folder1', [leaf])
        nested_folder2 = TMTree('nested_folder2', [nested_folder1])
        root_folder = TMTree('root_folder', [empty_folder, nested_folder2])

        empty_folder.move(nested_folder1)

        assert empty_folder in nested_folder1._subtrees

        assert empty_folder.data_size == 0
        assert nested_folder1.data_size == 10
        assert nested_folder2.data_size == 10
        assert root_folder.data_size == 10

        assert empty_folder not in root_folder._subtrees

    def test_move_node_to_itself(self) -> None:
        """Test moving a node to itself.
        """
        leaf = TMTree('leaf', [], 289)
        original_parent = leaf._parent_tree
        leaf.move(leaf)
        self.assertIs(leaf._parent_tree, original_parent)
        self.assertEqual(leaf.data_size, 289)

    def test_move_node_to_parent(self) -> None:
        """Test moving a node to its parent.
        """
        leaf = TMTree('leaf', [], 33)
        folder = TMTree('folder', [leaf], 33)
        leaf.move(folder)
        self.assertIn(leaf, folder._subtrees)
        self.assertEqual(folder.data_size, 33)

    def test_move_node_to_descendant(self) -> None:
        """Test that moving a node to one of its descendants is not allowed.
        """
        leaf = TMTree("leaf", [], 10)
        folder = TMTree("folder", [leaf], 10)
        folder.move(leaf)
        self.assertNotIn(folder, leaf._subtrees)


class TestExpand(unittest.TestCase):

    def test_two_folders(self):
        """Test that expanding one folder in a tree with two folders correctly
        updates the expanded status of the root and both folders.
        """
        leaf = TMTree("leaf", [], 10)
        leaf2 = TMTree("leaf2", [], 10)
        folder1 = TMTree("folder1", [leaf], 0)
        folder2 = TMTree("folder2", [leaf2], 0)
        root = TMTree("root", [folder1, folder2], 0)
        root.update_rectangles((0, 0, 100, 100))
        root.expand()
        folder1.expand()
        self.assertEqual(root._expanded, True)
        self.assertEqual(folder1._expanded, True)
        self.assertEqual(folder2._expanded, False)

    def test_four_folders(self):
        """Test that expanding one folder in a tree with four folders correctly
        updates the expanded status of the root and all folders.
        """
        leaf1 = TMTree("leaf1", [], 10)
        folder1 = TMTree("folder1", [leaf1], 0)
        leaf2 = TMTree("leaf2", [], 10)
        folder2 = TMTree("folder2", [leaf2], 0)
        leaf3 = TMTree("leaf3", [], 10)
        folder3 = TMTree("folder3", [leaf3], 0)
        leaf4 = TMTree("leaf4", [], 10)
        folder4 = TMTree("folder4", [leaf4], 0)
        root = TMTree("root", [folder1, folder2, folder3, folder4], 0)
        root.update_rectangles((0, 0, 100, 100))
        root.expand()
        folder1.expand()
        self.assertEqual(root._expanded, True)
        self.assertEqual(folder1._expanded, True)
        self.assertEqual(folder2._expanded, False)
        self.assertEqual(folder3._expanded, False)
        self.assertEqual(folder4._expanded, False)

    def test_multi_nested_folders(self):
        """Test that expand_all correctly expands all folders in a multi-nested
        structure.
        """
        leaf = TMTree("leaf", [], 10)
        folder1 = TMTree("folder1", [leaf], 0)
        folder2 = TMTree("folder2", [folder1], 0)
        folder3 = TMTree("folder3", [folder2], 0)
        folder4 = TMTree("folder4", [folder3], 0)
        root = TMTree("root", [folder4], 0)
        root.update_rectangles((0, 0, 100, 100))
        root.expand_all()
        self.assertTrue(all(subtree._expanded for subtree in
                            [root, folder1, folder2, folder3, folder4]))

    def test_empty_folders(self):
        """Test that expand_all correctly handles a tree with empty folders.
        """
        empty_folder1 = TMTree("empty_folder1", [], 0)
        empty_folder2 = TMTree("empty_folder2", [], 0)
        root = TMTree("root", [empty_folder1, empty_folder2], 0)
        root.update_rectangles((0, 0, 100, 100))
        root.expand_all()
        self.assertTrue(root._expanded)
        self.assertFalse(empty_folder1._expanded)
        self.assertFalse(empty_folder2._expanded)

    def test_expand_all_under_root(self):
        """Test that expand_all correctly expands every node under the root.
        """
        leaf1 = TMTree("leaf1", [], 10)
        leaf2 = TMTree("leaf2", [], 20)
        folder1 = TMTree("folder1", [leaf1, leaf2], 0)
        leaf3 = TMTree("leaf3", [], 30)
        folder2 = TMTree("folder2", [leaf3], 0)
        root = TMTree("root", [folder1, folder2], 0)
        root.update_rectangles((0, 0, 100, 100))
        root.expand_all()
        self.assertTrue(root._expanded)
        self.assertTrue(folder1._expanded)
        self.assertTrue(folder2._expanded)
        self.assertFalse(leaf1._expanded)
        self.assertFalse(leaf2._expanded)
        self.assertFalse(leaf3._expanded)

    def test_expand_tree_after_collapsing(self):
        """Test expanding a tree after it has been collapsed.
        """
        leaf1 = TMTree("leaf1", [], 10)
        leaf2 = TMTree("leaf2", [], 20)
        folder = TMTree("folder", [leaf1, leaf2], 30)
        root = TMTree("root", [folder], 30)

        root.expand_all()
        self.assertTrue(all(subtree._expanded for subtree in root._subtrees))
        root.collapse_all()
        self.assertFalse(any(subtree._expanded for subtree in root._subtrees))
        root.expand_all()
        self.assertTrue(all(subtree._expanded for subtree in root._subtrees))

    def test_expand_leaf(self) -> None:
        """Test that expanding a leaf does nothing.
        """
        node = TMTree("node", [], 515)
        node.expand()
        self.assertFalse(node._expanded)


class TestCollapse(unittest.TestCase):

    def test_collapse_leaf_node(self) -> None:
        """Test that collapsing a leaf node does nothing.
        """
        leaf = TMTree("leaf", [], 11)
        leaf.collapse()
        self.assertFalse(leaf._expanded)

    def test_collapse_node_no_parent_tree(self) -> None:
        """Test that collapsing a folder with no parent tree does nothing.
        """
        file = TMTree("file", [], 5)
        folder1 = TMTree("folder1", [file], 5)
        folder2 = TMTree("folder2", [folder1], 5)
        folder1.expand()
        folder2.expand()
        folder2.collapse()
        self.assertTrue(folder2._expanded)
        self.assertTrue(folder1._expanded)

    def test_collapse_node_parent_tree(self) -> None:
        """Test that collapsing a folder with a parent tree correctly collapses
        the folder.
        """
        file = TMTree("file", [], 5)
        folder1 = TMTree("folder1", [file], 5)
        folder2 = TMTree("folder2", [folder1], 5)
        root = TMTree("root", [folder2], 5)
        folder1.expand()
        folder2.expand()
        root.expand()
        folder2.collapse()
        self.assertFalse(folder2._expanded)
        self.assertFalse(folder1._expanded)


class TestCollapseAll(unittest.TestCase):

    def test_collapse_single_folder_with_leaf(self) -> None:
        """Test collapsing a single folder containing one leaf.
        """
        leaf = TMTree("leaf", [], 10)
        folder = TMTree("folder", [leaf], 10)
        folder.collapse_all()
        self.assertFalse(folder._expanded)
        self.assertFalse(leaf._expanded)

    def test_collapse_nested_folders_with_leaves(self) -> None:
        """Test collapsing nested folders containing multiple leaves.
        """
        leaf1 = TMTree("leaf1", [], 10)
        leaf2 = TMTree("leaf2", [], 20)
        child_folder = TMTree("child_folder", [leaf1, leaf2], 30)
        root_folder = TMTree("root_folder", [child_folder], 30)
        root_folder.collapse_all()
        self.assertFalse(root_folder._expanded)
        self.assertFalse(child_folder._expanded)
        self.assertFalse(leaf1._expanded)
        self.assertFalse(leaf2._expanded)

    def test_collapse_empty_folder(self) -> None:
        """Test collapsing an empty folder.
        """
        empty_folder = TMTree("empty_folder", [], 0)
        empty_folder.collapse_all()
        self.assertFalse(empty_folder._expanded)

    def test_collapse_folder_with_nested_empty_folders(self) -> None:
        """Test collapsing a folder with multiple nested empty folders.
        """
        empty_child1 = TMTree("empty_child1", [], 0)
        empty_child2 = TMTree("empty_child2", [], 0)
        nested_folder = TMTree("nested_folder", [empty_child1, empty_child2], 0)
        root_folder = TMTree("root_folder", [nested_folder], 0)
        root_folder.collapse_all()
        self.assertFalse(root_folder._expanded)
        self.assertFalse(nested_folder._expanded)
        self.assertFalse(empty_child1._expanded)
        self.assertFalse(empty_child2._expanded)

    def test_collapse_folder_with_single_empty_subfolder(self) -> None:
        """Test collapsing a folder with a single empty subfolder.
        """
        empty_subfolder = TMTree("empty_subfolder", [], 0)
        folder = TMTree("folder", [empty_subfolder], 72)
        folder.collapse_all()
        self.assertFalse(folder._expanded)
        self.assertFalse(empty_subfolder._expanded)

    def test_collapse_folder_with_mixed_subfolders(self) -> None:
        """Test collapsing a folder with mixed empty and non-empty subfolders.
        """
        empty_subfolder = TMTree("empty_subfolder", [], 0)
        leaf = TMTree("leaf", [], 37)
        non_empty_subfolder = TMTree("non_empty_subfolder", [leaf], 37)
        folder = TMTree("folder", [empty_subfolder, non_empty_subfolder], 109)
        folder.collapse_all()
        self.assertFalse(folder._expanded)
        self.assertFalse(empty_subfolder._expanded)
        self.assertFalse(non_empty_subfolder._expanded)
        self.assertFalse(leaf._expanded)

    def test_collapse_complex(self) -> None:
        """Test collapsing a complex multi-nested folder structure.
        """
        leaf = TMTree("leaf", [], 83)
        level3_folder = TMTree("level3_folder", [leaf], 83)
        level2_folder = TMTree("level2_folder", [level3_folder], 83)
        level1_folder = TMTree("level1_folder", [level2_folder], 83)
        root_folder = TMTree("root_folder", [level1_folder], 83)
        root_folder.collapse_all()
        self.assertFalse(root_folder._expanded)
        self.assertFalse(level1_folder._expanded)
        self.assertFalse(level2_folder._expanded)
        self.assertFalse(level3_folder._expanded)
        self.assertFalse(leaf._expanded)

    def test_collapse_complex2(self) -> None:
        """Test collapsing a complex folder with a mix of leaves and subfolders.
        """
        leaf1 = TMTree("leaf1", [], 21)
        leaf2 = TMTree("leaf2", [], 13)
        subfolder = TMTree("subfolder", [leaf2], 13)
        folder = TMTree("folder", [leaf1, subfolder], 34)
        folder.collapse_all()
        self.assertFalse(folder._expanded)
        self.assertFalse(leaf1._expanded)
        self.assertFalse(subfolder._expanded)
        self.assertFalse(leaf2._expanded)

    def test_collapse_all_large_tree_structure(self) -> None:
        """Test collapsing all nodes in a large tree structure.
        """
        root = TMTree("root", [], 0)
        current_folder = root
        for i in range(200):
            new_folder = TMTree(f"folder{i}", [], 0)
            current_folder._subtrees.append(new_folder)
            current_folder = new_folder
        root.expand_all()
        root.collapse_all()
        self.assertFalse(root._expanded)
        self.assertFalse(current_folder._expanded)


class TestDeleteSelf(unittest.TestCase):
    def setUp(self) -> None:
        """Set up a sample tree for testing.
        """
        self.leaf1 = TMTree('leaf1', [], 2)
        self.leaf2 = TMTree('leaf2', [], 3)
        self.child = TMTree('child', [self.leaf1, self.leaf2], 5)
        self.root = TMTree('root', [self.child], 5)

    def test_delete_leaf(self) -> None:
        """Test deleting a leaf from its parent.
        """
        self.leaf1.delete_self()
        assert self.leaf1 not in self.child._subtrees
        assert self.child.data_size == 3
        assert self.leaf1.data_size == 0

    def test_delete_internal_node(self) -> None:
        """Test deleting an internal node from its parent.
        """
        self.child.delete_self()
        assert self.child not in self.root._subtrees
        assert self.root.data_size == 0
        assert self.child.data_size == 0

    def test_delete_internal_node_with_multiple_children(self) -> None:
        """Test deleting an internal node with multiple children.
        """
        self.leaf1 = TMTree('leaf1', [], 2)
        self.leaf2 = TMTree('leaf2', [], 3)
        self.leaf3 = TMTree('leaf3', [], 5)
        self.child1 = TMTree('child1', [self.leaf1, self.leaf2], 5)
        self.child2 = TMTree('child2', [self.leaf3], 5)
        self.root = TMTree('root', [self.child1, self.child2], 10)
        self.child1.delete_self()
        assert self.child1 not in self.root._subtrees
        assert self.root.data_size == 5

    def test_delete_root_node(self) -> None:
        """Test attempting to delete the root node (should do nothing).
        """
        original_root = self.root
        self.root.delete_self()
        assert self.root == original_root
        self.assertFalse(self.root.delete_self())
        self.assertEqual(self.root.data_size, 5)

    def test_delete_leaf_complex(self) -> None:
        """Test deleting a leaf node in a more complex structure.
        """
        self.leaf1 = TMTree('leaf1', [], 2)
        self.leaf2 = TMTree('leaf2', [], 3)
        self.leaf3 = TMTree('leaf3', [], 5)
        self.leaf4 = TMTree('leaf4', [], 7)
        self.leaf5 = TMTree('leaf5', [], 11)

        self.child1 = TMTree('child1', [self.leaf1, self.leaf2], 5)
        self.child2 = TMTree('child2', [self.leaf3, self.leaf4], 12)
        self.child3 = TMTree('child3', [self.leaf5], 11)

        self.sub_root1 = TMTree('sub_root1', [self.child1, self.child2], 17)
        self.sub_root2 = TMTree('sub_root2', [self.child3], 11)

        self.root = TMTree('root', [self.sub_root1, self.sub_root2], 28)
        self.leaf4.delete_self()
        assert self.leaf4 not in self.child2._subtrees
        assert self.child2.data_size == 5
        assert self.sub_root1.data_size == 10
        assert self.root.data_size == 21

    def test_delete_root_of_subtree(self):
        """Test deleting the root of a subtree and its impact on the tree
        structure.
        """
        leaf1 = TMTree("leaf1", [], 5)
        leaf2 = TMTree("leaf2", [], 10)
        subfolder = TMTree("subfolder", [leaf1], 5)
        folder = TMTree("folder", [subfolder, leaf2], 15)
        root = TMTree("root", [folder], 15)

        subfolder.delete_self()
        self.assertNotIn(subfolder, folder._subtrees)
        self.assertEqual(folder.data_size, 10)
        self.assertEqual(root.data_size, 10)


class TestRepresentationInvariants(unittest.TestCase):

    def test_colour_invariant(self) -> None:
        """Test that the RGB colour values are each in the range 0-255.
        """
        tree = TMTree("tree", [], 10)
        for value in tree._colour:
            self.assertGreaterEqual(value, 0)
            self.assertLessEqual(value, 255)

    def test_name_and_subtrees_invariant(self) -> None:
        """Test that if _name is None, then _subtrees is empty, _parent_tree
        is None, and data_size is 0.
        """
        tree = TMTree(None, [TMTree("leaf", [], 10)])
        self.assertIsNone(tree._name)
        self.assertEqual(len(tree._subtrees), 1)
        self.assertIsNone(tree._parent_tree)
        self.assertEqual(tree.data_size, 10)

    def test_parent_tree_invariant(self) -> None:
        """Test that if _parent_tree is not None, then self is in
        _parent_tree._subtrees.
        """
        child = TMTree("child", [], 10)
        parent = TMTree("parent", [child], 10)
        self.assertIsNotNone(child._parent_tree)
        self.assertIn(child, parent._subtrees)

    def test_expanded_invariant(self) -> None:
        """Test that if _expanded is True, then _parent_tree._expanded is True
        and if _expanded is False, then _expanded is False for every tree in
        _subtrees.
        """
        child = TMTree("child", [], 10)
        parent = TMTree("parent", [child], 10)
        parent.expand()
        self.assertTrue(parent._expanded)
        self.assertTrue(child._parent_tree._expanded)

        parent.collapse()
        self.assertTrue(parent._expanded)
        self.assertFalse(child._expanded)

    def test_empty_tree_invariant(self) -> None:
        """Test that an empty tree has a data_size of 0, no subtrees, and no
        parent tree."""
        empty_tree = TMTree(None, [])
        self.assertEqual(empty_tree.data_size, 0)
        self.assertEqual(len(empty_tree._subtrees), 0)
        self.assertIsNone(empty_tree._parent_tree)


##############################################################################
# Helpers
##############################################################################

def is_valid_colour(colour: tuple[int, int, int]) -> bool:
    """Return True iff <colour> is a valid colour. That is, if all of its
    values are between 0 and 255, inclusive.
    """
    for i in range(3):
        if not 0 <= colour[i] <= 255:
            return False
    return True


def _sort_subtrees(tree: TMTree) -> None:
    """Sort the subtrees of <tree> in alphabetical order.
    THIS IS FOR THE PURPOSES OF THE SAMPLE TEST ONLY; YOU SHOULD NOT SORT
    YOUR SUBTREES IN THIS WAY. This allows the sample test to run on different
    operating systems.

    This is recursive, and affects all levels of the tree.
    """
    if not tree.is_empty():
        for subtree in tree._subtrees:
            _sort_subtrees(subtree)

        tree._subtrees.sort(key=lambda t: t._name)
