import axios from 'axios';
import {
    BrowserRouter,
    Routes,
    Route,
    Navigate
} from "react-router-dom";

import Login from "./pages/Login";
import Main from "./pages/Main";
import Register from "./pages/Register";

let token;

try {
  token = await axios.post(
    "/api/auth/refresh",
    {},
    { withCredentials: true }
  );
} catch (error) {
  token = error.response;
}

function ProtectedRoute({ children }) {
    if (token.status != 200) {
        return <Navigate to="/login" replace />;
    }

    return children;
}

export default function App() {
    return (
        <BrowserRouter>
            <Routes>
                <Route path="/login" element={<Login />} />
                <Route path="/register" element={<Register />} />

                <Route
                    path="/"
                    element={
                        <ProtectedRoute>
                            <Main />
                        </ProtectedRoute>
                    }
                />

                <Route path="*" element={<Navigate to="/" replace />} />
            </Routes>
        </BrowserRouter>
    );
}