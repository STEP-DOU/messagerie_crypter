import React, { useState } from "react";
import Login from "./components/Login.jsx";
import Chat from "./components/Chat.jsx";

function App() {
    const [token, setToken] = useState(null);

    return (
        <div>
            {!token ? (
                <Login setToken={setToken} />
            ) : (
                <Chat token={token} />
            )}
        </div>
    );
}

export default App;
