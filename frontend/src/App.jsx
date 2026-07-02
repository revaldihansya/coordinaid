import { useState } from 'react'
import './App.css'

function App() {
  // This state keeps track of which page the user is currently looking at
  const [currentView, setCurrentView] = useState('home')

  return (
    <div style={{ textAlign: 'center', padding: '50px', fontFamily: 'sans-serif' }}>
      <h1>ResRoute Command Center</h1>
      <p>Coordinating relief at the speed of data.</p>

      {/* HOME SCREEN */}
      {currentView === 'home' && (
        <div style={{ marginTop: '40px' }}>
          <h2>Select Your Portal</h2>
          <div style={{ display: 'flex', justifyContent: 'center', gap: '20px', marginTop: '20px' }}>
            
            <button 
              onClick={() => setCurrentView('donor')}
              style={{ padding: '20px', fontSize: '18px', cursor: 'pointer' }}
            >
              📦 Corporate Donor Portal
              <br/><small>Register incoming supplies</small>
            </button>

            <button 
              onClick={() => setCurrentView('requestor')}
              style={{ padding: '20px', fontSize: '18px', cursor: 'pointer' }}
            >
              🚨 Crisis Ground Command
              <br/><small>Log real-time regional needs</small>
            </button>

          </div>
        </div>
      )}

      {/* DONOR SCREEN */}
      {currentView === 'donor' && (
        <div style={{ marginTop: '40px' }}>
          <h2>Donor Portal</h2>
          <p>This is where the AI will ingest and analyze donor manifests.</p>
          <button onClick={() => setCurrentView('home')}>← Back to Home</button>
        </div>
      )}

      {/* REQUESTOR SCREEN */}
      {currentView === 'requestor' && (
        <div style={{ marginTop: '40px' }}>
          <h2>Crisis Ground Command</h2>
          <p>This is where NGOs will update the dynamic needs database.</p>
          <button onClick={() => setCurrentView('home')}>← Back to Home</button>
        </div>
      )}

    </div>
  )
}

export default App