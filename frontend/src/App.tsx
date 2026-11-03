import { useRef, useState } from 'react'
import { heartDiseaseAPI } from './services/api'

export default function App() {
  const [status, setStatus] = useState<'idle' | 'loading' | 'ok' | 'error'>('idle')
  const [message, setMessage] = useState<string>('')
  const pending = useRef(false)

  const ping = async () => {
    if (pending.current) return
    pending.current = true
    setStatus('loading')
    setMessage('')
    try {
      const data = await heartDiseaseAPI.getHealthStatus()
      setMessage(JSON.stringify(data, null, 2))
      setStatus('ok')
    } catch (error: unknown) {
      setMessage(error instanceof Error ? error.message : 'Health check failed')
      setStatus('error')
    } finally {
      pending.current = false
    }
  }

  return (
    <div style={{ padding: 24, fontFamily: 'system-ui, sans-serif' }}>
      <h1>Heart Disease Prediction</h1>
      <p role="status">Backend request: <strong>{status}</strong></p>
      <button onClick={ping} disabled={status === 'loading'} aria-busy={status === 'loading'}>Ping API</button>
      <pre aria-label="API response">{message}</pre>
    </div>
  )
}
