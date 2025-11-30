# Cosmos DB Prometheus Integration

## Overview
The application now pulls data from Azure Cosmos DB and exposes it as Prometheus metrics for Grafana dashboards.

## Implementation

### 1. New Database Function (`app/database.py`)
- `get_all_users()`: Fetches all users from the Cosmos DB "users" table

### 2. Updated Metrics (`app/metrics.py`)
Added new Cosmos DB-sourced metrics:
- `player_time_remaining_seconds{player, conversation_id}`: Time remaining for each player
- `player_message_count{player, conversation_id}`: Number of messages sent by each player
- `total_active_players`: Total number of active players
- `player_last_activity_timestamp{player, conversation_id}`: Unix timestamp of last activity

New method:
- `MetricsTracker.update_from_cosmos_db(users_data)`: Updates metrics from Cosmos DB data

### 3. Updated Main Application (`main.py`)
- Added background task `update_metrics_from_db()` that runs every 10 seconds
- Fetches all users from Cosmos DB and updates Prometheus metrics
- Starts automatically on application startup
- Enhanced `/chat` endpoint to track player name, user messages, agent messages, and response times

### 4. Updated Grafana Dashboard
The dashboard now uses Cosmos DB metrics:
- **Your Mission Time**: Shows `player_time_remaining_seconds` (time left, not time elapsed)
- **Your Time vs Other Players**: Compares time remaining across all players
- **Your Messages to AI Crew**: Shows `player_message_count` from Cosmos DB

## Data Flow

```
Azure Cosmos DB (users table)
        ↓
Background task (every 10s)
        ↓
MetricsTracker.update_from_cosmos_db()
        ↓
Prometheus Metrics (/metrics endpoint)
        ↓
Grafana Dashboard
```

## Cosmos DB Schema Used

```json
{
    "id": "conv_xxx",
    "name": "player_name",
    "time": 115,                    // Time remaining in seconds
    "messages": 5,                  // Number of messages sent
    "last_message_time": "ISO8601", // Last activity timestamp
    "last_message_role": "agent",
    "last_agent_message": "text"
}
```

## Available Metrics

### From Cosmos DB (updated every 10s):
- `player_time_remaining_seconds`: Time left for each player
- `player_message_count`: Messages sent by each player
- `total_active_players`: Count of all players
- `player_last_activity_timestamp`: Last activity time

### From Application Events (real-time):
- `chat_messages_total{player, sender}`: Chat messages by player and sender type
- `agent_messages_by_type{player, agent_type}`: Messages by specific agent
- `agent_response_time_seconds`: Agent response time histogram
- `puzzle_completions_total{player}`: Puzzle completions
- `puzzle_attempts_total{player}`: Puzzle attempts

## Grafana Queries

Example queries you can use:

```promql
# Time remaining for a specific player
player_time_remaining_seconds{player="John"}

# All players sorted by time remaining
sort_desc(player_time_remaining_seconds)

# Total active players
total_active_players

# Message count comparison
sort_desc(player_message_count)

# Players who messaged in last 5 minutes
player_last_activity_timestamp > (time() - 300)
```

## Running the Application

1. **Start Docker services:**
   ```bash
   docker-compose up -d
   ```

2. **Start FastAPI:**
   ```bash
   python3 -m uvicorn main:app --reload
   ```

3. **Access Grafana:** http://localhost:3000
   - Import dashboard from: `app/infra/grafana/space-odyssey-dashboard.json`

4. **View Metrics:** http://localhost:8000/metrics

## Notes

- Metrics update every 10 seconds from Cosmos DB
- Real-time events (chat, puzzles) are tracked immediately
- All metrics are labeled with player name for filtering
- Dashboard supports player selection via dropdown
