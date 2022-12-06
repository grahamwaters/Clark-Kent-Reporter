import nbformat
import re


class NotebookConverter:
    def __init__(self):
        self.notebook_name = "./output/generated_notebook.ipynb"
        self.markdown_report_name = "./output/generated_markdown_report.md"

    def table_maker(self, text, f):
        # Split the text into rows
        rows = text.split("\n")

        # Extract the column names from the first row
        columns = rows[0].split("|")
        columns = [column.strip() for column in columns]

        # Write the column names as a markdown table header
        f.write("|" + "|".join(columns) + "|\n")
        f.write("|" + "|".join(["---"] * len(columns)) + "|\n")

        # Write the rest of the rows as markdown table rows
        # for row in rows[1:]:
        #     # Split the row into cells and strip any leading/trailing whitespace
        #     cells = [cell.strip() for cell in row.split('|')]
        #     f.write('|' + '|'.join(cells) + '|\n')

        # put the data into the columns and rows
        for row in rows[1:]:
            if row.find("|") == -1:
                if row.find("   ") != -1:
                    # then the delimiter is '   ' not '|'
                    cells = [cell.strip() for cell in row.split("   ")]
                    f.write("|" + "|".join(cells) + "|\n")
                else:
                    # then the delimiter is ' ' not '|'
                    cells = [cell.strip() for cell in row.split(" ")]
                    f.write("|" + "|".join(cells) + "|\n")
            else:
                # then the delimiter is '|' not '   '
                cells = [cell.strip() for cell in row.split("|")]
                f.write("|" + "|".join(cells) + "|\n")
        # Add an extra newline at the end of the table
        f.write("\n")

    def jupyter_to_md(self, input_file_path):
        """
        Convert a Jupyter notebook to a markdown file.

        This method converts a Jupyter notebook to a markdown file by reading the input Jupyter notebook, iterating over its cells, and writing the contents of each markdown cell and code cell to the output markdown file. The contents of a markdown cell are written as-is, with a newline inserted between paragraphs. The contents of a code cell are written as a code block denoted by triple backticks (```), with the language specified as "python".

        Args:
            input_file_path (str): The path to the input Jupyter notebook.

        Returns:
            None
        """

        table_flag = False  # flag to indicate whether to write a table or not

        with open(input_file_path) as f:
            nb = nbformat.read(f, as_version=4)

        # Create a new markdown file
        with open(f"{self.markdown_report_name}", "w") as f:
            # Iterate over the cells in the Jupyter notebook
            for cell in nb["cells"]:
                # If the cell is a markdown cell, write its contents to the markdown file,
                # inserting a newline between paragraphs
                if cell["cell_type"] == "markdown":
                    text = cell["source"]
                    paragraphs = text.split("\n\n")
                    for paragraph in paragraphs:
                        f.write(paragraph + "\n\n")
                elif (
                    cell["cell_type"] == "code"
                    and cell["execution_count"] is not None
                    and cell["outputs"]
                    and "head" in cell["source"]
                    and table_flag
                ):
                    # use the table_maker function to write the table to the markdown file
                    for output in cell["outputs"]:
                        if output["output_type"] == "execute_result":
                            if output["data"]["text/plain"]:
                                text = output["data"]["text/plain"]
                                self.table_maker(text, f)

                elif (
                    cell["cell_type"] == "code"
                    and cell["execution_count"] is not None
                    and cell["outputs"]
                ):  # Note that we only write code cells that have been executed
                    f.write(
                        "\n```python\n"
                    )  # Note that we specify the language as python
                    f.write(cell["source"] + "\n")
                    f.write(
                        "\n```\n\n"
                    )  # Note the extra newline at the end of the code block

                    # Iterate over the outputs of the code cell and write each output
                    # to the markdown file
                    for output in cell["outputs"]:
                        if output["output_type"] == "execute_result":
                            # If the output is text, write it as a paragraph
                            if output["data"]["text/plain"]:
                                text = output["data"]["text/plain"]
                                paragraphs = text.split("\n\n")
                                for paragraph in paragraphs:
                                    f.write(paragraph + "\n\n")
                        elif output["output_type"] == "display_data":
                            # If the output is an image, write it as an image tag
                            if output["data"]["image/png"]:
                                image_data = output["data"]["image/png"]
                                f.write(f"![image]({image_data})\n\n")

    def md_to_jupyter(self, input_file_path):
        """
        Convert a markdown file to a Jupyter notebook.

        This method converts a markdown file to a Jupyter notebook by extracting the section titles, sections, and code blocks from the input markdown file and adding them as markdown cells and code cells, respectively, to the generated Jupyter notebook.

        Args:
            input_file_path (str): The path to the input markdown file.

        Returns:
            None
        """
        # Read the file
        with open(input_file_path) as f:
            text = f.read()

        # Use regular expressions to extract the section titles
        titles = re.findall(r"^# (.*)$", text, re.MULTILINE)

        # Use regular expressions to extract the sections (the text between the section titles)
        sections = re.findall(r"^#.*\n([\s\S]*?)^#", text, re.MULTILINE)

        # Use regular expressions to extract the code blocks
        code_blocks = re.findall(r"```(.+?)```", text, re.DOTALL)

        # Create a new notebook
        nb = nbformat.v4.new_notebook()

        # Add the section titles as markdown cells
        for title in titles:
            nb["cells"].append(nbformat.v4.new_markdown_cell(title))

        # Add the text of each section as markdown cells
        for section in sections:
            nb["cells"].append(nbformat.v4.new_markdown_cell(section))

        # Add the code blocks as code cells
        for code in code_blocks:
            nb["cells"].append(nbformat.v4.new_code_cell(code))
        # Save the notebook
        with open(f"{self.notebook_name}", "w") as f:
            nbformat.write(nb, f)


if __name__ == "__main__":
    converter = NotebookConverter()
    print("Converting Jupyter notebook to markdown...")
    converter.jupyter_to_md("./input/01_premodeling.ipynb")
    print("Converting markdown to Jupyter notebook...")
    converter.md_to_jupyter("./output/generated_markdown_report.md")
