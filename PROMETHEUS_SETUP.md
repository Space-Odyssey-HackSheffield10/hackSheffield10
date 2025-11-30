# Prometheus Instrumentation Implementation

## Files Created/Modified

### 1. **app/metrics.py** (NEW)
Custom Prometheus metrics for Space Odyssey game tracking:
- `player_info`: Player name and session info
- `game_duration_seconds`: Game duration with player and status labels
- `game_completed`: Counter for games completed (success/timeout)
- `puzzle_completions_total`: Counter for completed puzzles
- `puzzle_attempts_total`: Counter for puzzle attempts
- `chat_messages_total`: Chat messages by player and sender (user/agent)
- `agent_messages_by_type`: Messages by specific agent type
- `game_timeouts_total`: Counter for game timeouts
- `agent_response_time`: Histogram for agent response times

Includes `MetricsTracker` helper class with methods to easily record events.

### 2. **main.py** (MODIFIED)
Added:
- Import of `MetricsTracker` and new models
- Updated `/chat` endpoint to track user/agent messages and response times
- New endpoint `/game/start`: Record when player starts game
- New endpoint `/game/end`: Record game completion with duration and status
- New endpoint `/puzzle/attempt`: Record puzzle attempts and completions

### 3. **app/models.py** (MODIFIED)
Added new Pydantic models:
- `AgentRequest`: Added `player_name` field
- `GameStartRequest`: For game start events
- `GameEndRequest`: For game end events (with duration and success)
- `PuzzleEventRequest`: For puzzle events

### 4. **app/src/scripts/script.js** (MODIFIED)
Added:
- `playerName` variable to store player's name from input
- `gameStartTime` to track game duration
- `closeStartingScreen()` now captures player name and calls `/game/start` API
- `timer()` calls `recordGameEnd(false)` on timeout
- `recordGameEnd()` function to call `/game/end` API
- Export `playerName` to global scope for other scripts

### 5. **app/src/scripts/modal.js** (MODIFIED)
Updated:
- `sendMessage()` now includes `player_name` in the request body

### 6. **app/src/scripts/number-slider.js** (MODIFIED)
Updated:
- `checkWin()` now calls `/puzzle/attempt` API when puzzle is completed

## API Endpoints

### POST /chat
**Body:**
```json
{
  "message": "string",
  "player_name": "string"
}
```
Tracks user messages, agent responses, and response times.

### POST /game/start
**Body:**
```json
{
  "player_name": "string"
}
```
Records when a player starts a game.

### POST /game/end
**Body:**
```json
{
  "player_name": "string",
  "duration": 120.5,
  "success": true
}
```
Records game completion with duration in seconds and success status.

### POST /puzzle/attempt
**Body:**
```json
{
  "player_name": "string",
  "completed": true
}
```
Records puzzle attempts and completions.

## Metrics Available in Prometheus

All metrics are labeled with `player` for per-player tracking:

1. `game_duration_seconds{player="PlayerName", status="success|timeout"}`
2. `game_completed{player="PlayerName", status="success|timeout"}`
3. `puzzle_completions_total{player="PlayerName"}`
4. `chat_messages_total{player="PlayerName", sender="user|agent"}`
5. `agent_messages_by_type{player="PlayerName", agent_type="triage|director|..."}`
6. `game_timeouts_total{player="PlayerName"}`
7. `agent_response_time_seconds{agent_type="..."}`

## How to Use

1. **Start your services:**
   ```bash
   docker-compose up -d
   fastapi run main.py
   ```

2. **Access Prometheus:** http://localhost:9090
   - Query example: `game_duration_seconds`

3. **Access Grafana:** http://localhost:3000
   - Login: admin/admin
   - Import dashboard from: `app/infra/grafana/space-odyssey-dashboard.json`

4. **Play the game:**
   - Enter your name on the starting screen
   - Metrics are automatically tracked as you play

## Testing Metrics

You can query metrics directly at:
- http://localhost:8000/metrics

Example queries in Prometheus:
- `game_completed{status="success"}` - Successful games
- `sum(chat_messages_total{sender="user"})` - Total user messages
- `histogram_quantile(0.95, agent_response_time_seconds)` - 95th percentile response time
