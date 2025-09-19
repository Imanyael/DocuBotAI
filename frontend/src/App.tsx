import { useState } from 'react'
import { Button } from './components/ui/button'
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from './components/ui/card'
import { Menu, X, ChevronRight, Upload, Settings, Home, FileText, MessageSquare, AlertCircle, CheckCircle2, HelpCircle } from 'lucide-react'
import { Toaster } from './components/ui/toaster'
import { useToast } from './components/ui/use-toast'
import { HowToUse } from './components/HowToUse'
import { Documents } from './components/Documents'
import { Chat } from './components/Chat'
import { Settings as SettingsPage } from './components/Settings'

function NavItem({ icon: Icon, label, active = false, onClick }: { icon: any; label: string; active?: boolean; onClick?: () => void }) {
  return (
    <Button
      variant={active ? "secondary" : "ghost"}
      className="w-full justify-start gap-2 transition-all duration-200 hover:translate-x-1"
      onClick={onClick}
    >
      <Icon className={`h-4 w-4 transition-transform duration-200 ${active ? 'text-neutral-900 dark:text-neutral-50 scale-110' : ''}`} />
      {label}
    </Button>
  )
}

function App() {
  const { toast } = useToast()
  const [sidebarOpen, setSidebarOpen] = useState(true)
  const [activeNav, setActiveNav] = useState('dashboard')
  const [apiConnected, setApiConnected] = useState(false)
  const [isConnecting, setIsConnecting] = useState(false)

  const handleApiConnect = async () => {
    if (apiConnected || isConnecting) return
    setIsConnecting(true)
    
    try {
      // Simulate API connection
      await new Promise(resolve => setTimeout(resolve, 1500))
      setApiConnected(true)
      toast({
        title: "API Connected",
        description: "Successfully connected to the API service.",
        variant: "success",
      })
    } catch (error) {
      toast({
        title: "Connection Failed",
        description: "Failed to connect to the API. Please try again.",
        variant: "destructive",
      })
    } finally {
      setIsConnecting(false)
    }
  }

  const handleNavigation = (nav: string) => {
    if (activeNav === nav) return
    setActiveNav(nav)
    toast({
      title: "Navigation",
      description: `Switched to ${nav} view`,
    })
  }

  const renderContent = () => {
    switch (activeNav) {
      case 'documents':
        return <Documents />
      case 'chat':
        return <Chat />
      case 'settings':
        return <SettingsPage />
      case 'how-to-use':
        return <HowToUse />
      default:
        return (
          <div className="grid gap-6">
            {/* Welcome Card */}
            <Card>
              <CardHeader>
                <CardTitle>Welcome to DocuBot AI</CardTitle>
                <CardDescription>
                  Your intelligent document management assistant
                </CardDescription>
              </CardHeader>
              <CardContent>
                <p className="mb-4">Get started by uploading your documents or connecting to your API.</p>
                {!apiConnected && (
                  <div className="flex items-center gap-2 text-amber-600 dark:text-amber-500">
                    <AlertCircle className="h-4 w-4 animate-pulse" />
                    <p className="text-sm">Please connect your API to enable all features</p>
                  </div>
                )}
              </CardContent>
              <CardFooter className="gap-2">
                <Button 
                  className="gap-2 min-w-[160px] transition-all duration-300" 
                  onClick={() => handleNavigation('documents')}
                  disabled={!apiConnected}
                >
                  <Upload className="h-4 w-4" />
                  Upload Documents
                </Button>
                {!apiConnected && (
                  <Button 
                    variant="outline" 
                    className="gap-2 transition-all duration-300"
                    onClick={handleApiConnect}
                    disabled={isConnecting}
                  >
                    <Settings className={`h-4 w-4 ${isConnecting ? 'animate-spin' : ''}`} />
                    {isConnecting ? 'Connecting...' : 'Configure API'}
                  </Button>
                )}
              </CardFooter>
            </Card>

            {/* Quick Stats */}
            <div className="grid gap-4 md:grid-cols-3">
              <Card className="transition-all duration-300 hover:scale-105">
                <CardHeader className="flex flex-row items-center justify-between pb-2">
                  <CardTitle className="text-sm font-medium">Documents</CardTitle>
                  <FileText className="h-4 w-4 text-neutral-500" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">0</div>
                  <p className="text-xs text-neutral-500">Total documents processed</p>
                </CardContent>
              </Card>
              <Card className="transition-all duration-300 hover:scale-105">
                <CardHeader className="flex flex-row items-center justify-between pb-2">
                  <CardTitle className="text-sm font-medium">Chats</CardTitle>
                  <MessageSquare className="h-4 w-4 text-neutral-500" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">0</div>
                  <p className="text-xs text-neutral-500">Active conversations</p>
                </CardContent>
              </Card>
              <Card className="transition-all duration-300 hover:scale-105">
                <CardHeader className="flex flex-row items-center justify-between pb-2">
                  <CardTitle className="text-sm font-medium">API Status</CardTitle>
                  <Settings className={`h-4 w-4 ${apiConnected ? 'text-green-600' : 'text-neutral-500'}`} />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">{apiConnected ? 'Connected' : 'Not Connected'}</div>
                  <p className="text-xs text-neutral-500">
                    {apiConnected ? 'System is operational' : 'Please configure API'}
                  </p>
                </CardContent>
              </Card>
            </div>
          </div>
        )
    }
  }

  return (
    <div className="min-h-screen bg-neutral-50 dark:bg-neutral-950">
      {/* Header */}
      <header className="sticky top-0 z-50 w-full border-b border-neutral-200 bg-white/75 backdrop-blur dark:border-neutral-800 dark:bg-neutral-950/75">
        <div className="flex h-14 items-center px-4 md:px-6">
          <Button
            variant="ghost"
            size="icon"
            className="mr-2 hover:bg-neutral-100 dark:hover:bg-neutral-800 transition-all duration-200 hover:rotate-180"
            onClick={() => setSidebarOpen(!sidebarOpen)}
          >
            {sidebarOpen ? <X className="h-5 w-5" /> : <Menu className="h-5 w-5" />}
          </Button>
          <div className="flex items-center gap-2">
            <ChevronRight className="h-4 w-4" />
            <h1 className="text-lg font-semibold">DocuBot AI</h1>
          </div>
          <div className="ml-auto flex items-center gap-2">
            <Button 
              variant={apiConnected ? "secondary" : "outline"} 
              size="sm" 
              className="gap-2 min-w-[120px] transition-all duration-300"
              onClick={handleApiConnect}
              disabled={isConnecting}
            >
              {isConnecting ? (
                <>
                  <Settings className="h-4 w-4 animate-spin" />
                  <span className="animate-pulse">Connecting...</span>
                </>
              ) : apiConnected ? (
                <>
                  <CheckCircle2 className="h-4 w-4 text-green-600" />
                  Connected
                </>
              ) : (
                <>
                  <Settings className="h-4 w-4" />
                  Connect API
                </>
              )}
            </Button>
          </div>
        </div>
      </header>

      <div className="grid lg:grid-cols-5">
        {/* Sidebar */}
        <aside className={`${sidebarOpen ? '' : 'hidden'} lg:block lg:col-span-1`}>
          <div className="fixed inset-y-0 left-0 top-14 w-full border-r border-neutral-200 bg-white dark:border-neutral-800 dark:bg-neutral-950 lg:w-1/5">
            <nav className="grid gap-1 p-4">
              <NavItem 
                icon={Home} 
                label="Dashboard" 
                active={activeNav === 'dashboard'} 
                onClick={() => handleNavigation('dashboard')}
              />
              <NavItem 
                icon={FileText} 
                label="Documents" 
                active={activeNav === 'documents'} 
                onClick={() => handleNavigation('documents')}
              />
              <NavItem 
                icon={MessageSquare} 
                label="Chat" 
                active={activeNav === 'chat'} 
                onClick={() => handleNavigation('chat')}
              />
              <NavItem 
                icon={Settings} 
                label="Settings" 
                active={activeNav === 'settings'} 
                onClick={() => handleNavigation('settings')}
              />
              <NavItem 
                icon={HelpCircle} 
                label="How to Use" 
                active={activeNav === 'how-to-use'} 
                onClick={() => handleNavigation('how-to-use')}
              />
            </nav>
          </div>
        </aside>

        {/* Main Content */}
        <main className={`p-6 lg:col-span-${sidebarOpen ? '4' : '5'}`}>
          {renderContent()}
        </main>
      </div>
      <Toaster />
    </div>
  )
}

export default App
