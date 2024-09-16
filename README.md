# Visualization of 1,000 Research Papers Using Recursive Treemaps

An interactive data visualization tool developed to help users explore and manage large hierarchical datasets, such as 1,000+ academic research papers. This tool uses **recursive treemap algorithms** to visually represent complex data structures. It allows users to easily navigate through large directories, expand and collapse sections of the tree, and visualize data based on real-world metrics, such as the number of citations.

## Features

- **Recursive Treemaps**: Visualize hierarchical data using proportionally sized rectangles, making it easy to understand the structure and relationships within the dataset.
- **Interactive User Interface**: Users can expand, collapse, and resize data nodes in real-time, gaining deeper insights into their datasets.
- **File System Integration**: Visualize both academic research papers and file systems, showcasing their hierarchy and size-based relationships.
- **Python-based Visualization**: Built using Python, with the `os` library to manage file systems and `Pygame` for rendering visualizations.

## Getting Started

### Prerequisites

- Python 3.x
- Pygame (`pip install pygame`)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repository/treemap-visualization.git
   cd treemap-visualization
   ```

2. Install the required libraries:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the treemap visualizer:
   ```bash
   python treemap_visualiser.py
   ```

## Project Structure

- `papers.py`: Contains the logic for processing and visualizing the research papers dataset, including expansion/collapse rules.
- `tm_trees.py`: Defines the tree structure and recursive logic for treemap generation.
- `treemap_visualiser.py`: The main visualizer file, utilizing `Pygame` to render the treemaps.
- `cs1_papers.csv`: The dataset containing the research papers and their hierarchical structure.

## Usage

Once the tool is launched, it opens a graphical window that visualizes the hierarchical data as a treemap. Users can interact with the data by clicking on various sections of the visualization. The primary interaction features include:

- **Click to Select**: Click on any rectangle to select it. Once selected, the name and number of citations will be displayed at the bottom of the screen.
- **Expand/Collapse Nodes**: Use the `e` key to expand a selected node, and the `c` key to collapse a node. Pressing `a` expands all subtrees, while pressing `x` collapses the entire tree.
- **Resize Nodes**: Press the up and down arrow keys to increase or decrease the size of a selected node proportionally.
- **Delete Nodes**: Press the `Del` key to delete the selected node from the visualization.

### Example Visualizations

#### Initial State
When the tool is first opened, a simple treemap with the overall dataset is displayed.
![Initial State](/data/Initial_state.png)

#### Expanded View
After expanding some of the nodes, the user can explore the hierarchical structure of the research papers dataset.
![Expanded View](/data/Expanded%20View.png)

#### Fully Expanded View
With all nodes expanded, the complete structure of the dataset is revealed, showing detailed relationships and proportions between various subcategories.
![Fully Expanded View](/data/Fully%20Expanded%20View.png)

## Dataset

The dataset used in this project (`cs1_papers.csv`) contains over 1,000 academic research papers related to computer science education. The papers are categorized into a hierarchical structure, with subcategories representing different research areas. Each paper also includes metadata, such as the number of citations, which is used to proportionally size the rectangles in the treemap.

### Example Entry in `cs1_papers.csv`:
```csv
CS1,Tools,Visualization,74
CS1,Students,Measuring Success,116
...
```

## How It Works

The project is centered around using **recursive treemap algorithms** to break down complex hierarchical data into smaller parts, representing each node as a rectangle proportional to its size. The key steps involved in the algorithm include:

1. **Data Modeling**: The dataset is parsed and modeled as a tree structure using recursive methods. Each node in the tree represents a research paper or category.
2. **Treemap Generation**: A custom treemap algorithm calculates the size and position of each rectangle in the visualization based on the node’s size (e.g., number of citations).
3. **Rendering**: The `Pygame` library is used to render the treemap and provide interactive functionality, allowing users to expand/collapse nodes and resize elements in real time.

## License

This project is licensed under the University of Toronto License - see the [LICENSE](LICENSE) file for details.

---