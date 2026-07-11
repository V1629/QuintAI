import { BrowserRouter, Routes, Route } from 'react-router-dom'
import QuintAILanding from './pages/QuintAILanding'

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<QuintAILanding />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App