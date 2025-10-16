import streamlit as st
import random
import time

# Page configuration
st.set_page_config(
    page_title="🧠 AI Visual Challenge",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for amazing visuals
st.markdown("""
<style>
    .main-header {
        font-size: 4rem;
        background: linear-gradient(45deg, #FF6B6B, #4ECDC4, #45B7D1, #96CEB4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 2rem;
        animation: rainbow 3s ease-in-out infinite;
    }
    
    @keyframes rainbow {
        0% { filter: hue-rotate(0deg); }
        100% { filter: hue-rotate(360deg); }
    }
    
    .game-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 3rem;
        border-radius: 20px;
        margin: 2rem 0;
        box-shadow: 0 20px 40px rgba(0,0,0,0.3);
        color: white;
        position: relative;
        overflow: hidden;
    }
    
    .puzzle-item {
        background: linear-gradient(45deg, #FF6B6B, #4ECDC4);
        border: none;
        border-radius: 15px;
        padding: 2rem;
        font-size: 3rem;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 10px 20px rgba(0,0,0,0.2);
        margin: 0.5rem;
    }
    
    .puzzle-item:hover {
        transform: translateY(-10px) scale(1.05);
        box-shadow: 0 20px 40px rgba(0,0,0,0.3);
    }
    
    .score-display {
        font-size: 2rem;
        color: #FFD93D;
        font-weight: bold;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
    }
    
    .level-indicator {
        background: linear-gradient(45deg, #667eea, #764ba2);
        padding: 1rem 2rem;
        border-radius: 25px;
        color: white;
        font-size: 1.5rem;
        font-weight: bold;
        text-align: center;
        margin: 1rem 0;
        box-shadow: 0 10px 20px rgba(0,0,0,0.2);
    }
    
    .hint-box {
        background: linear-gradient(45deg, #FFD93D, #FF6B6B);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        color: white;
        font-size: 1.2rem;
        font-weight: bold;
        text-align: center;
        box-shadow: 0 10px 20px rgba(0,0,0,0.2);
    }
    
    .button-glow {
        background: linear-gradient(45deg, #4ECDC4, #45B7D1);
        border: none;
        color: white;
        padding: 1rem 2rem;
        border-radius: 25px;
        font-size: 1.2rem;
        font-weight: bold;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 10px 20px rgba(0,0,0,0.2);
        margin: 0.5rem;
    }
    
    .button-glow:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 30px rgba(0,0,0,0.3);
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

def display_header():
    """Display the amazing header"""
    st.markdown('<h1 class="main-header">🧠 AI Visual Challenge</h1>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="game-container">
    <h2>🎯 Welcome to the Ultimate AI Thinking Challenge!</h2>
    <p>This interactive visual puzzle tests the core skills you'll need to succeed in AI: <strong>pattern recognition</strong>, <strong>logical reasoning</strong>, and <strong>creative problem-solving</strong>.</p>
    
    <div class="hint-box">
    <h4>🎮 How to Play:</h4>
    <ul style="text-align: left; margin: 1rem 0;">
        <li>🎨 Look at the visual pattern puzzle</li>
        <li>🧩 Click the correct answer</li>
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
            "name": "Color Sequence",
            "description": "What comes next in this color pattern?",
            "sequence": "🔴 → 🟡 → 🔴 → 🟡 → ?",
            "options": ["🔴", "🟡", "🟢", "🔵"],
            "answer": 0,  # Index of correct answer
            "hint": "🌈 Red, yellow, red, yellow... what comes next?"
        },
        2: {
            "name": "Growing Pattern",
            "description": "What comes next in this growing pattern?",
            "sequence": "🔴 → 🔴🔴 → 🔴🔴🔴 → 🔴🔴🔴🔴 → ?",
            "options": ["🔴🔴🔴🔴🔴", "🔴🔴🔴🔴", "🔴🔴🔴", "🔴🔴"],
            "answer": 0,
            "hint": "🔍 Count the circles: 1, 2, 3, 4... what's next?"
        },
        3: {
            "name": "Shape Progression",
            "description": "What comes next in this color progression?",
            "sequence": "⬜ → 🟨 → 🟧 → 🟥 → ?",
            "options": ["🟪", "🟦", "🟩", "⬛"],
            "answer": 0,
            "hint": "🎨 White → yellow → orange → red... what comes after red?"
        },
        4: {
            "name": "Number Sequence",
            "description": "What comes next in this number sequence?",
            "sequence": "1️⃣ → 2️⃣ → 3️⃣ → 4️⃣ → ?",
            "options": ["5️⃣", "6️⃣", "7️⃣", "8️⃣"],
            "answer": 0,
            "hint": "🔢 1, 2, 3, 4... what number comes next?"
        },
        5: {
            "name": "Logic Challenge",
            "description": "What comes next in this pattern?",
            "sequence": "🐑 → 🐑🐑 → 🐑🐑🐑 → 🐑🐑🐑🐑 → ?",
            "options": ["🐑🐑🐑🐑🐑", "🐑🐑🐑🐑", "🐑🐑🐑", "🐑🐑"],
            "answer": 0,
            "hint": "🐑 Count the sheep: 1, 2, 3, 4... what's next?"
        }
    }
    
    return puzzles.get(level, puzzles[1])

def display_puzzle():
    """Display the current puzzle"""
    puzzle = create_puzzle(st.session_state.current_level)
    
    st.markdown(f"""
    <div class="game-container">
    <h2>🎯 Level {st.session_state.current_level}: {puzzle['name']}</h2>
    <p>{puzzle['description']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Display the sequence
    st.markdown("**Pattern:**")
    st.markdown(f"<div style='font-size: 2rem; text-align: center; margin: 2rem 0; padding: 2rem; background: linear-gradient(45deg, #667eea, #764ba2); border-radius: 15px; color: white;'>{puzzle['sequence']}</div>", unsafe_allow_html=True)
    
    # Display options
    st.markdown("**What comes next?**")
    
    # Create columns for options
    cols = st.columns(2)
    for i, option in enumerate(puzzle['options']):
        with cols[i % 2]:
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
    
    st.sidebar.markdown(f"""
    <div class="level-indicator">
    Lives: {'❤️' * st.session_state.lives}
    </div>
    """, unsafe_allow_html=True)
    
    if st.sidebar.button("🏠 Home", use_container_width=True):
        st.session_state.current_level = 1
        st.session_state.score = 0
        st.session_state.lives = 3
        st.session_state.current_answer = None
        st.session_state.attempts = 0
        st.session_state.game_completed = False
        st.rerun()
    
    if st.sidebar.button("🔄 Reset Game", use_container_width=True):
        initialize_session_state()
        st.rerun()

def display_results():
    """Display final results"""
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
