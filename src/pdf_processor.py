# import os
# from pdf2image import convert_from_path
# from .config import Config

# class PDFProcessor:
#     def __init__(self, poppler_path=Config.POPPLER_PATH):
#         self.poppler_path = poppler_path
    
#     def convert_pdf_to_images(self, pdf_path, output_dir=Config.DEFAULT_OUTPUT_DIR):
#         """
#         Convert PDF pages to images
        
#         Args:
#             pdf_path (str): Path to the PDF file
#             output_dir (str): Directory to save the images
            
#         Returns:
#             list: List of paths to the generated images
#         """
#         os.makedirs(output_dir, exist_ok=True)
        
#         # Convert PDF to images
#         pages = convert_from_path(pdf_path, poppler_path=self.poppler_path)
        
#         # Save images
#         image_paths = []
#         for i, page in enumerate(pages, start=1):
#             out_file = os.path.join(output_dir, f"page_{i}.jpg")
#             page.save(out_file, "JPEG")
#             image_paths.append(out_file)
#             print(f"Saved {out_file}")
        
#         return image_paths


import os
from pdf2image import convert_from_path
from .config import Config

class PDFProcessor:
    def __init__(self):
        self.poppler_path = Config.get_poppler_path()
    
    def convert_pdf_to_images(self, pdf_path, output_dir=Config.DEFAULT_OUTPUT_DIR):
        """
        Convert PDF pages to images
        
        Args:
            pdf_path (str): Path to the PDF file
            output_dir (str): Directory to save the images
            
        Returns:
            list: List of paths to the generated images
        """
        os.makedirs(output_dir, exist_ok=True)
        
        # Convert PDF to images with appropriate poppler path
        try:
            if self.poppler_path:
                pages = convert_from_path(pdf_path, poppler_path=self.poppler_path)
            else:
                pages = convert_from_path(pdf_path)
        except Exception as e:
            raise Exception(f"PDF conversion failed: {e}. Please ensure poppler-utils is installed.")
        
        # Save images
        image_paths = []
        for i, page in enumerate(pages, start=1):
            out_file = os.path.join(output_dir, f"page_{i}.jpg")
            page.save(out_file, "JPEG")
            image_paths.append(out_file)
            print(f"Saved {out_file}")
        
        return image_paths