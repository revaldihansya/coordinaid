import { useState } from 'react'
import './App.css'

function App() {
  const [currentView, setCurrentView] = useState('home')

  // Mock Database for Ground Command
  const [regionalNeeds, setRegionalNeeds] = useState([
    { region: 'Tropical Flood Zone', priority: 'Water & Meds', portCapacity: '95% Full', status: 'Critical' },
    { region: 'Alpine Earthquake Zone', priority: 'Tents & Blankets', portCapacity: '40% Full', status: 'Stable' }
  ])

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
          <button onClick={() => setCurrentView('home')} style={{ padding: '10px', cursor: 'pointer' }}>← Back to Home</button>
        </div>
      )}

      {/* REQUESTOR SCREEN (GROUND COMMAND) */}
      {currentView === 'requestor' && (
        <div style={{ marginTop: '40px', display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
          <h2>Crisis Ground Command</h2>
          <p>Active Regional Needs & Logistics Capacity</p>
          
          <div style={{ display: 'flex', gap: '20px', margin: '20px 0' }}>
            {regionalNeeds.map((zone, index) => (
              <div key={index} style={{ border: '1px solid #ccc', padding: '20px', borderRadius: '8px', textAlign: 'left', width: '250px' }}>
                <h3 style={{ margin: '0 0 10px 0' }}>{zone.region}</h3>
                <p><strong>Top Priority:</strong> {zone.priority}</p>
                <p><strong>Port Congestion:</strong> {zone.portCapacity}</p>
                <p style={{ color: zone.status === 'Critical' ? 'red' : 'green' }}>
                  <strong>Status:</strong> {zone.status}
                </p>
              </div>
            ))}
          </div>

          <button onClick={() => setCurrentView('home')} style={{ padding: '10px', cursor: 'pointer', marginTop: '20px' }}>← Back to Home</button>
        </div>
      )}

    </div>
  )
}

export default App