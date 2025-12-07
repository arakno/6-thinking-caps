import '../styles/ProgressTracker.css'

const HATS = {
  white: '⚪ White Hat',
  red: '🔴 Red Hat',
  black: '⚫ Black Hat',
  yellow: '🟡 Yellow Hat',
  green: '💚 Green Hat',
  blue: '🔵 Blue Hat',
}

export default function ProgressTracker({ status, error, onEdit, onNew }) {
  const getProgressPercentage = () => {
    if (status === 'initiated') return 0
    if (status === 'processing') return 50
    if (status === 'completed') return 100
    return 0
  }

  return (
    <div className="progress-tracker">
      <h2>Analysis in Progress...</h2>
      
      {error && (
        <div className="error-message">
          <span>❌ Error: {error}</span>
        </div>
      )}

      <div className="progress-bar-container">
        <div 
          className="progress-bar" 
          style={{ width: `${getProgressPercentage()}%` }}
        />
      </div>
      
      <p className="status-text">
        {status === 'initiated' && 'Initializing analysis...'}
        {status === 'processing' && 'Analyzing from multiple perspectives...'}
        {status === 'completed' && 'Analysis complete!'}
        {status === 'failed' && 'Analysis failed'}
      </p>

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

      <div className="hats-list">
        <h3>Thinking Hats</h3>
        <ul>
          {Object.entries(HATS).map(([key, label]) => (
            <li key={key} className={`hat ${key}`}>
              <span className="hat-label">{label}</span>
            </li>
          ))}
        </ul>
      </div>
    </div>
  )
}
