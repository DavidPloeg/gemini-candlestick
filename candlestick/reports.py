"""PDF report creation: Markdown to PDF, image to PDF, and merging."""
from img2pdf import convert  # Image to PDF conversion
import markdown
from pdf2image import convert_from_path  # PDF to image conversion
from pypdf import PdfWriter  # PDF file merging
from weasyprint import HTML  # HTML to PDF conversion


def markdown_to_pdf(markdown_text, output_pdf_path):
    """Converts Markdown text to a PDF file.

    Args:
        markdown_text (str): The Markdown text to convert.
        output_pdf_path (str): The path to save the output PDF file.
    """

    # Convert Markdown to HTML using the markdown library
    html_text = markdown.markdown(markdown_text)

    # Convert the HTML to PDF using the weasyprint library
    HTML(string=html_text).write_pdf(output_pdf_path)


def images_to_pdf(image_paths, output_pdf_path):
    """Combines image files into a single PDF, one image per page."""
    with open(output_pdf_path, "wb") as pdf_file:
        pdf_file.write(convert(image_paths))


def merge_pdfs(paths, output_filename):
    """
    Merges multiple PDF files into a single PDF file.

    Args:
        paths (list): A list of paths to the PDF files to be merged.
        output_filename (str): The name of the output PDF file.
    """

    # Create a PdfWriter object
    merger = PdfWriter()

    # Iterate over the list of PDF file paths
    for path in paths:
        # Append each PDF file to the merger
        merger.append(path)

    # Write the merged PDF to the output file
    merger.write(output_filename)

    # Close the PdfWriter object
    merger.close()


def make_pdf_uncroppable(input_pdf_path, output_pdf_path):
    """
    Converts a PDF to a sequence of images, effectively making it 'uncroppable'.

    This is achieved by treating each page of the PDF as a distinct image. 
    When opened, the PDF will appear as a single image per page, 
    preventing traditional cropping methods from being effective.

    Args:
        input_pdf_path (str): The path to the input PDF file.
        output_pdf_path (str): The path where the output 'uncroppable' PDF will be saved.
    """

    # Convert the input PDF to a list of PIL Image objects
    images = convert_from_path(input_pdf_path)

    # Handle cases where the PDF has multiple pages
    if len(images) > 1:
        # Save the first image as a PDF
        # Use save_all=True to indicate that multiple images will be saved
        # Append all subsequent images to the PDF
        images[0].save(
            output_pdf_path,
            "PDF",
            resolution=100.0,
            save_all=True,
            append_images=images[1:],
        )
    # Handle cases where the PDF has only one page
    else:
        # Save the single image as a PDF
        images[0].save(output_pdf_path, "PDF", resolution=100.0)
