let tiles = [];
let emptyIndex = 8;
let moves = 0;
let num_list = [1, 2, 3, 4, 5, 6, 7, 8];
let won = false;

// Initialize the puzzle
function initPuzzle() {
    tiles = Array.from({ length: 9 }, (_, i) => i + 1);
    tiles[8] = 0; // 0 represents the empty space
    emptyIndex = 8;
    moves = 0;
    updateMoveCount();
    renderPuzzle();
    shuffleList(num_list);
    shufflePuzzle();
}

function shuffleList(array){
    for (let i = array.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [array[i], array[j]] = [array[j], array[i]];
    }
    console.log(num_list);
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
    const row = Math.floor(index / 3);
    const col = index % 3;
    const emptyRow = Math.floor(emptyIndex / 3);
    const emptyCol = emptyIndex % 3;

    return (
        (row === emptyRow && Math.abs(col - emptyCol) === 1) ||
        (col === emptyCol && Math.abs(row - emptyRow) === 1)
    );
}

// Move a tile
function moveTile(index) {
    if (canMove(index)) {
        [tiles[index], tiles[emptyIndex]] = [tiles[emptyIndex], tiles[index]];
        emptyIndex = index;
        moves++;
        updateMoveCount();
        renderPuzzle();
    }
}

// Shuffle the puzzle
function shufflePuzzle() {
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
    const row = Math.floor(emptyIndex / 3);
    const col = emptyIndex % 3;

    if (row > 0) validMoves.push(emptyIndex - 3); // up
    if (row < 2) validMoves.push(emptyIndex + 3); // down
    if (col > 0) validMoves.push(emptyIndex - 1); // left
    if (col < 2) validMoves.push(emptyIndex + 1); // right

    return validMoves;
}

// Reset to solved state
function resetPuzzle() {
    // tiles = Array.from({ length: 9 }, (_, i) => i + 1);
    tiles = num_list;
    tiles[8] = 0;
    emptyIndex = 8;
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
        if (index === 8) return value === 0;
        return value === num_list[index];
    });
    const conversation_id = localStorage.getItem("conversation_id")

    if (isSolved && moves > 0) {
        document.getElementById('winMessage').classList.add('show');
        won = true;

        const counter = document.getElementById("timer");
        const [minutes, seconds] = counter.innerHTML.split(":").map(Number);
        const time = (minutes * 60) + seconds

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
