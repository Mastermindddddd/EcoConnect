import { useState } from 'react'
import Header from './components/Header.jsx'
import HeroSection from './components/HeroSection.jsx'
import WasteScanner from './components/WasteScanner.jsx'
import RecyclingCenters from './components/RecyclingCenters.jsx'
import WastepickerDashboard from './components/WastepickerDashboard.jsx'
import Footer from './components/Footer.jsx'
import './App.css'

function App() {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)

  const handleMenuClick = () => {
    setMobileMenuOpen(!mobileMenuOpen)
  }

  return (
    <div className="min-h-screen bg-background">
      <Header onMenuClick={handleMenuClick} />
      
      <main>
        <HeroSection />
        <WasteScanner />
        <RecyclingCenters />
        <WastepickerDashboard />
      </main>
      
      <Footer />
    </div>
  )
}

export default App
