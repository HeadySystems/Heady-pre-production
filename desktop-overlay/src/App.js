// HEADY_BRAND:BEGIN
// HEADY SYSTEMS :: SACRED GEOMETRY
// FILE: desktop-overlay/src/App.js
// LAYER: root
// 
//         _   _  _____    _  __   __
//        | | | || ____|  / \ \  / /
//        | |_| ||  _|   / _ \ \ V / 
//        |  _  || |___ / ___ \ | |  
//        |_| |_||_____/_/   \_\|_|  
// 
//    Sacred Geometry :: Organic Systems :: Breathing Interfaces
// HEADY_BRAND:END

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
