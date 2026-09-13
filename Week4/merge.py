import glob
import nbformat
from nbmerge import merge_notebooks

print
# 1. Collect all notebooks in the folder
notebook_files = glob.glob("*.ipynb")

print("Found the following notebook files:")
print(notebook_files)

# 2. Exclude your target output name so it doesn't merge into itself
if "nagarajan_graded_assignment1.ipynb" in notebook_files:
    notebook_files.remove("nagarajan_graded_assignment1.ipynb")

# 3. Merge and write out the file
merged_nb = merge_notebooks(".", notebook_files)
with open("nagarajan_graded_assignment1.ipynb", "w", encoding="utf-8") as f:
    nbformat.write(merged_nb, f)