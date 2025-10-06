import { useState, useRef } from 'react'
import { Camera, Upload, Loader2, CheckCircle, MapPin, Info } from 'lucide-react'
import { Button } from './ui/button.jsx'
import { Card, CardContent, CardHeader, CardTitle } from './ui/card.jsx'

export default function WasteScanner() {
  const [isScanning, setIsScanning] = useState(false)
  const [scanResult, setScanResult] = useState(null)
  const [selectedImage, setSelectedImage] = useState(null)
  const fileInputRef = useRef(null)

  // Mock scan function - in production this would call the backend API
  const mockScan = (imageFile) => {
    return new Promise((resolve) => {
      setTimeout(() => {
        const mockResults = [
          {
            identified_type: 'Plastic Bottle',
            confidence_score: 0.95,
            material_category: 'plastic',
            recyclable: true,
            disposal_method: 'Take to recycling center',
            preparation_tips: 'Remove cap and label, rinse clean',
            recommended_center: {
              name: 'GreenCycle Recycling',
              address: '789 Green St, Chicago, IL 60601',
              distance: 2.3
            }
          },
          {
            identified_type: 'Aluminum Can',
            confidence_score: 0.92,
            material_category: 'metal',
            recyclable: true,
            disposal_method: 'Take to recycling center',
            preparation_tips: 'Rinse clean, crushing is optional',
            recommended_center: {
              name: 'Central Waste Solutions',
              address: '321 Recycle Blvd, Chicago, IL 60602',
              distance: 1.8
            }
          },
          {
            identified_type: 'Paper Cup',
            confidence_score: 0.88,
            material_category: 'paper',
            recyclable: false,
            disposal_method: 'Regular trash (most paper cups have plastic lining)',
            preparation_tips: 'Check if your local facility accepts paper cups',
            recommended_center: null
          }
        ]
        
        const randomResult = mockResults[Math.floor(Math.random() * mockResults.length)]
        resolve(randomResult)
      }, 2000)
    })
  }

  const handleFileSelect = (event) => {
    const file = event.target.files[0]
    if (file) {
      setSelectedImage(file)
      handleScan(file)
    }
  }

  const handleScan = async (imageFile) => {
    setIsScanning(true)
    setScanResult(null)
    
    try {
      const result = await mockScan(imageFile)
      setScanResult(result)
    } catch (error) {
      console.error('Scan failed:', error)
    } finally {
      setIsScanning(false)
    }
  }

  const triggerFileInput = () => {
    fileInputRef.current?.click()
  }

  return (
    <section id="scan" className="py-20 bg-muted/30">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-12">
          <h2 className="text-3xl font-bold text-foreground mb-4">
            AI Waste Scanner
          </h2>
          <p className="text-lg text-muted-foreground">
            Upload a photo of your waste item to get instant identification and disposal recommendations
          </p>
        </div>

        <div className="grid lg:grid-cols-2 gap-8">
          {/* Upload Section */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center">
                <Camera className="w-5 h-5 mr-2" />
                Upload Waste Image
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {/* File Input */}
                <input
                  ref={fileInputRef}
                  type="file"
                  accept="image/*"
                  onChange={handleFileSelect}
                  className="hidden"
                />

                {/* Upload Area */}
                <div 
                  onClick={triggerFileInput}
                  className="border-2 border-dashed border-border rounded-xl p-8 text-center cursor-pointer hover:border-primary transition-colors"
                >
                  <div className="w-16 h-16 eco-gradient rounded-xl flex items-center justify-center mx-auto mb-4">
                    <Upload className="w-8 h-8 text-white" />
                  </div>
                  <p className="text-foreground font-medium mb-2">
                    Click to upload an image
                  </p>
                  <p className="text-muted-foreground text-sm">
                    Supports JPG, PNG, WebP (max 16MB)
                  </p>
                </div>

                {/* Selected Image Preview */}
                {selectedImage && (
                  <div className="text-center">
                    <p className="text-sm text-muted-foreground mb-2">
                      Selected: {selectedImage.name}
                    </p>
                    <img 
                      src={URL.createObjectURL(selectedImage)}
                      alt="Selected waste item"
                      className="max-w-full h-48 object-cover rounded-lg mx-auto"
                    />
                  </div>
                )}

                {/* Scan Button */}
                <Button 
                  onClick={() => selectedImage && handleScan(selectedImage)}
                  disabled={!selectedImage || isScanning}
                  className="w-full eco-button-primary"
                  size="lg"
                >
                  {isScanning ? (
                    <>
                      <Loader2 className="w-5 h-5 mr-2 animate-spin" />
                      Analyzing...
                    </>
                  ) : (
                    <>
                      <Camera className="w-5 h-5 mr-2" />
                      Scan Waste
                    </>
                  )}
                </Button>
              </div>
            </CardContent>
          </Card>

          {/* Results Section */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center">
                <CheckCircle className="w-5 h-5 mr-2" />
                Scan Results
              </CardTitle>
            </CardHeader>
            <CardContent>
              {!scanResult && !isScanning && (
                <div className="text-center py-12 text-muted-foreground">
                  <Camera className="w-12 h-12 mx-auto mb-4 opacity-50" />
                  <p>Upload an image to see identification results</p>
                </div>
              )}

              {isScanning && (
                <div className="text-center py-12">
                  <Loader2 className="w-12 h-12 mx-auto mb-4 animate-spin text-primary" />
                  <p className="text-foreground font-medium">Analyzing your waste item...</p>
                  <p className="text-muted-foreground text-sm mt-2">This may take a few seconds</p>
                </div>
              )}

              {scanResult && (
                <div className="space-y-6">
                  {/* Identification Result */}
                  <div>
                    <h3 className="text-xl font-semibold text-foreground mb-2">
                      {scanResult.identified_type}
                    </h3>
                    <div className="flex items-center space-x-4 text-sm text-muted-foreground mb-4">
                      <span>Confidence: {Math.round(scanResult.confidence_score * 100)}%</span>
                      <span className="capitalize">Category: {scanResult.material_category}</span>
                    </div>
                    
                    {/* Recyclable Status */}
                    <div className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium ${
                      scanResult.recyclable 
                        ? 'bg-primary/10 text-primary' 
                        : 'bg-destructive/10 text-destructive'
                    }`}>
                      {scanResult.recyclable ? '♻️ Recyclable' : '🗑️ Non-recyclable'}
                    </div>
                  </div>

                  {/* Disposal Method */}
                  <div>
                    <h4 className="font-medium text-foreground mb-2">Disposal Method</h4>
                    <p className="text-muted-foreground">{scanResult.disposal_method}</p>
                  </div>

                  {/* Preparation Tips */}
                  {scanResult.preparation_tips && (
                    <div>
                      <h4 className="font-medium text-foreground mb-2 flex items-center">
                        <Info className="w-4 h-4 mr-2" />
                        Preparation Tips
                      </h4>
                      <p className="text-muted-foreground">{scanResult.preparation_tips}</p>
                    </div>
                  )}

                  {/* Recommended Center */}
                  {scanResult.recommended_center && (
                    <div className="border border-border rounded-lg p-4">
                      <h4 className="font-medium text-foreground mb-2 flex items-center">
                        <MapPin className="w-4 h-4 mr-2" />
                        Nearest Recycling Center
                      </h4>
                      <div>
                        <p className="font-medium text-foreground">{scanResult.recommended_center.name}</p>
                        <p className="text-muted-foreground text-sm">{scanResult.recommended_center.address}</p>
                        <p className="text-primary text-sm font-medium mt-1">
                          {scanResult.recommended_center.distance} km away
                        </p>
                      </div>
                      <Button variant="outline" size="sm" className="mt-3">
                        Get Directions
                      </Button>
                    </div>
                  )}
                </div>
              )}
            </CardContent>
          </Card>
        </div>
      </div>
    </section>
  )
}
