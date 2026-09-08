import os
import pdfplumber
from PIL import Image, ImageDraw

# ====================== EDIT THIS ======================
# Folder containing the PDFs to process.
pdf_folder = r"C:\Users\MSK\Downloads\py\PDF Extraction\Draw_Bounding_Box_PDF"

# ---------------------- Process Each PDF File ----------------------
for pdf_file in os.listdir(pdf_folder):
    if pdf_file.endswith(".pdf"):
        pdf_path = os.path.join(pdf_folder, pdf_file)
        print(f"🔍 Processing {pdf_file}...")

        try:
            with pdfplumber.open(pdf_path) as pdf:
                # Only process the first page (or fewer, depending on the document)
                pages_to_search = [i for i in [0] if i < len(pdf.pages)]

                for page_num in pages_to_search:
                    page = pdf.pages[page_num]

                    # Get the full width and height of the page
                    page_width = page.width
                    page_height = page.height
                    print(f"📏 Page {page_num} dimensions: Width={page_width}, Height={page_height}")

                    # Set bounding box and crop (adjust as needed)
                    # Format: (x0, y0, x1, y1) => (left, top, right, bottom)
                    bounding_box = (0, 70, 150, 780)  # Example bounding box
                    cropped_page = page.within_bbox(bounding_box)

                    if cropped_page:
                        # ------------------ Visualize Cropped Area ------------------
                        # Convert the page to an image for debugging
                        im = page.to_image()

                        # Create an ImageDraw object
                        draw = ImageDraw.Draw(im.original)

                        # Draw a rectangle around the cropped area
                        draw.rectangle(bounding_box, outline="red", width=5)

                        # Save the image with the bounding box drawn
                        output_image_path = os.path.join(pdf_folder, f"{pdf_file}_page{page_num}_cropped.png")
                        im.original.save(output_image_path)

                        # Show the image with the bounding box
                        print(f"🔍 Image saved: {output_image_path}")
                        im.show()  # This may not work in some environments, but the image is saved as a PNG

        except Exception as e:
            print(f"❌ Error processing {pdf_file}: {e}")