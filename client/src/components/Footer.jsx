import { Recycle, Mail, Phone, MapPin, Github, Twitter, Linkedin } from 'lucide-react'

export default function Footer() {
  return (
    <footer className="bg-muted/50 border-t border-border">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          {/* Brand */}
          <div className="col-span-1 md:col-span-2">
            <div className="flex items-center space-x-3 mb-4">
              <div className="w-10 h-10 eco-gradient rounded-xl flex items-center justify-center">
                <Recycle className="w-6 h-6 text-white" />
              </div>
              <div>
                <h3 className="text-xl font-bold text-foreground">EcoConnect</h3>
                <p className="text-sm text-muted-foreground">Smart Waste Management</p>
              </div>
            </div>
            <p className="text-muted-foreground mb-6 max-w-md">
              Connecting households, waste pickers, and recycling centers through AI-powered 
              waste management solutions for a cleaner, more sustainable future.
            </p>
            <div className="flex space-x-4">
              <a href="#" className="text-muted-foreground hover:text-primary transition-colors">
                <Github className="w-5 h-5" />
              </a>
              <a href="#" className="text-muted-foreground hover:text-primary transition-colors">
                <Twitter className="w-5 h-5" />
              </a>
              <a href="#" className="text-muted-foreground hover:text-primary transition-colors">
                <Linkedin className="w-5 h-5" />
              </a>
            </div>
          </div>

          {/* Quick Links */}
          <div>
            <h4 className="font-semibold text-foreground mb-4">Quick Links</h4>
            <ul className="space-y-3">
              <li>
                <a href="#home" className="text-muted-foreground hover:text-primary transition-colors">
                  Home
                </a>
              </li>
              <li>
                <a href="#scan" className="text-muted-foreground hover:text-primary transition-colors">
                  Waste Scanner
                </a>
              </li>
              <li>
                <a href="#locate" className="text-muted-foreground hover:text-primary transition-colors">
                  Find Centers
                </a>
              </li>
              <li>
                <a href="#wastepicker" className="text-muted-foreground hover:text-primary transition-colors">
                  For Wastepickers
                </a>
              </li>
              <li>
                <a href="#community" className="text-muted-foreground hover:text-primary transition-colors">
                  Community
                </a>
              </li>
            </ul>
          </div>

          {/* Contact Info */}
          <div>
            <h4 className="font-semibold text-foreground mb-4">Contact</h4>
            <ul className="space-y-3">
              <li className="flex items-center space-x-3">
                <Mail className="w-4 h-4 text-muted-foreground" />
                <span className="text-muted-foreground">hello@ecoconnect.com</span>
              </li>
              <li className="flex items-center space-x-3">
                <Phone className="w-4 h-4 text-muted-foreground" />
                <span className="text-muted-foreground">+1 (555) 123-4567</span>
              </li>
              <li className="flex items-start space-x-3">
                <MapPin className="w-4 h-4 text-muted-foreground mt-0.5" />
                <span className="text-muted-foreground">
                  123 Green Street<br />
                  Chicago, IL 60601
                </span>
              </li>
            </ul>
          </div>
        </div>

        {/* Bottom Bar */}
        <div className="border-t border-border mt-12 pt-8 flex flex-col sm:flex-row justify-between items-center">
          <p className="text-muted-foreground text-sm">
            © 2024 EcoConnect. All rights reserved.
          </p>
          <div className="flex space-x-6 mt-4 sm:mt-0">
            <a href="#" className="text-muted-foreground hover:text-primary text-sm transition-colors">
              Privacy Policy
            </a>
            <a href="#" className="text-muted-foreground hover:text-primary text-sm transition-colors">
              Terms of Service
            </a>
            <a href="#" className="text-muted-foreground hover:text-primary text-sm transition-colors">
              Cookie Policy
            </a>
          </div>
        </div>
      </div>
    </footer>
  )
}