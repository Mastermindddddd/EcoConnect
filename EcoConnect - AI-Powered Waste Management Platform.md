# EcoConnect - AI-Powered Waste Management Platform

## Project Overview

EcoConnect is a comprehensive AI-powered waste management platform designed to connect households, waste pickers, and recycling centers. The platform helps users identify waste types, find nearby recycling centers, and manage waste efficiently, contributing to a cleaner and more sustainable environment.

## Key Features

1. **AI Waste Identification**
   - Upload images of waste items for instant identification
   - Get detailed information about material type and recyclability
   - Receive disposal recommendations and environmental impact information

2. **Recycling Center Locator**
   - Find nearby recycling centers based on user location
   - Filter centers by accepted material types
   - View detailed information including operating hours, contact details, and special instructions

3. **Wastepicker Dashboard**
   - Manage pickup requests and track earnings
   - View active and available pickups
   - Optimize routes for efficient waste collection

4. **Community Engagement**
   - Connect environmentally conscious individuals with professional waste pickers
   - Share waste management tips and success stories
   - Build a community focused on sustainable waste practices

## Technical Architecture

### Frontend
- **Framework**: React.js
- **State Management**: React Context API
- **Styling**: CSS with custom styling
- **Key Components**:
  - Header and Navigation
  - Hero Section
  - Waste Scanner
  - Recycling Centers Map and List
  - Wastepicker Dashboard
  - Footer

### Backend
- **Framework**: Flask (Python)
- **Database**: SQLite (development), PostgreSQL (production)
- **API Endpoints**:
  - `/api/health`: Health check endpoint
  - `/api/recycling-centers`: Get all recycling centers
  - `/api/identify-waste`: AI waste identification
  - `/api/waste-history/<user_id>`: Get user's waste identification history
  - `/api/waste-stats/<user_id>`: Get user's waste statistics
  - `/api/waste-categories`: Get supported waste categories
  - `/api/pickup-requests`: Manage pickup requests

### AI Integration
- **Waste Identification**: OpenAI Vision API for image analysis
- **Recommendation Engine**: Custom algorithm for disposal recommendations
- **Environmental Impact**: Database of environmental impact information for different waste types

## Installation and Setup

### Prerequisites
- Node.js 18+ and npm/pnpm
- Python 3.11+
- Flask and required Python packages

### Backend Setup
1. Clone the repository
2. Navigate to the backend directory: `cd ecoconnect_backend`
3. Create a virtual environment: `python -m venv venv`
4. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - Unix/MacOS: `source venv/bin/activate`
5. Install dependencies: `pip install -r requirements.txt`
6. Run the application: `python src/main.py`

### Frontend Setup
1. Navigate to the frontend directory: `cd ecoconnect_frontend`
2. Install dependencies: `pnpm install`
3. Start the development server: `pnpm run dev`
4. Build for production: `pnpm run build`

## API Documentation

### Health Check
```
GET /api/health
```
Response:
```json
{
  "status": "healthy",
  "message": "EcoConnect API is running"
}
```

### Get Recycling Centers
```
GET /api/recycling-centers
```
Response:
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "name": "GreenCycle Recycling",
      "address": "789 Green St, Chicago, IL 60601",
      "latitude": 41.8819,
      "longitude": -87.6278,
      "phone": "+1234567892",
      "email": "info@greencycle.com",
      "website": "https://greencycle.com",
      "operating_hours": {
        "monday": "8:00-17:00",
        "tuesday": "8:00-17:00",
        "wednesday": "8:00-17:00",
        "thursday": "8:00-17:00",
        "friday": "8:00-17:00",
        "saturday": "9:00-15:00",
        "sunday": "closed"
      },
      "accepted_materials": ["plastic", "paper", "glass", "metal"],
      "rating": 4.5,
      "total_reviews": 128,
      "special_instructions": "Please clean all containers before drop-off",
      "is_active": true,
      "created_at": "2025-08-16T15:05:53",
      "updated_at": "2025-08-16T15:05:53"
    }
  ],
  "total": 1
}
```

### Identify Waste
```
POST /api/identify-waste
```
Form data:
- `image`: Image file
- `user_id`: User ID (optional)
- `latitude`: User's latitude (optional)
- `longitude`: User's longitude (optional)

Response:
```json
{
  "success": true,
  "data": {
    "id": 1,
    "identified_type": "Plastic Water Bottle",
    "confidence_score": 0.95,
    "material_category": "plastic",
    "recyclable": true,
    "disposal_method": "Take to recycling center",
    "preparation_tips": "Clean containers, remove labels if possible",
    "environmental_impact": "Recycling plastic saves energy and reduces ocean pollution. Takes 450+ years to decompose.",
    "alternatives": [
      "Reuse containers for storage",
      "Upcycle into planters or organizers",
      "Return to store take-back programs"
    ],
    "image_path": "/static/uploads/12345-image.jpg",
    "recommended_center": {
      "id": 1,
      "name": "GreenCycle Recycling",
      "address": "789 Green St, Chicago, IL 60601",
      "distance": 2.3,
      "phone": "+1234567892",
      "operating_hours": {
        "monday": "8:00-17:00",
        "tuesday": "8:00-17:00",
        "wednesday": "8:00-17:00",
        "thursday": "8:00-17:00",
        "friday": "8:00-17:00",
        "saturday": "9:00-15:00",
        "sunday": "closed"
      }
    }
  },
  "message": "Waste identified successfully"
}
```

### Get Waste History
```
GET /api/waste-history/<user_id>
```
Query parameters:
- `page`: Page number (default: 1)
- `per_page`: Items per page (default: 20)

Response:
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "identified_type": "Plastic Water Bottle",
      "confidence_score": 0.95,
      "material_category": "plastic",
      "recyclable": true,
      "disposal_method": "Take to recycling center",
      "image_path": "/static/uploads/12345-image.jpg",
      "created_at": "2025-08-16T15:05:53",
      "recommended_center": {
        "id": 1,
        "name": "GreenCycle Recycling",
        "address": "789 Green St, Chicago, IL 60601"
      }
    }
  ],
  "pagination": {
    "page": 1,
    "per_page": 20,
    "total": 1,
    "pages": 1,
    "has_next": false,
    "has_prev": false
  }
}
```

### Get Waste Statistics
```
GET /api/waste-stats/<user_id>
```
Response:
```json
{
  "success": true,
  "data": {
    "total_scanned": 10,
    "recyclable_count": 8,
    "non_recyclable_count": 2,
    "category_breakdown": {
      "plastic": 5,
      "paper": 3,
      "glass": 1,
      "non_recyclable": 1
    },
    "recent_activity_30_days": 5,
    "recycling_rate": 80.0
  }
}
```

### Get Waste Categories
```
GET /api/waste-categories
```
Response:
```json
{
  "success": true,
  "data": {
    "plastic": {
      "recyclable": true,
      "color": "green",
      "disposal_method": "Take to recycling center",
      "preparation_tips": "Clean containers, remove labels if possible"
    },
    "paper": {
      "recyclable": true,
      "color": "blue",
      "disposal_method": "Take to recycling center",
      "preparation_tips": "Keep dry, remove any plastic components"
    }
  }
}
```

## Database Schema

### User
- `id`: Integer (Primary Key)
- `username`: String
- `email`: String
- `password_hash`: String
- `user_type`: String (household, wastepicker, admin)
- `created_at`: DateTime
- `updated_at`: DateTime

### RecyclingCenter
- `id`: Integer (Primary Key)
- `name`: String
- `address`: String
- `latitude`: Float
- `longitude`: Float
- `phone`: String
- `email`: String
- `website`: String
- `operating_hours`: JSON
- `accepted_materials`: JSON Array
- `rating`: Float
- `total_reviews`: Integer
- `special_instructions`: String
- `is_active`: Boolean
- `created_at`: DateTime
- `updated_at`: DateTime

### WasteItem
- `id`: Integer (Primary Key)
- `user_id`: Integer (Foreign Key)
- `image_path`: String
- `identified_type`: String
- `confidence_score`: Float
- `material_category`: String
- `recyclable`: Boolean
- `disposal_method`: String
- `recommended_center_id`: Integer (Foreign Key)
- `created_at`: DateTime

### PickupRequest
- `id`: Integer (Primary Key)
- `user_id`: Integer (Foreign Key)
- `wastepicker_id`: Integer (Foreign Key)
- `status`: String (pending, accepted, in_progress, completed, cancelled)
- `address`: String
- `latitude`: Float
- `longitude`: Float
- `waste_description`: String
- `waste_types`: JSON Array
- `estimated_weight`: Float
- `price`: Float
- `pickup_date`: DateTime
- `created_at`: DateTime
- `updated_at`: DateTime

## Deployment

### Backend Deployment
The backend is deployed at: https://zmhqivcm8ejq.manus.space

### Frontend Deployment
The frontend is packaged and ready for deployment.

## Future Enhancements

1. **Mobile Applications**
   - Develop native mobile apps for iOS and Android
   - Implement push notifications for pickup requests and updates

2. **Advanced AI Features**
   - Improve waste identification accuracy with more training data
   - Add multi-item identification in a single image
   - Implement waste volume estimation

3. **Gamification**
   - Add points and rewards for recycling activities
   - Create leaderboards and challenges
   - Implement badges and achievements

4. **Integration with Municipal Services**
   - Connect with city waste management systems
   - Integrate with government recycling programs
   - Provide real-time updates on municipal waste collection schedules

5. **Analytics Dashboard**
   - Enhanced data visualization for waste statistics
   - Community-wide impact metrics
   - Environmental benefit calculations

## Conclusion

EcoConnect provides a comprehensive solution for waste management challenges by connecting key stakeholders and leveraging AI technology. The platform helps users make informed decisions about waste disposal, supports waste pickers in optimizing their operations, and promotes sustainable waste management practices.

## Contact

For more information or support, please contact:
- Email: hello@ecoconnect.com
- Phone: +1 (555) 123-4567
- Address: 123 Green Street, Chicago, IL 60601

