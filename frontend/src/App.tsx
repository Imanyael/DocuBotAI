import { useState } from 'react'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { Home, Settings, Tool, Search, BarChart3, Menu, X } from 'lucide-react'

const queryClient = new QueryClient()

function App() {
  const [isSidebarOpen, setIsSidebarOpen] = useState(false)

  return (
    <QueryClientProvider client={queryClient}>
      <div className="min-h-screen bg-gradient-to-br from-light to-neutral/10">
        {/* Header */}
        <header className="fixed top-0 left-0 right-0 z-50 bg-white/70 backdrop-blur-lg border-b border-neutral/10">
          <div className="container mx-auto px-4 h-16 flex items-center justify-between">
            <div className="flex items-center gap-2">
              <button 
                className="lg:hidden p-2 hover:bg-neutral/10 rounded-lg"
                onClick={() => setIsSidebarOpen(!isSidebarOpen)}
              >
                {isSidebarOpen ? <X size={24} /> : <Menu size={24} />}
              </button>
              <h1 className="text-2xl font-bold bg-gradient-to-r from-primary-dark to-primary bg-clip-text text-transparent">
                DocuBotAI
              </h1>
            </div>
            <div className="flex items-center gap-4">
              {/* Add user profile and other header items here */}
            </div>
          </div>
        </header>

        {/* Sidebar */}
        <aside className={`fixed top-16 left-0 bottom-0 z-40 w-64 bg-white/70 backdrop-blur-lg border-r border-neutral/10 transform transition-transform duration-200 lg:translate-x-0 ${
          isSidebarOpen ? 'translate-x-0' : '-translate-x-full'
        }`}>
          <nav className="p-4 space-y-2">
            <NavItem icon={<Home size={20} />} label="Dashboard" isActive />
            <NavItem icon={<Tool size={20} />} label="Tools" />
            <NavItem icon={<Search size={20} />} label="Query" />
            <NavItem icon={<BarChart3 size={20} />} label="Analytics" />
            <NavItem icon={<Settings size={20} />} label="Settings" />
          </nav>
        </aside>

        {/* Main Content */}
        <main className={`pt-16 min-h-screen transition-all duration-200 ${
          isSidebarOpen ? 'lg:pl-64' : ''
        }`}>
          <div className="container mx-auto px-4 py-8">
            {/* Add router and page content here */}
            <div className="grid gap-6">
              {/* Placeholder content */}
              <section className="glass-card p-6">
                <h2 className="text-xl font-semibold mb-4">Welcome to DocuBotAI</h2>
                <p className="text-secondary">
                  Your AI-powered documentation assistant is ready to help.
                </p>
              </section>
            </div>
          </div>
        </main>
      </div>
    </QueryClientProvider>
  )
}

function NavItem({ icon, label, isActive = false }: { icon: React.ReactNode; label: string; isActive?: boolean }) {
  return (
    <a
      href="#"
      className={`flex items-center gap-3 px-4 py-2 rounded-lg transition-colors duration-200 ${
        isActive
          ? 'bg-primary/10 text-primary-dark'
          : 'text-secondary hover:bg-neutral/10'
      }`}
    >
      {icon}
      <span className="font-medium">{label}</span>
    </a>
  )
}

export default App
