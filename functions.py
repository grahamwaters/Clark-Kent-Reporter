import nbformat
import re
#* Convert a Jupyter notebook to a markdown file
def jupyter_to_md(input_file_path):
    f = open(input_file_path)
    # Read the Jupyter notebook
    with open('01_premodeling.ipynb') as f:
        nb = nbformat.read(f, as_version=4)

    # Create a new markdown file
    with open('generated_markdown_report.md', 'w') as f:
        # Iterate over the cells in the Jupyter notebook
        for cell in nb['cells']:
            # If the cell is a markdown cell, write its contents to the markdown file,
            # inserting a newline between paragraphs
            if cell['cell_type'] == 'markdown':
                text = cell['source']
                paragraphs = text.split('\n\n')
                for paragraph in paragraphs:
                    f.write(paragraph + '\n\n')
            # If the cell is a code cell, write its contents to the markdown file
            # as a code block denoted by triple backticks (```)
            elif cell['cell_type'] == 'code' and cell['execution_count'] is not None and cell['outputs']:
                f.write('```python\n') # Note that we specify the language as python
                f.write(cell['source']) # + '
                f.write('```\n\n') # Note the extra newline at the end of the code block

#* Convert a markdown file to a Jupyter notebook
def md_to_jupyter(input_file_path):
    # Read the file
    with open(input_file_path) as f:
        text = f.read()

    # Use regular expressions to extract the section titles
    titles = re.findall(r'^# (.*)$', text, re.MULTILINE)

    # Use regular expressions to extract the sections (the text between the section titles)
    sections = re.findall(r'^#.*\n([\s\S]*?)^#', text, re.MULTILINE)

    # Use regular expressions to extract the code blocks
    code_blocks = re.findall(r'```(.+?)```', text, re.DOTALL)

    # Create a new notebook
    nb = nbformat.v4.new_notebook()

    # Add the section titles as markdown cells
    for title in titles:
        nb['cells'].append(nbformat.v4.new_markdown_cell(title))

    # Add the text of each section as markdown cells
    for section in sections:
        nb['cells'].append(nbformat.v4.new_markdown_cell(section))

    # Add the code blocks as code cells
    for code in code_blocks:
        nb['cells'].append(nbformat.v4.new_code_cell(code))

    # Save the notebook
    with open('generated_notebook.ipynb', 'w') as f:
        nbformat.write(nb, f)
