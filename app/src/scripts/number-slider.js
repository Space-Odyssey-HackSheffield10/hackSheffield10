let tiles = [];
let emptyIndex = 15;
let moves = 0;

// Initialize the puzzle
function initPuzzle() {
    tiles = Array.from({ length: 16 }, (_, i) => i + 1);
    tiles[15] = 0; // 0 represents the empty space
    emptyIndex = 15;
    moves = 0;
    updateMoveCount();
    renderPuzzle();
    shufflePuzzle();
}

// Render the puzzle grid
function renderPuzzle() {
    const grid = document.getElementById('puzzleGrid');
    grid.innerHTML = '';
    
    tiles.forEach((value, index) => {
        const tile = document.createElement('div');
        tile.className = value === 0 ? 'tile empty' : 'tile';
        tile.textContent = value === 0 ? '' : value;
        tile.onclick = () => moveTile(index);
        grid.appendChild(tile);
    });

    checkWin();
}

// Check if tile can be moved
function canMove(index) {
    const row = Math.floor(index / 4);
    const col = index % 4;
    const emptyRow = Math.floor(emptyIndex / 4);
    const emptyCol = emptyIndex % 4;

    // Check if tile is adjacent to empty space
    return (
        (row === emptyRow && Math.abs(col - emptyCol) === 1) ||
        (col === emptyCol && Math.abs(row - emptyRow) === 1)
    );
}

// Move a tile
function moveTile(index) {
    if (canMove(index)) {
        // Swap tile with empty space
        [tiles[index], tiles[emptyIndex]] = [tiles[emptyIndex], tiles[index]];
        emptyIndex = index;
        moves++;
        updateMoveCount();
        renderPuzzle();
    }
}

// Shuffle the puzzle
function shufflePuzzle() {
    // Perform random valid moves to ensure solvability
    const shuffleMoves = 100;
    for (let i = 0; i < shuffleMoves; i++) {
        const validMoves = getValidMoves();
        const randomMove = validMoves[Math.floor(Math.random() * validMoves.length)];
        [tiles[randomMove], tiles[emptyIndex]] = [tiles[emptyIndex], tiles[randomMove]];
        emptyIndex = randomMove;
    }
    moves = 0;
    updateMoveCount();
    document.getElementById('winMessage').classList.remove('show');
    renderPuzzle();
}

// Get all valid moves
function getValidMoves() {
    const validMoves = [];
    const row = Math.floor(emptyIndex / 4);
    const col = emptyIndex % 4;

    // Check up, down, left, right
    if (row > 0) validMoves.push(emptyIndex - 4); // up
    if (row < 3) validMoves.push(emptyIndex + 4); // down
    if (col > 0) validMoves.push(emptyIndex - 1); // left
    if (col < 3) validMoves.push(emptyIndex + 1); // right

    return validMoves;
}

// Reset to solved state
function resetPuzzle() {
    tiles = Array.from({ length: 16 }, (_, i) => i + 1);
    tiles[15] = 0;
    emptyIndex = 15;
    moves = 0;
    updateMoveCount();
    document.getElementById('winMessage').classList.remove('show');
    renderPuzzle();
}

// Update move counter
function updateMoveCount() {
    document.getElementById('moveCount').textContent = moves;
}

// Check if puzzle is solved
async function checkWin() {
    const isSolved = tiles.every((value, index) => {
        if (index === 15) return value === 0;
        return value === index + 1;
    });
    const conversation_id = localStorage.getItem("conversation_id");
    const playerName = localStorage.getItem("username") || "anonymous";

    if (isSolved && moves > 0) {
        document.getElementById('winMessage').classList.add('show');

        const counter = document.getElementById("timer");
        const [minutes, seconds] = counter.innerHTML.split(":").map(Number);
        const time = (minutes * 60) + seconds

        // Record puzzle completion metric
        try {
            await fetch("/puzzle/complete", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    conversation_id,
                    player_name: playerName,
                    puzzle_name: "number-slider"
                })
            });
            console.log("SUCCESS recorded puzzle completion");
        } catch (err) {
            console.error("Failed to record puzzle completion:", err);
        }

        try {
            const response = await fetch("/add_time", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*"
                },
                body: JSON.stringify({
                    conversation_id,
                    time
                })
            });
            console.log("SUCCESS added time")
        } catch (err) {
            console.error(err);
        }

        try {
            const response = await fetch("/add_messages", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*"
                },
                body: JSON.stringify({
                    conversation_id
                })
            });
            console.log("SUCCESS added message")
        } catch (err) {
            console.error(err);
        }

    }
}

// Initialize on load
initPuzzle();
