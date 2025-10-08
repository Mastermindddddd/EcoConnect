import { Recycle, User, Menu } from 'lucide-react'
import { Link, useNavigate } from 'react-router-dom'
import { Button } from './ui/button.jsx'
import { useEffect, useState } from 'react'
import axios from 'axios'

export default function Header({ onMenuClick }) {
  const navigate = useNavigate()
  const [user, setUser] = useState(JSON.parse(localStorage.getItem("user")) || null)

  const handleLogout = async () => {
    await axios.post("http://localhost:5000/api/logout", {}, { withCredentials: true })
    localStorage.removeItem("user")
    setUser(null)
    navigate("/login")
  }

  useEffect(() => {
    const checkSession = async () => {
      try {
        const res = await axios.get("http://localhost:5000/api/session", { withCredentials: true })
        if (res.data.logged_in) {
          setUser(res.data.user)
          localStorage.setItem("user", JSON.stringify(res.data.user))
        } else {
          setUser(null)
          localStorage.removeItem("user")
        }
      } catch (error) {
        console.error("Session check failed:", error)
      }
    }
    checkSession()
  }, [])

  return (
    <header className="bg-white border-b border-border sticky top-0 z-50">
      <div className="max-w-8xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo and Brand */}
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 eco-gradient rounded-xl flex items-center justify-center">
              <Recycle className="w-6 h-6 text-white" />
            </div>
            <div>
              <h2 className="text-md font-bold text-foreground">EcoConnect</h2>
              <p className="text-xs text-muted-foreground">Smart Waste Management</p>
            </div>
          </div>

          {/* Desktop Navigation */}
          <nav className="hidden md:flex items-center space-x-8">
            <Link to="/" className="text-foreground hover:text-primary">Home</Link>
            <Link to="/recycling-centers" className="hover:text-primary">Recycling Centers</Link>
            <Link to="#community" className="text-foreground hover:text-primary">Community</Link>
            <Link to="/wastepicker-dashboard" className="text-foreground hover:text-primary">For Wastepickers</Link>
          </nav>

          {/* User Actions */}
          <div className="flex items-center space-x-4">
            {user ? (
              <>
                <span className="text-sm text-gray-700">Hello, {user.first_name || user.username}</span>
                <Button size="sm" className="hidden sm:flex bg-red-500 hover:bg-red-600" onClick={handleLogout}>
                  Logout
                </Button>
              </>
            ) : (
              <>
                <Link to="/login">
                  <Button variant="ghost" size="sm" className="hidden sm:flex">
                    <User className="w-4 h-4 mr-2" />
                    Sign In
                  </Button>
                </Link>
                <Link to="/registration">
                  <Button size="sm" className="hidden sm:flex eco-button-primary">Get Started</Button>
                </Link>
              </>
            )}

            {/* Mobile Menu Button */}
            <Button variant="ghost" size="sm" className="md:hidden" onClick={onMenuClick}>
              <Menu className="w-5 h-5" />
            </Button>
          </div>
        </div>
      </div>
    </header>
  )
}
