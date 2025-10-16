import streamlit as st
import random
import time
import json
from typing import List, Dict, Any
import pandas as pd

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
    
    .game-container::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
        animation: float 6s ease-in-out infinite;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px) rotate(0deg); }
        50% { transform: translateY(-20px) rotate(180deg); }
    }
    
    .puzzle-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 1rem;
        margin: 2rem 0;
        padding: 2rem;
        background: rgba(255,255,255,0.1);
        border-radius: 15px;
        backdrop-filter: blur(10px);
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
        position: relative;
        overflow: hidden;
    }
    
    .puzzle-item:hover {
        transform: translateY(-10px) scale(1.05);
        box-shadow: 0 20px 40px rgba(0,0,0,0.3);
    }
    
    .puzzle-item.selected {
        background: linear-gradient(45deg, #FFD93D, #FF6B6B);
        transform: scale(1.1);
        box-shadow: 0 0 30px rgba(255, 215, 61, 0.8);
    }
    
    .puzzle-item.correct {
        background: linear-gradient(45deg, #4ECDC4, #45B7D1);
        animation: correctPulse 0.6s ease-in-out;
    }
    
    .puzzle-item.wrong {
        background: linear-gradient(45deg, #FF6B6B, #FF8E8E);
        animation: wrongShake 0.6s ease-in-out;
    }
    
    @keyframes correctPulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.2); }
        100% { transform: scale(1); }
    }
    
    @keyframes wrongShake {
        0%, 100% { transform: translateX(0); }
        25% { transform: translateX(-10px); }
        75% { transform: translateX(10px); }
    }
    
    .score-display {
        font-size: 2rem;
        color: #FFD93D;
        font-weight: bold;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        background: linear-gradient(45deg, #FF6B6B, #4ECDC4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
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
    
    .progress-bar {
        height: 20px;
        background: rgba(255,255,255,0.2);
        border-radius: 10px;
        overflow: hidden;
        margin: 1rem 0;
    }
    
    .progress-fill {
        height: 100%;
        background: linear-gradient(90deg, #4ECDC4, #45B7D1);
        border-radius: 10px;
        transition: width 0.5s ease;
        position: relative;
    }
    
    .progress-fill::after {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
        animation: shimmer 2s infinite;
    }
    
    @keyframes shimmer {
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
        width: 10px;
        height: 10px;
        background: #FFD93D;
        animation: confetti-fall 3s linear infinite;
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
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
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
    }
    
    .button-glow:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 30px rgba(0,0,0,0.3);
    }
    
    .button-glow:active {
        transform: translateY(0);
    }
</style>
""", unsafe_allow_html=True)

class VisualAIGame:
    def __init__(self):
        self.initialize_session_state()
    
    def initialize_session_state(self):
        """Initialize all session state variables"""
        if 'current_level' not in st.session_state:
            st.session_state.current_level = 1
        if 'score' not in st.session_state:
            st.session_state.score = 0
        if 'lives' not in st.session_state:
            st.session_state.lives = 3
        if 'current_puzzle' not in st.session_state:
            st.session_state.current_puzzle = None
        if 'selected_items' not in st.session_state:
            st.session_state.selected_items = []
        if 'puzzle_attempts' not in st.session_state:
            st.session_state.puzzle_attempts = 0
        if 'show_hint' not in st.session_state:
            st.session_state.show_hint = False
        if 'game_completed' not in st.session_state:
            st.session_state.game_completed = False
    
    def display_header(self):
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
            <li>🧩 Click the items in the correct order</li>
            <li>💡 Use hints if you get stuck</li>
            <li>🏆 Complete all levels to win!</li>
        </ul>
        </div>
        
        <p><em>These are exactly the skills that make students successful in AI courses!</em></p>
        </div>
        """, unsafe_allow_html=True)
    
    def create_puzzle(self, level):
        """Create a visual puzzle based on level"""
        puzzles = {
            1: {
                "name": "Color Sequence",
                "description": "Click the colors in the correct order",
                "items": ["🔴", "🟡", "🔴", "🟡", "?"],
                "correct_order": [0, 1, 2, 3],
                "options": ["🔴", "🟡", "🟢", "🔵"],
                "hint": "🌈 Red, yellow, red, yellow... what comes next?"
            },
            2: {
                "name": "Growing Pattern",
                "description": "Click the shapes in the correct order",
                "items": ["🔴", "🔴🔴", "🔴🔴🔴", "🔴🔴🔴🔴", "?"],
                "correct_order": [0, 1, 2, 3],
                "options": ["🔴🔴🔴🔴🔴", "🔴🔴🔴🔴", "🔴🔴🔴", "🔴🔴"],
                "hint": "🔍 Count the circles: 1, 2, 3, 4... what's next?"
            },
            3: {
                "name": "Shape Progression",
                "description": "Click the shapes in the correct order",
                "items": ["⬜", "🟨", "🟧", "🟥", "?"],
                "correct_order": [0, 1, 2, 3],
                "options": ["🟪", "🟦", "🟩", "⬛"],
                "hint": "🎨 White → yellow → orange → red... what comes after red?"
            },
            4: {
                "name": "Number Sequence",
                "description": "Click the numbers in the correct order",
                "items": ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "?"],
                "correct_order": [0, 1, 2, 3],
                "options": ["5️⃣", "6️⃣", "7️⃣", "8️⃣"],
                "hint": "🔢 1, 2, 3, 4... what number comes next?"
            },
            5: {
                "name": "Logic Challenge",
                "description": "Click the items in the correct order",
                "items": ["🐑", "🐑🐑", "🐑🐑🐑", "🐑🐑🐑🐑", "?"],
                "correct_order": [0, 1, 2, 3],
                "options": ["🐑🐑🐑🐑🐑", "🐑🐑🐑🐑", "🐑🐑🐑", "🐑🐑"],
                "hint": "🐑 Count the sheep: 1, 2, 3, 4... what's next?"
            }
        }
        
        return puzzles.get(level, puzzles[1])
    
    def display_puzzle(self):
        """Display the current puzzle"""
        puzzle = self.create_puzzle(st.session_state.current_level)
        
        st.markdown(f"""
        <div class="game-container">
        <h2>🎯 Level {st.session_state.current_level}: {puzzle['name']}</h2>
        <p>{puzzle['description']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Display the sequence
        st.markdown("**Sequence:**")
        sequence_display = " → ".join(puzzle['items'])
        st.markdown(f"<div style='font-size: 2rem; text-align: center; margin: 2rem 0; padding: 2rem; background: linear-gradient(45deg, #667eea, #764ba2); border-radius: 15px; color: white;'>{sequence_display}</div>", unsafe_allow_html=True)
        
        # Display options
        st.markdown("**Click the items in the correct order:**")
        
        # Create a grid of clickable items
        cols = st.columns(2)
        for i, option in enumerate(puzzle['options']):
            with cols[i % 2]:
                if st.button(f"{option}", key=f"option_{i}", use_container_width=True):
                    if i not in st.session_state.selected_items:
                        st.session_state.selected_items.append(i)
                        st.session_state.puzzle_attempts += 1
                        st.rerun()
        
        # Display selected items
        if st.session_state.selected_items:
            st.markdown("**Your selection:**")
            selected_display = " → ".join([puzzle['options'][i] for i in st.session_state.selected_items])
            st.markdown(f"<div style='font-size: 1.5rem; text-align: center; margin: 1rem 0; padding: 1rem; background: linear-gradient(45deg, #4ECDC4, #45B7D1); border-radius: 10px; color: white;'>{selected_display}</div>", unsafe_allow_html=True)
        
        # Check button for manual completion
        if st.button("✅ Check Answer", key="check_answer"):
            if len(st.session_state.selected_items) == len(puzzle['correct_order']):
                if st.session_state.selected_items == puzzle['correct_order']:
                    st.success("🎉 Correct! Great job!")
                    st.session_state.score += 100 * st.session_state.current_level
                    st.session_state.current_level += 1
                    st.session_state.selected_items = []
                    st.session_state.puzzle_attempts = 0
                    st.session_state.show_hint = False
                    
                    if st.session_state.current_level > 5:
                        st.session_state.game_completed = True
                        st.balloons()
                    
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("❌ Not quite right! Try again!")
                    st.session_state.lives -= 1
                    st.session_state.selected_items = []
                    
                    if st.session_state.lives <= 0:
                        st.error("💀 Game Over! You ran out of lives!")
                        st.session_state.current_level = 1
                        st.session_state.score = 0
                        st.session_state.lives = 3
                        st.session_state.selected_items = []
                        st.session_state.puzzle_attempts = 0
                        st.session_state.show_hint = False
                        st.session_state.game_completed = False
                        time.sleep(2)
                        st.rerun()
                    
                    time.sleep(1)
                    st.rerun()
            else:
                st.warning("⚠️ Please select all items first!")
        
        # Hint button
        if st.session_state.puzzle_attempts >= 2:
            st.session_state.show_hint = True
        
        if st.session_state.show_hint:
            st.markdown(f"<div class='hint-box'>💡 Hint: {puzzle['hint']}</div>", unsafe_allow_html=True)
        
        # Reset button
        if st.button("🔄 Reset Puzzle", key="reset_puzzle"):
            st.session_state.selected_items = []
            st.session_state.puzzle_attempts = 0
            st.session_state.show_hint = False
            st.rerun()
    
    def display_sidebar(self):
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
        
        # Progress bar
        progress = (st.session_state.current_level - 1) / 5
        st.sidebar.markdown(f"""
        <div class="progress-bar">
        <div class="progress-fill" style="width: {progress * 100}%"></div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.sidebar.button("🏠 Home", use_container_width=True):
            st.session_state.current_level = 1
            st.session_state.score = 0
            st.session_state.lives = 3
            st.session_state.selected_items = []
            st.session_state.puzzle_attempts = 0
            st.session_state.show_hint = False
            st.session_state.game_completed = False
            st.rerun()
        
        if st.sidebar.button("🔄 Reset Game", use_container_width=True):
            self.initialize_session_state()
            st.rerun()
    
    def display_results(self):
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
    
    def run(self):
        """Main game loop"""
        self.display_header()
        self.display_sidebar()
        
        if st.session_state.game_completed:
            self.display_results()
        else:
            self.display_puzzle()

# Run the game
if __name__ == "__main__":
    game = VisualAIGame()
    game.run()
