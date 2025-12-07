import { useState } from 'react'
import '../styles/ResultsDisplay.css'

const HAT_COLORS = {
  white: '#f0f0f0',
  red: '#ff6b6b',
  black: '#2d3436',
  yellow: '#ffd93d',
  green: '#6bcf7f',
  blue: '#4d96ff',
}

const HAT_EMOJI = {
  white: '⚪',
  red: '🔴',
  black: '⚫',
  yellow: '🟡',
  green: '💚',
  blue: '🔵',
}

export default function ResultsDisplay({ results, onEdit, onNew }) {
  const [selectedHat, setSelectedHat] = useState('white')

  // Debug: Log what we're receiving
  console.log('Results received:', results)
  console.log('Available hats:', Object.keys(results.results))

  const selectedResult = results.results[selectedHat]

  // Get available hats in a consistent order
  const hatOrder = ['white', 'red', 'black', 'yellow', 'green', 'blue']
  const availableHats = hatOrder.filter(hat => results.results[hat])

  return (
    <div className="results-display">
      <h2>Analysis Results</h2>

      <div className="action-bar">
        {onEdit && (
          <button className="ghost-btn" onClick={onEdit}>
            Edit input
          </button>
        )}
        {onNew && (
          <button className="secondary-btn" onClick={onNew}>
            Start new conversation
          </button>
        )}
      </div>

      <div className="problem-statement">
        <h3>Problem Statement</h3>
        <p>{results.problem_statement}</p>
      </div>

      {availableHats.length === 0 ? (
        <div style={{ padding: '2rem', background: '#fff3cd', borderRadius: '8px', marginBottom: '2rem' }}>
          <p>⚠️ No hat results available. The analysis may have encountered issues.</p>
          {results.error_message && <p><strong>Error:</strong> {results.error_message}</p>}
        </div>
      ) : (
        <>
          <div className="hats-tabs">
            {availableHats.map((hat) => (
              <button
                key={hat}
                className={`hat-tab ${selectedHat === hat ? 'active' : ''}`}
                onClick={() => setSelectedHat(hat)}
                style={{
                  backgroundColor: selectedHat === hat ? HAT_COLORS[hat] : '#ffffff',
                  color: selectedHat === hat ? (hat === 'yellow' || hat === 'white' ? '#333' : '#fff') : '#333',
                }}
              >
                {HAT_EMOJI[hat]} {hat.charAt(0).toUpperCase() + hat.slice(1)}
              </button>
            ))}
          </div>

          {selectedResult && (
            <div className="result-detail">
              <div className="result-header">
                <h3>{selectedResult.agent_name}</h3>
                <span className="confidence">
                  Confidence: {selectedResult.confidence_level}
                </span>
              </div>

              <div className="result-section">
                <h4>Key Insights</h4>
                <ul>
                  {selectedResult.key_insights && selectedResult.key_insights.length > 0 ? (
                    selectedResult.key_insights.map((insight, idx) => (
                      <li key={idx}>{insight}</li>
                    ))
                  ) : (
                    <li>No insights available</li>
                  )}
                </ul>
              </div>

              <div className="result-section">
                <h4>Recommendations</h4>
                <ul>
                  {selectedResult.recommendations && selectedResult.recommendations.length > 0 ? (
                    selectedResult.recommendations.map((rec, idx) => (
                      <li key={idx}>{rec}</li>
                    ))
                  ) : (
                    <li>No recommendations available</li>
                  )}
                </ul>
              </div>

              <div className="result-meta">
                <small>Execution time: {selectedResult.execution_time_ms.toFixed(2)}ms</small>
              </div>
            </div>
          )}

          {results.results.blue && (
            <div className="synthesis-section">
              <h3>📋 Synthesis (Blue Hat Summary)</h3>
              <div className="synthesis-content">
                <div className="result-section">
                  <h4>Key Insights</h4>
                  <ul>
                    {results.results.blue.key_insights && results.results.blue.key_insights.length > 0 ? (
                      results.results.blue.key_insights.map((insight, idx) => (
                        <li key={idx}>{insight}</li>
                      ))
                    ) : (
                      <li>No synthesis insights available</li>
                    )}
                  </ul>
                </div>
                <div className="result-section">
                  <h4>Recommendations</h4>
                  <ul>
                    {results.results.blue.recommendations && results.results.blue.recommendations.length > 0 ? (
                      results.results.blue.recommendations.map((rec, idx) => (
                        <li key={idx}>{rec}</li>
                      ))
                    ) : (
                      <li>No synthesis recommendations available</li>
                    )}
                  </ul>
                </div>
              </div>
            </div>
          )}
        </>
      )}

      <div className="results-meta">
        <small>
          Created: {new Date(results.created_at).toLocaleString()}
          <br />
          Session ID: {results.session_id}
        </small>
      </div>
    </div>
  )
}
