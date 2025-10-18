# 🃏 Blackjack n Probability - Advanced Analytics & AI System

A comprehensive blackjack application with probability analysis, showcasing full-stack development, AI systems, privacy engineering, and high-performance computing with interactive card animations.

## 🚀 Features

### 🎮 Core Game
- **Polished Frontend**: Modern JS/HTML/CSS with responsive design
- **Real-time Gameplay**: Smooth card animations and game flow
- **Multiple Game Modes**: Standard, practice, and simulation modes

### 🧠 Advanced Analytics
- **Monte Carlo Simulations**: NumPy-powered statistical analysis
- **Strategy Optimization**: AI-driven optimal play recommendations
- **Performance Visualization**: Matplotlib charts and real-time metrics
- **Card Counting Analysis**: Hi-Lo system effectiveness tracking

### ⚡ High-Performance Engine
- **WebAssembly Core**: C++ engine compiled to WASM
- **Optimized Shuffling**: Cryptographically secure RNG
- **Benchmarking Suite**: Performance analysis tools
- **Memory Efficient**: Optimized data structures

### 🔒 Privacy Engineering
- **Granular Controls**: Standard/Minimal/Ephemeral modes
- **Data Transparency**: Clear collection policies
- **GDPR Compliance**: Export and deletion capabilities
- **Local Storage Options**: Offline-first architecture

### 🗄️ Backend Infrastructure
- **FastAPI**: Modern Python web framework
- **SQLAlchemy**: Robust ORM with relationship mapping
- **Alembic**: Database migration management
- **RESTful API**: Clean, documented endpoints

## 🛠️ Technology Stack

### Frontend
- **JavaScript ES6+**: Modern async/await patterns
- **HTML5**: Semantic markup and accessibility
- **CSS3**: Grid/Flexbox layouts, animations
- **WebAssembly**: High-performance computing

### Backend
- **Python 3.9+**: Core application logic
- **FastAPI**: API framework with automatic docs
- **SQLAlchemy**: Database ORM and migrations
- **Alembic**: Schema version control

### Analytics & AI
- **NumPy**: Numerical computing and simulations
- **Matplotlib**: Data visualization and charts
- **Pytesseract**: OCR text recognition
- **OpenCV**: Computer vision processing

### Systems Programming
- **C++17**: WebAssembly engine implementation
- **Emscripten**: C++ to WebAssembly compiler
- **CMake**: Build system configuration

## 📦 Installation

### Prerequisites
```bash
# Python 3.9+
python --version

# Node.js (for development tools)
node --version

# Emscripten SDK (for WebAssembly)
# Follow: https://emscripten.org/docs/getting_started/downloads.html
```

### Quick Start
```bash
# Clone the repository
git clone <repository-url>
cd blackjack-pro

# Install Python dependencies
pip install -r requirements.txt

# Initialize database
alembic upgrade head

# Build WebAssembly engine (optional)
cd wasm-engine
./build.sh
cd ..

# Start the backend
cd backend
python main.py

# Open frontend/enhanced_index.html in your browser
```

### Development Setup
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -r requirements.txt
pip install pytest black flake8 mypy

# Run tests
pytest

# Format code
black .

# Type checking
mypy backend/
```

## 🏗️ Project Structure

```
blackjack-pro/
├── frontend/                 # Enhanced web interface
│   ├── enhanced_index.html  # Main application page
│   ├── enhanced_script.js   # Core game logic
│   └── enhanced_style.css   # Modern styling
├── backend/                 # FastAPI application
│   ├── main.py             # API server entry point
│   └── routes/             # API endpoint definitions
├── database/               # Data layer
│   ├── models.py          # SQLAlchemy models
│   ├── database.py        # Database configuration
│   └── migrations/        # Alembic migration files
├── analytics/             # Statistical analysis
│   ├── monte_carlo.py     # Simulation engine
│   └── strategy.py        # Optimal play analysis
├── ocr/                   # Card recognition
│   ├── card_recognition.py # OCR implementation
│   └── templates/         # Card image templates
├── wasm-engine/           # High-performance core
│   ├── blackjack_engine.cpp # C++ implementation
│   ├── build.sh           # Build script
│   └── CMakeLists.txt     # Build configuration
├── privacy/               # Data protection
│   ├── telemetry.py       # Privacy controls
│   └── gdpr.py           # Compliance utilities
└── tests/                # Test suite
    ├── test_game.py      # Game logic tests
    ├── test_analytics.py # Analytics tests
    └── test_privacy.py   # Privacy tests
```

## 🎯 Usage Examples

### Basic Gameplay
```javascript
// Initialize the game
const game = new BlackjackPro();

// Start a new game
await game.newGame();

// Player actions
game.hit();
game.stand();
```

### Analytics Integration
```python
from analytics.monte_carlo import BlackjackAnalytics

# Run simulation
analyzer = BlackjackAnalytics()
result = analyzer.monte_carlo_simulation(
    player_cards=['ace_of_hearts', '10_of_spades'],
    dealer_up_card='6_of_diamonds',
    num_simulations=100000
)

print(f"Win probability: {result.win_probability:.2%}")
print(f"Optimal hits: {result.optimal_hits}")
```

### OCR Card Recognition
```python
from ocr.card_recognition import CardRecognition

# Capture and recognize cards
recognizer = CardRecognition()
cards = recognizer.capture_and_recognize(camera_index=0)
print(f"Detected cards: {cards}")
```

### Privacy Controls
```python
from privacy.telemetry import PrivacyManager, PrivacyMode

# Configure privacy settings
privacy = PrivacyManager(PrivacyMode.MINIMAL)
privacy.set_telemetry_enabled(False)

# Export user data (GDPR)
data = privacy.export_user_data(user_id="user123")
```

## 🔧 Configuration

### Environment Variables
```bash
# Database
DATABASE_URL=sqlite:///./blackjack.db

# API Settings
API_HOST=0.0.0.0
API_PORT=8000

# Privacy Settings
DEFAULT_PRIVACY_MODE=standard
TELEMETRY_ENABLED=true

# OCR Settings
TESSERACT_PATH=/usr/bin/tesseract
```

### Privacy Modes
- **Standard**: Full analytics and telemetry
- **Minimal**: Essential data only, 30-day retention
- **Ephemeral**: No persistent storage, diagnostic only

## 📊 Performance Benchmarks

### WebAssembly vs JavaScript
```
Simulation Performance (100k iterations):
- WASM Engine: ~150ms
- JavaScript: ~2.1s
- Speedup: ~14x faster
```

### Memory Usage
```
Peak Memory Consumption:
- Frontend: ~15MB
- Backend: ~45MB
- WASM Module: ~2MB
```

## 🧪 Testing

```bash
# Run all tests
pytest

# Test specific modules
pytest tests/test_analytics.py -v

# Coverage report
pytest --cov=backend --cov-report=html

# Performance tests
pytest tests/test_performance.py --benchmark-only
```

## 🚀 Deployment

### Docker Deployment
```bash
# Build containers
docker-compose build

# Start services
docker-compose up -d

# View logs
docker-compose logs -f
```

### Production Considerations
- Use PostgreSQL for production database
- Configure HTTPS with SSL certificates
- Set up monitoring and logging
- Implement rate limiting
- Configure CORS appropriately

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Code Style
- Python: Follow PEP 8, use Black formatter
- JavaScript: Use ESLint with Airbnb config
- C++: Follow Google C++ Style Guide
- Commit messages: Use conventional commits

## 🙏 Acknowledgments

- **Card Images**: Public domain playing card designs
- **Algorithms**: Based on published blackjack research
- **Libraries**: Thanks to all open-source contributors
- **Community**: Feedback and suggestions from users


---

**Built with ❤️ for learning and demonstration purposes**
