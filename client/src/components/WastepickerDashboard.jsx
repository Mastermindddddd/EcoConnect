import { useState, useEffect } from 'react'
import { DollarSign, MapPin, Clock, CheckCircle, TrendingUp, Package } from 'lucide-react'
import { Button } from './ui/button.jsx'
import { Card, CardContent, CardHeader, CardTitle } from './ui/card.jsx'
import { Badge } from './ui/badge.jsx'

export default function WastepickerDashboard() {
  const [stats, setStats] = useState({})
  const [activePickups, setActivePickups] = useState([])
  const [availablePickups, setAvailablePickups] = useState([])

  // Mock data
  const mockStats = {
    total_earnings: 650.75,
    completed_pickups: 42,
    active_pickups: 3,
    total_weight_collected: 125.5,
    recent_activity_30_days: 15,
    completion_rate: 93.33
  }

  const mockActivePickups = [
    {
      id: 1,
      pickup_address: '1234 W Elm St, Chicago, IL',
      waste_category: 'recyclable',
      estimated_weight: 2.5,
      payment_amount: 15.0,
      status: 'in_progress',
      distance: 0.8,
      requester: { first_name: 'John', last_name: 'D.' }
    },
    {
      id: 2,
      pickup_address: '7566 E Main St, Chicago, IL',
      waste_category: 'mixed',
      estimated_weight: 4.2,
      payment_amount: 25.0,
      status: 'accepted',
      distance: 1.3,
      requester: { first_name: 'Sarah', last_name: 'M.' }
    },
    {
      id: 3,
      pickup_address: 'B520 N 30th Ave, Chicago, IL',
      waste_category: 'organic',
      estimated_weight: 3.8,
      payment_amount: 20.0,
      status: 'accepted',
      distance: 3.2,
      requester: { first_name: 'Mike', last_name: 'R.' }
    }
  ]

  const mockAvailablePickups = [
    {
      id: 4,
      pickup_address: '456 Oak Avenue, Chicago, IL',
      waste_category: 'recyclable',
      estimated_weight: 3.0,
      payment_amount: 18.0,
      status: 'pending',
      distance: 2.1,
      requester: { first_name: 'Lisa', last_name: 'K.' },
      created_at: '2024-08-05T10:30:00Z'
    },
    {
      id: 5,
      pickup_address: '789 Pine Street, Chicago, IL',
      waste_category: 'mixed',
      estimated_weight: 5.5,
      payment_amount: 30.0,
      status: 'pending',
      distance: 1.7,
      requester: { first_name: 'David', last_name: 'W.' },
      created_at: '2024-08-05T09:15:00Z'
    }
  ]

  useEffect(() => {
    setStats(mockStats)
    setActivePickups(mockActivePickups)
    setAvailablePickups(mockAvailablePickups)
  }, [])

  const handleAcceptPickup = (pickupId) => {
    const pickup = availablePickups.find(p => p.id === pickupId)
    if (pickup) {
      pickup.status = 'accepted'
      setActivePickups([...activePickups, pickup])
      setAvailablePickups(availablePickups.filter(p => p.id !== pickupId))
    }
  }

  const handleUpdateStatus = (pickupId, newStatus) => {
    setActivePickups(activePickups.map(pickup => 
      pickup.id === pickupId ? { ...pickup, status: newStatus } : pickup
    ))
  }

  const getStatusColor = (status) => {
    switch (status) {
      case 'pending': return 'bg-yellow-100 text-yellow-800'
      case 'accepted': return 'bg-blue-100 text-blue-800'
      case 'in_progress': return 'bg-orange-100 text-orange-800'
      case 'completed': return 'bg-green-100 text-green-800'
      default: return 'bg-gray-100 text-gray-800'
    }
  }

  const getCategoryColor = (category) => {
    switch (category) {
      case 'recyclable': return 'bg-green-100 text-green-800'
      case 'organic': return 'bg-amber-100 text-amber-800'
      case 'mixed': return 'bg-purple-100 text-purple-800'
      case 'hazardous': return 'bg-red-100 text-red-800'
      default: return 'bg-gray-100 text-gray-800'
    }
  }

  return (
    <section id="wastepicker" className="py-20 bg-muted/30">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-12">
          <h2 className="text-3xl font-bold text-foreground mb-4">
            Wastepicker Dashboard
          </h2>
          <p className="text-lg text-muted-foreground">
            Manage your pickups, track earnings, and optimize your routes
          </p>
        </div>

        {/* Stats Overview */}
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <Card>
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-muted-foreground">Total Earnings</p>
                  <p className="text-2xl font-bold text-foreground">${stats.total_earnings}</p>
                </div>
                <div className="w-12 h-12 eco-gradient rounded-xl flex items-center justify-center">
                  <DollarSign className="w-6 h-6 text-white" />
                </div>
              </div>
              <div className="flex items-center mt-2">
                <TrendingUp className="w-4 h-4 text-green-600 mr-1" />
                <span className="text-sm text-green-600">+12% this month</span>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-muted-foreground">Active Pickups</p>
                  <p className="text-2xl font-bold text-foreground">{stats.active_pickups}</p>
                </div>
                <div className="w-12 h-12 bg-accent rounded-xl flex items-center justify-center">
                  <Package className="w-6 h-6 text-white" />
                </div>
              </div>
              <p className="text-sm text-muted-foreground mt-2">In progress</p>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-muted-foreground">Completed</p>
                  <p className="text-2xl font-bold text-foreground">{stats.completed_pickups}</p>
                </div>
                <div className="w-12 h-12 bg-green-500 rounded-xl flex items-center justify-center">
                  <CheckCircle className="w-6 h-6 text-white" />
                </div>
              </div>
              <p className="text-sm text-muted-foreground mt-2">{stats.completion_rate}% success rate</p>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-muted-foreground">Weight Collected</p>
                  <p className="text-2xl font-bold text-foreground">{stats.total_weight_collected} kg</p>
                </div>
                <div className="w-12 h-12 bg-orange-500 rounded-xl flex items-center justify-center">
                  <Package className="w-6 h-6 text-white" />
                </div>
              </div>
              <p className="text-sm text-muted-foreground mt-2">Total collected</p>
            </CardContent>
          </Card>
        </div>

        <div className="grid lg:grid-cols-2 gap-8">
          {/* Active Pickups */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center">
                <Clock className="w-5 h-5 mr-2" />
                Active Pickups ({activePickups.length})
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {activePickups.map(pickup => (
                  <div key={pickup.id} className="border border-border rounded-lg p-4">
                    <div className="flex justify-between items-start mb-3">
                      <div className="flex-1">
                        <p className="font-medium text-foreground">{pickup.pickup_address}</p>
                        <p className="text-sm text-muted-foreground">
                          {pickup.requester.first_name} {pickup.requester.last_name} • {pickup.distance} mi
                        </p>
                      </div>
                      <div className="text-right">
                        <p className="font-semibold text-foreground">${pickup.payment_amount}</p>
                        <p className="text-sm text-muted-foreground">{pickup.estimated_weight} kg</p>
                      </div>
                    </div>
                    
                    <div className="flex items-center justify-between">
                      <div className="flex space-x-2">
                        <Badge className={getStatusColor(pickup.status)}>
                          {pickup.status.replace('_', ' ')}
                        </Badge>
                        <Badge className={getCategoryColor(pickup.waste_category)}>
                          {pickup.waste_category}
                        </Badge>
                      </div>
                      
                      <div className="flex space-x-2">
                        {pickup.status === 'accepted' && (
                          <Button 
                            size="sm" 
                            onClick={() => handleUpdateStatus(pickup.id, 'in_progress')}
                          >
                            Start Pickup
                          </Button>
                        )}
                        {pickup.status === 'in_progress' && (
                          <Button 
                            size="sm" 
                            onClick={() => handleUpdateStatus(pickup.id, 'completed')}
                            className="bg-green-600 hover:bg-green-700"
                          >
                            Complete
                          </Button>
                        )}
                      </div>
                    </div>
                  </div>
                ))}
                
                {activePickups.length === 0 && (
                  <div className="text-center py-8 text-muted-foreground">
                    <Package className="w-12 h-12 mx-auto mb-4 opacity-50" />
                    <p>No active pickups</p>
                  </div>
                )}
              </div>
            </CardContent>
          </Card>

          {/* Available Pickups */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center">
                <MapPin className="w-5 h-5 mr-2" />
                Available Pickups ({availablePickups.length})
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {availablePickups.map(pickup => (
                  <div key={pickup.id} className="border border-border rounded-lg p-4">
                    <div className="flex justify-between items-start mb-3">
                      <div className="flex-1">
                        <p className="font-medium text-foreground">{pickup.pickup_address}</p>
                        <p className="text-sm text-muted-foreground">
                          {pickup.requester.first_name} {pickup.requester.last_name} • {pickup.distance} mi
                        </p>
                      </div>
                      <div className="text-right">
                        <p className="font-semibold text-foreground">${pickup.payment_amount}</p>
                        <p className="text-sm text-muted-foreground">{pickup.estimated_weight} kg</p>
                      </div>
                    </div>
                    
                    <div className="flex items-center justify-between">
                      <div className="flex space-x-2">
                        <Badge className={getCategoryColor(pickup.waste_category)}>
                          {pickup.waste_category}
                        </Badge>
                        <span className="text-sm text-muted-foreground">
                          Posted {new Date(pickup.created_at).toLocaleDateString()}
                        </span>
                      </div>
                      
                      <Button 
                        size="sm" 
                        onClick={() => handleAcceptPickup(pickup.id)}
                        className="eco-button-primary"
                      >
                        Accept
                      </Button>
                    </div>
                  </div>
                ))}
                
                {availablePickups.length === 0 && (
                  <div className="text-center py-8 text-muted-foreground">
                    <MapPin className="w-12 h-12 mx-auto mb-4 opacity-50" />
                    <p>No available pickups</p>
                    <p className="text-sm mt-2">Check back later for new requests</p>
                  </div>
                )}
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Quick Actions */}
        <div className="mt-8 text-center">
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Button size="lg" className="eco-button-primary">
              <MapPin className="w-5 h-5 mr-2" />
              Optimize Route
            </Button>
            <Button variant="outline" size="lg">
              <TrendingUp className="w-5 h-5 mr-2" />
              View Analytics
            </Button>
          </div>
        </div>
      </div>
    </section>
  )
}
