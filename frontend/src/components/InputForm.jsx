import { useState, useEffect } from 'react'
import '../styles/InputForm.css'

export default function InputForm({ onSubmit, initialProblemStatement = '', initialBackgroundContext = '', onStartNew }) {
  const [problemStatement, setProblemStatement] = useState(initialProblemStatement)
  const [backgroundContext, setBackgroundContext] = useState(initialBackgroundContext)
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    setProblemStatement(initialProblemStatement)
    setBackgroundContext(initialBackgroundContext)
  }, [initialProblemStatement, initialBackgroundContext])

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!problemStatement.trim()) {
      alert('Please enter a problem statement')
      return
    }
    
    setLoading(true)
    try {
      await onSubmit(problemStatement, backgroundContext)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="input-form">
      <div className="input-form__header">
        <h2>What problem would you like to analyze?</h2>
        {onStartNew && (
          <button type="button" className="ghost-btn" onClick={onStartNew}>
            Start new conversation
          </button>
        )}
      </div>
      
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="problem">Problem Statement *</label>
          <textarea
            id="problem"
            value={problemStatement}
            onChange={(e) => setProblemStatement(e.target.value)}
            placeholder="Enter the problem or decision you want to analyze..."
            rows="5"
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="context">Background Context (Optional)</label>
          <textarea
            id="context"
            value={backgroundContext}
            onChange={(e) => setBackgroundContext(e.target.value)}
            placeholder="Provide any relevant background information or constraints..."
            rows="4"
          />
        </div>

        <button type="submit" disabled={loading} className="submit-btn">
          {loading ? 'Analyzing...' : 'Start Analysis'}
        </button>
      </form>

      <div className="info-section">
        <h3>How it works:</h3>
        <ul>
          <li><strong>White Hat:</strong> Objective facts and data</li>
          <li><strong>Red Hat:</strong> Emotions and intuitions</li>
          <li><strong>Black Hat:</strong> Critical analysis and risks</li>
          <li><strong>Yellow Hat:</strong> Positive vision and opportunities</li>
          <li><strong>Green Hat:</strong> Creative alternatives and ideas</li>
          <li><strong>Blue Hat:</strong> Synthesis and decision framework</li>
        </ul>
      </div>
    </div>
  )
}
