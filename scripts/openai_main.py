import os
import re
import nbformat
from nbconvert import MarkdownExporter
from nbconvert.preprocessors import Preprocessor, ExecutePreprocessor

# Define a custom preprocessor that converts markdown cells with code blocks
# into markdown cells with the code blocks rendered as code outputs
class CodeBlockPreprocessor(Preprocessor):
    def preprocess(self, nb, resources):
        # Iterate over all cells in the notebook
        for cell in nb.cells:
            # Check if the cell is a markdown cell and if it contains code blocks
            if cell["cell_type"] == "markdown" and re.search(r"```(.*?)```", cell["source"], flags=re.DOTALL):
                # Create a new code cell with the code blocks from the markdown cell
                new_cell = nbformat.v4.new_code_cell("\n".join(re.findall(r"```(.*?)```", cell["source"], flags=re.DOTALL)))
                # Replace the markdown cell with the code cell
                nb.cells[nb.cells.index(cell)] = new_cell
        return nb, resources

# Define a function that converts a markdown file into a Jupyter Notebook
def markdown_to_notebook(markdown_file_path, notebook_file_path):
    # Read the markdown file]
    """
    markdown_to_notebook converts a markdown file into a Jupyter Notebook

    Args:

    :param markdown_file_path: Path to the markdown file
    :type markdown_file_path:
    :param notebook_file_path: Path to the Jupyter Notebook file
    :type notebook_file_path:
    """
    with open(markdown_file_path) as f:
        markdown_text = f.read()

    # Create a Jupyter Notebook with the markdown text
    notebook = nbformat.v4.new_notebook(markdown=markdown_text)

    # Create an exporter that converts Jupyter Notebooks to markdown
    exporter = MarkdownExporter()

    # Preprocess the notebook to convert markdown cells with code blocks
    # into markdown cells with the code blocks rendered as code outputs
    notebook, _ = CodeBlockPreprocessor().preprocess(notebook, {})

    # Export the preprocessed notebook to markdown
    markdown_text, _ = exporter.from_notebook_node(notebook)

    # Create a Jupyter Notebook with the preprocessed markdown text
    notebook = nbformat.v4.new_notebook(markdown=markdown_text)

    # Execute the code cells in the notebook
    ep = ExecutePreprocessor(timeout=600, kernel_name="python3")
    ep.preprocess(notebook, {})

    # Save the executed notebook to the specified file path
    with open(notebook_file_path, "w") as f:
        nbformat.write(notebook, f)



# Define a function that converts all markdown files in a directory into Jupyter Notebooks
def convert_directory(input_dir, output_dir):
    # Create the output directory if it does not exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Iterate over all files in the input directory
    for file_name in os.listdir(input_dir):
        # Check if the file is a markdown file
        if file_name.endswith(".md"):
            # Get the full paths to the input and output files
            input_file_path = os.path.join(input_dir, file_name)
            output_file_path = os.path.join(output_dir, os.path.splitext(file_name)[0] + ".ipynb")

            # Convert the markdown file into a Jupyter Notebook
            markdown_to_notebook(input_file_path, output_file_path)


convert_directory("../markdown_docs", "../generated_notebooks")
