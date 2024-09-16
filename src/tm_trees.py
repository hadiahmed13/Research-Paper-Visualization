"""
=== Module Description ===
This module contains the basic tree interface required by the treemap
visualiser. You will both add to the abstract class, and complete a
concrete implementation of a subclass to represent files and folders on your
computer's file system.
"""
from __future__ import annotations

import math
import os
import random
from typing import List, Tuple, Optional


class TMTree:
    """A TreeMappableTree: a tree that is compatible with the treemap
    visualiser.

    This is an abstract class that should not be instantiated directly.

    === Public Attributes ===
    rect:
        The pygame rectangle representing this node in the treemap
        visualization.
    data_size:
        The size of the data represented by this tree.

    === Private Attributes ===
    _colour:
        The RGB colour value of the root of this tree.
    _name:
        The root value of this tree, or None if this tree is empty.
    _subtrees:
        The subtrees of this tree.
    _parent_tree:
        The parent tree of this tree; i.e., the tree that contains this tree
        as a subtree, or None if this tree is not part of a larger tree.
    _expanded:
        Whether or not this tree is considered expanded for visualization.

    === Representation Invariants ===
    - data_size >= 0
    - If _subtrees is not empty, then data_size is equal to the sum of the
      data_size of each subtree.

    - _colour's elements are each in the range 0-255.

    - If _name is None, then _subtrees is empty, _parent_tree is None, and
      data_size is 0.
      This setting of attributes represents an empty tree.

    - if _parent_tree is not None, then self is in _parent_tree._subtrees

    - if _expanded is True, then _parent_tree._expanded is True
    - if _expanded is False, then _expanded is False for every tree
      in _subtrees
    - if _subtrees is empty, then _expanded is False
    """

    rect: Tuple[int, int, int, int]
    data_size: int
    _colour: Tuple[int, int, int]
    _name: str
    _subtrees: List[TMTree]
    _parent_tree: Optional[TMTree]
    _expanded: bool

    def __init__(self, name: str, subtrees: List[TMTree],
                 data_size: int = 0) -> None:
        """Initialize a new TMTree with a random colour and the provided <name>.

        If <subtrees> is empty, use <data_size> to initialize this tree's
        data_size.

        If <subtrees> is not empty, ignore the parameter <data_size>,
        and calculate this tree's data_size instead.

        Set this tree as the parent for each of its subtrees.

        Precondition: if <name> is None, then <subtrees> is empty.
        """
        self.rect = (0, 0, 0, 0)
        self._name = name
        self._subtrees = subtrees[:]
        self._parent_tree = None
        self._expanded = False

        self._colour = (random.randint(0, 255),
                        random.randint(0, 255), random.randint(0, 255))

        self.data_size = data_size
        self._sum_size()

        if self._subtrees:  # if the tree has subtrees.
            for subtree in self._subtrees:
                subtree._parent_tree = self  # setting id of this tree as parent

    def is_empty(self) -> bool:
        """Return True iff this tree is empty.
        """
        return self._name is None

    # helper to calculate the data size.
    def _sum_size(self) -> int:
        """Return the total data_size of this tree
        """

        if not self._subtrees:
            pass

        else:
            total = 0
            for tree in self._subtrees:
                total += tree._sum_size()
            self.data_size = total

        return self.data_size

    def get_parent(self) -> Optional[TMTree]:
        """Returns the parent of this tree.
        """
        return self._parent_tree

    def update_rectangles(self, rect: Tuple[int, int, int, int]) -> None:
        """Update the rectangles in this tree and its descendants using the
        treemap algorithm to fill the area defined by pygame rectangle <rect>.
        """
        self._handle_base_cases(rect)
        self._distribute_space_subtrees(rect)

    def _handle_base_cases(self, rect: Tuple[int, int, int, int]) -> None:
        """Handle base cases for updating rectangles."""
        # x, y, width, height = rect
        if self.is_empty() and self.data_size > 0:
            self.rect = rect
            return
        if self.data_size == 0:
            self.rect = (0, 0, 0, 0)
            for subtree in self._subtrees:
                subtree.update_rectangles(rect)

    def _distribute_space_subtrees(
            self, rect: Tuple[int, int, int, int]) -> None:
        """Distribute available space among subtrees based on their data
        size."""
        x, y, width, height = rect
        if not self.is_empty() and self.data_size > 0:
            self.rect = rect
            total_size = self.data_size
            offset = 0

            for i, subtree in enumerate(self._subtrees):
                proportion = subtree.data_size / total_size
                if width > height:
                    current_width = (self._calculate_dimension
                                     (proportion, width, offset,
                                      i == len(self._subtrees) - 1))
                    subtree.rect = (x + offset, y, current_width, height)
                    offset += current_width
                else:
                    current_height = (self._calculate_dimension
                                      (proportion, height, offset,
                                       i == len(self._subtrees) - 1))
                    subtree.rect = (x, y + offset, width, current_height)
                    offset += current_height

                subtree.update_rectangles(subtree.rect)

    def _calculate_dimension(self, proportion: float, total_dimension: int,
                             offset: int, is_last_subtree: bool) -> int:
        """Calculate dimension for a subtree rectangle, adjusting for the
        last subtree differently."""
        if not is_last_subtree:
            return int(total_dimension * proportion)
        else:
            return total_dimension - offset

    def get_rectangles(self) -> (
            List)[Tuple[Tuple[int, int, int, int], Tuple[int, int, int]]]:

        """Return a list with tuples for every leaf in the displayed-tree
        rooted at this tree. Each tuple consists of a tuple that defines the
        appropriate pygame rectangle to display for a leaf, and the colour
        to fill it with.
        """
        if self.is_empty():
            return []

        if self._expanded:
            if self.is_empty() or (self.data_size == 0 and not self._subtrees):
                return []
            elif not self._subtrees:
                return [(self.rect, self._colour)]
            else:
                rects = []
                for tree in self._subtrees:
                    rects.extend(tree.get_rectangles())
                return rects
        else:
            if self.data_size == 0 and not self._subtrees:
                return []
            return [(self.rect, self._colour)]


    def get_tree_at_position(self, pos: Tuple[int, int]) -> Optional[TMTree]:
        """Return the leaf in the displayed-tree rooted at this tree whose
        rectangle contains position <pos>, or None if <pos> is outside of this
        tree's rectangle.

        If <pos> is on the shared edge between two or more rectangles,
        always return the leftmost and topmost rectangle (wherever applicable).
        """
        if self._is_pos_inside_rect(pos):
            if self._is_leaf_or_not_expanded():
                return self
            else:
                return self._search_subtrees_for_pos(pos)
        return None

    def _is_pos_inside_rect(self, pos: Tuple[int, int]) -> bool:
        """Check if the position falls within this tree's rectangle."""
        x, y = pos
        lower_x, lower_y, upper_x, upper_y = self.rect
        return (lower_x <= x <= lower_x + upper_x
                and lower_y <= y <= lower_y + upper_y)

    def _is_leaf_or_not_expanded(self) -> bool:
        """Check if this tree is a leaf or not expanded."""
        return self._subtrees == [] or not self._expanded

    def _search_subtrees_for_pos(
            self, pos: Tuple[int, int]) -> Optional[TMTree]:
        """Recursively search the subtrees for a tree containing the
        position."""
        for tree in self._subtrees:
            pos_tree = tree.get_tree_at_position(pos)
            if pos_tree is not None:
                return pos_tree
        return None

    def update_data_sizes(self) -> int:
        """Update the data_size for this tree and its subtrees, based on the
        size of their leaves, and return the new size.

        If this tree is a leaf, return its size unchanged.
        """
        if not self._subtrees:
            return self.data_size
        else:
            # If the tree is not a leaf, sum the sizes of its subtrees.
            self.data_size = sum(subtree.update_data_sizes() for
                                 subtree in self._subtrees)
            return self.data_size

    def move(self, destination: TMTree) -> None:
        """If this tree is a leaf, and <destination> is not a leaf, move this
        tree to be the last subtree of <destination>. Otherwise, do nothing.
        """

        if self is destination or self._parent_tree is destination:
            return

        if not self._subtrees and destination._subtrees:
            self._parent_tree._subtrees.remove(self)
            if not self._parent_tree._subtrees:
                self._parent_tree._expanded = False
            self._parent_tree.data_size -= self.data_size
            self._helper_root()
            self._parent_tree = destination
            destination._subtrees.append(self)
            destination.data_size += self.data_size
            destination._helper_root()


    def change_size(self, factor: float) -> None:
        """Change the value of this tree's data_size attribute by <factor>.

        Do nothing if this tree is not a leaf.
        """
        if not self._is_leaf():
            return

        self._apply_size_change(factor)
        self._helper_root()

    def _is_leaf(self) -> bool:
        """Check if the current tree is a leaf."""
        return not self._subtrees

    def _apply_size_change(self, factor: float) -> None:
        """Apply the size change based on the given factor."""
        if factor > 0:
            self._increase_size(factor)
        else:
            self._decrease_size(factor)

    def _increase_size(self, factor: float) -> None:
        """Increase the data_size by the given factor, always rounding up."""
        self.data_size += math.ceil(self.data_size * factor)

    def _decrease_size(self, factor: float) -> None:
        """Decrease the data_size by the given factor, applying special
        handling for negative factors."""
        if self.data_size == 0:
            self.data_size += 1
        else:
            change = math.floor(self.data_size * factor)
            self.data_size = max(1, self.data_size + change)

    def delete_self(self) -> bool:
        """Removes the current node from the visualization and
        returns whether the deletion was successful.

        Only do this if this node has a parent tree.

        Do not set self._parent_tree to None, because it might be used
        by the visualiser to go back to the parent folder.
        """

        # Check if the current node has a parent tree
        if self._parent_tree is not None:
            # Remove the current node from its parent's _subtrees list
            self._parent_tree._subtrees.remove(self)
            if not self._parent_tree._subtrees:
                self._parent_tree._expanded = False
            self._parent_tree._recalculate_data_sizes()
            self._parent_tree.update_data_sizes()
            self.data_size = 0

            # Update the data_size of the parent and all ancestors
            self._helper_root()

            return True
        else:
            # The node does not have a parent and cannot be deleted
            return False

    def _recalculate_data_sizes(self) -> None:
        """helper for delete self, used to recalculate the data sizes after
        deletion"""
        # Recalculate data size starting from this node upwards.
        self.data_size = sum(subtree.data_size for subtree in self._subtrees)
        if self._parent_tree:
            self._parent_tree._recalculate_data_sizes()

    def _helper_root(self) -> None:
        """helper to get the top most root in the tree"""
        root = self
        while root._parent_tree is not None:
            root = root._parent_tree
        root.update_data_sizes()

    def expand(self) -> None:
        """Expand this tree, so that it's subtrees are shown.
        If this tree is expanded, or a leaf, do nothing.
        """
        if not self._subtrees:
            pass
        else:
            self._expanded = True

    def expand_all(self) -> None:
        """Expand this tree, and all trees within it.
        If this tree is expanded, or a leaf, do nothing.
        """
        if not self._subtrees:
            pass

        else:
            self._expanded = True
            for tree in self._subtrees:
                tree.expand_all()

    def collapse(self) -> None:
        """Collapse the selected group of trees.
        If the selected tree is the root of the tree, do nothing.
        """
        if self._parent_tree is not None:
            self._parent_tree._expanded = False
            self._expanded = False
            for subtree in self._parent_tree._subtrees:
                subtree._collapse_parent()

    # helper
    def _collapse_parent(self) -> None:
        """helper for the collapse function, Collapses all subtrees of this
        tree.
        """
        self._expanded = False

        if not self._subtrees:
            pass

        else:
            for tree in self._subtrees:
                tree._collapse_parent()

    def collapse_all(self) -> None:
        """Collapse every tree contained in the root of this tree.
        """
        root = self._get_root()
        root._collapse_parent()

    def _get_root(self) -> TMTree:
        """Return the root Tree of this TMTree
        """
        if self._parent_tree is None:
            return self

        else:
            return self._parent_tree._get_root()

    # Methods for the string representation
    def get_path_string(self) -> str:
        """
        Return a string representing the path containing this tree
        and its ancestors, using the separator for this OS between each
        tree's name.
        """
        if self._parent_tree is None:
            return self._name
        else:
            return self._parent_tree.get_path_string() + \
                self.get_separator() + self._name

    def get_separator(self) -> str:
        """Return the string used to separate names in the string
        representation of a path from the tree root to this tree.
        """
        raise NotImplementedError

    def get_suffix(self) -> str:
        """Return the string used at the end of the string representation of
        a path from the tree root to this tree.
        """
        raise NotImplementedError


def _same(trees: List[TMTree]) -> Optional[TMTree]:
    """Return the TMTree in matches that is closest to (0,0)
    """
    if len(trees) > 1:
        closest = trees[0]
        for tree in trees:
            if tree.rect[0] < closest.rect[0]:
                closest = tree
            elif tree.rect[1] < closest.rect[1]:
                closest = tree
        return closest

    elif len(trees) == 1:
        return trees[0]

    else:
        return None


class FileSystemTree(TMTree):
    """A tree representation of files and folders in a file system.

    The internal nodes represent folders, and the leaves represent regular
    files (e.g., PDF documents, movie files, Python source code files, etc.).

    The _name attribute stores the *name* of the folder or file, not its full
    path.

    The data_size attribute for regular files is simply the size of the file,
    as reported by os.path.getsize.
    """

    def __init__(self, path: str) -> None:
        """Store the file tree structure contained in the given file or folder.

        Precondition: <path> is a valid path for this computer.
        """
        # getting the basename of the path.
        name = os.path.basename(path)

        if os.path.isdir(path):
            # If it is a dir, then this list will keep track of the contents
            subtrees = []

            for filename in os.listdir(path):
                # This iterates over every item in the directory, creating a
                # full path for each item using os.path.join
                # For example, if path is /home/user/Documents and filename
                # is file.txt, file_path will be /home/user/Documents/file.txt.
                file_path = os.path.join(path, filename)

                # Recursively creating new FileSystemTree objects for filenames
                # in the directory
                subtree = FileSystemTree(file_path)
                subtrees.append(subtree)

            super().__init__(name, subtrees)

        else:
            # if it is not a folder(dir) then we just set the attributes and
            # get the file size.
            super().__init__(name, [])
            self.data_size = os.path.getsize(path)

    def get_separator(self) -> str:
        """Return the file separator for this OS.
        """
        return os.sep

    def get_suffix(self) -> str:
        """Return the final descriptor of this tree.
        """

        def convert_size(data_size: float, suffix: str = 'B') -> str:
            suffixes = {'B': 'kB', 'kB': 'MB', 'MB': 'GB', 'GB': 'TB'}
            if data_size < 1024 or suffix == 'TB':
                return f'{data_size:.2f}{suffix}'
            return convert_size(data_size / 1024, suffixes[suffix])

        components = []
        if len(self._subtrees) == 0:
            components.append('file')
        else:
            components.append('folder')
            components.append(f'{len(self._subtrees)} items')
        components.append(convert_size(self.data_size))
        return f' ({", ".join(components)})'
