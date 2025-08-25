import argparse
import os
from src.pdf_processor import PDFProcessor
from src.layout_detector import LayoutDetector
from src.entity_cropper import EntityCropper
from src.utils import get_image_files, clear_directory, setup_environment

def process_pdf(pdf_path, clear_existing=True):
    """
    Process a PDF file to extract layout entities
    
    Args:
        pdf_path (str): Path to the PDF file
        clear_existing (bool): Whether to clear existing output directories
        
    Returns:
        dict: All extracted entities by type
    """
    # Setup environment
    setup_environment()
    
    # Clear existing files if requested
    if clear_existing:
        from src.config import Config
        clear_directory(Config.DEFAULT_OUTPUT_DIR)
        clear_directory(Config.DEFAULT_ENTITIES_DIR)
        clear_directory(Config.DEFAULT_DETECTIONS_DIR)
    
    # Initialize components
    pdf_processor = PDFProcessor()
    layout_detector = LayoutDetector()
    entity_cropper = EntityCropper()
    
    # Step 1: Convert PDF to images
    print("Converting PDF to images...")
    image_paths = pdf_processor.convert_pdf_to_images(pdf_path)
    
    # Step 2: Process each image
    print("Detecting layout and cropping entities...")
    for page_no, img_path in enumerate(image_paths, start=1):
        print(f"Processing page {page_no}: {img_path}")
        
        # Detect layout
        results = layout_detector.detect_layout(img_path, save=True)
        
        # Crop entities
        entity_cropper.crop_entities_from_results(img_path, results, page_no)
    
    # Step 3: Get all entities
    all_entities = entity_cropper.get_all_entities()
    
    # Print summary
    print("\n=== EXTRACTION SUMMARY ===")
    for entity_type, files in all_entities.items():
        print(f"{entity_type}: {len(files)} items")
    
    return all_entities

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Document Layout Analysis Pipeline")
    parser.add_argument("pdf_path", help="Path to the PDF file to process")
    parser.add_argument("--keep-existing", action="store_true", 
                       help="Keep existing output files instead of clearing them")
    
    args = parser.parse_args()
    
    if not os.path.exists(args.pdf_path):
        print(f"Error: PDF file '{args.pdf_path}' not found.")
        exit(1)
    
    process_pdf(args.pdf_path, clear_existing=not args.keep_existing)