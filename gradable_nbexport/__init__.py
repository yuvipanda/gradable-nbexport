#!/usr/bin/env python3
"""
Generate PDF with cells with just given tag.

I can never figure out nbconvert's API, unfortunately.
"""
import os
import nbformat
import nbconvert
import tempfile
import subprocess
import typing
from copy import deepcopy


def filter_cells(notebook: nbformat.NotebookNode, filter):
    """
    Return new notebook object that matches filter function
    """
    picked_cells = []
    for cell in notebook.cells:
        if filter(cell):
            picked_cells.append(cell)

    new_nb = notebook.copy()
    new_nb.cells = picked_cells

    return new_nb

def generate_gradable_pdf(input_notebook: nbformat.NotebookNode, pdf_path: str, gradable_tag='gradable'):
    filtered_notebook = filter_cells(
        input_notebook,
        lambda cell: gradable_tag in cell.metadata.get('tags', [])
    )


    exporter = nbconvert.PDFExporter(config={})
    exporter.exclude_input_prompt = True
    exported_pdf, _ = exporter.from_notebook_node(nb=filtered_notebook, resources={'metadata': {'name': 'Something normal'}})

    with open(pdf_path, 'wb') as f:
        f.write(exported_pdf)

def download_gradable_pdf(notebook_file: str):
    output_name = os.path.splitext(os.path.basename(notebook_file))[0] + '.pdf'
    output_path = os.path.join(os.path.dirname(notebook_file), output_name)
    with open(notebook_file) as f:
        notebook = nbformat.read(f, as_version=4)
        generate_gradable_pdf(notebook, output_path)
    try:
        from IPython.display import HTML
        return HTML(f'Download <a href="{output_name}">{output_name}</a> & upload it to Canvas for your grade')
    except ImportError:
        print(f'Download {output_name} & upload it to Canvas for your grade')
