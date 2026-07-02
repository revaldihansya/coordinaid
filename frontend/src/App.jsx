import { useState, useEffect } from 'react'
import './App.css'

function App() {
  const [currentView, setCurrentView] = useState('home')
  
  // -- GROUND COMMAND STATE --
  const [regionalNeeds, setRegionalNeeds] = useState([])
  const [newZone, setNewZone] = useState({
    region: '', priority: '', portCapacity: '', status: 'Stable'
  })

  // -- DONOR PORTAL STATE --
  const [donorInput, setDonorInput] = useState('')
  const [triageResult, setTriageResult] = useState(null)

  // -- API: Fetch Needs --
  const fetchNeeds = async () => {
    try {
      const response = await fetch('http://127.0.0.1:8000/api/needs')
      const data = await response.json()
      setRegionalNeeds(data)
    } catch (error) {
      console.error("Failed to fetch data from backend.", error)
    }
  }

  useEffect(() => {
    if (currentView === 'requestor') fetchNeeds()
  }, [currentView])

  // -- API: Add New Zone --
  const handleAddZone = async (e) => {
    e.preventDefault() 
    try {
      const response = await fetch('http://127.0.0.1:8000/api/needs', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(newZone),
      })
      if (response.ok) {
        fetchNeeds()
        setNewZone({ region: '', priority: '', portCapacity: '', status: 'Stable' })
      }
    } catch (error) {
      console.error("Failed to add new zone.", error)
    }
  }

  // -- API: Submit Donation --
  const handleDonate = async (e) => {
    e.preventDefault()
    try {
      const response = await fetch('http://127.0.0.1:8000/api/donate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ raw_manifest: donorInput })
      })
      const data = await response.json()
      setTriageResult(data) // Save the backend's response to display it
    } catch (error) {
      console.error("Failed to process donation.", error)
    }
  }

  return (
    <div style={{ textAlign: 'center', padding: '50px', fontFamily: 'sans-serif' }}>
      <h1>ResRoute Command Center</h1>
      <p>Coordinating relief at the speed of data.</p>

      {/* HOME SCREEN */}
      {currentView === 'home' && (
        <div style={{ marginTop: '40px' }}>
          <h2>Select Your Portal</h2>
          <div style={{ display: 'flex', justifyContent: 'center', gap: '20px', marginTop: '20px' }}>
            <button onClick={() => setCurrentView('donor')} style={{ padding: '20px', fontSize: '18px', cursor: 'pointer' }}>
              📦 Corporate Donor Portal<br/><small>Register incoming supplies</small>
            </button>
            <button onClick={() => setCurrentView('requestor')} style={{ padding: '20px', fontSize: '18px', cursor: 'pointer' }}>
              🚨 Crisis Ground Command<br/><small>Log real-time regional needs</small>
            </button>
          </div>
        </div>
      )}

      {/* DONOR SCREEN */}
      {currentView === 'donor' && (
        <div style={{ marginTop: '40px', display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
          <h2>Corporate Donor Portal</h2>
          <p>Paste your unstructured manifest below. The AI will parse and route it.</p>
          
          <form onSubmit={handleDonate} style={{ display: 'flex', flexDirection: 'column', gap: '15px', width: '400px', marginTop: '20px' }}>
            <textarea 
              rows="6"
              placeholder="e.g., We have 500 tents and 50 boxes of winter coats ready to ship..."
              required
              value={donorInput}
              onChange={(e) => setDonorInput(e.target.value)}
              style={{ padding: '10px', fontSize: '16px', borderRadius: '8px', border: '1px solid #444' }}
            />
            <button type="submit" style={{ padding: '12px', cursor: 'pointer', fontSize: '16px', fontWeight: 'bold' }}>
              Run AI Triage
            </button>
          </form>

          {/* Display the result from the Python backend */}
          {triageResult && (
            <div style={{ marginTop: '30px', padding: '20px', border: '2px solid #51cf66', borderRadius: '8px', width: '400px', textAlign: 'left', background: '#f9f9f9', color: 'black' }}>
              <h3 style={{ margin: '0 0 10px 0', color: '#2b8a3e' }}>System Response</h3>
              <p><strong>Status:</strong> {triageResult.status}</p>
              <p><strong>AI Action:</strong> {triageResult.ai_directive}</p>
              <p style={{ fontStyle: 'italic', fontSize: '14px', color: '#555' }}>"{triageResult.original_text}"</p>
            </div>
          )}

          <button onClick={() => {setCurrentView('home'); setTriageResult(null); setDonorInput('')}} style={{ padding: '10px', cursor: 'pointer', marginTop: '40px' }}>← Back to Home</button>
        </div>
      )}

      {/* REQUESTOR SCREEN (GROUND COMMAND) */}
      {currentView === 'requestor' && (
        <div style={{ marginTop: '40px', display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
          <h2>Crisis Ground Command</h2>
          <p>Active Regional Needs & Logistics Capacity</p>
          
          <form onSubmit={handleAddZone} style={{ display: 'flex', gap: '10px', marginBottom: '30px', padding: '15px', borderRadius: '8px', border: '1px solid #444' }}>
            <input type="text" placeholder="Region Name" required value={newZone.region} onChange={(e) => setNewZone({...newZone, region: e.target.value})} style={{ padding: '8px' }} />
            <input type="text" placeholder="Priority Need" required value={newZone.priority} onChange={(e) => setNewZone({...newZone, priority: e.target.value})} style={{ padding: '8px' }} />
            <input type="text" placeholder="Port Capacity" required value={newZone.portCapacity} onChange={(e) => setNewZone({...newZone, portCapacity: e.target.value})} style={{ padding: '8px' }} />
            <select value={newZone.status} onChange={(e) => setNewZone({...newZone, status: e.target.value})} style={{ padding: '8px' }}>
              <option value="Stable">Stable</option>
              <option value="Critical">Critical</option>
            </select>
            <button type="submit" style={{ cursor: 'pointer', padding: '8px 16px' }}>Add Zone</button>
          </form>

          <div style={{ display: 'flex', gap: '20px', flexWrap: 'wrap', justifyContent: 'center' }}>
            {regionalNeeds.map((zone, index) => (
              <div key={index} style={{ border: '1px solid #555', padding: '20px', borderRadius: '8px', textAlign: 'left', width: '250px' }}>
                <h3 style={{ margin: '0 0 10px 0' }}>{zone.region}</h3>
                <p><strong>Priority:</strong> {zone.priority}</p>
                <p><strong>Capacity:</strong> {zone.portCapacity}</p>
                <p style={{ color: zone.status === 'Critical' ? '#ff6b6b' : '#51cf66' }}><strong>Status:</strong> {zone.status}</p>
              </div>
            ))}
          </div>

          <button onClick={() => setCurrentView('home')} style={{ padding: '10px', cursor: 'pointer', marginTop: '30px' }}>← Back to Home</button>
        </div>
      )}
    </div>
  )
}

export default App