

import { BrowserRouter as Router, Routes, Route  } from "react-router-dom";
import Home from "./Home";
import VilleDetail from "./VilleDetail";

function App() {
  return (
    <Router>
    
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/ville/:villeP" element={<VilleDetail />} />
      </Routes>
    </Router>
  );
}

export default App;


