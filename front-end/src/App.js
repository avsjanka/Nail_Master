import './App.css';
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import Admin from './components/Admin';
import User from './components/User';
import Shop from './components/Shop';

function App() {
  return (
    <div className="App">
      <BrowserRouter>
        <Routes>
          <Route extract path = "/" element = {<Shop/>}/>
          <Route extract path="/admin" element={<Admin />} />
          <Route extract path="/user" element={<User />} />
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;
