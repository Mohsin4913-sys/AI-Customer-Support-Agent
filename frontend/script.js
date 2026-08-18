const textarea = document.getElementById("question");
const form = document.getElementById("questionForm");
const sendButton = document.getElementById("sendButton");
const chatArea = document.getElementById("chatArea");


// ========================================
// Auto resize textarea
// ========================================

if (textarea) {

    textarea.addEventListener("input", function () {

        this.style.height = "auto";

        this.style.height =
            Math.min(this.scrollHeight, 120) + "px";

    });

}


// ========================================
// Enter to send
// Shift + Enter = new line
// ========================================

if (textarea) {

    textarea.addEventListener("keydown", function (event) {

        if (event.key === "Enter" && !event.shiftKey) {

            event.preventDefault();

            if (this.value.trim() !== "") {
                form.requestSubmit();
            }

        }

    });

}


// ========================================
// Submit question to Flask
// ========================================

if (form) {

    form.addEventListener("submit", async function (event) {

        event.preventDefault();

        const question = textarea.value.trim();

        if (!question) {
            return;
        }


        // Show customer message
        addMessage("user", question);


        // Clear input
        textarea.value = "";
        textarea.style.height = "auto";


        // Disable button
        sendButton.disabled = true;
        sendButton.innerHTML = "…";


        // Show loading message
        const loadingMessage = addLoadingMessage();


        try {

            const response = await fetch(
                "http://127.0.0.1:5000/ask",
                {
                    method: "POST",

                    headers: {
                        "Content-Type": "application/json"
                    },

                    body: JSON.stringify({
                        question: question
                    })
                }
            );


            const data = await response.json();


            // Remove loading message
            loadingMessage.remove();


            if (!response.ok) {

                addMessage(
                    "ai",
                    data.error || "Something went wrong."
                );

                return;
            }


            // Display AI answer
            addMessage(
                "ai",
                data.answer
            );


        } catch (error) {

            console.error(error);

            loadingMessage.remove();

            addMessage(
                "ai",
                "Unable to connect to the AI support server. Please make sure Flask is running."
            );

        } finally {

            sendButton.disabled = false;

            sendButton.innerHTML = "<span>➤</span>";

        }

    });

}


// ========================================
// Add message to chat
// ========================================

function addMessage(type, text) {

    const message = document.createElement("div");

    message.className =
        type === "user"
            ? "message user-message"
            : "message ai-message";


    const avatar = document.createElement("div");

    avatar.className =
        type === "user"
            ? "avatar user-avatar"
            : "avatar ai-avatar";

    avatar.textContent =
        type === "user"
            ? "You"
            : "AI";


    const content = document.createElement("div");

    content.className = "message-content";


    const label = document.createElement("div");

    label.className = "message-label";

    label.textContent =
        type === "user"
            ? "You"
            : "AI Support Agent";


    const bubble = document.createElement("div");

    bubble.className =
        type === "user"
            ? "message-bubble"
            : "message-bubble ai-bubble";


    // ========================================
    // Render AI Markdown
    // ========================================

    if (type === "ai") {

        bubble.innerHTML = marked.parse(text);

    } else {

        bubble.textContent = text;

    }


    content.appendChild(label);

    content.appendChild(bubble);

    message.appendChild(avatar);

    message.appendChild(content);

    chatArea.appendChild(message);


    scrollToBottom();
}


// ========================================
// Loading message
// ========================================

function addLoadingMessage() {

    const message = document.createElement("div");

    message.className = "message ai-message";


    const avatar = document.createElement("div");

    avatar.className = "avatar ai-avatar";

    avatar.textContent = "AI";


    const content = document.createElement("div");

    content.className = "message-content";


    const label = document.createElement("div");

    label.className = "message-label";

    label.textContent = "AI Support Agent";


    const loading = document.createElement("div");

    loading.className = "message-bubble ai-bubble loading";


    loading.innerHTML = `
        Thinking
        <div class="loading-dots">
            <span></span>
            <span></span>
            <span></span>
        </div>
    `;


    content.appendChild(label);

    content.appendChild(loading);

    message.appendChild(avatar);

    message.appendChild(content);

    chatArea.appendChild(message);


    scrollToBottom();


    return message;
}


// ========================================
// Suggestion buttons
// ========================================

function useSuggestion(question) {

    if (!textarea) {
        return;
    }

    textarea.value = question;

    textarea.style.height = "auto";

    textarea.style.height =
        Math.min(textarea.scrollHeight, 120) + "px";

    textarea.focus();

}


// ========================================
// New conversation
// ========================================

function newChat() {

    chatArea.innerHTML = `
        <div class="welcome-section" id="welcomeSection">

            <div class="welcome-icon">
                ✦
            </div>

            <h2>
                How can I help you?
            </h2>

            <p>
                I can help you with orders, payments,
                support tickets and company policies.
            </p>

            <div class="suggestions">

                <button
                    type="button"
                    onclick="useSuggestion('What is the status of order ORD1001?')"
                >
                    📦
                    <span>
                        <strong>Check an order</strong>
                        <small>What is the status of ORD1001?</small>
                    </span>
                </button>

                <button
                    type="button"
                    onclick="useSuggestion('What products are in order ORD1001?')"
                >
                    🛍️
                    <span>
                        <strong>View order items</strong>
                        <small>What products are in ORD1001?</small>
                    </span>
                </button>

                <button
                    type="button"
                    onclick="useSuggestion('How did I pay for order ORD1001?')"
                >
                    💳
                    <span>
                        <strong>Check payment</strong>
                        <small>How did I pay for ORD1001?</small>
                    </span>
                </button>

                <button
                    type="button"
                    onclick="useSuggestion('Can I return a product after 40 days?')"
                >
                    📚
                    <span>
                        <strong>Ask about a policy</strong>
                        <small>Can I return a product after 40 days?</small>
                    </span>
                </button>

            </div>

        </div>
    `;

    textarea.value = "";

    textarea.style.height = "auto";

    textarea.focus();

    scrollToBottom();
}


// ========================================
// Scroll chat
// ========================================

function scrollToBottom() {

    if (chatArea) {

        chatArea.scrollTop =
            chatArea.scrollHeight;

    }

}