import fitz


def extract_textboxes(pdf_file):
    # Open the PDF file
    doc = fitz.open(pdf_file)

    text_boxes = []

    # Iterate through each page
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)

        # Extract text annotations (which typically include text boxes)
        annotations = page.annots()

        # Iterate through each annotation
        for annot in annotations:
            import rich; from rich import inspect; from rich import print as rprint; import ipdb; ipdb.set_trace()
            if annot.type[0] == 8:  # Check if it's a text box
                textbox = {"page_number": page_num + 1, "text": annot.info["content"], "bbox": annot.rect}
                text_boxes.append(textbox)

    # Close the PDF
    doc.close()

    return text_boxes


# Example usage:
pdf_file = "res/Tu dien TVH - PAC.pdf"
text_boxes = extract_textboxes(pdf_file)

# Print extracted text boxes
for i, textbox in enumerate(text_boxes):
    print(f"Text Box {i + 1}:")
    print("Page Number:", textbox["page_number"])
    print("Text:", textbox["text"])
    print("Bounding Box:", textbox["bbox"])
    print()
