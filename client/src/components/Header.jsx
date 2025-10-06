import { Recycle, User, Menu } from 'lucide-react'
import { Link } from 'react-router-dom'
import { Button } from './ui/button.jsx'

export default function Header({ onMenuClick }) {
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
            <Link to="/" className="text-foreground hover:text-primary">
              Home
            </Link>
            <Link to="/recycling-centers" className="hover:text-primary">
              Recycling Centers
            </Link>
            {/*<Link to="#scan" className="text-foreground hover:text-primary transition-colors">
              Scan Waste
            </Link>*/}
            <Link to="#community" className="text-foreground hover:text-primary transition-colors">
              Community
            </Link>
            <Link to="/wastepicker-dashboard" className="text-foreground hover:text-primary transition-colors">
              For Wastepickers
            </Link>
          </nav>

          {/* User Actions */}
          <div className="flex items-center space-x-4">
            <Button variant="ghost" size="sm" className="hidden sm:flex">
              <User className="w-4 h-4 mr-2" />
              Sign In
            </Button>
            <Button size="sm" className="hidden sm:flex eco-button-primary">
              Get Started
            </Button>
            
            {/* Mobile Menu Button */}
            <Button 
              variant="ghost" 
              size="sm" 
              className="md:hidden"
              onClick={onMenuClick}
            >
              <Menu className="w-5 h-5" />
            </Button>
          </div>
        </div>
      </div>
    </header>
  )
}
