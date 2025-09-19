import { useState } from 'react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Send, Bot, User, FileText } from 'lucide-react'

interface Message {
  id: string
  type: 'user' | 'bot'
  content: string
  timestamp: Date
}

export function Chat() {
  const [messages, setMessages] = useState<Message[]>([])
  const [inputValue, setInputValue] = useState('')
  const [isProcessing, setIsProcessing] = useState(false)

  const handleSend = async () => {
    if (!inputValue.trim() || isProcessing) return

    const userMessage: Message = {
      id: Date.now().toString(),
      type: 'user',
      content: inputValue.trim(),
      timestamp: new Date()
    }

    setMessages(prev => [...prev, userMessage])
    setInputValue('')
    setIsProcessing(true)

    // Simulate bot response
    setTimeout(() => {
      const botMessage: Message = {
        id: (Date.now() + 1).toString(),
        type: 'bot',
        content: 'I understand your question about the document. Let me analyze it and provide a detailed response.',
        timestamp: new Date()
      }
      setMessages(prev => [...prev, botMessage])
      setIsProcessing(false)
    }, 1500)
  }

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSend()
    }
  }

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setInputValue(e.target.value)
  }

  return (
    <div className="grid gap-6">
      <Card className="col-span-3">
        <CardHeader>
          <CardTitle>Chat with DocuBot</CardTitle>
          <CardDescription>Ask questions about your documents</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="h-[60vh] flex flex-col">
            <div className="flex-1 overflow-y-auto space-y-4 p-4">
              {messages.length === 0 ? (
                <div className="text-center py-8">
                  <Bot className="h-12 w-12 text-neutral-400 mx-auto mb-4" />
                  <p className="text-neutral-600 dark:text-neutral-400">
                    No messages yet. Start a conversation!
                  </p>
                  <div className="mt-4 space-y-2">
                    <p className="text-sm text-neutral-500">Try asking:</p>
                    <Button
                      variant="outline"
                      className="w-full justify-start text-left"
                      onClick={() => setInputValue("What are the key points in the latest document?")}
                    >
                      "What are the key points in the latest document?"
                    </Button>
                    <Button
                      variant="outline"
                      className="w-full justify-start text-left"
                      onClick={() => setInputValue("Can you summarize the changes in version 2.0?")}
                    >
                      "Can you summarize the changes in version 2.0?"
                    </Button>
                    <Button
                      variant="outline"
                      className="w-full justify-start text-left"
                      onClick={() => setInputValue("Find all mentions of 'API endpoints' in the documentation.")}
                    >
                      "Find all mentions of 'API endpoints' in the documentation."
                    </Button>
                  </div>
                </div>
              ) : (
                messages.map(message => (
                  <div
                    key={message.id}
                    className={`flex items-start gap-3 ${
                      message.type === 'user' ? 'justify-end' : ''
                    }`}
                  >
                    {message.type === 'bot' && (
                      <div className="w-8 h-8 rounded-full bg-neutral-100 dark:bg-neutral-800 flex items-center justify-center">
                        <Bot className="h-5 w-5" />
                      </div>
                    )}
                    <div
                      className={`max-w-[80%] rounded-lg p-3 ${
                        message.type === 'user'
                          ? 'bg-blue-500 text-white'
                          : 'bg-neutral-100 dark:bg-neutral-800'
                      }`}
                    >
                      <p className="text-sm">{message.content}</p>
                      <p className="text-xs mt-1 opacity-70">
                        {message.timestamp.toLocaleTimeString()}
                      </p>
                    </div>
                    {message.type === 'user' && (
                      <div className="w-8 h-8 rounded-full bg-blue-500 flex items-center justify-center">
                        <User className="h-5 w-5 text-white" />
                      </div>
                    )}
                  </div>
                ))
              )}
              {isProcessing && (
                <div className="flex items-start gap-3">
                  <div className="w-8 h-8 rounded-full bg-neutral-100 dark:bg-neutral-800 flex items-center justify-center">
                    <Bot className="h-5 w-5" />
                  </div>
                  <div className="max-w-[80%] rounded-lg p-3 bg-neutral-100 dark:bg-neutral-800">
                    <div className="flex gap-1">
                      <span className="w-2 h-2 bg-neutral-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
                      <span className="w-2 h-2 bg-neutral-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }} />
                      <span className="w-2 h-2 bg-neutral-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }} />
                    </div>
                  </div>
                </div>
              )}
            </div>
            <div className="p-4 border-t dark:border-neutral-800">
              <div className="flex gap-2">
                <Input
                  placeholder="Type your message..."
                  value={inputValue}
                  onChange={handleInputChange}
                  onKeyPress={handleKeyPress}
                  disabled={isProcessing}
                />
                <Button
                  onClick={handleSend}
                  disabled={!inputValue.trim() || isProcessing}
                >
                  <Send className="h-4 w-4" />
                </Button>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Active Documents</CardTitle>
          <CardDescription>Documents available for chat context</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="text-center py-4">
            <FileText className="h-8 w-8 text-neutral-400 mx-auto mb-2" />
            <p className="text-sm text-neutral-600 dark:text-neutral-400">
              No active documents
            </p>
            <p className="text-xs text-neutral-500">
              Upload documents to start chatting about them
            </p>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}