import os
import fitz  # PyMuPDF
from pdf2image import convert_from_path
from paddleocr import PaddleOCR
from docx import Document
from PIL import Image
import numpy as np
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
import argparse
import logging

# Set logging level
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize PaddleOCR model
ocr = PaddleOCR(use_angle_cls=True, lang='ch')

def convert_pdf_to_txt_with_ocr(pdf_path, txt_path):
    """Convert PDF to TXT using OCR"""
    logging.info(f"Processing with OCR: {pdf_path}")
    text_content = ""
    try:
        for page in convert_from_path(pdf_path, dpi=300, first_page=1, last_page=None):
            image_np = np.array(page.convert('RGB'))
            result = ocr.ocr(image_np, cls=True)
            if result and result[0]:
                text_lines = [line[1][0] for line in result[0]]
                text_content += "\n".join(text_lines) + "\n"
            
            # Write to file after processing each page to save memory
            with open(txt_path, 'a', encoding='utf-8') as txt_file:
                txt_file.write(text_content)
            text_content = ""  # Clear content for next page
    except Exception as e:
        logging.error(f"Error processing PDF with OCR: {pdf_path}")
        logging.error(f"Error details: {str(e)}")

def convert_pdf_to_txt(pdf_path, txt_path):
    """Convert PDF to TXT, use OCR if MuPDF error occurs"""
    try:
        with fitz.open(pdf_path) as pdf_document:
            with open(txt_path, 'w', encoding='utf-8') as txt_file:
                for page in pdf_document:
                    text = page.get_text("text")
                    txt_file.write(text + "\n")
    except fitz.fitz.FileDataError as e:
        logging.warning(f"MuPDF error, switching to OCR: {pdf_path}")
        logging.warning(f"Error details: {str(e)}")
        convert_pdf_to_txt_with_ocr(pdf_path, txt_path)
    except Exception as e:
        logging.error(f"Error processing PDF: {pdf_path}")
        logging.error(f"Error details: {str(e)}")

def convert_docx_to_txt(docx_path, txt_path):
    """Convert DOCX to TXT"""
    try:
        doc = Document(docx_path)
        with open(txt_path, 'w', encoding='utf-8') as txt_file:
            for para in doc.paragraphs:
                txt_file.write(para.text + "\n")
    except Exception as e:
        logging.error(f"Error processing DOCX: {docx_path}")
        logging.error(f"Error details: {str(e)}")

def preprocess_text(text):
    """Preprocess text"""
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    # Remove special characters (keep Chinese, English, numbers, basic punctuation)
    text = re.sub(r'[^\u4e00-\u9fa5a-zA-Z0-9.,!?;:，。！？；：]', '', text)
    # Unify punctuation (convert Chinese punctuation to English)
    punctuation_map = {
        '，': ',', '。': '.', '！': '!', '？': '?', '；': ';', '：': ':'
    }
    for ch, en in punctuation_map.items():
        text = text.replace(ch, en)
    return text

def process_file(file_path, output_folder):
    """Process a single file"""
    filename = os.path.basename(file_path)
    txt_path = os.path.join(output_folder, os.path.splitext(filename)[0] + '.txt')
    
    if file_path.endswith('.pdf'):
        logging.info(f"Converting PDF: {filename}")
        convert_pdf_to_txt(file_path, txt_path)
        return file_path, txt_path
    elif file_path.endswith('.docx'):
        logging.info(f"Converting DOCX: {filename}")
        convert_docx_to_txt(file_path, txt_path)
        return file_path, txt_path
    else:
        return None

    # Preprocess the generated TXT file
    with open(txt_path, 'r', encoding='utf-8') as f:
        text = f.read()
    
    processed_text = preprocess_text(text)
    
    with open(txt_path, 'w', encoding='utf-8') as f:
        f.write(processed_text)
    
    logging.info(f"Processed and saved: {os.path.basename(txt_path)}")
    return file_path, txt_path

def process_files(input_folder, output_folder, max_workers=4):
    """Process all files in the folder"""
    processed_files = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_file = {}
        for filename in os.listdir(input_folder):
            file_path = os.path.join(input_folder, filename)
            if filename.endswith(('.pdf', '.docx')):
                future = executor.submit(process_file, file_path, output_folder)
                future_to_file[future] = file_path

        for future in as_completed(future_to_file):
            file_path = future_to_file[future]
            try:
                result = future.result()
                if result:
                    processed_files.append(result)
            except Exception as e:
                logging.error(f"Error processing file: {file_path}")
                logging.error(f"Error details: {str(e)}")
    
    return processed_files

def check_and_fix_small_files(processed_files, size_threshold=10*1024):  # 10KB
    """Check and fix small files"""
    for pdf_path, txt_path in processed_files:
        if os.path.getsize(txt_path) < size_threshold:
            logging.warning(f"Found file smaller than {size_threshold/1024}KB: {txt_path}")
            logging.info(f"Reprocessing PDF with OCR: {pdf_path}")
            convert_pdf_to_txt_with_ocr(pdf_path, txt_path)
            
            # Preprocess the regenerated TXT file
            with open(txt_path, 'r', encoding='utf-8') as f:
                text = f.read()
            
            processed_text = preprocess_text(text)
            
            with open(txt_path, 'w', encoding='utf-8') as f:
                f.write(processed_text)
            
            logging.info(f"Reprocessed and saved: {txt_path}")

def main():
    parser = argparse.ArgumentParser(description="Convert PDF and DOCX files to TXT format")
    parser.add_argument("input_folder", help="Input folder path")
    parser.add_argument("output_folder", help="Output folder path")
    parser.add_argument("--max_workers", type=int, default=4, help="Maximum number of worker threads")
    parser.add_argument("--size_threshold", type=int, default=10, help="Small file threshold (KB)")
    args = parser.parse_args()

    if not os.path.exists(args.output_folder):
        os.makedirs(args.output_folder)

    processed_files = process_files(args.input_folder, args.output_folder, args.max_workers)
    logging.info("Checking small files...")
    check_and_fix_small_files(processed_files, args.size_threshold * 1024)
    logging.info("All files processed.")

if __name__ == "__main__":
    main()