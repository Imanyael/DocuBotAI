import { useState } from 'react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Switch } from '@/components/ui/switch'
import { Settings as SettingsIcon, Key, Database, Bot, Sun, Moon } from 'lucide-react'

export function Settings() {
  const [apiKey, setApiKey] = useState('')
  const [databaseUrl, setDatabaseUrl] = useState('')
  const [maxTokens, setMaxTokens] = useState('2000')
  const [darkMode, setDarkMode] = useState(false)
  const [notifications, setNotifications] = useState(true)
  const [autoSave, setAutoSave] = useState(true)
  const [isSaving, setIsSaving] = useState(false)

  const handleSave = async () => {
    setIsSaving(true)
    // Simulate saving settings
    await new Promise(resolve => setTimeout(resolve, 1000))
    setIsSaving(false)
  }

  const handleApiKeyChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setApiKey(e.target.value)
  }

  const handleDatabaseUrlChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setDatabaseUrl(e.target.value)
  }

  const handleMaxTokensChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setMaxTokens(e.target.value)
  }

  return (
    <div className="grid gap-6">
      <Card>
        <CardHeader>
          <CardTitle>API Configuration</CardTitle>
          <CardDescription>Configure your API settings and credentials</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="space-y-2">
            <Label htmlFor="api-key">API Key</Label>
            <div className="flex gap-2">
              <Input
                id="api-key"
                type="password"
                placeholder="Enter your API key"
                value={apiKey}
                onChange={handleApiKeyChange}
              />
              <Button variant="outline" size="icon">
                <Key className="h-4 w-4" />
              </Button>
            </div>
          </div>
          <div className="space-y-2">
            <Label htmlFor="database-url">Database URL</Label>
            <div className="flex gap-2">
              <Input
                id="database-url"
                placeholder="Enter your database URL"
                value={databaseUrl}
                onChange={handleDatabaseUrlChange}
              />
              <Button variant="outline" size="icon">
                <Database className="h-4 w-4" />
              </Button>
            </div>
          </div>
          <div className="space-y-2">
            <Label htmlFor="max-tokens">Max Tokens</Label>
            <Input
              id="max-tokens"
              type="number"
              value={maxTokens}
              onChange={handleMaxTokensChange}
            />
            <p className="text-xs text-neutral-500">
              Maximum number of tokens to use in API requests
            </p>
          </div>
        </CardContent>
        <CardFooter>
          <Button onClick={handleSave} disabled={isSaving}>
            {isSaving ? (
              <>
                <SettingsIcon className="mr-2 h-4 w-4 animate-spin" />
                Saving...
              </>
            ) : (
              'Save API Settings'
            )}
          </Button>
        </CardFooter>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>AI Model Settings</CardTitle>
          <CardDescription>Configure AI model behavior and responses</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="flex items-center justify-between">
            <div className="space-y-0.5">
              <Label>Temperature</Label>
              <p className="text-sm text-neutral-500">
                Controls randomness in responses
              </p>
            </div>
            <input
              type="range"
              min="0"
              max="100"
              className="w-[200px]"
              value="70"
              onChange={() => {}}
            />
          </div>
          <div className="flex items-center justify-between">
            <div className="space-y-0.5">
              <Label>Response Length</Label>
              <p className="text-sm text-neutral-500">
                Maximum length of AI responses
              </p>
            </div>
            <input
              type="range"
              min="0"
              max="100"
              className="w-[200px]"
              value="80"
              onChange={() => {}}
            />
          </div>
          <div className="flex items-center justify-between">
            <div className="space-y-0.5">
              <Label>Context Window</Label>
              <p className="text-sm text-neutral-500">
                Number of previous messages to consider
              </p>
            </div>
            <input
              type="range"
              min="0"
              max="100"
              className="w-[200px]"
              value="60"
              onChange={() => {}}
            />
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Application Settings</CardTitle>
          <CardDescription>Configure general application preferences</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="flex items-center justify-between">
            <div className="space-y-0.5">
              <Label>Dark Mode</Label>
              <p className="text-sm text-neutral-500">
                Toggle dark mode appearance
              </p>
            </div>
            <Switch
              checked={darkMode}
              onCheckedChange={setDarkMode}
              className="data-[state=checked]:bg-green-500"
            />
          </div>
          <div className="flex items-center justify-between">
            <div className="space-y-0.5">
              <Label>Notifications</Label>
              <p className="text-sm text-neutral-500">
                Enable desktop notifications
              </p>
            </div>
            <Switch
              checked={notifications}
              onCheckedChange={setNotifications}
              className="data-[state=checked]:bg-green-500"
            />
          </div>
          <div className="flex items-center justify-between">
            <div className="space-y-0.5">
              <Label>Auto-save</Label>
              <p className="text-sm text-neutral-500">
                Automatically save changes
              </p>
            </div>
            <Switch
              checked={autoSave}
              onCheckedChange={setAutoSave}
              className="data-[state=checked]:bg-green-500"
            />
          </div>
        </CardContent>
      </Card>
    </div>
  )
}