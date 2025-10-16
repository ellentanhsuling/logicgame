import streamlit as st
import random
import time
import math

# Page configuration
st.set_page_config(
    page_title="🧠 AI Visual Problem Solver",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Amazing CSS with tons of animations and visual effects
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&display=swap');
    
    .main-header {
        font-family: 'Orbitron', monospace;
        font-size: 5rem;
        font-weight: 900;
        background: linear-gradient(45deg, #FF0080, #00FF80, #8000FF, #FF8000, #0080FF);
        background-size: 400% 400%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 2rem;
        animation: gradientShift 3s ease-in-out infinite, float 6s ease-in-out infinite;
        text-shadow: 0 0 30px rgba(255, 0, 128, 0.5);
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px) rotate(0deg); }
        50% { transform: translateY(-20px) rotate(2deg); }
    }
    
    .game-container {
        background: linear-gradient(135deg, #0F0F23 0%, #1A1A2E 25%, #16213E 50%, #0F3460 75%, #533483 100%);
        padding: 4rem;
        border-radius: 30px;
        margin: 2rem 0;
        box-shadow: 
            0 0 50px rgba(255, 0, 128, 0.3),
            0 0 100px rgba(0, 255, 128, 0.2),
            inset 0 0 50px rgba(255, 255, 255, 0.1);
        color: white;
        position: relative;
        overflow: hidden;
        border: 2px solid transparent;
        background-clip: padding-box;
    }
    
    .game-container::before {
        content: '';
        position: absolute;
        top: -2px;
        left: -2px;
        right: -2px;
        bottom: -2px;
        background: linear-gradient(45deg, #FF0080, #00FF80, #8000FF, #FF8000, #0080FF);
        border-radius: 30px;
        z-index: -1;
        animation: borderGlow 2s linear infinite;
    }
    
    @keyframes borderGlow {
        0% { filter: hue-rotate(0deg); }
        100% { filter: hue-rotate(360deg); }
    }
    
    .game-container::after {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: radial-gradient(circle at 20% 80%, rgba(255, 0, 128, 0.1) 0%, transparent 50%),
                    radial-gradient(circle at 80% 20%, rgba(0, 255, 128, 0.1) 0%, transparent 50%),
                    radial-gradient(circle at 40% 40%, rgba(128, 0, 255, 0.1) 0%, transparent 50%);
        animation: particleFloat 8s ease-in-out infinite;
        pointer-events: none;
    }
    
    @keyframes particleFloat {
        0%, 100% { transform: translate(0, 0) scale(1); }
        25% { transform: translate(20px, -20px) scale(1.1); }
        50% { transform: translate(-10px, -30px) scale(0.9); }
        75% { transform: translate(-20px, 10px) scale(1.05); }
    }
    
    .puzzle-display {
        background: linear-gradient(45deg, rgba(255, 0, 128, 0.2), rgba(0, 255, 128, 0.2));
        padding: 3rem;
        border-radius: 20px;
        margin: 2rem 0;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        position: relative;
        overflow: hidden;
    }
    
    .puzzle-display::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: conic-gradient(from 0deg, transparent, rgba(255, 255, 255, 0.1), transparent);
        animation: rotate 4s linear infinite;
    }
    
    @keyframes rotate {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    .shape-container {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 2rem;
        margin: 2rem 0;
        flex-wrap: wrap;
    }
    
    .shape-item {
        width: 120px;
        height: 120px;
        border-radius: 20px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 3rem;
        cursor: pointer;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        position: relative;
        overflow: hidden;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
    }
    
    .shape-item:hover {
        transform: translateY(-15px) scale(1.1) rotate(5deg);
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.4);
    }
    
    .shape-item.selected {
        transform: scale(1.2) rotate(10deg);
        box-shadow: 0 0 30px rgba(255, 255, 255, 0.8);
        animation: selectedPulse 0.6s ease-in-out;
    }
    
    @keyframes selectedPulse {
        0% { transform: scale(1.2) rotate(10deg); }
        50% { transform: scale(1.3) rotate(15deg); }
        100% { transform: scale(1.2) rotate(10deg); }
    }
    
    .shape-item.correct {
        background: linear-gradient(45deg, #00FF80, #00CC66);
        animation: correctCelebration 1s ease-in-out;
    }
    
    .shape-item.wrong {
        background: linear-gradient(45deg, #FF0080, #CC0066);
        animation: wrongShake 0.8s ease-in-out;
    }
    
    @keyframes correctCelebration {
        0% { transform: scale(1) rotate(0deg); }
        25% { transform: scale(1.3) rotate(10deg); }
        50% { transform: scale(1.1) rotate(-10deg); }
        75% { transform: scale(1.2) rotate(5deg); }
        100% { transform: scale(1) rotate(0deg); }
    }
    
    @keyframes wrongShake {
        0%, 100% { transform: translateX(0) rotate(0deg); }
        25% { transform: translateX(-15px) rotate(-5deg); }
        75% { transform: translateX(15px) rotate(5deg); }
    }
    
    .shape-item::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(45deg, transparent, rgba(255, 255, 255, 0.2), transparent);
        transform: translateX(-100%);
        transition: transform 0.6s;
    }
    
    .shape-item:hover::before {
        transform: translateX(100%);
    }
    
    .circle { 
        border-radius: 50%; 
        background: linear-gradient(45deg, #FF0080, #FF4080);
    }
    
    .square { 
        border-radius: 15px; 
        background: linear-gradient(45deg, #00FF80, #40FF80);
    }
    
    .triangle { 
        border-radius: 20px; 
        background: linear-gradient(45deg, #8000FF, #8040FF);
        clip-path: polygon(50% 0%, 0% 100%, 100% 100%);
    }
    
    .diamond { 
        border-radius: 20px; 
        background: linear-gradient(45deg, #FF8000, #FFA040);
        clip-path: polygon(50% 0%, 100% 50%, 50% 100%, 0% 50%);
    }
    
    .hexagon { 
        border-radius: 20px; 
        background: linear-gradient(45deg, #0080FF, #4080FF);
        clip-path: polygon(25% 0%, 75% 0%, 100% 50%, 75% 100%, 25% 100%, 0% 50%);
    }
    
    .star { 
        border-radius: 20px; 
        background: linear-gradient(45deg, #FFD700, #FFA500);
        clip-path: polygon(50% 0%, 61% 35%, 98% 35%, 68% 57%, 79% 91%, 50% 70%, 21% 91%, 32% 57%, 2% 35%, 39% 35%);
    }
    
    .score-display {
        font-family: 'Orbitron', monospace;
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(45deg, #FFD700, #FFA500);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 0 20px rgba(255, 215, 0, 0.5);
        animation: scoreGlow 2s ease-in-out infinite alternate;
    }
    
    @keyframes scoreGlow {
        0% { filter: brightness(1) drop-shadow(0 0 10px rgba(255, 215, 0, 0.5)); }
        100% { filter: brightness(1.2) drop-shadow(0 0 20px rgba(255, 215, 0, 0.8)); }
    }
    
    .level-indicator {
        background: linear-gradient(45deg, rgba(255, 0, 128, 0.3), rgba(0, 255, 128, 0.3));
        padding: 1.5rem 3rem;
        border-radius: 30px;
        color: white;
        font-size: 1.8rem;
        font-weight: bold;
        text-align: center;
        margin: 1rem 0;
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.3);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        animation: levelPulse 3s ease-in-out infinite;
    }
    
    @keyframes levelPulse {
        0%, 100% { transform: scale(1); box-shadow: 0 15px 35px rgba(0, 0, 0, 0.3); }
        50% { transform: scale(1.05); box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4); }
    }
    
    .hint-box {
        background: linear-gradient(45deg, rgba(255, 215, 0, 0.3), rgba(255, 165, 0, 0.3));
        padding: 2rem;
        border-radius: 20px;
        margin: 2rem 0;
        color: white;
        font-size: 1.4rem;
        font-weight: bold;
        text-align: center;
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.3);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        animation: hintGlow 2s ease-in-out infinite alternate;
    }
    
    @keyframes hintGlow {
        0% { box-shadow: 0 15px 35px rgba(0, 0, 0, 0.3), 0 0 20px rgba(255, 215, 0, 0.3); }
        100% { box-shadow: 0 15px 35px rgba(0, 0, 0, 0.3), 0 0 30px rgba(255, 215, 0, 0.6); }
    }
    
    .button-glow {
        background: linear-gradient(45deg, #FF0080, #00FF80);
        border: none;
        color: white;
        padding: 1.5rem 3rem;
        border-radius: 30px;
        font-size: 1.4rem;
        font-weight: bold;
        cursor: pointer;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.3);
        margin: 1rem;
        position: relative;
        overflow: hidden;
    }
    
    .button-glow:hover {
        transform: translateY(-8px) scale(1.05);
        box-shadow: 0 25px 50px rgba(0, 0, 0, 0.4);
    }
    
    .button-glow:active {
        transform: translateY(-4px) scale(1.02);
    }
    
    .button-glow::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
        transition: left 0.6s;
    }
    
    .button-glow:hover::before {
        left: 100%;
    }
    
    .progress-container {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 1rem;
        margin: 2rem 0;
        backdrop-filter: blur(10px);
    }
    
    .progress-bar {
        height: 25px;
        background: rgba(255, 255, 255, 0.2);
        border-radius: 15px;
        overflow: hidden;
        position: relative;
    }
    
    .progress-fill {
        height: 100%;
        background: linear-gradient(90deg, #FF0080, #00FF80, #8000FF);
        border-radius: 15px;
        transition: width 0.8s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        position: relative;
        overflow: hidden;
    }
    
    .progress-fill::after {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.4), transparent);
        animation: progressShimmer 2s infinite;
    }
    
    @keyframes progressShimmer {
        0% { transform: translateX(-100%); }
        100% { transform: translateX(100%); }
    }
    
    .celebration {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: 1000;
    }
    
    .confetti {
        position: absolute;
        width: 15px;
        height: 15px;
        background: linear-gradient(45deg, #FF0080, #00FF80, #8000FF, #FF8000, #0080FF);
        animation: confetti-fall 4s linear infinite;
    }
    
    @keyframes confetti-fall {
        0% {
            transform: translateY(-100vh) rotate(0deg);
            opacity: 1;
        }
        100% {
            transform: translateY(100vh) rotate(720deg);
            opacity: 0;
        }
    }
    
    .lives-display {
        display: flex;
        gap: 1rem;
        justify-content: center;
        align-items: center;
    }
    
    .life-heart {
        font-size: 2rem;
        animation: heartbeat 1.5s ease-in-out infinite;
    }
    
    @keyframes heartbeat {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.2); }
    }
    
    .sequence-display {
        font-size: 2.5rem;
        text-align: center;
        margin: 2rem 0;
        padding: 2rem;
        background: linear-gradient(45deg, rgba(255, 0, 128, 0.2), rgba(0, 255, 128, 0.2));
        border-radius: 20px;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        position: relative;
        overflow: hidden;
    }
    
    .sequence-display::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(45deg, transparent, rgba(255, 255, 255, 0.1), transparent);
        animation: sequenceGlow 3s ease-in-out infinite;
    }
    
    @keyframes sequenceGlow {
        0%, 100% { opacity: 0; }
        50% { opacity: 1; }
    }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize all session state variables"""
    if 'current_level' not in st.session_state:
        st.session_state.current_level = 1
    if 'score' not in st.session_state:
        st.session_state.score = 0
    if 'lives' not in st.session_state:
        st.session_state.lives = 3
    if 'current_answer' not in st.session_state:
        st.session_state.current_answer = None
    if 'attempts' not in st.session_state:
        st.session_state.attempts = 0
    if 'game_completed' not in st.session_state:
        st.session_state.game_completed = False
    if 'show_celebration' not in st.session_state:
        st.session_state.show_celebration = False

def display_header():
    """Display the amazing header"""
    st.markdown('<h1 class="main-header">🧠 AI Visual Problem Solver</h1>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="game-container">
    <h2>🎯 Welcome to the Ultimate AI Thinking Challenge!</h2>
    <p>This interactive visual puzzle tests the core skills you'll need to succeed in AI: <strong>pattern recognition</strong>, <strong>logical reasoning</strong>, and <strong>creative problem-solving</strong>.</p>
    
    <div class="hint-box">
    <h4>🎮 How to Play:</h4>
    <ul style="text-align: left; margin: 1rem 0;">
        <li>🎨 Look at the visual pattern puzzle</li>
        <li>🧩 Click the shape that comes next</li>
        <li>💡 Use hints if you get stuck</li>
        <li>🏆 Complete all levels to win!</li>
    </ul>
    </div>
    
    <p><em>These are exactly the skills that make students successful in AI courses!</em></p>
    </div>
    """, unsafe_allow_html=True)

def create_puzzle(level):
    """Create a visual puzzle based on level"""
    puzzles = {
        1: {
            "name": "Shape Sequence",
            "description": "What shape comes next in this pattern?",
            "sequence": ["🔴", "🔵", "🔴", "🔵", "?"],
            "options": ["🔴", "🔵", "🟢", "🟡"],
            "answer": 0,
            "hint": "🌈 Red, blue, red, blue... what comes next?"
        },
        2: {
            "name": "Growing Shapes",
            "description": "What comes next in this growing pattern?",
            "sequence": ["🔴", "🔴🔴", "🔴🔴🔴", "🔴🔴🔴🔴", "?"],
            "options": ["🔴🔴🔴🔴🔴", "🔴🔴🔴🔴", "🔴🔴🔴", "🔴🔴"],
            "answer": 0,
            "hint": "🔍 Count the circles: 1, 2, 3, 4... what's next?"
        },
        3: {
            "name": "Color Progression",
            "description": "What color comes next in this progression?",
            "sequence": ["⬜", "🟨", "🟧", "🟥", "?"],
            "options": ["🟪", "🟦", "🟩", "⬛"],
            "answer": 0,
            "hint": "🎨 White → yellow → orange → red... what comes after red?"
        },
        4: {
            "name": "Number Sequence",
            "description": "What number comes next in this sequence?",
            "sequence": ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "?"],
            "options": ["5️⃣", "6️⃣", "7️⃣", "8️⃣"],
            "answer": 0,
            "hint": "🔢 1, 2, 3, 4... what number comes next?"
        },
        5: {
            "name": "Logic Challenge",
            "description": "What comes next in this pattern?",
            "sequence": ["🐑", "🐑🐑", "🐑🐑🐑", "🐑🐑🐑🐑", "?"],
            "options": ["🐑🐑🐑🐑🐑", "🐑🐑🐑🐑", "🐑🐑🐑", "🐑🐑"],
            "answer": 0,
            "hint": "🐑 Count the sheep: 1, 2, 3, 4... what's next?"
        }
    }
    
    return puzzles.get(level, puzzles[1])

def display_puzzle():
    """Display the current puzzle with amazing visuals"""
    puzzle = create_puzzle(st.session_state.current_level)
    
    st.markdown(f"""
    <div class="game-container">
    <h2>🎯 Level {st.session_state.current_level}: {puzzle['name']}</h2>
    <p>{puzzle['description']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Display the sequence with amazing visuals
    st.markdown("**Pattern:**")
    sequence_display = " → ".join(puzzle['sequence'])
    st.markdown(f"<div class='sequence-display'>{sequence_display}</div>", unsafe_allow_html=True)
    
    # Display options with animated shapes
    st.markdown("**What comes next?**")
    
    # Create animated shape containers
    cols = st.columns(2)
    for i, option in enumerate(puzzle['options']):
        with cols[i % 2]:
            shape_class = ["circle", "square", "triangle", "diamond"][i % 4]
            if st.button(f"{option}", key=f"option_{i}", use_container_width=True):
                st.session_state.current_answer = i
                st.session_state.attempts += 1
                st.rerun()
    
    # Check answer if one is selected
    if st.session_state.current_answer is not None:
        if st.session_state.current_answer == puzzle['answer']:
            st.success("🎉 Correct! Great job!")
            st.session_state.score += 100 * st.session_state.current_level
            st.session_state.current_level += 1
            st.session_state.current_answer = None
            st.session_state.attempts = 0
            st.session_state.show_celebration = True
            
            if st.session_state.current_level > 5:
                st.session_state.game_completed = True
                st.balloons()
            
            time.sleep(1)
            st.rerun()
        else:
            st.error("❌ Not quite right! Try again!")
            st.session_state.lives -= 1
            st.session_state.current_answer = None
            
            if st.session_state.lives <= 0:
                st.error("💀 Game Over! You ran out of lives!")
                st.session_state.current_level = 1
                st.session_state.score = 0
                st.session_state.lives = 3
                st.session_state.current_answer = None
                st.session_state.attempts = 0
                st.session_state.game_completed = False
                st.session_state.show_celebration = False
                time.sleep(2)
                st.rerun()
            
            time.sleep(1)
            st.rerun()
    
    # Show hint if needed
    if st.session_state.attempts >= 2:
        st.markdown(f"<div class='hint-box'>💡 Hint: {puzzle['hint']}</div>", unsafe_allow_html=True)
    
    # Reset button
    if st.button("🔄 Reset Puzzle", key="reset_puzzle"):
        st.session_state.current_answer = None
        st.session_state.attempts = 0
        st.rerun()

def display_sidebar():
    """Display the sidebar with game info"""
    st.sidebar.title("🎮 Game Info")
    
    st.sidebar.markdown(f"""
    <div class="level-indicator">
    Level: {st.session_state.current_level}/5
    </div>
    """, unsafe_allow_html=True)
    
    st.sidebar.markdown(f"""
    <div class="score-display">
    Score: {st.session_state.score}
    </div>
    """, unsafe_allow_html=True)
    
    # Lives display with animated hearts
    lives_html = f"""
    <div class="level-indicator">
    Lives: <div class="lives-display">
    """
    for i in range(st.session_state.lives):
        lives_html += f'<span class="life-heart">❤️</span>'
    lives_html += "</div></div>"
    st.sidebar.markdown(lives_html, unsafe_allow_html=True)
    
    # Progress bar
    progress = (st.session_state.current_level - 1) / 5
    st.sidebar.markdown(f"""
    <div class="progress-container">
    <div class="progress-bar">
    <div class="progress-fill" style="width: {progress * 100}%"></div>
    </div>
    </div>
    """, unsafe_allow_html=True)
    
    if st.sidebar.button("🏠 Home", use_container_width=True):
        st.session_state.current_level = 1
        st.session_state.score = 0
        st.session_state.lives = 3
        st.session_state.current_answer = None
        st.session_state.attempts = 0
        st.session_state.game_completed = False
        st.session_state.show_celebration = False
        st.rerun()
    
    if st.sidebar.button("🔄 Reset Game", use_container_width=True):
        initialize_session_state()
        st.rerun()

def display_results():
    """Display final results with amazing visuals"""
    st.markdown("""
    <div class="game-container">
    <h2>🎉 Congratulations! You've completed the AI Visual Challenge!</h2>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="level-indicator">
    Final Score: {st.session_state.score}
    </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.score >= 2000:
        st.success("🌟 **Excellent!** You have strong analytical thinking skills that are perfect for AI!")
        st.markdown("""
        **You demonstrated:**
        - Excellent pattern recognition abilities
        - Strong logical reasoning skills
        - Creative problem-solving approach
        - Persistence when facing challenges
        
        **You're likely to succeed in our AI course!** The coding will be challenging, but your thinking skills will help you overcome obstacles.
        """)
    elif st.session_state.score >= 1500:
        st.info("👍 **Good!** You have solid analytical thinking skills.")
        st.markdown("""
        **You showed:**
        - Good pattern recognition ability
        - Basic logical reasoning
        - Some creative thinking
        - Moderate persistence
        
        **You could succeed in our AI course** with dedication and practice.
        """)
    elif st.session_state.score >= 1000:
        st.warning("⚠️ **Fair.** Your analytical thinking needs development.")
        st.markdown("""
        **Areas to improve:**
        - Pattern recognition
        - Logical reasoning
        - Creative problem-solving
        - Persistence with difficult problems
        
        **Our AI course might be challenging** for you. Consider taking a foundational programming course first.
        """)
    else:
        st.error("❌ **Needs significant improvement.**")
        st.markdown("""
        **Our AI course would be very difficult** without stronger analytical thinking skills.
        
        **We recommend:**
        - Taking basic programming courses first
        - Practicing logic puzzles regularly
        - Building problem-solving confidence
        - Considering if AI is the right path for you
        """)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Course information
    st.markdown("""
    <div class="game-container">
    <h4>📚 About Our AI Course</h4>
    <p><strong>What you'll learn:</strong> Machine learning, data analysis, neural networks, and AI applications</p>
    <p><strong>Prerequisites:</strong> Strong analytical thinking (like what this game tested), basic math, and willingness to learn programming</p>
    <p><strong>Time commitment:</strong> 6 months, 10-15 hours per week</p>
    <p><strong>Outcome:</strong> Build real AI projects and understand how AI systems work</p>
    </div>
    """, unsafe_allow_html=True)

def main():
    """Main game loop"""
    initialize_session_state()
    display_header()
    display_sidebar()
    
    if st.session_state.game_completed:
        display_results()
    else:
        display_puzzle()

# Run the game
if __name__ == "__main__":
    main()
