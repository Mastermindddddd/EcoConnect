import { Camera, MapPin, Users, Sparkles } from 'lucide-react'
import { Button } from './ui/button.jsx'

export default function HeroSection() {
  return (
    <section className="relative py-16 sm:py-20 lg:py-32 overflow-hidden">
      {/* Background gradient */}
      <div className="absolute inset-0 eco-gradient opacity-10"></div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative">
        <div className="text-center">
          {/* Badge */}
          <div className="inline-flex items-center px-4 py-2 rounded-full bg-primary/10 text-primary text-sm sm:text-base font-medium mb-6 sm:mb-8">
            <Sparkles className="w-4 h-4 mr-2" />
            AI-Powered Waste Management
          </div>

          {/* Main Heading */}
          <h1 className="text-3xl sm:text-5xl lg:text-6xl font-bold text-foreground leading-tight mb-4 sm:mb-6">
            Smart Waste Management
            <span className="block text-primary">for a Cleaner Future</span>
          </h1>

          {/* Subtitle */}
          <p className="text-base sm:text-lg md:text-xl text-muted-foreground max-w-2xl sm:max-w-3xl mx-auto mb-10 sm:mb-12 px-2">
            Connect households, waste pickers, and recycling centers through our AI-powered platform. 
            Identify waste types, find nearby recycling centers, and make a positive environmental impact.
          </p>

          {/* CTA Buttons */}
          <div className="flex flex-col sm:flex-row gap-4 justify-center mb-14 sm:mb-16 px-4">
            <Button 
              size="lg" 
              className="eco-button-primary text-lg sm:text-xl px-10 py-5 rounded-xl shadow-lg hover:scale-105 transition-transform duration-200"
            >
              <Camera className="w-6 h-6 mr-2" />
              Scan Waste Now
            </Button>
            <Button 
              variant="outline" 
              size="lg" 
              className="text-lg sm:text-xl px-10 py-5 rounded-xl border-2 shadow-md hover:bg-primary/10 hover:border-primary hover:text-primary transition-colors duration-200"
            >
              <MapPin className="w-6 h-6 mr-2" />
              Find Recycling Centers
            </Button>
          </div>

          {/* Feature Cards */}
          <div className="grid sm:grid-cols-2 md:grid-cols-3 gap-6 sm:gap-8 max-w-4xl mx-auto">
            <div className="eco-card p-6 text-center rounded-2xl">
              <div className="w-12 h-12 eco-gradient rounded-xl flex items-center justify-center mx-auto mb-4 shadow-md">
                <Camera className="w-6 h-6 text-white" />
              </div>
              <h3 className="text-lg font-semibold mb-2">AI Waste Identification</h3>
              <p className="text-muted-foreground text-sm sm:text-base">
                Simply take a photo of your waste and get instant identification with disposal recommendations.
              </p>
            </div>

            <div className="eco-card p-6 text-center rounded-2xl">
              <div className="w-12 h-12 eco-gradient rounded-xl flex items-center justify-center mx-auto mb-4 shadow-md">
                <MapPin className="w-6 h-6 text-white" />
              </div>
              <h3 className="text-lg font-semibold mb-2">Find Nearby Centers</h3>
              <p className="text-muted-foreground text-sm sm:text-base">
                Locate the closest recycling centers that accept your specific waste materials.
              </p>
            </div>

            <div className="eco-card p-6 text-center rounded-2xl sm:col-span-2 md:col-span-1">
              <div className="w-12 h-12 eco-gradient rounded-xl flex items-center justify-center mx-auto mb-4 shadow-md">
                <Users className="w-6 h-6 text-white" />
              </div>
              <h3 className="text-lg font-semibold mb-2">Connect Community</h3>
              <p className="text-muted-foreground text-sm sm:text-base">
                Join a community of environmentally conscious individuals and professional waste pickers.
              </p>
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}
