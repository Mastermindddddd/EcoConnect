import os
import uuid
import random
from typing import Dict, Any, Optional

class MockAIWasteClassifier:
    """
    Mock AI-powered waste classification service for deployment.
    Provides realistic mock responses without requiring OpenAI API.
    """
    
    def __init__(self):
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
        
        # Mock classification results
        self.mock_results = [
            {
                'identified_type': 'Plastic Water Bottle',
                'confidence_score': 0.95,
                'material_category': 'plastic',
                'specific_material': 'PET plastic',
                'condition': 'Good condition, clean',
                'size_estimate': 'Medium',
                'additional_notes': 'Standard single-use water bottle'
            },
            {
                'identified_type': 'Aluminum Can',
                'confidence_score': 0.92,
                'material_category': 'metal',
                'specific_material': 'Aluminum',
                'condition': 'Good condition',
                'size_estimate': 'Small',
                'additional_notes': 'Beverage can, recyclable'
            },
            {
                'identified_type': 'Paper Cup',
                'confidence_score': 0.88,
                'material_category': 'paper',
                'specific_material': 'Coated paper',
                'condition': 'Used, some staining',
                'size_estimate': 'Small',
                'additional_notes': 'Coffee cup with plastic lining'
            },
            {
                'identified_type': 'Glass Jar',
                'confidence_score': 0.94,
                'material_category': 'glass',
                'specific_material': 'Clear glass',
                'condition': 'Good condition',
                'size_estimate': 'Medium',
                'additional_notes': 'Food jar with metal lid'
            },
            {
                'identified_type': 'Food Waste',
                'confidence_score': 0.85,
                'material_category': 'organic',
                'specific_material': 'Organic matter',
                'condition': 'Fresh',
                'size_estimate': 'Small',
                'additional_notes': 'Fruit peels and vegetable scraps'
            },
            {
                'identified_type': 'Old Smartphone',
                'confidence_score': 0.91,
                'material_category': 'electronics',
                'specific_material': 'Mixed electronics',
                'condition': 'Used, functional',
                'size_estimate': 'Small',
                'additional_notes': 'Contains valuable materials and battery'
            }
        ]
    
    def classify_waste(self, image_path: str) -> Dict[str, Any]:
        """
        Mock classify waste from image.
        
        Args:
            image_path: Path to the waste image file
            
        Returns:
            Dictionary containing mock classification results
        """
        try:
            # Select a random mock result
            classification_result = random.choice(self.mock_results).copy()
            
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