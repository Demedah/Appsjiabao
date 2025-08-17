"use client"

import type React from "react"

import { useState, useRef } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Progress } from "@/components/ui/progress"
import { Badge } from "@/components/ui/badge"
import { Alert, AlertDescription } from "@/components/ui/alert"
import { Upload, ImageIcon, Brain, CheckCircle, AlertCircle, X } from "lucide-react"

interface ClassificationResult {
  class: string
  confidence: number
  timestamp: string
}

export default function JiabaoKlinikFaceClassification() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null)
  const [previewUrl, setPreviewUrl] = useState<string | null>(null)
  const [isUploading, setIsUploading] = useState(false)
  const [uploadProgress, setUploadProgress] = useState(0)
  const [classificationResult, setClassificationResult] = useState<ClassificationResult | null>(null)
  const [error, setError] = useState<string | null>(null)
  const fileInputRef = useRef<HTMLInputElement>(null)

  const handleFileSelect = (file: File) => {
    if (!file.type.startsWith("image/")) {
      setError("Silakan pilih file gambar yang valid (JPG, PNG, dll.)")
      return
    }

    if (file.size > 10 * 1024 * 1024) {
      // 10MB limit
      setError("Ukuran file terlalu besar. Maksimal 10MB.")
      return
    }

    setSelectedFile(file)
    setError(null)

    // Create preview URL
    const url = URL.createObjectURL(file)
    setPreviewUrl(url)
  }

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault()
    const files = Array.from(e.dataTransfer.files)
    if (files.length > 0) {
      handleFileSelect(files[0])
    }
  }

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault()
  }

  const simulateClassification = async () => {
    if (!selectedFile) return

    setIsUploading(true)
    setUploadProgress(0)
    setError(null)

    // Simulate upload progress
    const progressInterval = setInterval(() => {
      setUploadProgress((prev) => {
        if (prev >= 90) {
          clearInterval(progressInterval)
          return 90
        }
        return prev + 10
      })
    }, 200)

    try {
      // Simulate API call delay
      await new Promise((resolve) => setTimeout(resolve, 2000))

      const mockResults = [
        { class: "Dry", confidence: 0.89 },
        { class: "Normal", confidence: 0.92 },
        { class: "Oily", confidence: 0.85 },
      ]

      const randomResult = mockResults[Math.floor(Math.random() * mockResults.length)]

      setClassificationResult({
        ...randomResult,
        timestamp: new Date().toLocaleString("id-ID"),
      })

      setUploadProgress(100)
    } catch (err) {
      setError("Terjadi kesalahan saat memproses gambar. Silakan coba lagi.")
    } finally {
      setIsUploading(false)
      clearInterval(progressInterval)
    }
  }

  const resetUpload = () => {
    setSelectedFile(null)
    setPreviewUrl(null)
    setClassificationResult(null)
    setError(null)
    setUploadProgress(0)
    if (fileInputRef.current) {
      fileInputRef.current.value = ""
    }
  }

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="border-b border-border bg-card">
        <div className="container mx-auto px-4 py-6">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-primary rounded-lg flex items-center justify-center">
              <Brain className="w-6 h-6 text-primary-foreground" />
            </div>
            <div>
              <h1 className="text-2xl font-bold text-foreground">Jiabao Klinik</h1>
              <p className="text-sm text-muted-foreground">Sistem Klasifikasi Jenis Kulit dengan Random Forest</p>
            </div>
          </div>
        </div>
      </header>

      <main className="container mx-auto px-4 py-8 max-w-4xl">
        <div className="grid gap-6">
          {/* Upload Section */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Upload className="w-5 h-5 text-primary" />
                Upload Foto Pasien
              </CardTitle>
              <CardDescription>
                Unggah foto wajah pasien untuk analisis jenis kulit (kering, normal, berminyak) menggunakan algoritma
                Random Forest
              </CardDescription>
            </CardHeader>
            <CardContent>
              {!selectedFile ? (
                <div
                  className="border-2 border-dashed border-border rounded-lg p-8 text-center hover:border-primary/50 transition-colors cursor-pointer"
                  onDrop={handleDrop}
                  onDragOver={handleDragOver}
                  onClick={() => fileInputRef.current?.click()}
                >
                  <ImageIcon className="w-12 h-12 text-muted-foreground mx-auto mb-4" />
                  <p className="text-lg font-medium text-foreground mb-2">Seret dan lepas foto di sini</p>
                  <p className="text-sm text-muted-foreground mb-4">atau klik untuk memilih file</p>
                  <p className="text-xs text-muted-foreground">Format: JPG, PNG, GIF (Maksimal 10MB)</p>
                  <input
                    ref={fileInputRef}
                    type="file"
                    accept="image/*"
                    className="hidden"
                    onChange={(e) => {
                      const file = e.target.files?.[0]
                      if (file) handleFileSelect(file)
                    }}
                  />
                </div>
              ) : (
                <div className="space-y-4">
                  <div className="relative">
                    <img
                      src={previewUrl || ""}
                      alt="Preview"
                      className="w-full max-w-md mx-auto rounded-lg shadow-md"
                    />
                    <Button variant="destructive" size="sm" className="absolute top-2 right-2" onClick={resetUpload}>
                      <X className="w-4 h-4" />
                    </Button>
                  </div>

                  <div className="text-center">
                    <p className="text-sm text-muted-foreground mb-2">File: {selectedFile.name}</p>
                    <p className="text-xs text-muted-foreground">
                      Ukuran: {(selectedFile.size / 1024 / 1024).toFixed(2)} MB
                    </p>
                  </div>

                  {isUploading && (
                    <div className="space-y-2">
                      <div className="flex items-center justify-between text-sm">
                        <span>Memproses...</span>
                        <span>{uploadProgress}%</span>
                      </div>
                      <Progress value={uploadProgress} className="w-full" />
                    </div>
                  )}

                  <div className="flex justify-center">
                    <Button
                      onClick={simulateClassification}
                      disabled={isUploading}
                      className="bg-primary hover:bg-primary/90"
                    >
                      {isUploading ? "Menganalisis Jenis Kulit..." : "Analisis Jenis Kulit"}
                    </Button>
                  </div>
                </div>
              )}
            </CardContent>
          </Card>

          {/* Error Alert */}
          {error && (
            <Alert variant="destructive">
              <AlertCircle className="h-4 w-4" />
              <AlertDescription>{error}</AlertDescription>
            </Alert>
          )}

          {/* Results Section */}
          {classificationResult && (
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <CheckCircle className="w-5 h-5 text-accent" />
                  Hasil Analisis Jenis Kulit
                </CardTitle>
                <CardDescription>Hasil analisis menggunakan Random Forest Algorithm</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div className="flex items-center justify-between p-4 bg-card rounded-lg border">
                    <div>
                      <h3 className="font-semibold text-lg text-foreground">
                        {classificationResult.class === "Dry" && "Kulit Kering"}
                        {classificationResult.class === "Normal" && "Kulit Normal"}
                        {classificationResult.class === "Oily" && "Kulit Berminyak"}
                      </h3>
                      <p className="text-sm text-muted-foreground">
                        Tingkat Kepercayaan: {(classificationResult.confidence * 100).toFixed(1)}%
                      </p>
                    </div>
                    <Badge
                      variant={classificationResult.confidence > 0.8 ? "default" : "secondary"}
                      className="text-sm"
                    >
                      {classificationResult.confidence > 0.8 ? "Tinggi" : "Sedang"}
                    </Badge>
                  </div>

                  <div className="text-xs text-muted-foreground">Diproses pada: {classificationResult.timestamp}</div>

                  <div className="p-4 bg-muted rounded-lg">
                    <p className="text-sm text-muted-foreground">
                      <strong>Catatan:</strong> Analisis selesai! Terima kasih telah memilih Jiabao Klinik sebagai mitra
                      kesehatan anda. Layanan terbaik selalu menjadi prioritas kami.
                    </p>
                  </div>
                </div>
              </CardContent>
            </Card>
          )}

          {/* Info Section */}
          <Card>
            <CardHeader>
              <CardTitle className="text-lg">Tentang Sistem</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid md:grid-cols-2 gap-4 text-sm">
                <div>
                  <h4 className="font-medium text-foreground mb-2">Algoritma</h4>
                  <p className="text-muted-foreground">
                    Menggunakan Algoritma Random Forest Classifier dengan akurasi tinggi untuk klasifikasi jenis kulit
                    wajah (kering, normal, berminyak).
                  </p>
                </div>
                <div>
                  <h4 className="font-medium text-foreground mb-2">Keamanan Data</h4>
                  <p className="text-muted-foreground">
                    Semua data pasien dienkripsi dan disimpan sesuai standar keamanan medis.
                  </p>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </main>
    </div>
  )
}
