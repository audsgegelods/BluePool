import react from 'react'
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import Login from './pages/Login'
import Home from './pages/Home'
import Register from './pages/Register'
import NotFound from './pages/NotFound'
import RideList from './pages/Rides/RideList'
import RideCreate from './pages/Rides/RideCreate'
import RideDetail from './pages/Rides/RideDetail'
import ProtectedRoute from './components/ProtectedRoute'
import './styles/base.css'


function Logout() {
  localStorage.clear()
  return <Navigate to="/login" />
}

function RegisterAndLogout() {
  localStorage.clear()
  return <Register />
}

function App() {

  return (
    <BrowserRouter>
      <Routes>
        <Route 
          path="/"
          element={
            <ProtectedRoute>
              <Home />
            </ProtectedRoute>
          }
        />
        <Route path="/login/" element={<Login />} />
        <Route path="/logout/" element={<Logout />} />
        <Route path="/user/register/" element={<RegisterAndLogout />} />
        <Route path="/rides/" element={<RideList />} />
        <Route path="/rides/create/" element={<RideCreate />} />
        <Route path="/rides/:id/" element={<RideDetail />} />
        <Route path="*" element={<NotFound />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App
