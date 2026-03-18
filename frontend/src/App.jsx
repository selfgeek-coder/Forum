import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import Home from "./pages/Home";
import Post from "./pages/Post";
import Login from "./pages/Login";
import Register from "./pages/Register";
import "./index.css";

function App() {
    return (
        <Router>
            <Routes>
                <Route path="/" element={<Home />} />
                <Route path="/post/:id" element={<Post />} />
                <Route path="/login" element={<Login />} />
                <Route path="/register" element={<Register />} />
                <Route path="/create-post" element={<Navigate to="/?create=1" replace />} />
            </Routes>
        </Router>
    );
}

export default App;