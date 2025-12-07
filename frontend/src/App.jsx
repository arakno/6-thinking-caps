import { useState, useRef } from 'react'
import InputForm from './components/InputForm'
import ProgressTracker from './components/ProgressTracker'
import ResultsDisplay from './components/ResultsDisplay'
import './App.css'

function App() {
  const [sessionId, setSessionId] = useState(null)
  const [status, setStatus] = useState(null)
  const [results, setResults] = useState(null)
  const [error, setError] = useState(null)
  const [formData, setFormData] = useState({ problemStatement: '', backgroundContext: '' })
  const pollRef = useRef(null)

  const clearPoll = () => {
    if (pollRef.current) {
      clearInterval(pollRef.current)
      pollRef.current = null
    }
  }

  const handleSubmit = async (problemStatement, backgroundContext) => {
    setError(null)
    clearPoll()
    setResults(null)
    setStatus('initiated')
    setFormData({ problemStatement, backgroundContext })
    try {
      // Create session
      const createRes = await fetch('/api/sessions', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          problem_statement: problemStatement,
          background_context: backgroundContext,
        }),
      })
      
      if (!createRes.ok) throw new Error('Failed to create session')
      
      const session = await createRes.json()
      setSessionId(session.session_id)
      
      // Start analysis
      const analyzeRes = await fetch(`/api/sessions/${session.session_id}/analyze`, {
        method: 'POST',
      })
      
      if (!analyzeRes.ok) throw new Error('Failed to start analysis')
      
      // Poll for progress
      pollRef.current = setInterval(async () => {
        try {
          const progressRes = await fetch(`/api/sessions/${session.session_id}/progress`)
          const progress = await progressRes.json()
          setStatus(progress.status)
          if (progress.error_message) {
            setError(progress.error_message)
          }
          
          if (progress.status === 'completed') {
            clearPoll()
            
            // Fetch results
            const resultsRes = await fetch(`/api/sessions/${session.session_id}/results`)
            const resultsData = await resultsRes.json()
            setResults(resultsData)
          } else if (progress.status === 'failed') {
            clearPoll()
            setError(progress.error_message || 'Analysis failed')
          }
        } catch (err) {
          console.error('Progress poll error:', err)
        }
      }, 2000)
      
    } catch (err) {
      setError(err.message || 'An error occurred')
      console.error(err)
    }
  }

  const handleEditPrevious = () => {
    clearPoll()
    setSessionId(null)
    setStatus(null)
    setResults(null)
    // keep formData to prefill
  }

  const handleNewConversation = () => {
    clearPoll()
    setSessionId(null)
    setStatus(null)
    setResults(null)
    setError(null)
    setFormData({ problemStatement: '', backgroundContext: '' })
  }

  return (
    <div className="app">
      <header className="app-header">
        <h1>🎩 6 Thinking Hats Analysis</h1>
        <p>Multi-perspective problem analysis powered by AI</p>
      </header>

      <main className="app-main">
        {!sessionId ? (
          <InputForm
            onSubmit={handleSubmit}
            initialProblemStatement={formData.problemStatement}
            initialBackgroundContext={formData.backgroundContext}
            onStartNew={handleNewConversation}
          />
        ) : !results ? (
          <ProgressTracker
            status={status}
            error={error}
            onEdit={handleEditPrevious}
            onNew={handleNewConversation}
          />
        ) : (
          <ResultsDisplay
            results={results}
            onEdit={handleEditPrevious}
            onNew={handleNewConversation}
          />
        )}
      </main>

      <footer className="app-footer">
        <p>© 2025 6 Thinking Caps Multi-Agent System</p>
      </footer>
    </div>
  )
}

export default App
