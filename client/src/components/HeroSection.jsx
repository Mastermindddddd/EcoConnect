import { Camera, MapPin, Users, Sparkles } from "lucide-react"
import { Button } from "./ui/button"

export default function HeroSection() {
  return (
    <section className="relative py-12 sm:py-16 lg:py-24 xl:py-32 overflow-hidden">
      {/* Background gradient */}
      <div className="absolute inset-0 eco-gradient opacity-10"></div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative">
        <div className="text-center">
          {/* Badge */}
          <div className="inline-flex items-center px-3 py-1.5 sm:px-4 sm:py-2 rounded-full bg-primary/10 text-primary text-xs sm:text-sm font-medium mb-4 sm:mb-6 lg:mb-8">
            <Sparkles className="w-3 h-3 sm:w-4 sm:h-4 mr-1.5 sm:mr-2 flex-shrink-0" />
            <span className="whitespace-nowrap">AI-Powered Waste Management</span>
          </div>

          {/* Main Heading */}
          <h1 className="text-2xl sm:text-3xl md:text-5xl lg:text-6xl font-bold text-foreground leading-tight mb-3 sm:mb-4 lg:mb-6 px-2 text-balance">
            Smart Waste Management
            <span className="block text-primary mt-1 sm:mt-2">for a Cleaner Future</span>
          </h1>

          {/* Subtitle */}
          <p className="text-sm sm:text-base md:text-lg lg:text-xl text-muted-foreground max-w-xl sm:max-w-2xl lg:max-w-3xl mx-auto mb-8 sm:mb-10 lg:mb-12 px-4 sm:px-6 text-pretty leading-relaxed">
            Connect households, waste pickers, and recycling centers through our AI-powered platform. Identify waste
            types, find nearby recycling centers, and make a positive environmental impact.
          </p>

          {/* CTA Buttons */}
          <div className="flex flex-col sm:flex-row gap-4 justify-center mb-10 sm:mb-12 lg:mb-16 px-4 sm:px-0">
            <Button
              size="lg"
              className="eco-button-primary text-lg sm:text-lg lg:text-xl px-8 py-7 sm:px-8 sm:py-6 lg:px-10 rounded-2xl shadow-xl hover:shadow-2xl hover:scale-[1.02] active:scale-[0.98] transition-all duration-200 w-full sm:w-auto font-semibold"
            >
              <Camera className="w-6 h-6 sm:w-6 sm:h-6 mr-2.5 flex-shrink-0" />
              <span>Scan Waste Now</span>
            </Button>
            <Button
              variant="outline"
              size="lg"
              className="text-lg sm:text-lg lg:text-xl px-8 py-7 sm:px-8 sm:py-6 lg:px-10 rounded-2xl border-2 shadow-lg hover:shadow-xl hover:bg-primary/10 hover:border-primary hover:text-primary hover:scale-[1.02] active:scale-[0.98] transition-all duration-200 w-full sm:w-auto bg-background/80 backdrop-blur-sm font-semibold"
            >
              <MapPin className="w-6 h-6 sm:w-6 sm:h-6 mr-2.5 flex-shrink-0" />
              <span>Find Centers</span>
            </Button>
          </div>

          {/* Feature Cards */}
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-6 lg:gap-8 max-w-5xl mx-auto px-2 sm:px-0">
            {/* AI Waste Identification */}
            <div className="eco-card p-5 sm:p-6 text-center rounded-2xl hover:shadow-lg transition-shadow duration-200">
              <div className="w-10 h-10 sm:w-12 sm:h-12 eco-gradient rounded-xl flex items-center justify-center mx-auto mb-3 sm:mb-4 shadow-md">
                <Camera className="w-5 h-5 sm:w-6 sm:h-6 text-white" />
              </div>
              <h3 className="text-base sm:text-lg font-semibold mb-2 text-balance">AI Waste Identification</h3>
              <p className="text-muted-foreground text-xs sm:text-sm lg:text-base text-pretty leading-relaxed">
                Simply take a photo of your waste and get instant identification with disposal recommendations.
              </p>
            </div>

            {/* Find Nearby Centers */}
            <div className="eco-card p-5 sm:p-6 text-center rounded-2xl hover:shadow-lg transition-shadow duration-200">
              <div className="w-10 h-10 sm:w-12 sm:h-12 eco-gradient rounded-xl flex items-center justify-center mx-auto mb-3 sm:mb-4 shadow-md">
                <MapPin className="w-5 h-5 sm:w-6 sm:h-6 text-white" />
              </div>
              <h3 className="text-base sm:text-lg font-semibold mb-2 text-balance">Find Nearby Centers</h3>
              <p className="text-muted-foreground text-xs sm:text-sm lg:text-base text-pretty leading-relaxed">
                Locate the closest recycling centers that accept your specific waste materials.
              </p>
            </div>

            {/* Connect Community */}
            <div className="eco-card p-5 sm:p-6 text-center rounded-2xl hover:shadow-lg transition-shadow duration-200 sm:col-span-2 lg:col-span-1">
              <div className="w-10 h-10 sm:w-12 sm:h-12 eco-gradient rounded-xl flex items-center justify-center mx-auto mb-3 sm:mb-4 shadow-md">
                <Users className="w-5 h-5 sm:w-6 sm:h-6 text-white" />
              </div>
              <h3 className="text-base sm:text-lg font-semibold mb-2 text-balance">Connect Community</h3>
              <p className="text-muted-foreground text-xs sm:text-sm lg:text-base text-pretty leading-relaxed">
                Join a community of environmentally conscious individuals and professional waste pickers.
              </p>
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}
