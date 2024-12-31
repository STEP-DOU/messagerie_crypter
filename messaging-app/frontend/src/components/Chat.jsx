import React, { useState, useEffect } from "react";
import axios from "../services/api.js";

function Chat({ token }) {
    const [recipient, setRecipient] = useState("");
    const [message, setMessage] = useState("");
    const [messages, setMessages] = useState([]);

    const sendMessage = async () => {
        try {
            const response = await axios.post(
                "/send_message",
                {
                    sender: "your_username", // Changez par le username connecté
                    recipient,
                    message,
                },
                { headers: { Authorization: `Bearer ${token}` } }
            );
            alert(response.data.message);
        } catch (error) {
            console.error(error);
            alert("Erreur lors de l'envoi du message");
        }
    };

    const fetchMessages = async () => {
        try {
            const response = await axios.get(`/get_messages/your_username`, {
                headers: { Authorization: `Bearer ${token}` },
            });
            setMessages(response.data);
        } catch (error) {
            console.error(error);
            alert("Erreur lors de la récupération des messages");
        }
    };

    useEffect(() => {
        fetchMessages();
    }, []);

    return (
        <div>
            <h1>Messagerie</h1>
            <input
                type="text"
                placeholder="Destinataire"
                value={recipient}
                onChange={(e) => setRecipient(e.target.value)}
            />
            <textarea
                placeholder="Message"
                value={message}
                onChange={(e) => setMessage(e.target.value)}
            />
            <button onClick={sendMessage}>Envoyer</button>
            <div>
                <h2>Messages reçus</h2>
                {messages.map((msg, index) => (
                    <div key={index}>
                        <p><strong>De :</strong> {msg.sender}</p>
                        <p><strong>Message :</strong> {msg.encrypted_message}</p>
                    </div>
                ))}
            </div>
        </div>
    );
}

export default Chat;
