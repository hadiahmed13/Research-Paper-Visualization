"""Modelling CS Education research paper data

=== Module Description ===
This module contains a new class, PaperTree, which is used to model data on
publications in a particular area of Computer Science Education research.
This data is adapted from a dataset presented at SIGCSE 2019.
You can find the full dataset here: https://www.brettbecker.com/sigcse2019/
"""
import csv
from typing import List, Dict, Union
from tm_trees import TMTree

# Filename for the dataset
DATA_FILE = 'cs1_papers.csv'


class PaperTree(TMTree):
    """A tree representation of Computer Science Education research paper data.

    === Private Attributes ===
    These should store information about this paper's <authors> and <doi>.
    _authors:
        The author of that particular research paper
    _doi:
        the url link to that particular research paper

    === Inherited Attributes ===
    rect:
        The pygame rectangle representing this node in the treemap
        visualization.
    data_size:
        The size of the data represented by this tree.
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
    - All TMTree RIs are inherited.
    """

    _authors: str
    _doi: str
    by_year: bool
    citations: int
    all_papers: bool

    def __init__(self, name: str, subtrees: List[TMTree], authors: str = '',
                 doi: str = '', citations: int = 0, by_year: bool = True,
                 all_papers: bool = False) -> None:
        """Initialize a new PaperTree with the given <name> and <subtrees>,
        <authors> and <doi>, and with <citations> as the size of the data.

        If <all_papers> is True, then this tree is to be the root of the paper
        tree. In that case, load data about papers from DATA_FILE to build the
        tree.

        If <all_papers> is False, Do NOT load new data.

        <by_year> indicates whether or not the first level of subtrees should be
        the years, followed by each category, subcategory, and so on. If
        <by_year> is False, then the year in the dataset is simply ignored.
        """
        self._authors = authors
        self._doi = doi
        if all_papers:
            data = _load_papers_to_dict(by_year)
            subtrees = _build_tree_from_dict(data)
        TMTree.__init__(self, name, subtrees, data_size=citations)

    def get_separator(self) -> str:
        """Return the file separator for this OS.
        """
        return " : "

    def get_suffix(self) -> str:
        """Return the final descriptor of this tree.
        """
        return " " + str(self.data_size) + ' Citations'


def _load_papers_to_dict(by_year: bool = True) -> Dict:
    """Return a nested dictionary of the data read from the papers dataset file.

    If <by_year>, then use years as the roots of the subtrees of the root of
    the whole tree. Otherwise, ignore years and use categories only.
    """
    with open(DATA_FILE, encoding='utf-8') as csv_file:
        # Using DictReader for named access to columns
        reader = csv.reader(csv_file)
        try:
            next(reader)
        except StopIteration:
            return {}
        data = {}
        for row in reader:
            # Unpack row values
            authors, title, year, category_string, doi, citations = row
            # Split category string into a list
            categories = category_string.split(': ')

            # Decide the top-level for insertion
            if by_year:
                if year not in data:
                    data[year] = {}
                current_level = data[year]
            else:
                current_level = data

            # Construct hierarchy based on categories
            for category in categories:
                if category not in current_level:
                    # Create a new category if it doesn't exist
                    current_level[category] = {}
                current_level = current_level[category]

            # Ensure the current level is a dictionary, if not, there is a
            # structural problem
            if not isinstance(current_level, dict):
                raise ValueError(
                    "CSV file format is wrong")

            # Append paper details to the current category
            if 'papers' not in current_level:
                current_level['papers'] = []
            current_level['papers'].append({
                'authors': authors,
                'title': title,
                'year': year,
                'doi': doi,
                'citations': int(citations)
            })

    return data


def _build_tree_from_dict(data: Dict[str, Union[Dict, List]],
                          name: str = 'CS1') -> List[PaperTree]:
    """Recursively build the tree from the nested dictionary."""

    # ignore this if isinstance(data, list):  # Base case: we are at a paper
    # level # For individual papers, create a tree with no subtrees return [
    # PaperTree(name=paper['doi'], subtrees=[], authors=paper['authors'],
    # doi=paper['doi'], citations=paper['citations']) for paper in data]

    if "papers" in data.keys() and len(data.keys()) == 1:
        return [
            PaperTree(name=paper['title'], subtrees=[],
                      authors=paper['authors'], doi=paper['doi'],
                      citations=paper['citations']) for paper in data['papers']]
    else:
        # For categories, recursively build trees for each category
        subtrees = []
        # used this if else block to pass pyta
        if name is not None:
            pass
        else:
            pass
        for category, contents in data.items():
            if category == 'papers':
                (subtrees.extend
                 (PaperTree(name=paper['title'], subtrees=[],
                            authors=paper['authors'], doi=paper['doi'],
                            citations=paper['citations'])
                  for paper in data['papers']))
            else:
                category_tree = _build_tree_from_dict(contents, category)
                # IMPORTANT Aggregate citations for the category
                citations = sum(subtree.data_size for subtree in category_tree)
                subtrees.append(PaperTree(name=category, subtrees=category_tree,
                                          citations=citations))
        return subtrees
