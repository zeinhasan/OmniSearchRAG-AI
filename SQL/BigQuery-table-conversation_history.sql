CREATE TABLE `your_project_id.your_dataset_id.conversation_history` (
    id INT64,                           -- Unique ID for each entry
    user_id INT64 NOT NULL,             -- ID of the user
    query STRING NOT NULL,              -- User's query
    response STRING NOT NULL,           -- AI model's response
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP()  -- Timestamp of the conversation
);