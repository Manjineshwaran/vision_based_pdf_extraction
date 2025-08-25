from PIL import Image
import os
from .config import Config

class EntityCropper:
    def __init__(self, entities_dir=Config.DEFAULT_ENTITIES_DIR):
        self.entities_dir = entities_dir
        os.makedirs(entities_dir, exist_ok=True)
    
    def crop_entities_from_results(self, image_path, results, page_no):
        """
        Crop detected entities from an image based on detection results
        
        Args:
            image_path (str): Path to the original image
            results: Detection results from YOLO
            page_no (int): Page number for naming
            
        Returns:
            dict: Dictionary of cropped entities by category
        """
        img = Image.open(image_path)
        cropped_entities = {}
        
        for r in results:
            boxes = r.boxes.xyxy.cpu().numpy()   # [x1, y1, x2, y2]
            classes = r.boxes.cls.cpu().numpy()  # class IDs
            scores = r.boxes.conf.cpu().numpy()  # confidence scores

            for idx, (box, cls, score) in enumerate(zip(boxes, classes, scores), start=1):
                cls_name = r.names[int(cls)]  # e.g., 'table', 'text', 'formula'
                x1, y1, x2, y2 = map(int, box)

                # Crop region
                cropped = img.crop((x1, y1, x2, y2))

                # Make folder for class
                class_dir = os.path.join(self.entities_dir, cls_name)
                os.makedirs(class_dir, exist_ok=True)

                # Save cropped entity
                out_file = os.path.join(class_dir, f"page{page_no}_{cls_name}_{idx}.jpg")
                cropped.save(out_file)
                
                # Add to results dictionary
                if cls_name not in cropped_entities:
                    cropped_entities[cls_name] = []
                cropped_entities[cls_name].append(out_file)
                
                print(f"[PAGE {page_no}] Saved {cls_name} → {out_file}")
        
        return cropped_entities
    
    def get_all_entities(self):
        """Get all cropped entities organized by type"""
        entities = {}
        for entity_type in os.listdir(self.entities_dir):
            entity_dir = os.path.join(self.entities_dir, entity_type)
            if os.path.isdir(entity_dir):
                entities[entity_type] = [
                    os.path.join(entity_dir, f) for f in os.listdir(entity_dir) 
                    if f.endswith(('.jpg', '.jpeg', '.png'))
                ]
        return entities