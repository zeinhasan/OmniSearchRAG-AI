CREATE TABLE conversation_history (
    id INT AUTO_INCREMENT PRIMARY KEY,  -- Unique ID for each entry
    user_id INT NOT NULL,               -- ID of the user
    query TEXT NOT NULL,                -- User's query
    response TEXT NOT NULL,             -- AI model's response
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP  -- Timestamp of the conversation
);