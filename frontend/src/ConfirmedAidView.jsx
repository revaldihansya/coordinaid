import React, { useState, useEffect } from 'react';

function ConfirmedAidView({ onBack }) {
  const [confirmedAid, setConfirmedAid] = useState([]);

  useEffect(() => {
    const fetchConfirmedAid = async () => {
      try {
        const response = await fetch('http://127.0.0.1:8000/api/confirmed');
        const data = await response.json();
        setConfirmedAid(data);
      } catch (error) {
        console.error("Failed to fetch confirmed aid data.", error);
      }
    };
    fetchConfirmedAid();
  }, []);

  return (
    <div style={{ marginTop: '40px', display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
      <h2>Confirmed Aid Routes</h2>
      <p>Tracking successfully routed and verified supply chains.</p>
      
      <div style={{ display: 'flex', gap: '20px', flexWrap: 'wrap', justifyContent: 'center', marginTop: '20px' }}>
        {confirmedAid.length === 0 ? <p>No confirmed aid routes active yet.</p> : null}
        
        {confirmedAid.map((aid, index) => (
          <div key={index} style={{ border: '2px solid #339af0', padding: '20px', borderRadius: '8px', textAlign: 'left', width: '300px', background: '#e7f5ff', color: 'black' }}>
            <h3 style={{ margin: '0 0 10px 0', color: '#1864ab' }}>Route: {aid.destination_route}</h3>
            <p><strong>Donation:</strong> {aid.donation}</p>
            <p><strong>Donor:</strong> {aid.donor}</p>
            <p><strong>Time:</strong> {new Date(aid.timestamp).toLocaleString()}</p>
            <hr style={{ borderColor: '#a5d8ff', margin: '15px 0' }} />
            <p style={{ fontStyle: 'italic', fontSize: '14px', margin: 0, color: '#495057' }}>
              Manifest: "{aid.manifest}"
            </p>
          </div>
        ))}
      </div>

      <button onClick={onBack} style={{ padding: '10px', cursor: 'pointer', marginTop: '40px' }}>← Back to Home</button>
    </div>
  );
}

export default ConfirmedAidView;