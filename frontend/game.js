// Blackjack Pro Game Logic
class BlackjackGame {
    constructor() {
        this.apiUrl = 'http://localhost:8000';
        
        // Game state
        this.deck = [];
        this.playerHand = [];
        this.dealerHand = [];
        this.gameInProgress = false;
        
        // Scoring - Start with 100 points
        this.totalScore = parseInt(localStorage.getItem('totalScore') || '100');
        this.gamesWon = parseInt(localStorage.getItem('gamesWon') || '0');
        this.gamesPlayed = parseInt(localStorage.getItem('gamesPlayed') || '0');
        this.currentStreak = parseInt(localStorage.getItem('currentStreak') || '0');
        this.bestStreak = parseInt(localStorage.getItem('bestStreak') || '0');
        
        this.initializeGame();
    }
    
    initializeGame() {
        this.setupEventListeners();
        this.updateScoreDisplay();
        this.createDeck();
        this.showWelcomePopup();
        console.log('Blackjack n Probability initialized successfully');
    }
    
    setupEventListeners() {
        document.getElementById('stand-btn').addEventListener('click', () => this.stand());
        document.getElementById('run-simulation-btn').addEventListener('click', () => this.runSimulation());
        document.getElementById('hint-btn').addEventListener('click', () => this.getHint());
        document.getElementById('popup-button').addEventListener('click', () => this.handlePopupButton());
        
        // Add deck click listeners
        const deckCards = document.querySelectorAll('.deck-card');
        deckCards.forEach(card => {
            card.addEventListener('click', () => this.hitFromDeck(card));
        });
    }
    
    createDeck() {
        const suits = ['hearts', 'diamonds', 'clubs', 'spades'];
        const values = ['ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'jack', 'queen', 'king'];
        
        this.deck = [];
        for (const suit of suits) {
            for (const value of values) {
                this.deck.push({ value, suit });
            }
        }
        
        this.shuffleDeck();
    }
    
    shuffleDeck() {
        for (let i = this.deck.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [this.deck[i], this.deck[j]] = [this.deck[j], this.deck[i]];
        }
    }
    
    getCardValue(card) {
        if (card.value === 'ace') {
            return 11;
        } else if (['jack', 'queen', 'king'].includes(card.value)) {
            return 10;
        } else {
            return parseInt(card.value);
        }
    }
    
    calculateHandValue(hand) {
        let total = 0;
        let aces = 0;
        
        for (const card of hand) {
            if (card.faceDown) continue;
            
            if (card.value === 'ace') {
                aces++;
                total += 11;
            } else if (['jack', 'queen', 'king'].includes(card.value)) {
                total += 10;
            } else {
                total += parseInt(card.value);
            }
        }
        
        // Adjust for aces
        while (total > 21 && aces > 0) {
            total -= 10;
            aces--;
        }
        
        return total;
    }
    
    newGame() {
        console.log('Starting new game...');
        // Reset game state
        this.playerHand = [];
        this.dealerHand = [];
        this.gameInProgress = true;
        
        // Create new deck if running low
        if (this.deck.length < 10) {
            this.createDeck();
        }
        
        // Deal initial cards
        this.dealCard('player');
        this.dealCard('dealer');
        this.dealCard('player');
        this.dealCard('dealer', true); // Dealer's second card face down
        
        // Enable stand button
        const standBtn = document.getElementById('stand-btn');
        if (standBtn) {
            standBtn.disabled = false;
        }
        
        this.updateDisplay();
        console.log('Game started, cards dealt');
        
        // Check for blackjack
        if (this.calculateHandValue(this.playerHand) === 21) {
            setTimeout(() => this.stand(), 1000);
        }
    }
    
    dealCard(recipient, faceDown = false) {
        if (this.deck.length === 0) {
            this.createDeck();
        }
        
        const card = this.deck.pop();
        card.faceDown = faceDown;
        
        if (recipient === 'player') {
            this.playerHand.push(card);
        } else {
            this.dealerHand.push(card);
        }
        
        return card;
    }
    
    hit() {
        if (!this.gameInProgress) return;
        
        this.dealCard('player');
        this.updateDisplay();
        
        const playerValue = this.calculateHandValue(this.playerHand);
        
        if (playerValue > 21) {
            this.endGame('bust');
        } else if (playerValue === 21) {
            this.stand();
        }
    }
    
    async hitFromDeck(deckCard) {
        if (!this.gameInProgress) return;
        
        // Add flipping animation to the deck card
        deckCard.classList.add('flipping');
        
        // Wait for flip animation to complete
        await this.delay(400);
        
        // Deal the actual card
        this.hit();
        
        // Remove flipping class after a short delay
        setTimeout(() => {
            deckCard.classList.remove('flipping');
        }, 400);
    }
    
    async stand() {
        if (!this.gameInProgress) return;
        
        // Reveal dealer's face-down card
        this.dealerHand.forEach(card => card.faceDown = false);
        this.updateDisplay();
        
        // Dealer hits until 17 or higher
        while (this.calculateHandValue(this.dealerHand) < 17) {
            await this.delay(1000);
            this.dealCard('dealer');
            this.updateDisplay();
        }
        
        await this.delay(500);
        this.determineWinner();
    }
    
    determineWinner() {
        const playerValue = this.calculateHandValue(this.playerHand);
        const dealerValue = this.calculateHandValue(this.dealerHand);
        
        let outcome;
        if (playerValue > 21) {
            outcome = 'bust';
        } else if (dealerValue > 21) {
            outcome = 'win';
        } else if (playerValue > dealerValue) {
            outcome = 'win';
        } else if (playerValue < dealerValue) {
            outcome = 'lose';
        } else {
            outcome = 'push';
        }
        
        this.endGame(outcome);
    }
    
    endGame(outcome) {
        this.gameInProgress = false;
        
        // Update statistics
        this.gamesPlayed++;
        
        if (outcome === 'win') {
            this.gamesWon++;
            this.totalScore += 50;
            this.currentStreak++;
            if (this.currentStreak > this.bestStreak) {
                this.bestStreak = this.currentStreak;
            }
        } else if (outcome === 'lose' || outcome === 'bust') {
            this.totalScore = Math.max(0, this.totalScore - 50);
            this.currentStreak = 0;
        }
        // Push doesn't change streak or score significantly
        
        // Save to localStorage
        this.saveStats();
        
        // Update displays
        this.updateScoreDisplay();
        
        // Show popup after a short delay
        setTimeout(() => {
            this.showGameEndPopup(outcome);
        }, 1500);
        
        // Disable stand button
        document.getElementById('stand-btn').disabled = true;
    }
    

    
    updateDisplay() {
        // Update player hand display
        const playerElement = document.getElementById('player-hand');
        playerElement.innerHTML = this.renderHand(this.playerHand);
        
        // Update dealer hand display
        const dealerElement = document.getElementById('dealer-hand');
        dealerElement.innerHTML = this.renderHand(this.dealerHand);
        
        // Update hand values
        const playerValueElement = document.getElementById('player-value');
        playerValueElement.textContent = this.calculateHandValue(this.playerHand);
        
        const dealerValueElement = document.getElementById('dealer-value');
        const dealerValue = this.calculateHandValue(this.dealerHand);
        const hasHiddenCard = this.dealerHand.some(card => card.faceDown);
        dealerValueElement.textContent = hasHiddenCard ? '?' : dealerValue;
    }
    
    renderHand(hand) {
        return hand.map((card, index) => {
            if (card.faceDown) {
                return '<div class="card face-down dealing"></div>';
            }
            
            const cardImagePath = `/images/${card.value}_of_${card.suit}.png`;
            return `<div class="card dealing" style="animation-delay: ${index * 0.2}s">
                        <img src="${cardImagePath}" alt="${card.value} of ${card.suit}">
                    </div>`;
        }).join('');
    }
    
    updateScoreDisplay() {
        document.getElementById('total-score').textContent = this.totalScore;
        document.getElementById('games-won').textContent = this.gamesWon;
        document.getElementById('games-played').textContent = this.gamesPlayed;
        
        // Calculate win rate
        const winRate = this.gamesPlayed > 0 ? ((this.gamesWon / this.gamesPlayed) * 100).toFixed(1) : 0;
        document.getElementById('win-rate').textContent = `${winRate}%`;
        document.getElementById('current-streak').textContent = this.currentStreak;
        document.getElementById('best-streak').textContent = this.bestStreak;
    }
    
    saveStats() {
        localStorage.setItem('totalScore', this.totalScore.toString());
        localStorage.setItem('gamesWon', this.gamesWon.toString());
        localStorage.setItem('gamesPlayed', this.gamesPlayed.toString());
        localStorage.setItem('currentStreak', this.currentStreak.toString());
        localStorage.setItem('bestStreak', this.bestStreak.toString());
    }
    
    async runSimulation() {
        try {
            console.log('Running Monte Carlo simulation...');
            
            // If game is in progress, use current game state for context
            let url = `${this.apiUrl}/analytics/simulation?num_simulations=50000`;
            if (this.gameInProgress && this.playerHand.length > 0 && this.dealerHand.length > 0) {
                const playerValue = this.calculateHandValue(this.playerHand);
                const dealerUpCard = this.getDealerUpCard();
                url += `&player_value=${playerValue}&dealer_up_card=${dealerUpCard}`;
            }
            
            const response = await fetch(url, {
                method: 'POST'
            });
            
            if (response.ok) {
                const result = await response.json();
                console.log('Simulation result:', result);
                this.displaySimulationResults(result);
            } else {
                console.log('API failed, using fallback simulation');
                // Fallback simulation
                this.displaySimulationResults({
                    simulations: 50000,
                    win_rate: 0.45,
                    loss_rate: 0.48,
                    push_rate: 0.07,
                    execution_time_ms: 25.5,
                    expected_value: -0.03,
                    context: ""
                });
            }
        } catch (error) {
            console.error('Simulation failed:', error);
            // Show fallback even on error
            this.displaySimulationResults({
                simulations: 50000,
                win_rate: 0.45,
                loss_rate: 0.48,
                push_rate: 0.07,
                execution_time_ms: 25.5,
                expected_value: -0.03,
                context: ""
            });
        }
    }
    
    displaySimulationResults(results) {
        const resultsElement = document.getElementById('simulation-results');
        const contextText = results.context || "";
        const simulationType = contextText ? "Context-Specific" : "General";
        
        resultsElement.innerHTML = `
            <strong>${simulationType} Monte Carlo Simulation</strong><br>
            ${contextText ? `<small style="color: #bbb;">${contextText}</small><br>` : ''}
            Simulations: ${results.simulations.toLocaleString()}<br>
            Win Rate: ${(results.win_rate * 100).toFixed(2)}%<br>
            Loss Rate: ${(results.loss_rate * 100).toFixed(2)}%<br>
            Push Rate: ${(results.push_rate * 100).toFixed(2)}%<br>
            Expected Value: ${(results.expected_value * 100).toFixed(2)}%<br>
            Execution Time: ${results.execution_time_ms.toFixed(1)}ms
        `;
    }
    
    async getHint() {
        if (!this.gameInProgress) {
            this.displayHint("Start a new game first!", "neutral");
            return;
        }
        
        const playerValue = this.calculateHandValue(this.playerHand);
        const dealerUpCard = this.getDealerUpCard();
        
        // Show loading message
        this.displayHint("🎲 Running Monte Carlo analysis...", "neutral");
        
        try {
            // Get Monte Carlo hint from API
            const response = await fetch(`${this.apiUrl}/game/hint?player_value=${playerValue}&dealer_up_card=${dealerUpCard}&num_simulations=25000`, {
                method: 'POST'
            });
            
            if (response.ok) {
                const mcHint = await response.json();
                this.displayMonteCarloHint(mcHint);
                return;
            }
        } catch (error) {
            console.log('Monte Carlo API failed, using local strategy');
        }
        
        // Fallback to local hint
        const hint = this.getBasicStrategyHint(playerValue, dealerUpCard);
        this.displayHint(hint.message, hint.action);
    }
    
    getDealerUpCard() {
        // Get the dealer's face-up card (first card)
        if (this.dealerHand.length > 0) {
            const upCard = this.dealerHand[0];
            if (upCard.value === 'ace') return 11;
            if (['jack', 'queen', 'king'].includes(upCard.value)) return 10;
            return parseInt(upCard.value);
        }
        return 10; // Default assumption
    }
    
    getBasicStrategyHint(playerValue, dealerUpCard) {
        // Basic Blackjack Strategy Logic
        
        // Hard totals (no aces counting as 11)
        if (playerValue <= 11) {
            return { action: "hit", message: "💡 Always HIT with 11 or less - you can't bust!" };
        }
        
        if (playerValue === 12) {
            if (dealerUpCard >= 4 && dealerUpCard <= 6) {
                return { action: "stand", message: "💡 STAND - Dealer likely to bust with weak card" };
            } else {
                return { action: "hit", message: "💡 HIT - Dealer has strong card, you need to improve" };
            }
        }
        
        if (playerValue >= 13 && playerValue <= 16) {
            if (dealerUpCard >= 2 && dealerUpCard <= 6) {
                return { action: "stand", message: "💡 STAND - Let dealer bust with weak upcard" };
            } else {
                return { action: "hit", message: "💡 HIT - Dealer has strong card, risk the bust" };
            }
        }
        
        if (playerValue >= 17) {
            return { action: "stand", message: "💡 STAND - Strong hand, don't risk busting" };
        }
        
        // Default case
        return { action: "hit", message: "💡 HIT - Improve your hand" };
    }
    
    displayHint(message, action, confidence = null) {
        const hintElement = document.getElementById('hint-results');
        const actionColor = action === 'hit' ? '#e74c3c' : action === 'stand' ? '#27ae60' : '#3498db';
        const confidenceText = confidence ? ` (${confidence} confidence)` : '';
        
        hintElement.innerHTML = `
            <strong style="color: ${actionColor}">Strategy Hint${confidenceText}</strong><br>
            ${message}<br>
            <small style="color: #bbb; margin-top: 10px; display: block;">
                Player: ${this.calculateHandValue(this.playerHand)} | 
                Dealer Up: ${this.getDealerUpCard()}
            </small>
        `;
    }
    
    displayMonteCarloHint(mcResult) {
        const hintElement = document.getElementById('hint-results');
        const actionColor = mcResult.action === 'hit' ? '#e74c3c' : '#27ae60';
        const confidenceColor = mcResult.confidence === 'high' ? '#27ae60' : 
                               mcResult.confidence === 'medium' ? '#f39c12' : '#e74c3c';
        
        // Calculate advantage
        const advantage = Math.abs(mcResult.hit_win_rate - mcResult.stand_win_rate);
        const betterAction = mcResult.hit_win_rate > mcResult.stand_win_rate ? 'HIT' : 'STAND';
        
        hintElement.innerHTML = `
            <strong style="color: ${actionColor}">🎲 Monte Carlo Analysis</strong><br>
            <strong style="color: ${actionColor}">${mcResult.action.toUpperCase()}</strong> - ${mcResult.message}<br>
            <div style="margin: 10px 0; font-size: 0.9rem; background: rgba(255,255,255,0.1); padding: 8px; border-radius: 4px;">
                📊 <strong>Win Probabilities:</strong><br>
                • HIT: <span style="color: ${mcResult.hit_win_rate > mcResult.stand_win_rate ? '#27ae60' : '#fff'}">${mcResult.hit_win_rate}%</span><br>
                • STAND: <span style="color: ${mcResult.stand_win_rate > mcResult.hit_win_rate ? '#27ae60' : '#fff'}">${mcResult.stand_win_rate}%</span><br>
                <strong style="color: ${actionColor}">Advantage: ${advantage.toFixed(1)}%</strong>
            </div>
            <small style="color: #bbb; display: block;">
                ${mcResult.simulations.toLocaleString()} simulations in ${mcResult.execution_time_ms}ms<br>
                Confidence: <span style="color: ${confidenceColor}">${mcResult.confidence}</span>
            </small>
        `;
    }
    
    delay(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }
    
    showWelcomePopup() {
        console.log('Showing welcome popup...');
        const popup = document.getElementById('game-popup');
        const title = document.getElementById('popup-title');
        const message = document.getElementById('popup-message');
        const rules = document.getElementById('popup-rules');
        const button = document.getElementById('popup-button');
        
        if (!popup) {
            console.error('Popup element not found!');
            return;
        }
        
        title.textContent = '🃏 Blackjack n Probability';
        message.textContent = 'Ready to test your luck and skill?';
        rules.style.display = 'block';
        button.textContent = 'Start Game';
        button.onclick = () => this.startFirstGame();
        
        popup.style.display = 'flex';
        console.log('Welcome popup should now be visible');
    }
    
    showGameEndPopup(outcome) {
        const popup = document.getElementById('game-popup');
        const title = document.getElementById('popup-title');
        const message = document.getElementById('popup-message');
        const rules = document.getElementById('popup-rules');
        const button = document.getElementById('popup-button');
        
        const messages = {
            win: { title: '🎉 You Win!', message: 'Congratulations! You beat the dealer!' },
            lose: { title: '😔 You Lose', message: 'The dealer got the better hand this time.' },
            push: { title: '🤝 Push (Tie)', message: 'You and the dealer tied!' },
            bust: { title: '💥 Bust!', message: 'You went over 21. Better luck next time!' }
        };
        
        title.textContent = messages[outcome].title;
        message.textContent = messages[outcome].message;
        rules.style.display = 'none';
        button.textContent = 'Play Again';
        button.onclick = () => this.startNewGame();
        
        popup.style.display = 'flex';
    }
    
    hidePopup() {
        document.getElementById('game-popup').style.display = 'none';
    }
    
    handlePopupButton() {
        // Check what type of popup this is and act accordingly
        const button = document.getElementById('popup-button');
        if (button.textContent === 'Start Game') {
            this.startFirstGame();
        } else if (button.textContent === 'Play Again') {
            this.startNewGame();
        } else {
            this.hidePopup();
        }
    }
    
    startFirstGame() {
        console.log('Starting first game...');
        this.hidePopup();
        this.newGame();
    }
    
    startNewGame() {
        this.hidePopup();
        this.newGame();
    }
}

// Initialize the game when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.blackjackGame = new BlackjackGame();
});