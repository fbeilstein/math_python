#!/bin/bash

# Find problem folders
folders=($(find . -maxdepth 1 -type d -name "*_problem" -exec basename {} \;))

if [ ${#folders[@]} -eq 0 ]; then
    echo "No problem folders found."
    exit 1
fi

echo "Select a problem to prepare a release for:"
select problem in "${folders[@]}"; do
    if [ -n "$problem" ]; then
        break
    else
        echo "Invalid selection."
    fi
done

echo "Preparing release for $problem..."

# Create a staging directory
staging_dir=$(mktemp -d)
release_dir="$staging_dir/$problem"

# Export only committed files using git archive
git archive HEAD "$problem" | tar -x -C "$staging_dir"

if [ ! -d "$release_dir" ]; then
    echo "Error: Failed to export git-committed files."
    exit 1
fi

cd "$release_dir"

# Compile problem.tex to PDF and remove description folder
if [ -d "description" ]; then
    if [ -f "description/problem.tex" ]; then
        echo "Compiling problem.tex to PDF..."
        (cd description && pdflatex -interaction=nonstopmode problem.tex > /dev/null 2>&1 && pdflatex -interaction=nonstopmode problem.tex > /dev/null 2>&1)
        if [ -f "description/problem.pdf" ]; then
            mv description/problem.pdf ./
        else
            echo "Warning: PDF compilation failed."
        fi
    fi
    rm -rf description
fi

# Python script to strip function bodies while preserving docstrings
cat << 'EOF' > /tmp/strip_solutions.py
import sys

def process(filepath):
    try:
        with open(filepath, 'r') as f:
            lines = f.readlines()
    except FileNotFoundError:
        return
        
    out = []
    in_func = False
    base_indent = 0
    in_doc = False
    doc_char = ""
    added_pass = False
    
    for i, line in enumerate(lines):
        stripped = line.lstrip()
        indent = len(line) - len(stripped)
        
        if not in_func:
            if stripped.startswith("def ") and "#contains solution" in line:
                out.append(line.replace("#contains solution", "").rstrip() + "\n")
                in_func = True
                base_indent = indent
                added_pass = False
            else:
                out.append(line)
            continue
            
        if in_func:
            if in_doc:
                out.append(line)
                if doc_char in stripped:
                    in_doc = False
                    out.append(" " * (base_indent + 4) + "pass\n")
                    added_pass = True
                continue
                
            if not added_pass and (stripped.startswith('"""') or stripped.startswith("'''")):
                out.append(line)
                doc_char = stripped[:3]
                if line.count(doc_char) >= 2:
                    out.append(" " * (base_indent + 4) + "pass\n")
                    added_pass = True
                else:
                    in_doc = True
                continue
                
            if stripped == "":
                continue
                
            if stripped.startswith("#") and indent > base_indent:
                continue
                
            if indent <= base_indent:
                in_func = False
                if not added_pass:
                    out.append(" " * (base_indent + 4) + "pass\n")
                out.append(line)

    # If the file ended while still inside a function
    if in_func and not added_pass:
        out.append(" " * (base_indent + 4) + "pass\n")

    with open(filepath, 'w') as f:
        f.writelines(out)

if __name__ == '__main__':
    process(sys.argv[1])
EOF

# Strip solutions from implementation_tasks.py if it exists
if [ -f "implementation_tasks.py" ]; then
    echo "Stripping solutions from implementation_tasks.py..."
    python3 /tmp/strip_solutions.py implementation_tasks.py
fi

# Clean up the python script
rm -f /tmp/strip_solutions.py

# Create zip archive
cd "$staging_dir"
zip_file="${problem}.zip"
zip -r "$zip_file" "$problem" > /dev/null

# Move the zip file back to the current working directory
cd - > /dev/null
mv "$staging_dir/$zip_file" .
rm -rf "$staging_dir"

echo "Release successfully prepared: $zip_file"
