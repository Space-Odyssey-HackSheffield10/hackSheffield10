"""
Prometheus metrics for Space Odyssey game tracking
"""

from prometheus_client import Counter, Gauge, Histogram, Info

# Player info
player_info = Info('player_name', 'Player name and session info')

# Game duration tracking
game_duration_seconds = Gauge(
    'game_duration_seconds',
    'Duration of game in seconds',
    ['player', 'status']
)

# Game completion tracking
game_completed = Counter(
    'game_completed',
    'Total number of games completed',
    ['player', 'status']  # status: 'success' or 'timeout'
)

# Puzzle tracking
puzzle_completions_total = Counter(
    'puzzle_completions_total',
    'Total number of puzzles completed',
    ['player']
)

puzzle_attempts_total = Counter(
    'puzzle_attempts_total',
    'Total number of puzzle attempts',
    ['player']
)

# Chat message tracking
chat_messages_total = Counter(
    'chat_messages_total',
    'Total chat messages sent',
    ['player', 'sender']  # sender: 'user' or 'agent'
)

# Agent-specific message tracking
agent_messages_by_type = Counter(
    'agent_messages_by_type',
    'Messages sent by specific agent types',
    ['player', 'agent_type']  # agent_type: director, engineer, navigator, etc.
)

# Game timeout tracking
game_timeouts_total = Counter(
    'game_timeouts_total',
    'Total number of game timeouts',
    ['player']
)

# Response time for agent interactions
agent_response_time = Histogram(
    'agent_response_time_seconds',
    'Agent response time in seconds',
    ['agent_type']
)


class MetricsTracker:
    """Helper class to track game metrics"""
    
    @staticmethod
    def set_player_name(player_name: str):
        """Set the current player's name"""
        player_info.info({'player': player_name})
    
    @staticmethod
    def record_game_start(player_name: str):
        """Record when a game starts"""
        pass  # Can add game start tracking if needed
    
    @staticmethod
    def record_game_completion(player_name: str, duration: float, success: bool):
        """Record game completion with duration and status"""
        status = 'success' if success else 'timeout'
        game_duration_seconds.labels(player=player_name, status=status).set(duration)
        game_completed.labels(player=player_name, status=status).inc()
        
        if not success:
            game_timeouts_total.labels(player=player_name).inc()
    
    @staticmethod
    def record_puzzle_attempt(player_name: str):
        """Record a puzzle attempt"""
        puzzle_attempts_total.labels(player=player_name).inc()
    
    @staticmethod
    def record_puzzle_completion(player_name: str):
        """Record a successful puzzle completion"""
        puzzle_completions_total.labels(player=player_name).inc()
    
    @staticmethod
    def record_user_message(player_name: str):
        """Record a message sent by the user"""
        chat_messages_total.labels(player=player_name, sender='user').inc()
    
    @staticmethod
    def record_agent_message(player_name: str, agent_type: str = 'unknown'):
        """Record a message sent by an agent"""
        chat_messages_total.labels(player=player_name, sender='agent').inc()
        agent_messages_by_type.labels(player=player_name, agent_type=agent_type).inc()
    
    @staticmethod
    def record_agent_response_time(agent_type: str, duration: float):
        """Record agent response time"""
        agent_response_time.labels(agent_type=agent_type).observe(duration)
