import { useState, useEffect } from 'react'
import { MapPin, Phone, Clock, Star, Navigation, Filter } from 'lucide-react'
import { Button } from '../components/ui/button.jsx'
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card.jsx'
import { Badge } from '../components/ui/badge.jsx'

export default function RecyclingCenters() {
  const [centers, setCenters] = useState([])
  const [filteredCenters, setFilteredCenters] = useState([])
  const [selectedMaterial, setSelectedMaterial] = useState('all')
  const [userLocation, setUserLocation] = useState(null)

  // Mock recycling centers data
  const mockCenters = [
    {
      id: 1,
      name: 'GreenCycle Recycling',
      address: '789 Green St, Chicago, IL 60601',
      latitude: 41.8819,
      longitude: -87.6278,
      phone: '+1234567892',
      email: 'info@greencycle.com',
      website: 'https://greencycle.com',
      operating_hours: {
        monday: '8:00-17:00',
        tuesday: '8:00-17:00',
        wednesday: '8:00-17:00',
        thursday: '8:00-17:00',
        friday: '8:00-17:00',
        saturday: '9:00-15:00',
        sunday: 'closed'
      },
      accepted_materials: ['plastic', 'paper', 'glass', 'metal'],
      special_instructions: 'Please clean all containers before drop-off',
      rating: 4.5,
      total_reviews: 128,
      distance: 2.3
    },
    {
      id: 2,
      name: 'Central Waste Solutions',
      address: '321 Recycle Blvd, Chicago, IL 60602',
      latitude: 41.8756,
      longitude: -87.6244,
      phone: '+1234567893',
      email: 'contact@centralwaste.com',
      website: 'https://centralwaste.com',
      operating_hours: {
        monday: '7:00-18:00',
        tuesday: '7:00-18:00',
        wednesday: '7:00-18:00',
        thursday: '7:00-18:00',
        friday: '7:00-18:00',
        saturday: '8:00-16:00',
        sunday: '10:00-14:00'
      },
      accepted_materials: ['plastic', 'paper', 'glass', 'metal', 'electronics'],
      special_instructions: 'Electronics accepted on weekends only',
      rating: 4.2,
      total_reviews: 89,
      distance: 1.8
    },
    {
      id: 3,
      name: 'EcoHub Recycling Center',
      address: '555 Earth Way, Chicago, IL 60603',
      latitude: 41.8892,
      longitude: -87.6189,
      phone: '+1234567894',
      email: 'hello@ecohub.com',
      website: 'https://ecohub.com',
      operating_hours: {
        monday: '9:00-16:00',
        tuesday: '9:00-16:00',
        wednesday: '9:00-16:00',
        thursday: '9:00-16:00',
        friday: '9:00-16:00',
        saturday: '10:00-15:00',
        sunday: 'closed'
      },
      accepted_materials: ['plastic', 'paper', 'organic', 'hazardous'],
      special_instructions: 'Hazardous waste by appointment only',
      rating: 4.8,
      total_reviews: 203,
      distance: 3.1
    }
  ]

  const materialTypes = ['all', 'plastic', 'paper', 'glass', 'metal', 'electronics', 'organic', 'hazardous']

  useEffect(() => {
    // Simulate loading centers
    setCenters(mockCenters)
    setFilteredCenters(mockCenters)
  }, [])

  useEffect(() => {
    // Filter centers by material type
    if (selectedMaterial === 'all') {
      setFilteredCenters(centers)
    } else {
      const filtered = centers.filter(center => 
        center.accepted_materials.includes(selectedMaterial)
      )
      setFilteredCenters(filtered)
    }
  }, [selectedMaterial, centers])

  const getCurrentLocation = () => {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          setUserLocation({
            latitude: position.coords.latitude,
            longitude: position.coords.longitude
          })
        },
        (error) => {
          console.error('Error getting location:', error)
        }
      )
    }
  }

  const formatOperatingHours = (hours) => {
    const days = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']
    const today = days[new Date().getDay()]
    const todayHours = hours[today]
    return todayHours || 'Closed'
  }

  const renderStars = (rating) => {
    const fullStars = Math.floor(rating)
    const hasHalfStar = rating % 1 !== 0
    const stars = []

    for (let i = 0; i < fullStars; i++) {
      stars.push(<Star key={i} className="w-4 h-4 fill-yellow-400 text-yellow-400" />)
    }
    
    if (hasHalfStar) {
      stars.push(<Star key="half" className="w-4 h-4 fill-yellow-400/50 text-yellow-400" />)
    }

    return stars
  }

  return (
    <section id="locate" className="py-20">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-12">
          <h2 className="text-3xl font-bold text-foreground mb-4">
            Find Recycling Centers
          </h2>
          <p className="text-lg text-muted-foreground">
            Locate nearby recycling centers that accept your specific waste materials
          </p>
        </div>

        {/* Filters */}
        <div className="mb-8">
          <div className="flex flex-col sm:flex-row gap-4 items-center justify-between">
            <div className="flex items-center space-x-4">
              <Filter className="w-5 h-5 text-muted-foreground" />
              <span className="text-sm font-medium text-foreground">Filter by material:</span>
              <div className="flex flex-wrap gap-2">
                {materialTypes.map(material => (
                  <Button
                    key={material}
                    variant={selectedMaterial === material ? "default" : "outline"}
                    size="sm"
                    onClick={() => setSelectedMaterial(material)}
                    className="capitalize"
                  >
                    {material}
                  </Button>
                ))}
              </div>
            </div>
            
            <Button 
              variant="outline" 
              onClick={getCurrentLocation}
              className="flex items-center"
            >
              <Navigation className="w-4 h-4 mr-2" />
              Use My Location
            </Button>
          </div>
        </div>

        {/* Centers Grid */}
        <div className="grid lg:grid-cols-2 xl:grid-cols-3 gap-6">
          {filteredCenters.map(center => (
            <Card key={center.id} className="hover:shadow-lg transition-shadow">
              <CardHeader>
                <div className="flex justify-between items-start">
                  <div>
                    <CardTitle className="text-lg">{center.name}</CardTitle>
                    <div className="flex items-center mt-2">
                      <div className="flex items-center mr-4">
                        {renderStars(center.rating)}
                        <span className="ml-2 text-sm text-muted-foreground">
                          {center.rating} ({center.total_reviews})
                        </span>
                      </div>
                      {center.distance && (
                        <span className="text-sm font-medium text-primary">
                          {center.distance} km
                        </span>
                      )}
                    </div>
                  </div>
                </div>
              </CardHeader>
              
              <CardContent className="space-y-4">
                {/* Address */}
                <div className="flex items-start space-x-3">
                  <MapPin className="w-5 h-5 text-muted-foreground mt-0.5" />
                  <div>
                    <p className="text-sm text-foreground">{center.address}</p>
                  </div>
                </div>

                {/* Phone */}
                <div className="flex items-center space-x-3">
                  <Phone className="w-5 h-5 text-muted-foreground" />
                  <p className="text-sm text-foreground">{center.phone}</p>
                </div>

                {/* Operating Hours */}
                <div className="flex items-center space-x-3">
                  <Clock className="w-5 h-5 text-muted-foreground" />
                  <p className="text-sm text-foreground">
                    Today: {formatOperatingHours(center.operating_hours)}
                  </p>
                </div>

                {/* Accepted Materials */}
                <div>
                  <p className="text-sm font-medium text-foreground mb-2">Accepted Materials:</p>
                  <div className="flex flex-wrap gap-2">
                    {center.accepted_materials.map(material => (
                      <Badge key={material} variant="secondary" className="capitalize">
                        {material}
                      </Badge>
                    ))}
                  </div>
                </div>

                {/* Special Instructions */}
                {center.special_instructions && (
                  <div className="bg-muted/50 p-3 rounded-lg">
                    <p className="text-xs text-muted-foreground">
                      <strong>Note:</strong> {center.special_instructions}
                    </p>
                  </div>
                )}

                {/* Actions */}
                <div className="flex space-x-2 pt-4">
                  <Button size="sm" className="flex-1 eco-button-primary">
                    <Navigation className="w-4 h-4 mr-2" />
                    Directions
                  </Button>
                  <Button variant="outline" size="sm" className="flex-1">
                    <Phone className="w-4 h-4 mr-2" />
                    Call
                  </Button>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>

        {filteredCenters.length === 0 && (
          <div className="text-center py-12">
            <MapPin className="w-12 h-12 mx-auto mb-4 text-muted-foreground opacity-50" />
            <p className="text-foreground font-medium mb-2">No centers found</p>
            <p className="text-muted-foreground">
              Try selecting a different material type or check back later.
            </p>
          </div>
        )}
      </div>
    </section>
  )
}
