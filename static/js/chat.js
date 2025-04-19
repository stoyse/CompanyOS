document.addEventListener("DOMContentLoaded", () => {
    const chatBox = document.getElementById("chat-box");
    const chatInput = document.getElementById("chat-input");
    const sendButton = document.getElementById("send-button");
    const recipient = chatBox.dataset.username;

    function loadChat() {
        fetch(`/chat/${recipient}`)
            .then(response => response.json())
            .then(messages => {
                chatBox.innerHTML = "";
                messages.forEach(msg => {
                    const messageDiv = document.createElement("div");
                    messageDiv.className = msg.sender === recipient ? "text-left mb-2" : "text-right mb-2";
                    messageDiv.innerHTML = `
                        <span class="inline-block px-3 py-2 rounded ${msg.sender === recipient ? 'bg-gray-200 text-black' : 'bg-blue-500 text-white'}">
                            <strong>${msg.sender}</strong>: ${msg.content}
                        </span>
                    `;
                    chatBox.appendChild(messageDiv);
                });
                chatBox.scrollTop = chatBox.scrollHeight; // Auto-scroll to bottom
            });
    }

    function sendMessage() {
        const content = chatInput.value.trim();
        if (content === "") return;

        fetch(`/chat/${recipient}`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ message: content })
        }).then(() => {
            chatInput.value = "";
            loadChat();
        });
    }

    sendButton.addEventListener("click", sendMessage);

    chatInput.addEventListener("keydown", (e) => {
        if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });

    loadChat();
    setInterval(loadChat, 5000); // Refresh alle 5 Sekunden
});