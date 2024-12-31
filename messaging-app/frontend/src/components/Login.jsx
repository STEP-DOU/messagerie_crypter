import React, { useState } from "react";
import axios from "../services/api.js";

function Login({ setToken }) {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [publicKey, setPublicKey] = useState("");

    const handleRegister = async () => {
        try {
            const response = await axios.post("/register", {
                username,
                password,
                public_key: publicKey,
            });
            alert(response.data.message);
        } catch (error) {
            console.error(error);
            alert("Erreur lors de l'inscription");
        }
    };

    const handleLogin = async () => {
        try {
            const response = await axios.post("/login", {
                username,
                password,
            });
            setToken(response.data.access_token);
        } catch (error) {
            console.error(error);
            alert("Erreur lors de la connexion");
        }
    };

    return (
        <div>
            <h1>Connexion ou Inscription</h1>
            <input
                type="text"
                placeholder="Nom d'utilisateur"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
            />
            <input
                type="password"
                placeholder="Mot de passe"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
            />
            <textarea
                placeholder="Clé publique (pour inscription uniquement)"
                value={publicKey}
                onChange={(e) => setPublicKey(e.target.value)}
            />
            <button onClick={handleRegister}>S'inscrire</button>
            <button onClick={handleLogin}>Se connecter</button>
        </div>
    );
}

export default Login;
