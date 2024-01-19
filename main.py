from PIL import Image
from reportlab.pdfgen import canvas
from io import BytesIO
import os

def add_image_to_pdf(pdf_canvas, image_path, page_width, page_height):
    # Open the image and resize it to fit the page
    img = Image.open(image_path)
    img_width, img_height = img.width, img.height

    scale_factor = min(page_width / img_width, page_height / img_height)
    img = img.resize((int(img_width * scale_factor), int(img_height * scale_factor)))

    # Calculate the position to center the image on the page
    x_position = (page_width - img.width) / 2
    y_position = (page_height - img.height) / 2

    # Draw the image on the PDF canvas
    pdf_canvas.drawImage(image_path, x_position, y_position, width=img.width, height=img.height)

if __name__ == "__main__":
    # Create a PDF file
    pdf_path = "sushant_images.pdf"
    pdf_buffer = BytesIO()
    pdf_canvas = canvas.Canvas(pdf_buffer)

    # Set the page size (assuming letter size, adjust as needed)
    page_width, page_height = 612, 792  # Letter size in points (8.5 x 11 inches)

    # Get the current script directory
    script_directory = os.path.dirname(os.path.abspath(__file__))

    # List all image files in the script directory and sort them by filename
    image_files = sorted([f for f in os.listdir(script_directory) if f.lower().endswith(('.jpg'))], key=lambda x: int(x.split('.')[0]))

    for image_file in image_files:
        # Construct the full image path
        image_path = os.path.join(script_directory, image_file)

        # Add the image to the PDF canvas
        add_image_to_pdf(pdf_canvas, image_path, page_width, page_height)

        # Start a new page for the next image
        pdf_canvas.showPage()

    # Save the PDF file
    pdf_canvas.save()

    # Write the PDF buffer to a file
    with open(pdf_path, "wb") as pdf_file:
        pdf_file.write(pdf_buffer.getvalue())

    print(f"PDF file '{pdf_path}' created successfully.")
