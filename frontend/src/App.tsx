import { useState } from 'react'
import { Button } from './components/ui/button'
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from './components/ui/card'
import { Menu, X, ChevronRight, Upload, Settings, Home, FileText, MessageSquare } from 'lucide-react'

function NavItem({ icon: Icon, label, active = false }: { icon: any; label: string; active?: boolean }) {
  return (
    <Button
      variant={active ? "secondary" : "ghost"}
      className="w-full justify-start gap-2"
    >
      <Icon className="h-4 w-4" />
      {label}
    </Button>
  )
}

function App() {
  const [sidebarOpen, setSidebarOpen] = useState(true)

  return (
    <div className="min-h-screen bg-neutral-50 dark:bg-neutral-950">
      {/* Header */}
      <header className="sticky top-0 z-50 w-full border-b border-neutral-200 bg-white/75 backdrop-blur dark:border-neutral-800 dark:bg-neutral-950/75">
        <div className="flex h-14 items-center px-4 md:px-6">
          <Button
            variant="ghost"
            size="icon"
            className="mr-2"
            onClick={() => setSidebarOpen(!sidebarOpen)}
          >
            {sidebarOpen ? <X className="h-5 w-5" /> : <Menu className="h-5 w-5" />}
          </Button>
          <div className="flex items-center gap-2">
            <ChevronRight className="h-4 w-4" />
            <h1 className="text-lg font-semibold">DocuBot AI</h1>
          </div>
          <div className="ml-auto flex items-center gap-2">
            <Button variant="outline" size="sm" className="gap-2">
              <Upload className="h-4 w-4" />
              Connect API
            </Button>
          </div>
        </div>
      </header>

      <div className="grid lg:grid-cols-5">
        {/* Sidebar */}
        <aside className={`${sidebarOpen ? '' : 'hidden'} lg:block lg:col-span-1`}>
          <div className="fixed inset-y-0 left-0 top-14 w-full border-r border-neutral-200 bg-white dark:border-neutral-800 dark:bg-neutral-950 lg:w-1/5">
            <nav className="grid gap-1 p-4">
              <NavItem icon={Home} label="Dashboard" active />
              <NavItem icon={FileText} label="Documents" />
              <NavItem icon={MessageSquare} label="Chat" />
              <NavItem icon={Settings} label="Settings" />
            </nav>
          </div>
        </aside>

        {/* Main Content */}
        <main className={`p-6 lg:col-span-${sidebarOpen ? '4' : '5'}`}>
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
                <p>Get started by uploading your documents or connecting to your API.</p>
              </CardContent>
              <CardFooter>
                <Button className="gap-2">
                  <Upload className="h-4 w-4" />
                  Upload Documents
                </Button>
              </CardFooter>
            </Card>

            {/* Quick Stats */}
            <div className="grid gap-4 md:grid-cols-3">
              <Card>
                <CardHeader className="flex flex-row items-center justify-between pb-2">
                  <CardTitle className="text-sm font-medium">Documents</CardTitle>
                  <FileText className="h-4 w-4 text-neutral-500" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">0</div>
                  <p className="text-xs text-neutral-500">Total documents processed</p>
                </CardContent>
              </Card>
              <Card>
                <CardHeader className="flex flex-row items-center justify-between pb-2">
                  <CardTitle className="text-sm font-medium">Chats</CardTitle>
                  <MessageSquare className="h-4 w-4 text-neutral-500" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">0</div>
                  <p className="text-xs text-neutral-500">Active conversations</p>
                </CardContent>
              </Card>
              <Card>
                <CardHeader className="flex flex-row items-center justify-between pb-2">
                  <CardTitle className="text-sm font-medium">API Status</CardTitle>
                  <Settings className="h-4 w-4 text-neutral-500" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">Ready</div>
                  <p className="text-xs text-neutral-500">System is operational</p>
                </CardContent>
              </Card>
            </div>
          </div>
        </main>
      </div>
    </div>
  )
}

export default App
