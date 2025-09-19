import { Button } from './ui/button'
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from './ui/card'
import { Upload, FileText, AlertCircle } from 'lucide-react'
import { useState } from 'react'

export function Documents() {
  const [selectedFiles, setSelectedFiles] = useState<File[]>([])
  const [uploading, setUploading] = useState(false)
  const [uploadProgress, setUploadProgress] = useState(0)

  const handleFileSelect = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files) {
      setSelectedFiles(Array.from(event.target.files))
    }
  }

  const handleUpload = async () => {
    if (!selectedFiles.length || uploading) return
    setUploading(true)
    setUploadProgress(0)

    try {
      // Simulate upload process
      for (let i = 0; i <= 100; i += 10) {
        await new Promise(resolve => setTimeout(resolve, 300))
        setUploadProgress(i)
      }
      setSelectedFiles([])
    } catch (error) {
      console.error('Upload failed:', error)
    } finally {
      setUploading(false)
      setUploadProgress(0)
    }
  }

  return (
    <div className="grid gap-6">
      <Card>
        <CardHeader>
          <CardTitle>Document Management</CardTitle>
          <CardDescription>Upload and manage your documents</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid gap-4">
            <div className="border-2 border-dashed border-neutral-200 dark:border-neutral-800 rounded-lg p-6 text-center">
              <input
                type="file"
                multiple
                onChange={handleFileSelect}
                className="hidden"
                id="file-upload"
              />
              <label
                htmlFor="file-upload"
                className="cursor-pointer flex flex-col items-center gap-2"
              >
                <Upload className="h-8 w-8 text-neutral-400" />
                <p className="text-sm text-neutral-600 dark:text-neutral-400">
                  Drag and drop your files here, or click to select files
                </p>
                <p className="text-xs text-neutral-500">
                  Supports PDF, DOC, DOCX, TXT (max 10MB each)
                </p>
              </label>
            </div>

            {selectedFiles.length > 0 && (
              <div className="space-y-2">
                <p className="text-sm font-medium">Selected Files:</p>
                {selectedFiles.map((file, index) => (
                  <div
                    key={index}
                    className="flex items-center gap-2 text-sm p-2 bg-neutral-50 dark:bg-neutral-900 rounded"
                  >
                    <FileText className="h-4 w-4" />
                    <span>{file.name}</span>
                    <span className="text-xs text-neutral-500">
                      ({(file.size / 1024 / 1024).toFixed(2)} MB)
                    </span>
                  </div>
                ))}
              </div>
            )}

            {uploading && (
              <div className="space-y-2">
                <div className="h-2 w-full bg-neutral-100 dark:bg-neutral-800 rounded-full overflow-hidden">
                  <div
                    className="h-full bg-green-500 transition-all duration-300"
                    style={{ width: `${uploadProgress}%` }}
                  />
                </div>
                <p className="text-xs text-neutral-500 text-center">
                  Uploading: {uploadProgress}%
                </p>
              </div>
            )}
          </div>
        </CardContent>
        <CardFooter>
          <Button
            onClick={handleUpload}
            disabled={!selectedFiles.length || uploading}
            className="w-full sm:w-auto"
          >
            {uploading ? 'Uploading...' : 'Upload Selected Files'}
          </Button>
        </CardFooter>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Recent Documents</CardTitle>
          <CardDescription>Your recently uploaded documents</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="text-center py-8">
            <AlertCircle className="h-8 w-8 text-neutral-400 mx-auto mb-2" />
            <p className="text-sm text-neutral-600 dark:text-neutral-400">
              No documents uploaded yet
            </p>
            <p className="text-xs text-neutral-500">
              Upload some documents to see them here
            </p>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}