# hackSheffield10 - Space Odyssey Game Simulator and Data Visualization
---

## Overview
Space Odyssey is a first-person game where you must try to safely land your spaceship by solving puzzles using the guidance of your agent comrades. However, not all information your comrades give will help you, so it is up to you to try to decipher their clues and survive!

## Tech Stack
- Vanilla JS, HTML, and CSS frontend
- FastAPI backend
- Integration with OpenAI agents for multi-agent and human interaction
- Azure Cosmos DB for data storage
- Prometheus and Grafana for data collection and visualization

## Running the Application
To run the application locally follow these simple steps in a terminal:
```
python -m venv .venv
python -m pip install --upgrade pip
pip install -r requirements.txt
```
Then to run it 
```
fastapi dev main.py # DEV version
```
OR
```
fastapi run main.py # PROD version
```

## Plan
- Game similar to keep talking and noone explodes but the user is trying to land prepare for emergency landing of their spaceship
- There are 2 panels on their ship's dashboard
- The left panel contains a groupchat, the user is actively recieving messages from a Navigator, an Engineer and a Director
- The user is unable to message in this groupchat, only read them
- The user must read these messages before they disappear off the top of the screen, however some will be useful instructions to solve the puzzles to prepare for landing, others will be the team panicking etc
- The right panel will contain the games/activities the user has to complete
- Making a mistake will cause the user to crash and the game will end
- After losing, there will be a link to a grafana page where the user can look at their game stats
