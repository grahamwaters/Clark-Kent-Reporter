import os
import pandas as pd
import os
import nbformat
import re
import datetime as dt
import configparser
import numpy as np
# user-defined variables
project_name = "my_project" # get this from the first <h1> tag in the readme.md file or the first markdown header with only one # symbol in the readme.md file
author = "Graham Waters"
license_text = "MIT License"

# read the config file
config = configparser.ConfigParser()
config.read("config.ini")

# get the values
path = config["DEFAULT"]["path"]
scripts_path = config["DEFAULT"]["scripts_path"]
notebooks_path = config["DEFAULT"]["notebooks_path"]

# print the values
print(path)
print(scripts_path)
print(notebooks_path)

# Global Variables

date = dt.datetime.now().strftime("%Y-%m-%d")

# set the readme text to blank
readme_text = "" # initially the file is empty

# read a readme.md file and make a report jupyter notebook that has the appropriate sections (from the table of contents in the readme.md file)
# What are the expected sections in a data science report notebook?
# The answer is:
# 1. Introduction
# 2. Table of Contents
# 3. Data
# 4. Data Cleaning
# 5. Data Exploration
# 6. Data Analysis
# 7. Conclusions
# 8. References

# We want to create a jupyter notebook that has the following pattern for it's sections:

# A header markdown cell with the project name
# A markdown cell with the table of contents
# A markdown cell for the Introduction (with the text from the readme.md file for the Introduction)
# add a code cell below this markdown cell for the user to add any code they want to the Introduction.

# A markdown cell for the Data Section (with the text from the readme.md file for the Data Section).
# This section is about explaining what kinds of data are in the dataset and how the data was collected.

# A markdown cell for the Data Cleaning Section (with the text from the readme.md file for the Data Cleaning Section).
# This section is about explaining how the data was cleaned.
# what kinds of dirtiness was found in the data and how it was cleaned?
# were there any missing values? how were they handled?

# A markdown cell for the Data Exploration Section (with the text from the readme.md file for the Data Exploration Section).
# This section is about explaining how the data was explored.

# make a function that generates a jupyter notebook based on the table of contents in the readme.md file.
# the pattern it uses is:
# A header markdown cell with the project name
# For each section in the table of contents:
#   A markdown cell with the section name
#   A markdown cell with the text from the readme.md file for that section
#   add a code cell below this markdown cell for the user to add any code they want to the section.



def remove_markdown_comments(readme_text):
    beginning_len = len(readme_text)
    # remove the markdown comments from the readme.md file
    # <!-- marks the start of a comment and --> marks the end of a comment
    # comment_reg_pattern = r"<!--(.*?)-->"
    # create a variable to hold the comment text
    comment_text = ""
    # find the first comment
    comment_start = readme_text.find("<!--")
    # find the end of the comment
    comment_end = readme_text.find("-->")
    # while there are comments in the readme.md file
    while comment_start != -1 and comment_end != -1:
        # get the comment text
        comment_text = readme_text[comment_start:comment_end + 3]
        # remove the comment text from the readme.md file
        readme_text = readme_text.replace(comment_text, "")
        # find the next comment
        comment_start = readme_text.find("<!--")
        # find the end of the comment
        comment_end = readme_text.find("-->")
        print(comment_text[0:10],"..",comment_text[-10:])
    ending_len = len(readme_text)
    print(f"removed {beginning_len - ending_len} characters from the readme.md file")

    return readme_text


def get_project_name(readme_text):
    """
    get_project_name takes a string of text and returns a string

    Parameters

    :param readme_text: a string of text
    :type readme_text: str
    :return: a string
    :rtype: str
    """
    # get the name of the project from the first <h1> tag in the readme.md file or the first markdown header with only one # symbol in the readme.md file
    # the readme text is split with '\n' as the delimiter not actual newlines.

    # split the readme.md file into lines
    lines = readme_text.split("\n")  # split on newlines

    # find the line that starts with "#"
    project_name_line = [line for line in lines if line.startswith("#")][0]

    # remove the "#" symbols
    project_name = project_name_line.replace("#", "")

    # remove the spaces
    project_name = project_name.strip()

    return project_name

def parse_table_of_contents(readme_text):
    """
    parse_table_of_contents takes a string of text and returns a list of tuples

    Parameters

    :param readme_text: a string of text
    :type readme_text: str
    :return: a list of tuples
    :rtype: list
    """
    # parse the table of contents from the readme.md file
    # returns a list of tuples (section_name, section_level)
    # section_level is an integer
    # section_name is a string

    # the readme text is split with '\n' as the delimiter not actual newlines.

    # get the name of the project from the first <h1> tag in the readme.md file or the first markdown header with only one # symbol in the readme.md file
    global project_name
    project_name = get_project_name(readme_text)

    # remove the commments
    readme_text = remove_markdown_comments(readme_text) # this function modifies the global variable readme_text

    # split the readme.md file into lines
    lines = readme_text.split("\n")  # split on newlines

    # find the line that starts with "Table of Contents"
    table_of_contents_line = [
        line for line in lines if line.lower().find("table of contents") > -1
    ][0]

    # find the line number of that line
    table_of_contents_line_number = lines.index(table_of_contents_line)

    # find the list of lines that are the table of contents
    table_of_contents_lines = lines[table_of_contents_line_number + 1 :]

    # remove the lines that are empty
    table_of_contents_lines = [line for line in table_of_contents_lines if line != ""]

    # remove the lines that are not section headers
    table_of_contents_lines = [
        line for line in table_of_contents_lines if line.startswith("#")
    ]

    # parse the section names and section levels
    table_of_contents = []
    for line in table_of_contents_lines:
        # count the number of "#" symbols
        section_level = line.count("#")
        # remove the "#" symbols
        section_name = line.replace("#", "")
        # remove the spaces
        section_name = section_name.strip()
        # make a tuple
        section = (section_name, section_level)
        # append the tuple to the list of sections
        table_of_contents.append(section)

    return table_of_contents


def startup():
    global readme_text
    # read the readme.md file
    with open(path, "r") as f:
        readme_text = f.read()

    # parse the table of contents
    table_of_contents = parse_table_of_contents(readme_text)
    return table_of_contents, readme_text


def process_flow_controller():
    # from start to finish, examine the readme and end with a populated, fully functional report jupyter notebook that can be tweaked and then presented to the end-user as the final report.
    global project_name
    (
        table_of_contents,
        readme_text,
    ) = startup()  # read the readme.md file and parse the table of contents

    # using the table of contents, create the sections of the report notebook
    generate_report_notebook(project_name, table_of_contents, readme_text)

def create_data_section(report_notebook):
    global readme_text
    # generate the data section of the report notebook
    # the data section is a markdown cell with the text from the readme.md file for the Data Section.
    # This section is about explaining what kinds of data are in the dataset and how the data was collected.

    # find the line that starts with "Data" and
    return


def get_special_blocks_from_text(text):


    # if you see a \n followed by a | character followed by a space, then you are in a special block header and you should start a new special block
    # watch for the next \n character and stop when you see it. The text between where you started and where you stopped is the special block header text.
    header_pattern = r'\n\|\s'
    #
    # Now... for the special block body text...
    # if you see a \n followed by a | character you are in a new row of a table and you need to keep capturing text
    body_pattern = r'\n\|(.*?)\|\n\n'
    # keep going until you see text followed by a | character followed by a \n character followed by a \n character and then stop. The text between where you started and where you stopped is the special block body text.
    #end_pattern = r'\|\n\n'

    # find the first match for the header pattern
    header_match = re.search(header_pattern, text) # this is a string
    # find the index of the first match for the header pattern
    header_match_index = header_match.start() # this is an integer
    # find the first match for the body pattern after the header pattern
    body_match = re.search(body_pattern, text[header_match_index:]) # this is a string
    # find the index of the first match for the body pattern after the header pattern
    body_match_index = body_match.start() + header_match_index # this is an integer
    # get the special block header text
    # with start and end
    special_block_header_text = text[header_match_index:body_match_index]
    # get the special block body text
    special_block_body_text = text[body_match_index:]


    # add the special block header text to the body text separated by a newline
    special_block_text = special_block_header_text + '\n' + special_block_body_text

    # return the special block header text and the special block body text
    return special_block_text







def get_text(section_name, markdown_text):
    """
    get_text takes a section name and a string of markdown text and returns a string of text

    Parameters

    :param section_name: a string of text
    :type section_name: str
    :param markdown_text: a string of text
    :type markdown_text: str
    :return: a string of text
    :rtype: str
    """
    try:
        # get the text for a section from the readme.md file
        # how? find the line that starts with the section name, and is not in the table of contents (using regex) then find the next line that starts with a "#" symbol. The text between those two lines is the text for the section.

        # Removing comments
        markdown_text = remove_markdown_comments(markdown_text) # this function removes any commented code from the readme.md file



        # find the special blocks in the text and return them as a list of strings (each string is a special block of text)
        #!special_blocks = get_special_blocks_from_text(markdown_text)
        #!print("length of special blocks: ", len(special_blocks))
        #!print("special blocks: ", special_blocks)


        # we want to preserve the tables that we find and reproduce them in the report notebook as they are formatted in the readme.md file. Find any in this section and save it to the section text variable.
        # take the tables out of the markdown text and put them in a list, preserving the order of the tables in the markdown text

        # this list of tables should be a list of tuples, each tuple is a table and the first element of the tuple is the table text and the second element is the table location in the markdown text
        # the table location is the index of the table in the markdown text
        # the table text is the text of the table in the markdown text
        # tables = re.findall(table_pattern, markdown_text) # this is a list of tuples, each tuple is a table and the first element of the tuple is the table text and the second element is the table location in the markdown text

        # # remove the tables from the markdown text
        # markdown_text = re.sub(table_pattern, "", markdown_text)

        # step 1: find the line that starts with the section name
        pattern = r"^" + section_name + r".*?$" # the ^ symbol means the start of the line, the $ symbol means the end of the line, the .*? means any number of any characters
        section_name_line = re.findall(pattern, markdown_text, re.MULTILINE)[0] # this is a string of text containing the section name
        # step 2: find the line number of that line
        section_name_line_number = markdown_text.split("\n").index(section_name_line)
        # step 3: find the next line that starts with a "#" symbol
        lines = markdown_text.split("\n")
        # find the line numbers of the lines that start with a "#" symbol
        section_header_line_numbers = [i for i, line in enumerate(lines) if line.startswith("#")]
        # find the line numbers of the lines that start with a "#" symbol that are after the line that starts with the section name
        section_header_line_numbers = [i for i in section_header_line_numbers if i > section_name_line_number]
        # find the line number of the next line that starts with a "#" symbol
        next_section_header_line_number = section_header_line_numbers[0]

        # add the tables back into the markdown text
        # markdown_text = markdown_text.split("\n") # split the markdown text into lines
        # for table in tables:
        #     markdown_text.insert(table[1], table[0])
        # markdown_text = "\n".join(markdown_text) # join the markdown text back into a string

        # markdown_text = " ".join(markdown_text) # this is a string of text with the tables in it
        # step 4: get the text between those two lines while keeping the newlines in the text
        markdown_text = " ".join(lines[section_name_line_number + 1 : next_section_header_line_number])
        # also preserve the bullet points and make them look the same in the markdown text as they do in the readme.md file. We want to make sure the markdown text looks the same as the readme.md file. This includes the * and the - characters. Also, the bullet points are indented by 4 spaces, and could be indented by 2 spaces. We want to preserve that indentation. They may also be numeric i.e. 1, 2, 3, etc. We want to preserve that too.




        bullet_points = re.findall(r"\n[ ]{0,4}[-*][ ]{1,4}", markdown_text)

        # finding the bullet points is not working. It is finding the bullet points in the table of contents. We need to find the bullet points in the section text, not the table of contents. This is because the table of contents is a list of bullet points, and the section text is also a list of bullet points. We need to find the bullet points in the section text, not the table of contents.

        # bullet points could be any of the following:
        # - bullet point (pattern 1)
        # * bullet point (pattern 2)
        # 1. bullet point (pattern 3)
        # 2. bullet point (any number) (pattern 4)
        #  - bullet point (indented by 2 spaces) (pattern 5)
        #  * bullet point (indented by 2 spaces)  (pattern 6)
        # etc.

        # find these patterns in the markdown text
        pattern_1 = r"\n[ ]{0,4}[-][ ]{1,4}"
        pattern_2 = r"\n[ ]{0,4}[*][ ]{1,4}"
        pattern_3 = r"\n[ ]{0,4}[0-9]+[.][ ]{1,4}"
        pattern_4 = r"\n[ ]{0,4}[0-9]+[.][ ]{1,4}"
        pattern_5 = r"\n[ ]{2,4}[-][ ]{1,4}"
        pattern_6 = r"\n[ ]{2,4}[*][ ]{1,4}"

        # find the bullet points in the markdown text
        bullet_points = re.findall(pattern_1, markdown_text)
        bullet_points += re.findall(pattern_2, markdown_text)
        bullet_points += re.findall(pattern_3, markdown_text)
        bullet_points += re.findall(pattern_4, markdown_text)
        bullet_points += re.findall(pattern_5, markdown_text)
        bullet_points += re.findall(pattern_6, markdown_text)

        # make sure there is a newline character at the end of the bullet point
        bullet_points = [bullet_point + "\n" for bullet_point in bullet_points]

        # replace the bullet points with the same bullet points, but with 4 spaces in front of them
        bullet_points = [bullet_point.replace(bullet_point, "    " + bullet_point) for bullet_point in bullet_points]

        # replace the bullet points in the markdown text with the new bullet points
        for bullet_point in bullet_points:
            markdown_text = markdown_text.replace(bullet_point.strip(), bullet_point)

        # also preserve the code blocks and make them look the same in the markdown text as they do in the readme.md file. We want to make sure the markdown text looks the same as the readme.md file. This includes the ``` characters. Also, the code blocks are indented by 4 spaces, and could be indented by 2 spaces. We want to preserve that indentation.

        # code blocks could be any of the following:
        # ```python
        # code
        # ```
        # ```python (indented by 2 spaces)
        # code
        # ```
        # etc.

        # find these patterns in the markdown text
        pattern_1 = r"\n[ ]{0,4}```.*?\n.*?\n[ ]{0,4}```" # this pattern finds the code blocks that are not indented by 2 spaces
        pattern_2 = r"\n[ ]{2,4}```.*?\n.*?\n[ ]{2,4}```" # this pattern finds the code blocks that are indented by 2 spaces

        if re.findall(pattern_1, markdown_text):
            code_blocks = re.findall(pattern_1, markdown_text)
        elif re.findall(pattern_2, markdown_text):
            code_blocks = re.findall(pattern_2, markdown_text)
        else:
            code_blocks = []

        if len(code_blocks) > 0:
            # find the code blocks in the markdown text

            # make sure there is a newline character at the end of the code block
            code_blocks = [code_block + "\n\n" for code_block in code_blocks]

            # replace the code blocks with the same code blocks, but with 4 spaces in front of them
            code_blocks = [code_block.replace(code_block, "    " + code_block) for code_block in code_blocks]

            # replace the code blocks in the markdown text with the new code blocks
            for code_block in code_blocks:
                markdown_text = markdown_text.replace(code_block.strip(), code_block) # the strip() function removes the newline character at the end of the code block so that it can be replaced with the new code block that has a newline character at the end of it (the new code block is the same as the old code block, but with 4 spaces in front of it)

        # also preserve the images and make them look the same in the markdown text as they do in the readme.md file. We want to make sure the markdown text looks the same as the readme.md file. This includes the ![]() characters. Also, the images are indented by 4 spaces, and could be indented by 2 spaces. We want to preserve that indentation.

        # images could be any of the following:
        # ![image](image.png)
        # ![image](image.png) (indented by 2 spaces)
        # etc.

        # find these patterns in the markdown text
        pattern_1 = r"\n[ ]{0,4}!\[.*?\]\(.*?\)"
        pattern_2 = r"\n[ ]{2,4}!\[.*?\]\(.*?\)"

        # find the images in the markdown text
        images = re.findall(pattern_1, markdown_text, re.MULTILINE | re.DOTALL)
        images += re.findall(pattern_2, markdown_text, re.MULTILINE | re.DOTALL)

        # make sure there is a newline character at the end of the image
        images = [image + "\n" for image in images]

        # replace the images with the same images, but with 4 spaces in front of them
        images = [image.replace(image, "    " + image) for image in images]

        # replace the images in the markdown text with the new images
        for image in images:
            markdown_text = markdown_text.replace(image.strip(), image)



        for bullet_point in bullet_points:
            markdown_text = markdown_text.replace(
                bullet_point, bullet_point.replace(" ", " ")
            )  # replace the space with a non-breaking space so that the markdown text looks the same as the readme.md file. The non-breaking space is a special character that looks like a space but it is not a space. It is a special character that tells the markdown renderer to render the space as a space. The markdown renderer will not render a space as a space if it is followed by a newline character. So we need to replace the space with a non-breaking space so that the markdown renderer will render the space as a space.

        #^ Graham: Hey Copilot, why are my bullet points not staying formatted in the generated notebook?
        #* Copilot: I don't know, but I can help you fix it. I think you need to replace the spaces with non-breaking spaces. I can do that for you.
        #^ Graham: Why do I need to replace the spaces with non-breaking spaces?
        #* Copilot: Non-breaking spaces are special characters that look like spaces but they are not spaces. They are special characters that tell the markdown renderer to render the space as a space. The markdown renderer will not render a space as a space if it is followed by a newline character. So we need to replace the space with a non-breaking space so that the markdown renderer will render the space as a space.
        #^ Graham: Thanks Copilot, that was very helpful. Could you share the code to do that?
        #* Copilot: Sure, here you go. I think you need to replace the space with a non-breaking space so that the markdown renderer will render the space as a space. I can do that for you. Here is the code: markdown_text = markdown_text.replace(bullet_point, bullet_point.replace(" ", " "))



        markdown_text = "\n" + markdown_text # add a newline character to the beginning of the markdown text so that the markdown text looks the same as the readme.md file. The readme.md file has a newline character at the beginning of the text for each section.
        # add  to the end of the text
        markdown_text = markdown_text + "\n" # add a newline character to the end of the markdown text so that the markdown text looks the same as the readme.md file. The readme.md file has a newline character at the end of the text for each section. This is important because the markdown renderer will not render a newline character at the end of the text.
    except Exception as e:
        markdown_text = "\n\nSection Text Not Found\n\n"
        print(e)


    # the tables have this  | |  in them replace with  |\n|
    markdown_text = markdown_text.replace('| |', '|\n|')

    return markdown_text


def programmatic_pandas(readme_text, table_of_contents):

    # clear the destination df to make it clean and new (no artifacts from previous runs).

    great_panda_df = pd.DataFrame(
        columns=["section_name", "section_text", "section_level"]
    )

    # The table of contents contains tuples that have this format: ('Steps for Data Cleaning in this Study', 2) for example. The first item in the tuple is the section name and the second item is the level of the section. The level is used to denote how many "#" symbols to put in front of the section name.
    # if a section is level 2, then it belongs under the section that preceeded it with a level of 1. etc. So we need to keep track of the previous section name and level.
    # create a variable to keep track of the previous section name
    # I want markdown cells for all cells in the table of contents that are level 1 preceeded with a level one header in a markdown cell.
    # if there are level 2 sections, then I want a markdown cell for the level 2 section preceeded with a level 2 header in a markdown cell.
    # if there are level 3 sections, then I want a markdown cell for the level 3 section preceeded with a level 3 header in a markdown cell. etc.

    # loop through the table of contents, and populate the great_panda_df dataframe with the section names and section_level.
    for section in table_of_contents:
        # get the section name
        section_name = section[0]
        # get the section level
        section_level = section[1]
        # add the section name and section level to the great_panda_df dataframe
        great_panda_df = great_panda_df.append(
            {"section_name": section_name, "section_level": section_level},
            ignore_index=True,
        )

    # populate the great_panda_df dataframe with the section text
    great_panda_df["section_text"] = great_panda_df["section_name"].apply(
        lambda x: get_text(x, readme_text)
    )

    # add a markdown cell for each section in the table of contents according to the guidelines above.
    # create a list to hold the markdown cells
    markdown_cells = []
    # loop through the great_panda_df dataframe
    for index, row in great_panda_df.iterrows():
        # get the section name
        section_name = row["section_name"]
        # get the section level
        section_level = row["section_level"]
        # get the section text
        section_text = row["section_text"]
        # create a markdown cell for the section name
        markdown_cell = "#" * section_level + " " + section_name
        # add the markdown cell to the markdown_cells list
        markdown_cells.append(markdown_cell)
        # add the section text to the markdown_cells list
        markdown_cells.append(section_text)
        # add a code cell to the markdown_cells list
        markdown_cells.append("")

    # save great_panda_df to a csv file
    great_panda_df.to_csv("../data/great_panda_df.csv", index=False)
    # save the markdown_cells list to a text file
    with open("markdown_cells.txt", "w") as f:
        for cell in markdown_cells:
            f.write(cell + "\n\n")

    return markdown_cells

def generate_report_notebook(project_name, table_of_contents, readme_text):
    # global readme_text
    global author, date, license_type
    # generate a jupyter notebook based on the table of contents in the readme.md file.
    # the pattern it uses is:
    # A header markdown cell with the project name
    # For each section in the table of contents:
    #   A markdown cell with the section name
    #   A markdown cell with the text from the readme.md file for that section
    #   add a code cell below this markdown cell for the user to add any code they want to the section.

    # create a jupyter notebook object
    report_notebook = nbformat.v4.new_notebook()
    print("Creating a new notebook")
    print("With the following sections:")
    # loop through the table of contents
    for section in table_of_contents:
        # get the section name
        section_name = section[0]
        # get the section level
        section_level = section[1]
        if section_level == 1:
            print(section_name)
        elif section_level == 2:
            print("\t" + section_name)
        elif section_level == 3:
            print("\t\t" + section_name)
        else:
            print("\t\t\t" + section_name)

    # create a markdown cell with the project name
    if '#' not in project_name:
        project_name = "# {ProjectName}\n**A project by {author}, prepared {date}**".format(
        ProjectName=project_name, author=author, date=date
    )
    else:
        project_name = project_name + "{ProjectName}\n**A project by {author}, prepared {date}**".format(ProjectName = project_name, author = author, date = date) # add the project name to the markdown cell
    # add the markdown cell to the notebook
    # add the project name markdown cell to the notebook
    project_name_cell = nbformat.v4.new_markdown_cell(project_name)
    # add the markdown cell to the report notebook
    report_notebook.cells.append(project_name_cell)

    # create a markdown cell with the table of contents
    # table_of_contents_cell = nbformat.v4.new_markdown_cell("# Table of Contents")
    # add the markdown cell to the report notebook
    # report_notebook.cells.append(table_of_contents_cell)

    # create a markdown cell for the Introduction (with the text from the readme.md file for the Introduction)
    # add a code cell below this markdown cell for the user to add any code they want to the Introduction.
    # get the list of sections from the table of contents that are level 1 sections
    list_of_sections = [section for section in table_of_contents if section[1] == 1]
    # get the section name for the Introduction
    introduction_section_name = list_of_sections[0][0]
    # create a markdown cell with the section name
    introduction_section_name_cell = nbformat.v4.new_markdown_cell(
        introduction_section_name
    )
    # add the markdown cell to the report notebook
    report_notebook.cells.append(introduction_section_name_cell)

    # for each section in the table of contents add the pattern of cells to the report notebook
    for section in table_of_contents:
        # get the section name and section level
        section_name = section[0]
        section_level = section[1]
        print(
            f'Adding section "{section_name}" to the notebook with section level {section_level}'
        )
        # create a markdown cell with the section name
        # add the markdown cell to the report notebook
        if '#' not in section_name:
            section_name = "#" * section_level + " " + section_name
        else:
            pass # add the section name to the markdown cell
        section_name_cell = nbformat.v4.new_markdown_cell(section_name)
        print(
            f'Adding markdown cell with section name "{section_name}" to the notebook'
        )
        report_notebook.cells.append(section_name_cell)
        # create a markdown cell with the text from the readme.md file for that section

        section_text = get_text(section_name, readme_text)

        section_text_cell = nbformat.v4.new_markdown_cell(section_text)
        print(
            f"Adding {len(section_text)} characters of text to the notebook in a markdown cell"
        )

        # add the markdown cell to the report notebook
        report_notebook.cells.append(section_text_cell)
        # add a code cell below this markdown cell for the user to add any code they want to the section.
        code_cell = nbformat.v4.new_code_cell("")
        print(f"Adding code cell to the notebook")
        # add the code cell to the report notebook
        report_notebook.cells.append(code_cell)

    # write the report notebook to a file
    # if the file already exists, overwrite it, otherwise create a new file
    proj = str(project_name.replace(" ","_").lower().strip())
    # only keep the first 10 characters of the project name and take out any non-alphanumeric characters
    # find the first line break in the project name
    first_line_break = proj.find("\n") # get the index of the first line break
    # only keep the characters before the first line break that are alphanumeric
    proj = "".join([char for char in proj[:first_line_break] if char.isalnum()])
    # keep either the first 40 characters or the whole project name, whichever is shorter
    proj = proj[:40]
    report_path = os.getcwd() + f"/notebooks/{proj}_generated_report.ipynb"
    if os.path.exists(report_path):
        os.remove(report_path)
        print("Overwriting existing report notebook")
        print("Report notebook path: " + report_path)
    with open(report_path, "w") as f:
        nbformat.write(report_notebook, f)


process_flow_controller()
