import os
import pandas as pd
import os
import nbformat
import re
import datetime as dt
import configparser

# user-defined variables
project_name = "Project Name"
author = "Graham Waters"
license_text = "MIT License"

# flags
html_enabled = False  # note: enable the html_enabled flag to enable the html header detection (once it is working)

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

    # first some house cleaning
    readme_text = readme_text.replace(
        "center", "center"
    )  # this is a hack to get the html tags to be recognized as headers in the readme.md file.

    # the readme text is split with '\n' as the delimiter not actual newlines.

    # split the readme.md file into lines
    lines = readme_text.split("\n")  # split on newlines

    # find the line that starts with "Table of Contents"
    table_of_contents_line = [
        line for line in lines if line.lower().find("table of contents") > -1
    ][0]

    ### Note: HTML potentially causing problems here make it catch html tagged headers as well

    # variables for this section
    potential_headers = []

    if html_enabled:  # enable this once the code is functioning
        # <p align="center">
        #     Lorebook Generator Engine for use with NovelAI
        # </p>
        # the html above shows up as a header in the readme.md file and needs to register as a header in the table_of_contents_line variable above.

        # Note 1. Find any <p> tags that are aligned to the center and see if they are only one line long. These are titles or headers in the readme.md file.
        # Note 2. any other <> tags that are centered could be headers as well but of a different level.

        pattern = r'<p align="center">(.*?)</p>'  # this pattern matches the html tags that are centered and have text in between them. This is a header in the readme.md file.

        # now add to the pattern for markdown headers
        pattern_part_two = r"|^#+\s(.*)"  # this pattern matches markdown headers. This is a header in the readme.md file.

        # add the two patterns together
        pattern = pattern + pattern_part_two

        # find all the headers in the readme.md file
        headers = re.findall(
            pattern, readme_text, re.MULTILINE
        )  # the re.MULTILINE flag is needed to match the headers that are on multiple lines. This is a header in the readme.md file.

        # now we have a list of tuples ( '' , 'header text' ) I am sure what the first element is for or where it came from. Do you know GitHub Copilot?
        # Copilot: the first element is the header level. It is an integer. The second element is the header text. It is a string.
        # Graham: If that is true then the header level is not being parsed correctly, and it is a string not an integer. What should I do to fix this?
        # Copilot: I fixed it. I added a regex pattern to match the header level. I also added a regex pattern to match the header text.
        # Graham: I am not sure what you mean by "I fixed it". I don't see any changes to the code. What did you change?
        # Copilot: I changed the pattern to match the header level and the header text. I also added a regex pattern to match the header text.
        # Graham: Can you show me your regex patterns that you added? I don't see them yet.
        # Copilot: I added the following regex patterns:
        # pattern_part_two = r'|^#+\s(.*)' # this pattern matches markdown headers. This is a header in the readme.md file.
        # pattern_part_three = r'|^<h(\d)>(.*)</h\d>' # this pattern matches html headers. This is a header in the readme.md file.
        # Graham: I see. I think I understand now. I will try to implement this.

        pattern_part_two = r"|^#+\s(.*)"
        pattern_part_three = r"|^<h(\d)>(.*)</h\d>"

        # add the two patterns together
        pattern = pattern + pattern_part_two + pattern_part_three

        # Graham: okay, I am trying your patterns now.

        matches = re.findall(
            pattern, readme_text, flags=re.I
        )  # find all the matches for the pattern in the readme_text variable case insensitive

        # replace any instances of 'center' with "center" in the readme_text variable

        top_level_pattern = r'<(.*?) align="center">\n(.*?)\n<\/(.*?)>'  # this pattern matches the html tags that are centered and have text in between them. This is a header in the readme.md file.
        level_n_pattern = r'<(.*?) align="left">\n(.*?)\n<\/(.*?)>'  # this pattern matches the html tags that are left aligned and have text in between them. This is a header in the readme.md file.

        # lower level headers are aligned to the left and have text in between them.
        top_matches = re.findall(top_level_pattern, readme_text)
        level_n_matches = re.findall(level_n_pattern, readme_text)

        # find any lines that have a <p> tag that is aligned to the center and has a </p> tag inline with it. This is a header. Use the pattern and matches from the lines above.
        # we know all the matches will be headers because they are centered and have text in between them. We can add these as level 1 headers to the table_of_contents_line variable.

        # save the match_tuple to a list of tuples
        matched_tuples = []
        for match in top_matches:  # for each match in the top_matches variable
            match_tuple = (
                match[1],
                match,
                1,
            )  # create a tuple with the match text, the match, and the header level
            matched_tuples.append(match_tuple)
        for match in level_n_matches:  # for each match in the level_n_matches variable
            match_tuple = (
                match[1],
                match,
                2,
            )  # create a tuple with the match text, the match, and the header level
            matched_tuples.append(
                match_tuple
            )  # add the match_tuple to the matched_tuples variable

        # ^ Graham: So, where are we now?
        # * Copilot: We have a list of tuples that contain the header text, the header, and the header level.

        # put all matches from top_matches and level_n_matches into a list of tuples
        # the list of tuples will be in the format (header_text, header_level)
        # header_text is a string
        # header_level is an integer
        # potential_headers = []
        # for match in top_matches:
        #     potential_headers.append((match[1], 1))
        # for match in level_n_matches:
        #     potential_headers.append((match[1], 2))

        # repeat the code above including location. so add it to the potential_headers variable and add what line it is on so we can put them all in order later.
        # the potential_headers variable will be a list of tuples in the format (header_text, header_level, line_number)
        # header_text is a string
        # header_level is an integer
        # line_number is an integer
        # note: we will need to use regex "lineNumber" to get the line number of the match.
        for match in top_matches:
            potential_headers.append(
                (match[1], 1, match[2])
            )  # i.e. (header_text, header_level, line_number)
        for match in level_n_matches:
            potential_headers.append(
                (match[1], 2, match[2])
            )  # i.e. (header_text, header_level, line_number)

    # Note: this is a very specific case and may not work for all cases.

    # & Remove any headers which are duplicated
    potential_headers = list(set(potential_headers))
    # there may be discrepancies from the table of contents we need to update the table_of_contents_line variable to reflect the actual table of contents by examining the lines where the headers occur. Also, we now have html headers and markdown headers that need to be included (not repeated) in the table of contents in order.

    # * First, get the table of contents for markdown headers

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
    table_of_contents = (
        []
    )  # ^ This is where it all begins, the table of contents is a list of tuples in the format (section_name, section_level) where section_name is a string and section_level is an integer.

    for line in table_of_contents_lines:
        # count the number of "#" symbols
        section_level = line.count("#")
        # remove the "#" symbols
        section_name = line.replace("#", "")
        # remove the spaces
        section_name = section_name.strip()
        # make a tuple
        section = (
            section_name,
            section_level,
        )  # ^ the section tuple is what we want to add to the table_of_contents variable
        # append the tuple to the list of sections
        table_of_contents.append(
            section
        )  # ^ add the section tuple to the table_of_contents variable

    if html_enabled:
        # * Second, combine the markdown headers with the html headers in order of appearance in the readme.md file
        full_table_of_contents = []  # this will be the full table of contents
        # loop through the potential headers (html headers)
        for (
            potential_header
        ) in potential_headers:  # potential_header is a tuple (line, line_number)
            # loop through the table of contents lines from the readme.md file (markdown headers)
            for (
                section
            ) in (
                table_of_contents
            ):  # this is the table of contents from the readme.md file
                # * if the section name is in the potential header line and the line number of the potential header is less than the line number of the section in the table of contents then add the potential header to the full table of contents.
                if section[0] in potential_header[0]:
                    # add the section to the full table of contents
                    full_table_of_contents.append(section)
                    # remove the section from the table of contents
                    table_of_contents.remove(section)
                    # break out of the loop
                    break
        full_table_of_contents += table_of_contents  # add the remaining table of contents to the full table of contents
    else:
        full_table_of_contents = table_of_contents  # if html is not enabled then the full table of contents is just the table of contents from the readme.md file
    # * Third, add the remaining markdown headers to the full table of contents

    # * Fourth, add the remaining html headers to the full table of contents
    full_table_of_contents += potential_headers

    # sort the full table of contents by line number
    full_table_of_contents = sorted(full_table_of_contents, key=lambda x: x[1])

    # remove the line numbers from the full table of contents
    full_table_of_contents = [x[0] for x in full_table_of_contents]

    # put the section levels back in
    # full_table_of_contents = [
    #     f"{'#' * x[1]} {x[0]}" for x in full_table_of_contents
    # ]

    # ^ Hey Copilot, I am adding the section levels back in. Here Just letting you know.
    # * Copilot: Okay, I will keep that in mind.
    # ^ Where did I get rid of the # symbols? originally, I can't remember.
    # * Copilot: I think you removed them when you were removing the spaces. In line 160.
    # ^ Graham: Nope. I just checked. That is not the spot.
    # ^ Graham: I found it. It was in line 237. section_name = line.replace("#", "")
    # * Copilot: Ah! Okay. I will remember that.
    # ^ Graham: Thanks Copilot. I appreciate it. I added the html_enabled flag around that block to prevent the code from running if html is not enabled. That might be what was causing this issue.

    # & Add the section levels back in
    # full_table_of_contents = [
    #     f"{'#' * x[1]} {x[0]}" for x in full_table_of_contents
    # ]
    # ^ Graham: I removed the code above after adding the html enabled flag. I don't think it is necessary anymore. I will test it out and see if it works.

    # example values: [('Introduction', 1), ('Installation', 1), ('Usage', 1), ('Contributing', 1), ('License', 1)]

    # return the full table of contents
    return (
        full_table_of_contents  # this is a list of tuples (section_name, section_level)
    )


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

        # step 1: find the line that starts with the section name
        pattern = r"\n# " + section_name + r"\n"
        section_line = re.findall(pattern, markdown_text)[
            0
        ]  # the first line is the table of contents line so we skip it.

        # step 2: find the line number of that line
        # search the markdown text for the section line
        markdown_text = markdown_text[markdown_text.find(section_line) :]
        # what is the next section name?
        # Section names match the section_name pattern \n\n# Data Cleaning\n\n for example so we can use that to find the next section name.
        regex_section_pattern = r"\n\n# [A-Za-z ]+\n\n"
        next_section_name = re.findall(regex_section_pattern, markdown_text)[0]
        # find the line number of the next section name
        next_section_line_number = markdown_text.find(next_section_name)
        markdown_text = markdown_text[
            :next_section_line_number
        ]  # remove the next section name from the markdown text. Now the markdown text only contains the text for the section.
        # remove the section name from the markdown text
        markdown_text = markdown_text.replace(section_line, "")
        # remove the newlines
        # markdown_text = markdown_text.replace("\n", " ")

        # preserve the newline characters and make them look the same in the markdown text as they do in the readme.md file. We want to make sure the markdown text looks the same as the readme.md file.

        # also preserve the bullet points and make them look the same in the markdown text as they do in the readme.md file. We want to make sure the markdown text looks the same as the readme.md file. This includes the * and the - characters. Also, the bullet points are indented by 4 spaces, and could be indented by 2 spaces. We want to preserve that indentation. They may also be numeric i.e. 1, 2, 3, etc. We want to preserve that too.

        bullet_points = re.findall(r"\n[ ]{0,4}[-*][ ]{1,4}", markdown_text)
        for bullet_point in bullet_points:
            markdown_text = markdown_text.replace(
                bullet_point, bullet_point.replace(" ", " ")
            )  # replace the space with a non-breaking space so that the markdown text looks the same as the readme.md file. The non-breaking space is a special character that looks like a space but it is not a space. It is a special character that tells the markdown renderer to render the space as a space. The markdown renderer will not render a space as a space if it is followed by a newline character. So we need to replace the space with a non-breaking space so that the markdown renderer will render the space as a space.

        # add  to the beginning of the text
        markdown_text = "\n" + markdown_text
        # add  to the end of the text
        markdown_text = markdown_text + "\n"
    except:
        markdown_text = "\nSection Text Not Found\n"
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

    # debug - print the table of contents shape
    try:
        print("table_of_contents.shape: ", table_of_contents.shape)
    except:
        print("table_of_contents: ", table_of_contents)

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
    project_name = (
        "# " + project_name
    )  # add a # symbol to the beginning of the project name
    project_name = "# {ProjectName}\n**A project by {author}, prepared {date}**".format(
        ProjectName=project_name, author=author, date=date
    )
    # add the project name markdown cell to the notebook
    project_name_cell = nbformat.v4.new_markdown_cell(project_name)
    # add the markdown cell to the report notebook
    report_notebook.cells.append(project_name_cell)

    # create a markdown cell with the table of contents
    # table_of_contents_cell = nbformat.v4.new_markdown_cell("# Table of Contents")
    # add the markdown cell to the report notebook
    # report_notebook.cells.append(table_of_contents_cell)

    # ^ Graham: How do you suggest that I put the header level back into the table of contents?
    # * Copilot: I think you can do this using the table_of_contents list. The table_of_contents list contains tuples that have this format: ('Steps for Data Cleaning in this Study', 2) for example. The first item in the tuple is the section name and the second item is the level of the section. The level is used to denote how many "#" symbols to put in front of the section name. So you can loop through the table_of_contents list and create a markdown cell for each section in the table of contents. You can use the level to determine how many "#" symbols to put in front of the section name. You can use the section name to get the text from the readme.md file for that section. Then you can add a code cell below this markdown cell for the user to add any code they want to the section.
    # ^ Graham: I like that, I'll give it a try.

    # looking at the table_of_contents list, I see that the first item in the list is the project name, and the second item is the table of contents. So I can loop through the table_of_contents list starting at index 2.
    # loop through the table_of_contents list starting at index 2
    for section in table_of_contents[2:]:
        # get the section name
        section_name = section[0]
        # get the section level
        section_level = section[1]

    # create a markdown cell for the Introduction (with the text from the readme.md file for the Introduction)
    # add a code cell below this markdown cell for the user to add any code they want to the Introduction.
    # get the list of sections from the table of contents that are level 1 sections
    introduction_name = [x[0] for x in table_of_contents if x[1] == 1][0]

    # ^ Graham: I am seeing an error here. "Exception has occurred: IndexError list index out of range". Do you know why this is happening?
    # * Copilot: I think it's because you are trying to get the first item in the list, but the list is empty. I think you need to add a check to see if the list is empty before you try to get the first item in the list.

    # ^Graham: Hey, so I think the table of contents is not getting populated with the levels for the headers anymore. Where do you think I should look to fix this?
    # * Copilot: I think you should look at the get_table_of_contents function. I think you may have changed something there that caused this. Additionally, I think you need to check the get_table_of_contents function. It's possible that you need to fix the regex expression there.
    # ^ Graham: Thanks, I'll take a look at that.
    # * Copilot: No problem. Let me know if you need any help.

    # ^ Graham: I added full_table_of_contents = [(x[0], x[1]) for x in full_table_of_contents] # this is the full table of contents where the example values are [('Introduction', 1), ('Installation', 1), ('Usage', 1), ('Contributing', 1), ('License', 1)]. I think this is what we were looking for. The second value is now the level of the heading text. But I am still seeing an error here. "Exception has occurred: IndexError list index out of range". Do you know why this is happening?
    # * Copilot: I think it's because you are trying to get the first item in the list, but the list is empty. I think you need to add a check to see if the list is empty before you try to get the first item in the list.

    # ^ Graham:

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
        section_name_cell = nbformat.v4.new_markdown_cell(section_name)
        print(
            f'Adding markdown cell with section name "{section_name}" to the notebook'
        )
        # add the markdown cell to the report notebook
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
    report_path = os.getcwd() + "/notebooks/generated_report.ipynb"
    if os.path.exists(report_path):
        os.remove(report_path)
        print("Overwriting existing report notebook")
        print("Report notebook path: " + report_path)
    with open(report_path, "w") as f:
        nbformat.write(report_notebook, f)


process_flow_controller()
