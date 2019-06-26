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
from canvasapi import Canvas
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


def submit_assignment(
    notebook_file: str,
    assignment_name: str,
    canvas_course_id: int,
    canvas_url: str = '',
    canvas_api_key: str = '',
):

    if canvas_url == '':
        if 'CANVAS_API_URL' not in os.environ:
            raise ValueError('Could not find CANVAS_API_URL in environment, canvas_url must be passed in')
        canvas_url = os.environ['CANVAS_API_URL']
    if canvas_api_key == '':
        if 'CANVAS_API_KEY' not in os.environ:
            raise ValueError('Could not find CANVAS_API_KEY in environment, canvas_api_key must be passed in')
        canvas_api_key = os.environ['CANVAS_API_KEY']

    canvas = Canvas(canvas_url, canvas_api_key)
    course = canvas.get_course(canvas_course_id)

    selected_assignment = None
    for assignment in course.get_assignments():
        if assignment.name == assignment_name:
            selected_assignment = assignment
            break
    else:
        raise ValueError(
            f'No assignment {assignment_name} found in course {course.name}'
        )

    with open(notebook_file)  as f:
        with tempfile.TemporaryDirectory() as d:
            pdf_path = os.path.join(
                d,
                os.path.splitext(os.path.basename(notebook_file))[0] + '.pdf'
            )
            generate_gradable_pdf(nbformat.read(f, as_version=4), pdf_path)
            print(selected_assignment.submit(
                {'submission_type': 'online_upload', 'user_id':47030},
                pdf_path,
                user_id=47030
            ))


def main():
    with open('Assignment 01.ipynb') as f:
        generate_gradable_pdf(
            nbformat.read(f, as_version=4),
            'Assignment 01.pdf',
        )

if __name__ == '__main__':
    main()