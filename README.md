

## Setup Instructions

### Prerequisites

Before running the project, ensure the following are installed:

- **Python 3.8+**
- **Docker** (for containerization)
- **Docker Compose** (for managing multi-container Docker applications)
- **Redis** (for caching and Celery backend)
- **OpenAI API Key** (for GPT-3.5 integration)

### Steps

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/tone-rewriter.git
   cd tone-rewriter
   ```

2. **Create a `.env` file** in the root directory with the following content:

   ```env
   OPENAI_API_KEY="your-openai-api-key-here"
   REDIS_URL="redis://localhost:6379/0"
   ```

3. **Install dependencies:**

   Ensure you have `pip` and `venv` installed. Then, set up a virtual environment and install the required packages:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   pip install -r requirements.txt
   ```

4. **Start the Redis server (if not using Docker for Redis):**

   You can either install Redis locally or use Docker to run Redis.

   To run Redis using Docker, you can use the following command:

   ```bash
   docker run -p 6379:6379 redis
   ```

---

## Usage Guide

After setting up the environment, you can run the FastAPI server using Uvicorn.

1. **Run the FastAPI server:**

   ```bash
   uvicorn app.main:app --reload
   ```

2. **Access the API at** `http://localhost:8000`.

---

## API Reference

### 1. `POST /rewrite`

**Description:**  
This endpoint accepts a text and tone, then queues the rewrite task in the background using Celery.

**Request Body:**

```json
{
  "text": "Your text to be rewritten.",
  "tone": "formal"
}
```

**Response:**

```json
{
  "task_id": "some-task-id"
}
```

**Example Request:**

```bash
curl -X 'POST' \
  'http://localhost:8000/rewrite' \
  -H 'Content-Type: application/json' \
  -d '{
    "text": "Please send me the report by 5 PM.",
    "tone": "casual"
  }'
```

### 2. `GET /result/{task_id}`

**Description:**  
This endpoint checks the status of a rewrite task. If the task is complete, it returns the rewritten text. Otherwise, it returns the status "Processing...".

**Response:**

```json
{
  "result": "Rewritten text based on the requested tone."
}
```

**Example Request:**

```bash
curl -X 'GET' 'http://localhost:8000/result/some-task-id'
```

---

## Architecture Explanation

- **FastAPI**: A modern, fast (high-performance) web framework for building APIs with Python.
- **Celery**: Used for background task processing to handle asynchronous tasks like interacting with the OpenAI API for text rewriting.
- **Redis**: Used as a message broker for Celery and also to store the rewritten results as cache.
- **OpenAI GPT-3**: Utilized for rewriting text in various tones (formal, casual, etc.).

---

## Assumptions

- You already have a Redis server running, either locally or using Docker.
- You have an active OpenAI API key that is properly configured in the `.env` file.
- Docker Compose is being used to handle services like Redis and the backend server.
- The rewrite task takes a small amount of time to process depending on the text and tone. If the text is too long or complex, the API may take longer to respond.

---

## Example Input/Output

**Example Input 1:**

Request:

```json
{
  "text": "Please send me the report by 5 PM.",
  "tone": "casual"
}
```

Response:

```json
{
  "task_id": "3f2d7ef5-038b-4a95-adba-759b53ddd4de"
}
```

**Example Input 2:**

Request:

```json
{
  "task_id": "3f2d7ef5-038b-4a95-adba-759b53ddd4de"
}
```

Response:

```json
{
  "result": "Hey, can you send me the report by 5 PM?"
}
```

---

## Docker Setup and Usage

### 1. **Build and start the Docker containers:**

In the project directory, run:

```bash
docker-compose up --build
```

This will build the Docker images for the FastAPI app and Celery worker and start the Redis container.

### 2. **Stopping the Docker containers:**

To stop the containers, run:

```bash
docker-compose down
```

### 3. **Access the API:**

- Once the containers are up, you can access the API at `http://localhost:8000`.
- To test the API, you can use tools like **Postman** or **cURL**.

---

## Conclusion

This README provides an overview of setting up and running the Tone Rewriter API, including the usage of Docker for containerization and Redis for background task processing. The FastAPI framework serves the API endpoints, while Celery handles background tasks asynchronously. 

