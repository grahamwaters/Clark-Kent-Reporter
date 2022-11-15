import os

#^ Task 1
#^ create a data processing file (python) that has the imports and the data loaded already (so you can just start coding)

# code:
# make the code file
if os.exists("code.py"):
    os.remove("code.py")
os.system("touch code.py") # create the file if it doesn't exist

# write the imports to the file
with open("code.py", "w") as f:
    f.write("import os # for file management")



#^ Task 2
#^ create a data exploration notebook (jupyter) that imports the dataframe(s) from the data processing file in the first cell. Make this in the same folder as the data processing file.
