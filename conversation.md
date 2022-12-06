Graham Waters
Hey Assistant, I have a code question.

Sure, I'll do my best to help. What's your question?




Graham Waters
Let me share the details of my project with you.

Project Name: The Clark Kent Reporter
Project Purpose: Transform markdown documents that contain code blocks and commentary into fully functional Jupyter Notebook reports.

What does The Clark Kent Reporter do?
This tool converts a traditionally formatted overview (in a readme file) into a populated Jupyter Notebook for data science presentations or findings presentations. It doesn't magically transform your work from a document to a presentation, which will still require the careful work that data scientists and analysts are known for. However, it does make sure you don't have to start from scratch when making an interactive and working notebook out of something that would otherwise take hours manually write everything out again. I realized how many readmes I would be reading if I did it the old-fashioned way.

Example Use Case
Let's say I have a project that generates lorebooks for NovelAI project I can use this this tool to generate my overview notebook for the project as follows:

The Files
The readme file for NovelAI Lorebook Generator README.md.
The MOCKUP_README.md file in the root directory of this repository.
The Steps
Currently I open the readme file in a text editor and copy the text.
Then I paste the text into the MOCKUP_README.md file in the root directory of this repository.
Then I open Clark Kent Reporter in Visual Studio Code and run the script.
The destination and source files are set in the main.py file. You can change them to whatever you want.
The script will generate a notebook file in the destination directory. In this case, it will be in the notebooks directory. The file will be named generated_notebook.ipynb. If this is not the case for you, please open an issue and I will look into it.

2 / 2


Based on your description, it sounds like The Clark Kent Reporter is a tool that converts markdown files into Jupyter Notebook files. It does this by taking the text from a markdown file (such as a README file) and pasting it into a MOCKUP_README file in the root directory of the repository. From there, the main.py file in Clark Kent Reporter is run, which generates a Jupyter Notebook file in the specified destination directory. Is that correct?




Graham Waters
Yes, but the user pastes the text from their readme file into the MOCKUP_README file in this project.

Ah, I see. So the user pastes the text from their own readme file into the MOCKUP_README file in the Clark Kent Reporter project, and then runs the main.py script to generate the Jupyter Notebook file. That makes sense. Is there anything else you need help with?



Graham Waters
import os
import pandas as pd
import nbformat
import re
import datetime as dt
import configparser

# user-defined variables
project_name = "my_project"  # get this from the first <h1> tag in the readme.md file or the first markdown header with only one # symbol in the readme.md file
author = "Graham Waters"
license_text = "MIT License"

# functionality flags
generate_python_script_flag = (
    True  # generate a python script from the code blocks in the readme.md file
)
execute_in_background_flag = True  # dynamically update the .py file when the readme file is saved at the absolute path specified by readme_file_path
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
readme_text = ""  # initially the file is empty

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
        comment_text = readme_text[comment_start : comment_end + 3]
        # remove the comment text from the readme.md file
        readme_text = readme_text.replace(comment_text, "")
        # find the next comment
        comment_start = readme_text.find("<!--")
        # find the end of the comment
        comment_end = readme_text.find("-->")
        print(comment_text[0:10], "..", comment_text[-10:])
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
    readme_text = remove_markdown_comments(
        readme_text
    )  # this function modifies the global variable readme_text

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


def startup(path=path):
    global readme_text
    # read the readme.md file
    with open(path, "r") as f:
        readme_text = f.read()

    # parse the table of contents
    table_of_contents = parse_table_of_contents(readme_text)
    return table_of_contents, readme_text


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
    header_pattern = r"\n\|\s"
    #
    # Now... for the special block body text...
    # if you see a \n followed by a | character you are in a new row of a table and you need to keep capturing text
    body_pattern = r"\n\|(.*?)\|\n\n"
    # keep going until you see text followed by a | character followed by a \n character followed by a \n character and then stop. The text between where you started and where you stopped is the special block body text.
    # end_pattern = r'\|\n\n'

    # find the first match for the header pattern
    header_match = re.search(header_pattern, text)  # this is a string
    # find the index of the first match for the header pattern
    header_match_index = header_match.start()  # this is an integer
    # find the first match for the body pattern after the header pattern
    body_match = re.search(body_pattern, text[header_match_index:])  # this is a string
    # find the index of the first match for the body pattern after the header pattern
    body_match_index = body_match.start() + header_match_index  # this is an integer
    # get the special block header text
    # with start and end
    special_block_header_text = text[header_match_index:body_match_index]
    # get the special block body text
    special_block_body_text = text[body_match_index:]

    # add the special block header text to the body text separated by a newline
    special_block_text = special_block_header_text + "\n" + special_block_body_text

    # return the special block header text and the special block body text
    return special_block_text


# #!deprecated
# def preserve_code(md_text):
#     # format the code blocks in the markdown text so they look the same as they do in the readme.md file, in a jupyter notebook markdown cell. Do this by adding the ``` characters to the beginning and end of the code block. Also, the code blocks are indented by 4 spaces, and could be indented by 2 spaces. We want to preserve that indentation. We want to reproduce any code blocks from the readme accurately in the destination notebook file so we need to add an extra new line before and after the code block. We also want to preserve the code blocks in the markdown text so we can use them in the destination notebook file.

#     # find the index of the first instance of a code block in the markdown text
#     first_code_block_index = md_text.find('```\n')
#     # find the index of the last instance of a code block in the markdown text
#     last_code_block_index = md_text.rfind('```\n')
#     # find the index of the first character after the last code block in the markdown text
#     first_char_after_last_code_block_index = last_code_block_index + 4

#     # get the text before the first code block
#     text_before_first_code_block = md_text[:first_code_block_index]
#     # get the text after the last code block
#     text_after_last_code_block = md_text[first_char_after_last_code_block_index:]

#     # get the text between the first and last code blocks
#     text_between_first_and_last_code_blocks = md_text[first_code_block_index:first_char_after_last_code_block_index]
#     # split the text between the first and last code blocks by the newline character
#     text_between_first_and_last_code_blocks_split = text_between_first_and_last_code_blocks.split('\n')
#     # remove the first and last elements from the list, which are the ``` characters
#     text_between_first_and_last_code_blocks_split = text_between_first_and_last_code_blocks_split[1:-1]

#     # create a new list to store the text that will be put into the notebook markdown cell
#     new_text_between_first_and_last_code_blocks_split = []

#     # iterate through the text between the first and last code blocks, splitting each line by the spaces at the beginning of the line
#     for line in text_between_first_and_last_code_blocks_split:
#         line_split = line.split('    ')
#         # if the line is indented by 4 spaces, add 2 spaces to the beginning of the line
#         if len(line_split) > 1:
#             new_text_between_first_and_last_code_blocks_split.append('  ' + line_split[1])
#         # if the line is indented by 2 spaces, add 2 spaces to the beginning of the line
#         elif len(line_split) == 1:
#             new_text_between_first_and_last_code_blocks_split.append('  ' + line_split[0])

#     # add the ``` characters to the beginning and end of the code block
#     new_text_between_first_and_last_code_blocks_split = ['```'] + new_text_between_first_and_last_code_blocks_split + ['```']

#     # join the list of lines in the code block with the newline character
#     new_text_between_first_and_last_code_blocks = '\n'.join(new_text_between_first_and_last_code_blocks_split)

#     # join the text before the first code block, the new text between the first and last code blocks, and the text after the last code block
#     new_md_text = text_before_first_code_block + new_text_between_first_and_last_code_blocks + text_after_last_code_block

#     return new_md_text


# #!deprecated
# def get_code_block_from_text(text):
#     # find the index of the first instance of a code block in the markdown text
#     first_code_block_index = text.find('```\n')
#     # find the index of the last instance of a code block in the markdown text
#     last_code_block_index = text.rfind('```\n')
#     # find the index of the first character after the last code block in the markdown text
#     first_char_after_last_code_block_index = last_code_block_index + 4

#     # get the text between the first and last code blocks
#     text_between_first_and_last_code_blocks = text[first_code_block_index:first_char_after_last_code_block_index]
#     # split the text between the first and last code blocks by the newline character
#     text_between_first_and_last_code_blocks_split = text_between_first_and_last_code_blocks.split('\n')
#     # remove the first and last elements from the list, which are the ``` characters
#     text_between_first_and_last_code_blocks_split = text_between_first_and_last_code_blocks_split[1:-1]

#     # create a new list to store the text that will be put into the notebook markdown cell
#     new_text_between_first_and_last_code_blocks_split = []

#     # iterate through the text between the first and last code blocks, splitting each line by the spaces at the beginning of the line
#     for line in text_between_first_and_last_code_blocks_split:
#         line_split = line.split('    ')
#         # if the line is indented by 4 spaces, add 2 spaces to the beginning of the line
#         if len(line_split) > 1:
#             new_text_between_first_and_last_code_blocks_split.append('  ' + line_split[1])
#         # if the line is indented by 2 spaces, add 2 spaces to the beginning of the line
#         elif len(line_split) == 1:
#             new_text_between_first_and_last_code_blocks_split.append('  ' + line_split[0])

#     # add the ``` characters to the beginning and end of the code block
#     new_text_between_first_and_last_code_blocks_split = ['```'] + new_text_between_first_and_last_code_blocks_split + ['```']

#     # join the list of lines in the code block with the newline character
#     new_text_between_first_and_last_code_blocks = '\n'.join(new_text_between_first_and_last_code_blocks_split)

#     return new_text_between_first_and_last_code_blocks

# #!deprecated
# def get_any_code_or_block(text):
#     # just extract anything between ``` and ``` and return the list of paragraphs
#     key_phrase = '```'
#     code_blocks = []
#     while key_phrase in text: # while there are still code blocks in the text
#         start_index = text.find(key_phrase) # find the index of the first instance of the key phrase
#         end_index = text.find(key_phrase, start_index + 1) # find the index of the second instance of the key phrase
#         code_blocks.append(text[start_index:end_index + 3]) # add the code block to the list of code blocks
#         text = text[end_index + 3:] # remove the code block from the text
#     return code_blocks

# ^Testing
def extract_python(markdown_text):
    # pull out the code from the text
    code_pattern = r"```python(.*?)```\n"
    code_blocks = re.findall(code_pattern, markdown_text, re.DOTALL)
    # remove the ```python and ``` from the code blocks while keeping the indendation and newlines
    code_blocks = [re.sub(r"```python\n", "", code_block) for code_block in code_blocks]
    code_blocks = [re.sub(r"\n```", "", code_block) for code_block in code_blocks]
    code_string = "\n\n".join(
        code_blocks
    )  # join the code blocks together with two newlines between each block of code
    return code_string


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
        markdown_text = remove_markdown_comments(
            markdown_text
        )  # this function removes any commented code from the readme.md file

        # find the special blocks in the text and return them as a list of strings (each string is a special block of text)
        #!special_blocks = get_special_blocks_from_text(markdown_text)
        #!print("length of special blocks: ", len(special_blocks))
        #!print("special blocks: ", special_blocks)

        # we want to preserve the tables that we find and reproduce them in the report notebook as they are formatted in the readme.md file. Find any in this section and save it to the section text variable.
        # take the tables out of the markdown text and put them in a list, preserving the order of the tables in the markdown text

        # if the cell contains code then return the code block instead of the text
        # code_language_flags = ['```python','```c++','```c','```java','```javascript','```html','```css','```bash','```sql','```r','```swift','```go','```php','```ruby','```julia','```kotlin','```scala','```rust','```haskell','```perl','```lua','```matlab','```fortran','```cobol','```d','```dart','```groovy','```objectivec','```pascal','```powershell','```prolog','```racket','```scheme','```typescript','```verilog','```vhdl']

        # if any(flag in markdown_text for flag in code_language_flags):
        #     # get the code block from the markdown text
        #     if markdown_text.count('```') == 2:
        #         text_before_code = markdown_text.split('```')[0]
        #         text_after_code = markdown_text.split('```')[-1]

        #     code_block = get_code_block_from_text(markdown_text)
        #     # return the code block
        #     full_block = text_before_code + '\n\n' + code_block + '\n\n' + text_after_code

        #     return full_block # this is a string of text

        # this list of tables should be a list of tuples, each tuple is a table and the first element of the tuple is the table text and the second element is the table location in the markdown text
        # the table location is the index of the table in the markdown text
        # the table text is the text of the table in the markdown text
        # tables = re.findall(table_pattern, markdown_text) # this is a list of tuples, each tuple is a table and the first element of the tuple is the table text and the second element is the table location in the markdown text

        # # remove the tables from the markdown text
        # markdown_text = re.sub(table_pattern, "", markdown_text)

        # step 1: find the line that starts with the section name
        pattern = (
            r"^" + section_name + r".*?$"
        )  # the ^ symbol means the start of the line, the $ symbol means the end of the line, the .*? means any number of any characters
        section_name_line = re.findall(pattern, markdown_text, re.MULTILINE)[
            0
        ]  # this is a string of text containing the section name
        # step 2: find the line number of that line
        section_name_line_number = markdown_text.split("\n").index(section_name_line)
        # step 3: find the next line that starts with a "#" symbol
        lines = markdown_text.split("\n")
        # find the line numbers of the lines that start with a "#" symbol
        section_header_line_numbers = [
            i for i, line in enumerate(lines) if line.startswith("#")
        ]
        # find the line numbers of the lines that start with a "#" symbol that are after the line that starts with the section name
        section_header_line_numbers = [
            i for i in section_header_line_numbers if i > section_name_line_number
        ]
        # find the line number of the next line that starts with a "#" symbol
        next_section_header_line_number = section_header_line_numbers[0]

        # add the tables back into the markdown text
        # markdown_text = markdown_text.split("\n") # split the markdown text into lines
        # for table in tables:
        #     markdown_text.insert(table[1], table[0])
        # markdown_text = "\n".join(markdown_text) # join the markdown text back into a string

        # markdown_text = " ".join(markdown_text) # this is a string of text with the tables in it
        # step 4: get the text between those two lines while keeping the newlines in the text
        markdown_text = " ".join(
            lines[section_name_line_number + 1 : next_section_header_line_number]
        )
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
        bullet_points = [
            bullet_point.replace(bullet_point, "    " + bullet_point)
            for bullet_point in bullet_points
        ]

        # replace the bullet points in the markdown text with the new bullet points
        for bullet_point in bullet_points:
            markdown_text = markdown_text.replace(bullet_point.strip(), bullet_point)

        # code blocks

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
                bullet_point, bullet_point.replace(" ", " ")
            )  # replace the space with a non-breaking space so that the markdown text looks the same as the readme.md file. The non-breaking space is a special character that looks like a space but it is not a space. It is a special character that tells the markdown renderer to render the space as a space. The markdown renderer will not render a space as a space if it is followed by a newline character. So we need to replace the space with a non-breaking space so that the markdown renderer will render the space as a space.

        markdown_text = (
            "\n" + markdown_text
        )  # add a newline character to the beginning of the markdown text so that the markdown text looks the same as the readme.md file. The readme.md file has a newline character at the beginning of the text for each section.
        # add  to the end of the text
        markdown_text = (
            markdown_text + "\n"
        )  # add a newline character to the end of the markdown text so that the markdown text looks the same as the readme.md file. The readme.md file has a newline character at the end of the text for each section. This is important because the markdown renderer will not render a newline character at the end of the text.
    except Exception as e:
        markdown_text = "\n\nSection Text Not Found\n\n"
        print(e)

    # the tables have this  | |  in them replace with  |\n|
    markdown_text = markdown_text.replace("| |", "|\n|")

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
    if "#" not in project_name:
        project_name = (
            "# {ProjectName}\n**A project by {author}, prepared {date}**".format(
                ProjectName=project_name, author=author, date=date
            )
        )
    else:
        project_name = (
            project_name
            + "{ProjectName}\n**A project by {author}, prepared {date}**".format(
                ProjectName=project_name, author=author, date=date
            )
        )  # add the project name to the markdown cell
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
        if "#" not in section_name:
            section_name = "#" * section_level + " " + section_name
        else:
            pass  # add the section name to the markdown cell
        section_name_cell = nbformat.v4.new_markdown_cell(section_name)
        print(
            f'Adding markdown cell with section name "{section_name}" to the notebook'
        )
        report_notebook.cells.append(section_name_cell)
        # create a markdown cell with the text from the readme.md file for that section

        section_text = get_text(section_name, readme_text)

        # preserving code blocks
        # section_text = preserve_code(section_text) #note: the deprecated functions might work...  this could have been the issue.

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
    proj = str(project_name.replace(" ", "_").lower().strip())
    # only keep the first 10 characters of the project name and take out any non-alphanumeric characters
    # find the first line break in the project name
    first_line_break = proj.find("\n")  # get the index of the first line break
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


def generate_report_py_file():
    proj = str(project_name.replace(" ", "_").lower().strip())
    first_line_break = proj.find("\n")  # get the index of the first line break
    proj = "".join([char for char in proj[:first_line_break] if char.isalnum()])
    proj = proj[:40]
    report_path = os.getcwd() + f"/notebooks/{proj}_generated_report.ipynb"
    if generate_python_script_flag:
        # save the python code to another file (a python script)
        # if the file already exists, overwrite it, otherwise create a new file
        # the python script will be saved in the same folder as the report notebook
        report_path = os.getcwd() + f"/notebooks/{proj}_generated_report.py"
        if os.path.exists(report_path):
            os.remove(report_path)
            print("Overwriting existing report notebook")
            print("Report notebook path: " + report_path)

        # get the python code from the notebook
        python_code = extract_python(readme_text)
        # write the python code to a file
        with open(report_path, "w") as f:
            f.write(python_code)


def process_flow_controller(
    readme_path=path, py_path=scripts_path, ipynb_path=notebooks_path
):
    """
    process_flow_controller takes a string of text and returns a list of tuples
    _extended_summary_
    :param readme_path: a string of text that is the path to the readme.md file     , defaults to path
    :type readme_path: str, optional
    :param py_path: a string of text that is the path to the scripts folder, defaults to scripts_path
    :type py_path: str, optional
    :param ipynb_path: a string of text that is the path to the notebooks folder, defaults to notebooks_path
    :type ipynb_path: str, optional
    """
    # from start to finish, examine the readme and end with a populated, fully functional report jupyter notebook that can be tweaked and then presented to the end-user as the final report.
    global project_name
    (
        table_of_contents,
        readme_text,
    ) = startup()  # read the readme.md file and parse the table of contents

    # using the table of contents, create the sections of the report notebook
    generate_report_notebook(project_name, table_of_contents, readme_text)


def background_process_flow(readme_path=None, py_path=None):
    # what is the purpose of this function?
    # this function is a background process that will run in the background and will extract the python from the readme.md file (every 10  minutes) and save it to an updating python script at the specified script path (py_path). This allows the user to write in markdown and have it dynamically translated into python scripts they can deploy.
    """
    background_process_flow takes a string of text and returns a list of tuples. This function is a background process that will run in the background and will extract the python from the readme.md file (every 10  minutes) and save it to an updating python script at the specified script path (py_path). This allows the user to write in markdown and have it dynamically translated into python scripts they can deploy.
    :param readme_path: a string of text that is the path to the readme.md file     , defaults to path
    :type readme_path: str, optional
    :param py_path: a string of text that is the path to the scripts folder, defaults to scripts_path
    :type py_path: str, optional
    """
    global project_name
    (
        table_of_contents,
        readme_text,
    ) = startup()  # read the readme.md file and parse the table of contents

    # we are now going to extract the python code from the readme.md file and save it to a python script
    # the python script will be saved in the same folder as the report notebook

    # we will be using the function extract_python(readme_text)
    # this function will take the readme_text and extract the python code from it
    # the python code will be saved to a python script
    # the script is to be saved at the destination py_path (the path provided by the user in this function)
    # the script is to be named project_name_generated_report.py
    # if the file already exists, overwrite it, otherwise create a new file

    # flow
    # 1. extract the python code from the readme.md file
    # 2. save the python code to a python script
    # 3. save the python script to the destination py_path
    # 4. name the python script project_name_generated_report.py
    # 5. if the file already exists, overwrite it, otherwise create a new file

    # code
    readme_text_content = readme_text
    python_code = extract_python(readme_text_content)
    # save the python code to another file (a python script)
    # if the file already exists, overwrite it, otherwise create a new file
    # the python script will be saved in the same folder as the report notebook
    proj = str(project_name.replace(" ", "_").lower().strip())
    first_line_break = proj.find("\n")  # get the index of the first line break
    proj = "".join([char for char in proj[:first_line_break] if char.isalnum()])
    proj = proj[:40]
    script_path = py_path  # the path to the scripts file is provided by the user
    # save the python script to the destination py_path
    script_path = py_path + f"/{proj}_python_code.py"
    if os.path.exists(script_path):
        os.remove(script_path)
        print("rewriting existing python script")
        print("python script path: " + script_path)
    with open(script_path, "w") as f:
        f.write(python_code)

    # write the python code to a file

    return


import time

# ^ Run the .py generation in the background so that the user can continue to use the notebook while the report is being generated or updated in the background.
if execute_in_background_flag:
    absolute_path_to_readme = "/Volumes/Backups of Grahams IMAC/PythonProjects/Reddit-NLP-Analysis/README.md"  # note: could be dynamically generated from the user's input
    absolute_path_to_pyfilefolder = "/Volumes/Backups of Grahams IMAC/PythonProjects/Reddit-NLP-Analysis/scripts"  # note: could be dynamically generated from the user's input

    while True:  # until user stops the process
        print("running background process")
        background_process_flow(absolute_path_to_readme, absolute_path_to_pyfilefolder)
        print("sleeping for 5 minutes")
        time.sleep(300)
else:
    process_flow_controller()  # run with the default settings

It looks like this script is defining a number of variables, including project_name, author, and license_text, and then reading a configuration file to get the values for path, scripts_path, and notebooks_path. It then defines a number of global variables, including date and readme_text, which are initially empty.

After that, it defines a function called remove_markdown_comments that takes a string of text (presumably the contents of a markdown file) as input and removes any markdown comments from that text. It then returns the resulting text.

It also looks like there is a function called generate_jupyter_notebook that is not yet defined, but is used later on in the script. This function apparently takes a table of contents from a markdown file and generates a Jupyter Notebook based on that table of contents.

Is there anything specific you would like help with?




Graham Waters
write me a pythons script that Transform markdown documents that contain code blocks and commentary into fully functional Jupyter Notebook reports.

Here is a possible Python script that you could use to transform markdown documents that contain code blocks and commentary into Jupyter Notebook reports:

Copy code
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
    # Read the markdown file
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
    for file_name in



Graham Waters
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

#####

That is what we have so far. What does the code do?

2 / 2


This script defines a custom preprocessor called CodeBlockPreprocessor that converts markdown cells in a Jupyter Notebook that contain code blocks into markdown cells with the code blocks rendered as code outputs.

It also defines a function called markdown_to_notebook that takes a path to a markdown file and a path to a Jupyter Notebook file as input, and converts the markdown file into a Jupyter Notebook file. It does this by reading the markdown file, creating a Jupyter Notebook with the markdown text, preprocessing the notebook to convert markdown cells with code blocks into code cells, executing the code cells, and then saving the executed notebook to the specified file path.

This script also contains a commented-out function called convert_directory that is not yet implemented. This function would be used to convert all markdown files in a specified input directory into Jupyter Notebooks and save them to a specified output directory.




Graham Waters
What should we do next?

To complete the script, you could implement the convert_directory function as follows:

Copy code
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
With this function implemented, you could use the script to convert all markdown files in a specified input directory into Jupyter Notebooks and save them to a specified output directory. For example, you could use the following code to convert all markdown files in the "markdown" directory to Jupyter Notebooks and save them to the "notebooks" directory:

Copy code
convert_directory("markdown", "notebooks")
You




Graham Waters
I believe you have to use this format ```python convert_directory("../markdown_docs", "../generated_notebooks")```

Yes, you are correct. In order to use the convert_directory function to convert all markdown files in the "markdown_docs" directory to Jupyter Notebooks and save them to the "generated_notebooks" directory, you would need to use the following code:

Copy code
convert_directory("../markdown_docs", "../generated_notebooks")
This code assumes that the "markdown_docs" directory is located in the parent directory of the script, and that the "generated_notebooks" directory is also located in the parent directory of the script.

You could also specify absolute paths to the input and output directories, like this:

Copy code
convert_directory("/home/user/markdown_docs", "/home/user/generated_notebooks")
This code will convert all markdown files in the "/home/user/markdown_docs" directory to Jupyter Notebooks and save them to the "/home/user/generated_notebooks" directory. You can specify any valid path to the input and output directories on your system.




Graham Waters
Where did we define ExecutePreprocessor?

2 / 2


The ExecutePreprocessor class is defined in the nbconvert.preprocessors.execute module, which is a part of the nbconvert package. In order to use the ExecutePreprocessor class, you need to import it from this module, like this:

Copy code
from nbconvert.preprocessors.execute import ExecutePreprocessor
After importing this class, you can create an instance of ExecutePreprocessor and use it to execute the code cells in a Jupyter Notebook, like this:

Copy code
ep = ExecutePreprocessor(timeout=600, kernel_name="python3")
ep.preprocess(notebook, {})
In this code, we create an instance of ExecutePreprocessor with a timeout of 600 seconds and a kernel name of "python3". We then call the preprocess method on this instance to execute the code cells in the notebook object. This method takes the notebook and a dictionary of resources as input, and returns the preprocessed notebook and the updated resources.

You can learn more about the ExecutePreprocessor class and the preprocess method in the nbconvert documentation:

https://nbconvert.readthedocs.io/en/latest/api/preprocessors.html#nbconvert.preprocessors.ExecutePreprocessor

https://nbconvert.readthedocs.io/en/latest/api/preprocessors.html#nbconvert.preprocessors.Preprocessor.preprocess




Graham Waters
oh! thank you, I forgot to ask, what imports should I include for these code blocks?

In order to use the code blocks that I provided, you will need to import the following modules:

Copy code
import os
import re
import nbformat
from nbconvert import MarkdownExporter
from nbconvert.preprocessors.execute import ExecutePreprocessor
The os module provides functions for interacting with the operating system, such as functions for working with files and directories. The re module provides functions for working with regular expressions, which are used to search for code blocks in markdown cells. The nbformat module provides functions for working with Jupyter Notebooks. The MarkdownExporter class is part of the nbconvert package, and is used to convert Jupyter Notebooks to markdown. The ExecutePreprocessor class is also part of the nbconvert package, and is used to execute the code cells in a Jupyter Notebook.

You can learn more about these modules and classes in the Python documentation and the nbconvert documentation:

https://docs.python.org/3/library/os.html

https://docs.python.org/3/library/re.html

https://nbformat.readthedocs.io/en/latest/

https://nbconvert.readthedocs.io/en/latest/

https://nbconvert.readthedocs.io/en/latest/api/exporters.html#nbconvert.exporters.MarkdownExporter

https://nbconvert.readthedocs.io/en/latest/api/preprocessors.html#nbconvert.preprocessors.ExecutePreprocessor




Graham Waters
rewrite markdown_to_notebook and include alivebar progress bars on every for loop please.

Here is a modified version of the markdown_to_notebook function that includes alivebar progress bars on every for loop:

Copy code
import os
import re
import alive_progress
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
    with open(markdown_file_path) as f:
        markdown_text = f.read()

    # Create a Jupyter Notebook with the markdown text
    notebook = nbformat.v4.new_notebook(markdown=markdown_text)

    # Create an exporter that converts Jupyter Notebooks to markdown
    exporter = MarkdownExporter()

    # Preprocess the notebook to convert markdown cells with code blocks
    # into markdown cells with the code blocks rendered as code outputs
    with alive_progress.bar(nb.cells) as bar:
        for cell in nb.cells:
            notebook, _ = CodeBlockPreprocessor().preprocess(notebook, {})
            bar()

    # Export the preprocessed notebook to markdown
    with alive_progress.bar(notebook) as bar:
        markdown_text, _ = exporter.from_notebook_node(notebook)
        bar()

    # Create a Jupyter Notebook with the preprocessed markdown text
    notebook = nbformat.v4.new_notebook(markdown=markdown_text)





Graham Waters
can you also do that for the convert directory function?

Sure, here is a modified version of the convert_directory function that includes alivebar progress bars on every for loop:

Copy code
import os
from alive_progress import alive_bar

# Define a function that converts all markdown files in a directory into Jupyter Notebooks
def convert_directory(markdown_dir_path, notebook_dir_path):
    # Create the notebook directory if it doesn't exist
    if not os.path.exists(notebook_dir_path):
        os.makedirs(notebook_dir_path)

    # Iterate over all files in the markdown directory
    markdown_file_paths = [
        os.path.join(markdown_dir_path, f) for f in os.listdir(markdown_dir_path) if f.endswith(".md")
    ]
    with alive_progress.filling_squares(len(markdown_file_paths), bar="classic", spinner="dots") as bar:
        for markdown_file_path in markdown_file_paths:
            # Convert the markdown file into a Jupyter Notebook
            notebook_file_name = os.path.splitext(os.path.basename(markdown_file_path))[0] + ".ipynb"
            notebook_file_path = os.path.join(notebook_dir_path, notebook_file_name)
            markdown_to_notebook(markdown_file_path, notebook_file_path)
            bar()
The alive_bar function is used to create a progress bar that shows the progress of the for loop that iterates over the files in the markdown directory. This allows the user to see how far the function has progressed and how much longer it will take to complete. You can learn more about alivebar and its various options in the alivebar documentation:

https://pypi.org/project/alive-progress/

https://pypi.org/project/alive-progress/#progress-bars




Graham Waters
alive progress has no attribute "filling squares"

You're right, I made a mistake. The correct syntax for creating a progress bar with alivebar is with alive_progress.bar(...) as bar:. Here is the correct version of the convert_directory function:

Copy code
import os
from alive_progress import alive_bar

# Define a function that converts all markdown files in a directory into Jupyter Notebooks
def convert_directory(markdown_dir_path, notebook_dir_path):
    # Create the notebook directory if it doesn't exist
    if not os.path.exists(notebook_dir_path):
        os.makedirs(notebook_dir_path)

    # Iterate over all files in the markdown directory
    markdown_file_paths = [
        os.path.join(markdown_dir_path, f) for f in os.listdir(markdown_dir_path) if f.endswith(".md")
    ]
    with alive_progress.bar(len(markdown_file_paths)) as bar:
        for markdown_file_path in markdown_file_paths:
            # Convert the markdown file into a Jupyter Notebook
            notebook_file_name = os.path.splitext(os.path.basename(markdown_file_path))[0] + ".ipynb"
            notebook_file_path = os.path.join(notebook_dir_path, notebook_file_name)
            markdown_to_notebook(markdown_file_path, notebook_file_path)
            bar()
You can customize the appearance of the progress bar by passing optional arguments to the alive_progress.bar function. For example, you can use the bar="classic" argument to specify that the progress bar should be a classic bar instead of a filling squares bar. You can learn more about the various customization options in the alivebar documentation:

https://pypi.org/project/alive-progress/#progress-bars




Try again

Free Research Preview: ChatGPT is optimized for dialogue. Our goal is to make AI systems more natural to interact with, and your feedback will help us improve our systems and make them safer.
Reset Thread
Light Mode
OpenAI Discord
Learn More
Log out


---

Open sidebar

Graham Waters
Hey

Hello! How can I help you today? Is there something on your mind you'd like to talk about? I'm here to listen and provide any help or advice I can.



Graham Waters
# OCD vs. Autism (A Reddit Thread NLP Analysis)
*A project by Graham Waters, 2022*

![banner](./images/1.png)

# Executive Summary

The end goal for our client is likely a more clinical application of classification to assist users seeking help on public forums by using psychoanalysis from text data; however, this is beyond the scope of our initial study. Instead, we hope that by learning how these subreddits present linguistically, we gain insight into the most predictive features that can serve as the first stepping stone toward such a clinical application in the future.

**Note**: This study is focused solely on linguistic features present in Reddit posts and is not a formal means of diagnosis for identifying autism-spectrum or obsessive-compulsive disorder.

---

# A Table of Contents
- [OCD vs. Autism (A Reddit Thread NLP Analysis)](#ocd-vs-autism-a-reddit-thread-nlp-analysis)
- [Executive Summary](#executive-summary)
- [A Table of Contents](#a-table-of-contents)
- [Methods](#methods)
  - [Data Collection](#data-collection)
    - [Reddit API](#reddit-api)
    - [Keywords](#keywords)
  - [Feature Engineering](#feature-engineering)
    - [Text Preprocessing](#text-preprocessing)
    - [Model Building](#model-building)
      - [Logistic Regression](#logistic-regression)
      - [Adaboost](#adaboost)
      - [Decision Tree](#decision-tree)
      - [Keyword Vectorizer](#keyword-vectorizer)
    - [Visualization](#visualization)
  - [Results](#results)
  - [References](#references)


---
# Methods
## Data Collection
### Reddit API
We collected data from the `r/Autism` and `r/OCD` subreddits using the Reddit API. We used the Python library `requests` to make requests to the API and parse the JSON response. The following code snippet shows the request and parsing steps.
```python
import requests
from bs4 import BeautifulSoup

url = 'https://www.reddit.com/r/Autism/'
headers = dict()
headers.update(dict(Accept='application/json', Authorization='Bearer <token>'))
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.content, "html.parser")
posts = soup.findAll('div', class_="listing-item-container")
```
The `BeautifulSoup` library was used to parse the HTML content of the page. We then iterated over the posts and extracted the post title, link, and body.
### Keywords
We also collected keywords from the posts. We did this by searching for the keyword in the post's text. If the keyword was found, we appended it to a list.
```python
def get_keywords(post):
    """Get the keywords from a post"""
    # Get the keywords from the post
    keywords = set()
    for word in re.split("\W+", post.text):
        if word in keywords:
            continue
        else:
            keywords.add(word)
    return keywords
```
## Feature Engineering
### Text Preprocessing
We preprocessed the text data by removing punctuation and lower casing the words. We also removed stop words and added them to the stop words list.
```python
stop_words = set(stopwords.words("english"))

# Remove Punctuation
def remove_punctuation(text):
    """Remove punctuation from a string"""
    return ''.join(ch for ch in text if ch not in stop_words)

# Lower Case
def lowercase(text):
    """Lower case a string"""
    return text.lower()
```
### Model Building
#### Logistic Regression
Logistic regression is a binary classification model that uses log odds as its output. In this study, we used the `scikit-learn` library to build a logistic regression model. The following code snippet shows how we built our model.
```python
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

lr = LogisticRegression(C=1e6)
lr.fit(df_ocd.drop(columns=('self_text', 'author'), axis=1), df_ocd.target)
accuracy = accuracy_score(lr.predict(df_ocd.drop(columns=('self_text', 'author'), axis=1)), df_ocd.target)
print(f'Accuracy: {accuracy}')
```
#### Adaboost
Adaboost is an ensemble learning algorithm that combines multiple weak learners into a strong learner. It is often used in conjunction with logistic regression. The following code snippet shows how we built our adaboost model.
```python
from sklearn.ensemble import AdaBoostClassifier
from sklearn.metrics import accuracy_score
adaboost = AdaBoostClassifier(n_estimators=100, random_state=0)
adaboost.fit(df_ocd.drop(columns=('self_text', 'author'), axis=1), df_ocd.target)
accuracy = accuracy_score(adaboost.predict(df_ocd.drop(columns=('self_text', 'author'), axis=1)), df_ocd.target)
print(f'Accuracy: {accuracy}')
```
#### Decision Tree
Decision trees are a type of tree-based machine learning algorithm that are commonly used in classification problems. They are useful because they are easy to understand and interpret. The following code snippet shows how we built our decision tree model.
```python
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
dt = DecisionTreeClassifier(random_state=0)
dt.fit(df_ocd.drop(columns=('self_text', 'author'), axis=1), df_ocd.target)
accuracy = accuracy_score(dt.predict(df_ocd.drop(columns=('self_text', 'author'), axis=1)), df_ocd.target)
print(f'Accuracy: {accuracy}')
```
#### Keyword Vectorizer
In order to extract features from the text data, we first need to tokenize the text. This can be done using the `sklearn` library's `CountVectorizer`. We then passed the tokens to the `TfidfTransformer` to generate tf-idsf vectors.
```python
from sklearn.feature_extraction.text import TfidfVectorizer
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(df_ocd.drop(columns=('self_text', 'author'), axis=1).astype(str))
tf_vocab = Counter().most_common(len(stop_words)+5)
for i in range(10):
    print(i, len(set(tokens)))
    for j, k in enumerate(tf_vocab):
        if k >= 5:
            break
        X_k = np.array(np.where(X == k))
        X_j = np.zeros((0, 0))
        for x in X_k:
            X_j += 1 * x
        X = np.vstack((X, X_j))
    print(i + 1, len(set(tokens)))
    for j, k in enumerate(tf_vocab):
        if k > 4:
            break
        X_k = np.array(np.where(X == k))
        X_j = np.zeros((0, 0))
        for x in X_k:
            X_j += 1 * x
        X = np.hstack((X, X_j))
        print(i + 2, len(set(tokens)))
```
### Visualization
After building the models, we plotted the results. For the logistic regression model, we created a bar plot showing the predicted probability of being OCD versus the actual value. The following code snippet shows how we generated the figure.
```python
plt.figure()
ax = plt.subplot(111)
x = df_ocd.target.values
y = lr.predict(x)
bar_width = .35
color_map = sns.light_palette("Greens", 10)
colors = color_map.as_hex()
labels = list(range(len(df_ocd.target.index)))
rects = ax.bar(labels, y, width=bar_width, label='Predicted Probability', edgecolor=None, align="center")
ax.legend(loc="best")
ax.set_yticks(np.arange(0, 1.05, .25))
ax.set_xticklabels(list(df_ocd.target.index))
ax.invert_yaxis()
ax.set_title("Logistic Regression Predictions")
fig = plt.gcf()
fig.tight_layout()
```
For the adaboost model, we used a confusion matrix to show the performance of the classifier. The following code snippet shows how we generated the figure.
```python
import numpy as np
from matplotlib import pyplot as plt
confusion_matrix = pd.crosstab(df_ocd.target, df_ocd.prediction)
cm = confusion_matrix(df_ocd.target, df_ocd.prediction)
num_classes = cm.sum(1).max()+1
class_names = list(range(num_classes))
row_positions = np.argsort(-df_ocd.target)
col_indices = np.argpartition(df_ocd.target, -df_ocd.target.size-1)
for row_number, col_name in zip(row_positions, class_names):
    fig = plt.figure()
    ax = plt.subplot(2, num_classes, row_number)
    cnt = conf_matrix.iloc.get_value(row_position=row_number, column_label=col_name)
    ax.barh(class_names, cnt)
    ax.set_ylabel(col_name)
    ax.set_xlim(0, num_classes)
    ax.set_xticks(np.arange(0, num_classes, 1))
    ax.grid()
    plt.savefig('images/logreg_confusion_matrix.png')
    plt.close()
```
Finally, for the decision tree model, we used a dendrogram to visualize the structure of the tree. The following code snippet shows how we generated the figure.
```python
# Plotting the Dendogram
from scipy.cluster.hierarchy import linkage
linkage_obj = linkage(distance_func=euclidean)
dendro = linkage_obj.apply(X)
plt.figure()
plt.show()
```
## Results
The final results are presented below.
<img src="/docs/assets/results.png" alt="Results">


## References
* Gedanke, J., & König, S. (2018). Mood profiles of autism and obsessive compulsive disorder subgroups on reddit. Retrieved from https://www.reddit.com/r/MoodProfiles/comments/8nqw7b/mood_profiles_of_autism_and_obsessive_compulsive/
* Hsu, C.-Y., Lin, Y.-H., Wang, P.-J., Chen, W.-C., Tsai, M.-L., Huang, L.-W., ... & Chiu, E. (2017). A survey on deep learning methods applied to natural language processing tasks. arXiv preprint arXiv:1704.01375.



------------

# Instructions

So, I want to extract the structure of this file and generate a report from it. Notice that there is an executive summary, a table of contents, and code blocks throughout.

The Report Notebook -
The final notebook should have the following structure:

I. Introduction (Executive Summary)
... for each section (marked by hashes and/or <div> tags) we need to extract the title for that section and add it as a title markdown cell. Then the text (noncode) of the cell goes in another markdown cell beneath the title. Any code blocks should be placed after the markdown cells and before the next section header.

This is a study on the differences between two mental health conditions, obsessive-compulsive disorder (OCD) and autism, as they are presented on the Reddit platform. The study uses natural language processing techniques to analyze posts from the r/OCD and r/Autism subreddits and identify linguistic features that can be used to distinguish between the two. The study is not intended to be a formal means of diagnosing either condition, but rather to provide insight into how these conditions are discussed on Reddit. The methods section describes the data collection, feature engineering, and model building processes used in the study. The results section presents the findings of the analysis, and the references section provides a list of sources used in the study.




Graham Waters
Correct, I want to take this markdown file and transform it into a Jupyter Notebook.

To convert this markdown file into a Jupyter Notebook, you will need to have Jupyter installed on your computer. Once you have Jupyter installed, you can open the command prompt or terminal and navigate to the directory where the markdown file is located. Then, run the following command:

jupyter nbconvert --to notebook [markdown_file_name].md

This will create a new Jupyter Notebook file with the same name as the markdown file, but with the .ipynb extension. You can then open the Jupyter Notebook file in Jupyter and view it.




Graham Waters

------------

# Instructions

So, I want to extract the structure of this file and generate a report from it. Notice that there is an executive summary, a table of contents, and code blocks throughout.

The Report Notebook -
The final notebook should have the following structure:

I. Introduction (Executive Summary)
... for each section (marked by hashes and/or <div> tags) we need to extract the title for that section and add it as a title markdown cell. Then the text (noncode) of the cell goes in another markdown cell beneath the title. Any code blocks should be placed after the markdown cells and before the next section header.

To extract the structure of this file and generate a report, you can use regular expressions to match the titles of each section and the code blocks in the file. You can then use these regular expressions to create a new Jupyter Notebook file with the desired structure, where each section title is represented as a markdown cell, followed by any text in the section as another markdown cell, and any code blocks as code cells.

Here is an example of how you might use regular expressions to extract the section titles and code blocks from the file:

Copy code
import re

# Read the file
with open('file.md') as f:
    text = f.read()

# Use regular expressions to extract the section titles
titles = re.findall(r'^# (.*)$', text, re.MULTILINE)

# Use regular expressions to extract the code blocks
code_blocks = re.findall(r'```(.+?)```', text, re.DOTALL)
Once you have the section titles and code blocks, you can use the Jupyter Notebook API to create a new notebook file with the desired structure. For example:

Copy code
from IPython.nbformat.v4 import new_notebook, new_markdown_cell, new_code_cell

# Create a new notebook
nb = new_notebook()

# Add the section titles as markdown cells
for title in titles:
    nb['cells'].append(new_markdown_cell(source=title))

# Add the text of each section as markdown cells
for section in sections:
    nb['cells'].append(new_markdown_cell(source=section))

# Add the code blocks as code cells
for code in code_blocks:
    nb['cells'].append(new_code_cell(source=code))

# Save the notebook
with open('report.ipynb', 'w') as f:
    f.write(nb.writes(4))
This will create a new Jupyter Notebook file called report.ipynb with the desired structure. You can then open the file in Jupyter to view it.



Graham Waters
/opt/anaconda3/lib/python3.9/site-packages/IPython/nbformat.py:12: ShimWarning: The `IPython.nbformat` package has been deprecated since IPython 4.0. You should import from nbformat instead.
  warn("The `IPython.nbformat` package has been deprecated since IPython 4.0. "---------------------------------------------------------------------------
NameError                                 Traceback (most recent call last)
/var/folders/34/d1tlq3k91hb0lj6x90xpzb4r0000gn/T/ipykernel_58143/686253140.py in <module>
      9
     10 # Add the text of each section as markdown cells
---> 11 for section in sections:
     12     nb['cells'].append(new_markdown_cell(source=section))
     13

NameError: name 'sections' is not defined

In the code you provided, there is a reference to a variable called sections, but it is not defined. This is causing the NameError exception to be raised. You can fix this error by defining the sections variable and assigning it a value before trying to iterate over it.

Here is an example of how you might do this:

Copy code
from IPython.nbformat.v4 import new_notebook, new_markdown_cell, new_code_cell

# Read the file
with open('file.md') as f:
    text = f.read()

# Use regular expressions to extract the section titles
titles = re.findall(r'^# (.*)$', text, re.MULTILINE)

# Use regular expressions to extract the sections (the text between the section titles)
sections = re.findall(r'^#.*\n([\s\S]*?)^#', text, re.MULTILINE)

# Use regular expressions to extract the code blocks
code_blocks = re.findall(r'```(.+?)```', text, re.DOTALL)

# Create a new notebook
nb = new_notebook()

# Add the section titles as markdown cells
for title in titles:
    nb['cells'].append(new_markdown_cell(source=title))

# Add the text of each section as markdown cells
for section in sections:
    nb['cells'].append(new_markdown_cell(source=section))

# Add the code blocks as code cells
for code in code_blocks:
    nb['cells'].append(new_code_cell(source=code))

# Save the notebook
with open('report.ipynb', 'w') as f:
    f.write(nb.writes(4))
This code defines the sections variable and uses regular expressions to extract the text between the section titles. It then adds the section titles as markdown cells, the section text as markdown cells, and the code blocks as code cells to the Jupyter Notebook file.




Graham Waters
what are my imports?

It looks like the code you provided is trying to import several modules from the IPython package, specifically new_notebook, new_markdown_cell, and new_code_cell. These are functions that are used to create new Jupyter Notebook files and add cells to them. Additionally, the code is importing the re module, which provides regular expression matching capabilities.

Here is a list of all the imports in the code you provided:

Copy code
from IPython.nbformat.v4 import new_notebook, new_markdown_cell, new_code_cell
import re
These imports should be at the top of the file, before any other code.




Graham Waters
The `IPython.nbformat` package has been deprecated since IPython 4.0. You should import from nbformat instead.

The IPython.nbformat package has been deprecated since IPython 4.0 and is no longer supported. Instead, you should use the nbformat package to create and manipulate Jupyter Notebook files. To fix this warning, you can update the imports in your code to use the nbformat package instead of the IPython.nbformat package.

Here is an example of how you might update your imports to use the nbformat package:

Copy code
from nbformat import v4 as nbf
import re
Once you have updated your imports, you can use the nbf module to create new notebook files and add cells to them. For example:

Copy code
# Create a new notebook
nb = nbf.new_notebook()

# Add the section titles as markdown cells
for title in titles:
    nb['cells'].append(nbf.new_markdown_cell(source=title))

# Add the text of each section as markdown cells
for section in sections:
    nb['cells'].append(nbf.new_markdown_cell(source=section))

# Add the code blocks as code cells
for code in code_blocks:
    nb['cells'].append(nbf.new_code_cell(source=code))
You can then save the notebook using the write method, as shown in the previous example.

Copy code
# Save the notebook
with open('report.ipynb', 'w') as f:
    f.write(nb.writes(4))



Graham Waters
# Save the notebook
with open('report.ipynb', 'w') as f:
    f.write(nb.writes(4))


this gives a keyerror because nb has no "writes"

You are correct, there is no writes method in the nbformat package. To write the Jupyter Notebook file to a file, you should use the write method instead.

Here is an example of how you might update your code to use the write method:

Copy code
# Save the notebook
with open('report.ipynb', 'w') as f:
    f.write(nbformat.write(nb, 4))
This code uses the write method to serialize the nb object (the Jupyter Notebook file) to a string and write it to the report.ipynb file. The 4 argument specifies the version of the Jupyter Notebook format to use when writing the file.

Alternatively, you can use the writes method to serialize the nb object to a string and then write it to the file, like this:

Copy code
# Save the notebook
with open('report.ipynb', 'w') as f:
    f.write(nbformat.writes(nb, 4))
This is equivalent to using the write method, but it uses the writes method to serialize the nb object to a string first. Either way, the result should be the same.




Graham Waters
could I use

# Save the notebook
with open('report.ipynb', 'w') as f:
    nbf.write(nb, f)

Yes, you can use the write method in this way to write the Jupyter Notebook file to a file. The write method takes two arguments: the nb object (the Jupyter Notebook file) and the file object to write to.

Here is an example of how you might use the write method in this way:

Copy code
# Save the notebook
with open('report.ipynb', 'w') as f:
    nbf.write(nb, f)
This code opens the report.ipynb file in write mode, then uses the write method to write the nb object (the Jupyter Notebook file) to the file. This is equivalent to using the writes method to serialize the nb object to a string and then writing the string to the file, as shown in the previous examples.

Regardless of which method you use, the result should be the same: a new Jupyter Notebook file will be created with the structure and content of the original markdown file.




Graham Waters
Still getting this error, "AttributeError: module 'nbformat.v4' has no attribute 'write'"

It looks like you are trying to use the write method from the nbformat.v4 module, but this module does not have a write method. The nbformat package does not have a v4 submodule, so you cannot use the .v4 suffix when importing the package.

To fix this error, you can update your imports to remove the .v4 suffix, like this:

Copy code
import nbformat
import re
This will import the nbformat package and the re module without the .v4 suffix. You can then use the nbformat package to create new Jupyter Notebook files and add cells to them, as shown in the previous examples.

Once you have updated your imports, you can use the write method from the nbformat package, like this:

Copy code
# Save the notebook
with open('report.ipynb', 'w') as f:
    nbformat.write(nb, f)
This code will use the write method to write the nb object (the Jupyter Notebook file) to the report.ipynb file. This should fix the AttributeError you are seeing.




Graham Waters
how does that impact the other parts of the code?

like this one:

# Create a new notebook
nb = nbf.new_notebook()

# Add the section titles as markdown cells
for title in titles:
    nb['cells'].append(nbf.new_markdown_cell(source=title))

# Add the text of each section as markdown cells
for section in sections:
    nb['cells'].append(nbf.new_markdown_cell(source=section))

# Add the code blocks as code cells
for code in code_blocks:
    nb['cells'].append(nbf.new_code_cell(source=code))


Save & Submit
Cancel

1 / 2

Removing the .v4 suffix from the nbformat import will not have any impact on the other parts of the code. The nbformat package provides a consistent interface for working with Jupyter Notebook files, regardless of the version of the Jupyter Notebook format that is being used.

Here is an example of how the code might look after updating the imports:

Copy code
import nbformat
import re

# Read the file
with open('file.md') as f:
    text = f.read()

# Use regular expressions to extract the section titles
titles = re.findall(r'^# (.*)$', text, re.MULTILINE)

# Use regular expressions to extract the sections (the text between the section titles)
sections = re.findall(r'^#.*\n([\s\S]*?)^#', text, re.MULTILINE)

# Use regular expressions to extract the code blocks
code_blocks = re.findall(r'```(.+?)```', text, re.DOTALL)

# Create a new notebook
nb = nbformat.new_notebook()

# Add the section titles as markdown cells
for title in titles:
    nb['cells'].append(nbf.new_markdown_cell(source=title))

# Add the text of each section as markdown cells
for section in sections:
    nb['cells'].append(nbf.new_markdown_cell(source=section))

# Add the code blocks as code cells
for code in code_blocks:
    nb['cells'].append(nbf.new_code_cell(source=code))

# Save the notebook
with open('report.ipynb', 'w') as f:
    nbformat.write(nb, f)
As you can see, removing the .v4 suffix from the nbformat import does not impact any other part of the code. The nbformat package provides the same functions and methods regardless of which version of the Jupyter Notebook format is being used.




Graham Waters
import nbformat
import re

# Read the file
with open('file.md') as f:
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
    nb['cells'].append(nbf.new_markdown_cell(source=title))

# Add the text of each section as markdown cells
for section in sections:
    nb['cells'].append(nbf.new_markdown_cell(source=section))

# Add the code blocks as code cells
for code in code_blocks:
    nb['cells'].append(nbf.new_code_cell(source=code))

# Save the notebook
with open('report.ipynb', 'w') as f:
    nbformat.write(nb, f)

---
this works

3 / 3


​



·
Free Research Preview: ChatGPT is optimized for dialogue. Our goal is to make AI systems more natural to interact with, and your feedback will help us improve our systems and make them safer.
