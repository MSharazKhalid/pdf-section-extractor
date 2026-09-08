import os
import pdfplumber
import pandas as pd

# ====================== EDIT THIS ======================
# Folder containing the PDFs to process.
pdf_folder = r"C:\Users\MSK\Desktop\modmed\pdf"  # Raw strings

# ---------------------- Keywords ----------------------
keywords = [
    "Hemoglobin A1C",
    "hba1c",
    "Hemoglobin",
    "HgA1c",
    "a1c"
]

# ---------------------- Function to Search Keywords in Text ----------------------

def check_keywords_in_text(text, keywords):
    """
    Check if any of the provided keywords exist in the text.
    Return matched keywords and the corresponding lines.
    """
    matched_lines = []
    matched_keywords_set = set()

    for line in text.split('\n'):
        for kw in keywords:
            if kw.lower() in line.lower():
                matched_lines.append(line.strip())
                matched_keywords_set.add(kw)
                # Removed break to allow checking all keywords in the same line

    return matched_lines, matched_keywords_set

# ---------------------- Process PDFs ----------------------

# Prepare DataFrame for storing results
df = pd.DataFrame(columns=["PDF File", "Matched Keywords", "Status"])

# Read and process each PDF file in the folder
for pdf_file in os.listdir(pdf_folder):
    if pdf_file.endswith(".pdf"):
        pdf_path = os.path.join(pdf_folder, pdf_file)
        print(f"Processing {pdf_file}...")

        try:
            with pdfplumber.open(pdf_path) as pdf:
                # Extract text from all pages of the PDF
                full_text = ""
                for page in pdf.pages:
                    full_text += page.extract_text()

                # Check for matched keywords in the extracted text
                matched_lines, matched_keywords = check_keywords_in_text(full_text, keywords)

                if matched_lines:
                    # If keywords are found, update the status and matched keywords
                    status_text = "; ".join(matched_lines)
                    matched_keywords_text = ", ".join(sorted(matched_keywords))
                    new_row = pd.DataFrame([{"PDF File": pdf_file, "Matched Keywords": matched_keywords_text, "Status": status_text}])
                    df = pd.concat([df, new_row], ignore_index=True)
                else:
                    # If no keywords are found, set the status as "No Match"
                    new_row = pd.DataFrame([{"PDF File": pdf_file, "Matched Keywords": "", "Status": "No Match"}])
                    df = pd.concat([df, new_row], ignore_index=True)

        except Exception as e:
            print(f"Error processing {pdf_file}: {e}")
            new_row = pd.DataFrame([{"PDF File": pdf_file, "Matched Keywords": "", "Status": "Error"}])
            df = pd.concat([df, new_row], ignore_index=True)

# ---------------------- Save Results to Excel ----------------------

# Save the DataFrame with results to a new Excel file
output_file = "pdf_keyword_results_001.xlsx"
df.to_excel(output_file, index=False)
print(f"✅ Script completed and results saved to {output_file}.")
