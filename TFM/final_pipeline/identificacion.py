import fitz

def analyze_advanced_mixed_pdf(file_path, chars_threshold=50, image_coverage_threshold=0.2):
    """
    Analyzes a PDF document by evaluating both text density and image area coverage 
    to accurately detect scanned pages, even those with hidden OCR layers or headers.
    
    Args:
        file_path (str): Path to the PDF file.
        chars_threshold (int): Minimum characters required to consider a page text-based.
        image_coverage_threshold (float): Proportion of the page area (0.0 to 1.0) 
                                          covered by a single image to classify it as a scan.
        
    Returns:
        dict: Detailed breakdown of the document classification.
    """
    result_summary = {
        "file_path": file_path,
        "total_pages": 0,
        "document_type": "unknown", 
        "scanned_pages_count": 0,
        "text_pages_count": 0,
        "page_details": []
    }

    try:
        document = fitz.open(file_path)
        total_pages = len(document)
        result_summary["total_pages"] = total_pages
        
        if total_pages == 0:
            return result_summary
            
        for page_index in range(total_pages):
            page = document.load_page(page_index)
            
            # 1. Text Analysis
            page_text = page.get_text().strip()
            text_length = len(page_text)
            
            # 2. Image Coverage Analysis
            page_area = page.rect.width * page.rect.height
            max_image_coverage = 0.0
            
            # get_image_info() returns a list of dictionaries with image bounding boxes
            image_list = page.get_image_info()
            
            for img in image_list:
                bbox = img.get("bbox")
                if bbox:
                    # Calculate area of the image block (width * height)
                    img_area = (bbox[2] - bbox[0]) * (bbox[3] - bbox[1])
                    coverage = img_area / page_area
                    if coverage > max_image_coverage:
                        max_image_coverage = coverage
            
            # 3. Classification Logic
            # A page is scanned if it lacks text OR if a massive image covers the page
            is_scanned = (text_length < chars_threshold) or (max_image_coverage >= image_coverage_threshold)
            
            if is_scanned:
                result_summary["scanned_pages_count"] += 1
            else:
                result_summary["text_pages_count"] += 1
                
            page_info = {
                "page_number": page_index + 1,
                "character_count": text_length,
                "max_image_coverage": round(max_image_coverage, 4),
                "is_scanned": is_scanned
            }
            result_summary["page_details"].append(page_info)
            
        # Overall document classification
        if result_summary["scanned_pages_count"] == total_pages:
            result_summary["document_type"] = "fully_scanned"
        elif result_summary["text_pages_count"] == total_pages:
            result_summary["document_type"] = "fully_text_based"
        else:
            result_summary["document_type"] = "mixed_content"
            
        return result_summary

    except Exception as error:
        print(f"Error processing document: {error}")
        return result_summary

# Usage example:
# results = analyze_advanced_mixed_pdf("documento_complejo.pdf")