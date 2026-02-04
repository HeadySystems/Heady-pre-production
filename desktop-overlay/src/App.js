import React from 'react'
import { createRoot } from 'react-dom/client'
import './App.css'

const App = () => {
  return (
    <div className="overlay">
      <div className="companion-ui">
        <h1>HeadyE Companion</h1>
        {/* AI Task Assistant will be integrated here */}
      </div>
    </div>
  )
}

const container = document.getElementById('root')
const root = createRoot(container)
root.render(<App />)
