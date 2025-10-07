import { useState } from 'react'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Header from './components/Header.jsx'
import HeroSection from './components/HeroSection.jsx'
import WasteScanner from './components/WasteScanner.jsx'
import RecyclingCenters from './components/RecyclingCenters.jsx'
import WastepickerDashboard from './components/WastepickerDashboard.jsx'
import Footer from './components/Footer.jsx'
import RegistrationForm from './pages/RegistrationForm.jsx'
import LoginForm from './pages/LoginForm.jsx'
import './App.css'

function App() {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)

  const handleMenuClick = () => {
    setMobileMenuOpen(!mobileMenuOpen)
  }

  return (
    <Router>
      <div className="min-h-screen bg-background">
        <Header onMenuClick={handleMenuClick} />

        <main>
          <Routes>
            {/* Home page */}
            <Route
              path="/"
              element={
                <>
                  <HeroSection />
                  <WasteScanner />
                </>
              }
            />

            {/* Recycling centers page */}
            <Route path="/wastepicker-dashboard" element={<WastepickerDashboard />} />
            <Route path="/recycling-centers" element={<RecyclingCenters />} />
            <Route path="/registration" element={<RegistrationForm />} />
            <Route path="/login" element={<LoginForm />} />
          </Routes>
        </main>

        <Footer />
      </div>
    </Router>
  )
}

export default App
