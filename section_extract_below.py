import os
import pdfplumber
import pandas as pd

# ====================== EDIT THIS ======================
# Folder containing the PDFs to process.
# Specify the folder path where PDF files are located
pdf_folder = r"C:\Users\MSK\Downloads\py\PDF Extraction\PDF"

# ---------------------- Keywords ----------------------
# Keywords to search for in lowercase for case-insensitive matching
keywords = [kw.lower() for kw in [
    "Medications"
]]

# ---------------------- Function to Search Keywords ----------------------
def check_keywords_in_text(text, keywords):
    """
    Check if any of the provided keywords exist in the given text.
    If a keyword is found, return the current line and the next line.
    Returns:
        matched_lines: List of lines below the matched keyword
        matched_keywords_set: Set of matched keywords (for reporting)
    """
    matched_lines = []
    matched_keywords_set = set()
    lines = text.split('\n')

    for i in range(len(lines) - 1):  # Ensure we don't go out of range
        line = lines[i].lower()
        next_line = lines[i + 1].strip()

        for kw in keywords:
            if kw in line:
                matched_lines.append(next_line)  # Append the next line
                matched_keywords_set.add(kw)
                break  # Skip checking other keywords if one is matched in the line

    return matched_lines, matched_keywords_set

# ---------------------- Initialize DataFrame and Counters ----------------------
# Create an empty DataFrame to store results of the scan
df = pd.DataFrame(columns=["PDF File", "Matched Keywords", "Status"])

# Track progress
total_files = 0
success_count = 0
error_count = 0

# ---------------------- Process Each PDF File ----------------------
for pdf_file in os.listdir(pdf_folder):
    if pdf_file.endswith(".pdf"):
        total_files += 1
        pdf_path = os.path.join(pdf_folder, pdf_file)
        print(f"🔍 Processing {pdf_file}...")

        try:
            with pdfplumber.open(pdf_path) as pdf:
                full_text = ""

                # Safe page selection (only page 0 and 1 if available)
                pages_to_search = [i for i in [0, 1] if i < len(pdf.pages)]

                for page_num in pages_to_search:
                    page = pdf.pages[page_num]

                    # Only extract text from a specific region using bounding box
                    bounding_box = (0, 70, 150, 780)
                    cropped_page = page.within_bbox(bounding_box)
                    if cropped_page:
                        cropped_text = cropped_page.extract_text()
                        if cropped_text:
                            full_text += cropped_text

                # Search extracted cropped text for keyword matches
                matched_lines, matched_keywords = check_keywords_in_text(full_text, keywords)

                # Build result row based on match status
                if matched_lines:
                    status_text = "; ".join(matched_lines)
                    matched_keywords_text = ", ".join(sorted(matched_keywords))
                    new_row = pd.DataFrame([{
                        "PDF File": pdf_file,
                        "Matched Keywords": matched_keywords_text,
                        "Status": status_text
                    }])
                    success_count += 1
                else:
                    new_row = pd.DataFrame([{
                        "PDF File": pdf_file,
                        "Matched Keywords": "",
                        "Status": "No Match"
                    }])

                # Append result row to the main DataFrame
                df = pd.concat([df, new_row], ignore_index=True)

        except Exception as e:
            # Log error and add to DataFrame
            print(f"❌ Error processing {pdf_file}: {e}")
            error_count += 1
            new_row = pd.DataFrame([{
                "PDF File": pdf_file,
                "Matched Keywords": "",
                "Status": "Error"
            }])
            df = pd.concat([df, new_row], ignore_index=True)

        # To check if all files are being processed correctly, print each file's status
        print(f"Processed: {pdf_file}")

# ---------------------- Save Results to Excel ----------------------
# Export the results DataFrame to an Excel file
output_file = "pdf_keyword_results.xlsx"
df.to_excel(output_file, index=False)

# ---------------------- Print Final Summary ----------------------
print(f"\n✅ Script completed.")
print(f"📁 Total files processed: {total_files}")
print(f"✔️ Successes: {success_count}")
print(f"❌ Errors: {error_count}")
print(f"💾 Results saved to {output_file}")
