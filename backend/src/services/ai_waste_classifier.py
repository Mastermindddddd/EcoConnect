import os
import base64
import json
from typing import Dict, Any, Optional
from openai import OpenAI

class AIWasteClassifier:
    """
    AI-powered waste classification service using OpenAI's vision capabilities.
    Identifies waste types from images and provides disposal recommendations.
    """
    
    def __init__(self):
        self.client = OpenAI()
        
        # Waste categories and their properties
        self.waste_categories = {
            'plastic': {
                'recyclable': True,
                'color': 'green',
                'disposal_method': 'Take to recycling center',
                'preparation_tips': 'Clean containers, remove labels if possible'
            },
            'paper': {
                'recyclable': True,
                'color': 'blue',
                'disposal_method': 'Take to recycling center',
                'preparation_tips': 'Keep dry, remove any plastic components'
            },
            'glass': {
                'recyclable': True,
                'color': 'green',
                'disposal_method': 'Take to recycling center',
                'preparation_tips': 'Rinse clean, remove caps and lids'
            },
            'metal': {
                'recyclable': True,
                'color': 'silver',
                'disposal_method': 'Take to recycling center',
                'preparation_tips': 'Rinse clean, crushing is optional'
            },
            'organic': {
                'recyclable': True,
                'color': 'brown',
                'disposal_method': 'Compost or organic waste bin',
                'preparation_tips': 'Remove any non-organic materials'
            },
            'electronics': {
                'recyclable': True,
                'color': 'purple',
                'disposal_method': 'Take to electronics recycling center',
                'preparation_tips': 'Remove batteries, wipe personal data'
            },
            'hazardous': {
                'recyclable': False,
                'color': 'red',
                'disposal_method': 'Take to hazardous waste facility',
                'preparation_tips': 'Do not mix with regular waste, handle with care'
            },
            'textile': {
                'recyclable': True,
                'color': 'pink',
                'disposal_method': 'Donate or take to textile recycling',
                'preparation_tips': 'Clean and dry, separate by material type'
            },
            'non_recyclable': {
                'recyclable': False,
                'color': 'gray',
                'disposal_method': 'Regular trash bin',
                'preparation_tips': 'Minimize waste by choosing reusable alternatives'
            }
        }
    
    def encode_image(self, image_path: str) -> str:
        """Encode image to base64 string for API submission."""
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    
    def classify_waste(self, image_path: str) -> Dict[str, Any]:
        """
        Classify waste from image using OpenAI Vision API.
        
        Args:
            image_path: Path to the waste image file
            
        Returns:
            Dictionary containing classification results
        """
        try:
            # Encode the image
            base64_image = self.encode_image(image_path)
            
            # Create the prompt for waste classification
            prompt = """
            You are an expert waste management AI. Analyze this image and identify the waste item(s).
            
            Please provide a JSON response with the following structure:
            {
                "identified_type": "Specific item name (e.g., 'Plastic Water Bottle', 'Aluminum Can')",
                "confidence_score": 0.95,
                "material_category": "One of: plastic, paper, glass, metal, organic, electronics, hazardous, textile, non_recyclable",
                "specific_material": "More specific material type if applicable",
                "condition": "Description of item condition",
                "size_estimate": "Small/Medium/Large",
                "additional_notes": "Any other relevant observations"
            }
            
            Focus on accuracy and provide the most specific identification possible.
            Consider the material composition, shape, and any visible markings or labels.
            """
            
            # Make API call to OpenAI
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{base64_image}"
                                }
                            }
                        ]
                    }
                ],
                max_tokens=500,
                temperature=0.1
            )
            
            # Parse the response
            result_text = response.choices[0].message.content
            
            # Try to extract JSON from the response
            try:
                # Find JSON in the response
                start_idx = result_text.find('{')
                end_idx = result_text.rfind('}') + 1
                json_str = result_text[start_idx:end_idx]
                classification_result = json.loads(json_str)
            except (json.JSONDecodeError, ValueError):
                # Fallback if JSON parsing fails
                classification_result = {
                    "identified_type": "Unknown Item",
                    "confidence_score": 0.5,
                    "material_category": "non_recyclable",
                    "specific_material": "Unknown",
                    "condition": "Cannot determine",
                    "size_estimate": "Unknown",
                    "additional_notes": "Classification failed, manual review needed"
                }
            
            # Enhance with category information
            category = classification_result.get('material_category', 'non_recyclable')
            category_info = self.waste_categories.get(category, self.waste_categories['non_recyclable'])
            
            # Build final result
            final_result = {
                **classification_result,
                'recyclable': category_info['recyclable'],
                'disposal_method': category_info['disposal_method'],
                'preparation_tips': category_info['preparation_tips'],
                'category_color': category_info['color']
            }
            
            return final_result
            
        except Exception as e:
            # Return error result
            return {
                "identified_type": "Classification Error",
                "confidence_score": 0.0,
                "material_category": "non_recyclable",
                "recyclable": False,
                "disposal_method": "Unable to classify - please consult local waste guidelines",
                "preparation_tips": "Manual classification needed",
                "error": str(e)
            }
    
    def get_disposal_recommendations(self, classification_result: Dict[str, Any], 
                                   user_location: Optional[Dict[str, float]] = None) -> Dict[str, Any]:
        """
        Get enhanced disposal recommendations based on classification and location.
        
        Args:
            classification_result: Result from classify_waste method
            user_location: Optional dict with 'latitude' and 'longitude'
            
        Returns:
            Enhanced recommendations with location-specific advice
        """
        recommendations = {
            'primary_method': classification_result.get('disposal_method'),
            'preparation_steps': classification_result.get('preparation_tips'),
            'recyclable': classification_result.get('recyclable', False),
            'environmental_impact': self._get_environmental_impact(classification_result),
            'alternatives': self._get_alternatives(classification_result)
        }
        
        # Add location-specific recommendations if location provided
        if user_location:
            recommendations['location_specific'] = self._get_location_recommendations(
                classification_result, user_location
            )
        
        return recommendations
    
    def _get_environmental_impact(self, classification_result: Dict[str, Any]) -> str:
        """Get environmental impact information for the waste type."""
        category = classification_result.get('material_category', 'non_recyclable')
        
        impact_info = {
            'plastic': 'Recycling plastic saves energy and reduces ocean pollution. Takes 450+ years to decompose.',
            'paper': 'Recycling paper saves trees and reduces landfill waste. Decomposes in 2-6 weeks.',
            'glass': 'Glass can be recycled indefinitely without quality loss. Takes 1 million years to decompose.',
            'metal': 'Recycling aluminum saves 95% of energy vs. new production. Never loses quality when recycled.',
            'organic': 'Composting reduces methane emissions and creates nutrient-rich soil.',
            'electronics': 'Contains valuable materials and toxic substances. Proper recycling prevents pollution.',
            'hazardous': 'Improper disposal can contaminate soil and water. Always use designated facilities.',
            'textile': 'Textile recycling reduces water usage and chemical pollution from new production.',
            'non_recyclable': 'Consider reducing consumption and finding reusable alternatives.'
        }
        
        return impact_info.get(category, 'Proper disposal helps protect the environment.')
    
    def _get_alternatives(self, classification_result: Dict[str, Any]) -> list:
        """Get alternative disposal or reuse suggestions."""
        category = classification_result.get('material_category', 'non_recyclable')
        item_type = classification_result.get('identified_type', '').lower()
        
        alternatives = {
            'plastic': [
                'Reuse containers for storage',
                'Upcycle into planters or organizers',
                'Return to store take-back programs'
            ],
            'paper': [
                'Use as wrapping paper or craft material',
                'Shred for compost (non-glossy paper)',
                'Donate books and magazines'
            ],
            'glass': [
                'Reuse jars for food storage',
                'Repurpose as vases or candle holders',
                'Return bottles to deposit programs'
            ],
            'metal': [
                'Reuse cans as planters',
                'Sell to scrap metal dealers',
                'Donate to metal recycling drives'
            ],
            'electronics': [
                'Donate working devices to charities',
                'Trade in for store credit',
                'Participate in manufacturer take-back programs'
            ],
            'textile': [
                'Donate to clothing charities',
                'Repurpose as cleaning rags',
                'Use for craft projects'
            ]
        }
        
        return alternatives.get(category, ['Consider reducing future consumption'])
    
    def _get_location_recommendations(self, classification_result: Dict[str, Any], 
                                    user_location: Dict[str, float]) -> Dict[str, Any]:
        """Get location-specific disposal recommendations."""
        # This would integrate with the recycling centers database
        # For now, return general location-based advice
        return {
            'nearest_facilities': 'Check the Find Centers section for nearby recycling facilities',
            'local_programs': 'Contact your local waste management authority for specific programs',
            'pickup_services': 'Consider scheduling a pickup with local waste pickers'
        }

# Utility functions for the service
def save_uploaded_image(image_file, upload_dir: str = '/tmp/uploads') -> str:
    """Save uploaded image file and return the path."""
    import os
    import uuid
    from werkzeug.utils import secure_filename
    
    # Create upload directory if it doesn't exist
    os.makedirs(upload_dir, exist_ok=True)
    
    # Generate unique filename
    filename = secure_filename(image_file.filename)
    unique_filename = f"{uuid.uuid4()}_{filename}"
    file_path = os.path.join(upload_dir, unique_filename)
    
    # Save the file
    image_file.save(file_path)
    
    return file_path