from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import uvicorn
import os

app = FastAPI(title="Blackjack n Probability API", version="1.0.0")

# CORS middleware for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
frontend_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")
images_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "images")
styles_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "styles")

app.mount("/static", StaticFiles(directory=frontend_path), name="static")
app.mount("/images", StaticFiles(directory=images_path), name="images")
app.mount("/styles", StaticFiles(directory=styles_path), name="styles")

@app.get("/")
async def root():
    """Serve the main game page"""
    game_html_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend", "game.html")
    return FileResponse(game_html_path)

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/game/new")
async def new_game():
    """Start a new blackjack game"""
    return {
        "game_id": "game_123",
        "status": "started",
        "player_cards": [],
        "dealer_cards": [],
        "message": "New game started"
    }

@app.post("/game/{game_id}/hit")
async def hit_card(game_id: str):
    """Player hits (draws a card)"""
    return {
        "game_id": game_id,
        "action": "hit",
        "new_card": "ace_of_hearts",
        "player_total": 21,
        "status": "active"
    }

@app.post("/game/{game_id}/stand")
async def stand(game_id: str):
    """Player stands (ends turn)"""
    return {
        "game_id": game_id,
        "action": "stand",
        "dealer_cards": ["king_of_spades", "7_of_hearts"],
        "dealer_total": 17,
        "outcome": "win",
        "status": "completed"
    }

def simulate_blackjack_game(player_value=None, dealer_up_card=None, action="random"):
    """Simulate a single blackjack game"""
    import random
    
    # If no specific values provided, simulate a complete random game
    if player_value is None:
        # Simulate initial deal - more realistic card distribution
        deck = [1,2,3,4,5,6,7,8,9,10,10,10,10] * 4  # Standard deck
        random.shuffle(deck)
        
        card1 = deck.pop()
        card2 = deck.pop()
        
        player_value = 0
        aces = 0
        
        for card in [card1, card2]:
            if card == 1:  # Ace
                aces += 1
                player_value += 11
            else:
                player_value += card
        
        # Adjust for aces
        while player_value > 21 and aces > 0:
            player_value -= 10
            aces -= 1
            
        # Simulate optimal basic strategy play
        while player_value < 21:
            # Get dealer up card if not provided
            if dealer_up_card is None:
                dealer_up_card = deck.pop()
                if dealer_up_card == 1:
                    dealer_up_card = 11
            
            # Basic strategy decision
            should_hit = False
            if player_value <= 11:
                should_hit = True
            elif player_value == 12 and 4 <= dealer_up_card <= 6:
                should_hit = False
            elif player_value == 12:
                should_hit = True
            elif 13 <= player_value <= 16 and 2 <= dealer_up_card <= 6:
                should_hit = False
            elif 13 <= player_value <= 16:
                should_hit = True
            else:  # 17+
                should_hit = False
            
            if should_hit:
                new_card = deck.pop()
                if new_card == 1:
                    new_card = 11 if player_value + 11 <= 21 else 1
                player_value += new_card
            else:
                break
    
    if dealer_up_card is None:
        dealer_up_card = random.randint(1, 13)
        if dealer_up_card == 1:
            dealer_up_card = 11
        elif dealer_up_card > 10:
            dealer_up_card = 10
    
    # For specific hint simulations
    if action == "hit" and player_value is not None:
        hit_card = random.randint(1, 13)
        if hit_card == 1:
            hit_card = 11 if player_value + 11 <= 21 else 1
        elif hit_card > 10:
            hit_card = 10
        player_value += hit_card
    # If action is "stand", player_value stays the same
    
    # Player busts
    if player_value > 21:
        return "lose"
    
    # Simulate dealer play
    dealer_total = dealer_up_card
    
    # Dealer draws hole card
    hole_card = random.randint(1, 13)
    if hole_card == 1:
        hole_card = 11
    elif hole_card > 10:
        hole_card = 10
    dealer_total += hole_card
    
    # Dealer hits until 17+
    while dealer_total < 17:
        card = random.randint(1, 13)
        if card == 1:
            card = 11 if dealer_total + 11 <= 21 else 1
        elif card > 10:
            card = 10
        dealer_total += card
    
    # Determine winner
    if dealer_total > 21:
        return "win"
    elif player_value > dealer_total:
        return "win"
    elif player_value < dealer_total:
        return "lose"
    else:
        return "push"

@app.post("/analytics/simulation")
async def run_simulation(num_simulations: int = 10000, player_value: int = None, dealer_up_card: int = None):
    """Run Monte Carlo simulation - general or context-specific"""
    import time
    
    start_time = time.time()
    
    wins = 0
    losses = 0
    pushes = 0
    
    for _ in range(num_simulations):
        if player_value is not None and dealer_up_card is not None:
            # Context-specific simulation using optimal play
            result = simulate_blackjack_game(player_value, dealer_up_card, "optimal")
        else:
            # General blackjack simulation
            result = simulate_blackjack_game()
        
        if result == "win":
            wins += 1
        elif result == "lose":
            losses += 1
        else:
            pushes += 1
    
    end_time = time.time()
    execution_time_ms = (end_time - start_time) * 1000
    
    win_rate = wins / num_simulations
    loss_rate = losses / num_simulations
    push_rate = pushes / num_simulations
    
    context_msg = ""
    if player_value is not None and dealer_up_card is not None:
        context_msg = f" (Player: {player_value}, Dealer: {dealer_up_card})"
    
    return {
        "simulations": num_simulations,
        "win_rate": win_rate,
        "loss_rate": loss_rate,
        "push_rate": push_rate,
        "execution_time_ms": execution_time_ms,
        "expected_value": win_rate - loss_rate,
        "context": context_msg
    }

@app.get("/privacy/settings")
async def get_privacy_settings():
    """Get current privacy settings"""
    return {
        "privacy_mode": "standard",
        "telemetry_enabled": True,
        "data_retention_days": 365,
        "anonymization_enabled": False
    }

@app.post("/privacy/settings")
async def update_privacy_settings(privacy_mode: str, telemetry_enabled: bool):
    """Update privacy settings"""
    return {
        "privacy_mode": privacy_mode,
        "telemetry_enabled": telemetry_enabled,
        "message": "Privacy settings updated successfully"
    }

@app.post("/game/hint")
async def get_monte_carlo_hint(player_value: int, dealer_up_card: int, num_simulations: int = 10000):
    """Get Monte Carlo-based strategy hint using the same simulation engine"""
    import time
    
    start_time = time.time()
    
    # Simulate STAND scenario
    stand_wins = 0
    stand_losses = 0
    stand_pushes = 0
    
    # Simulate HIT scenario  
    hit_wins = 0
    hit_losses = 0
    hit_pushes = 0
    
    for _ in range(num_simulations):
        # STAND Simulation - use the same engine
        stand_result = simulate_blackjack_game(player_value, dealer_up_card, "stand")
        if stand_result == "win":
            stand_wins += 1
        elif stand_result == "lose":
            stand_losses += 1
        else:
            stand_pushes += 1
        
        # HIT Simulation - use the same engine
        hit_result = simulate_blackjack_game(player_value, dealer_up_card, "hit")
        if hit_result == "win":
            hit_wins += 1
        elif hit_result == "lose":
            hit_losses += 1
        else:
            hit_pushes += 1
    
    # Calculate win probabilities (treating pushes as half wins)
    stand_win_rate = (stand_wins + stand_pushes * 0.5) / num_simulations
    hit_win_rate = (hit_wins + hit_pushes * 0.5) / num_simulations
    
    end_time = time.time()
    execution_time_ms = (end_time - start_time) * 1000
    
    # Determine recommendation
    if player_value > 21:
        action = "stand"
        message = "You're busted - must STAND"
        confidence = "certain"
    elif player_value == 21:
        action = "stand" 
        message = "Perfect 21 - STAND and enjoy!"
        confidence = "certain"
    elif hit_win_rate > stand_win_rate + 0.02:  # 2% threshold for clear advantage
        action = "hit"
        advantage = (hit_win_rate - stand_win_rate) * 100
        message = f"HIT - {advantage:.1f}% better win rate than standing"
        confidence = "high" if advantage > 5 else "medium"
    elif stand_win_rate > hit_win_rate + 0.02:
        action = "stand"
        advantage = (stand_win_rate - hit_win_rate) * 100
        message = f"STAND - {advantage:.1f}% better win rate than hitting"
        confidence = "high" if advantage > 5 else "medium"
    else:
        # Very close - go with higher probability
        if hit_win_rate >= stand_win_rate:
            action = "hit"
            message = "Marginal HIT - probabilities are very close"
        else:
            action = "stand"
            message = "Marginal STAND - probabilities are very close"
        confidence = "low"
    
    return {
        "action": action,
        "message": message,
        "confidence": confidence,
        "stand_win_rate": round(stand_win_rate * 100, 1),
        "hit_win_rate": round(hit_win_rate * 100, 1),
        "simulations": num_simulations,
        "execution_time_ms": round(execution_time_ms, 1)
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)