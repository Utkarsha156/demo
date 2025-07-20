-- Users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Stories table
CREATE TABLE stories (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    title VARCHAR(255),
    user_input TEXT NOT NULL,
    conversation_history JSON,
    country_theme VARCHAR(100) DEFAULT 'Indian',
    status VARCHAR(50) DEFAULT 'in_progress',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Story pages table
CREATE TABLE story_pages (
    id SERIAL PRIMARY KEY,
    story_id INTEGER REFERENCES stories(id),
    page_number INTEGER NOT NULL,
    content TEXT NOT NULL,
    image_url VARCHAR(500),
    image_prompt TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(story_id, page_number)
);

-- Indexes for better performance
CREATE INDEX idx_stories_user_id ON stories(user_id);
CREATE INDEX idx_story_pages_story_id ON story_pages(story_id);