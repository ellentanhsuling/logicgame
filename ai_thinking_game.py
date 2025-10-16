import streamlit as st
import random
import time
import json
from typing import List, Dict, Any
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="AI Thinking Challenge",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #2E86AB;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: bold;
    }
    .game-container {
        background-color: #FFFFFF;
        padding: 2rem;
        border-radius: 10px;
        margin: 1rem 0;
        border: 2px solid #2E86AB;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .game-container h2 {
        color: #2E86AB;
        font-size: 2rem;
        margin-bottom: 1rem;
    }
    .game-container h3 {
        color: #A23B72;
        font-size: 1.5rem;
        margin-bottom: 0.8rem;
    }
    .game-container h4 {
        color: #F18F01;
        font-size: 1.3rem;
        margin-bottom: 0.6rem;
    }
    .game-container p, .game-container li {
        color: #2C3E50;
        font-size: 1.1rem;
        line-height: 1.6;
    }
    .score-display {
        font-size: 1.5rem;
        color: #27AE60;
        font-weight: bold;
        background-color: #D5F4E6;
        padding: 0.5rem;
        border-radius: 5px;
    }
    .puzzle-box {
        background-color: #F8F9FA;
        padding: 1.5rem;
        border-radius: 8px;
        border: 2px solid #A23B72;
        margin: 1rem 0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    .puzzle-box h4 {
        color: #A23B72;
        font-size: 1.3rem;
        margin-bottom: 1rem;
    }
    .puzzle-box p {
        color: #2C3E50;
        font-size: 1.1rem;
    }
    .success-message {
        color: #27AE60;
        font-weight: bold;
        font-size: 1.2rem;
        background-color: #D5F4E6;
        padding: 1rem;
        border-radius: 5px;
        border-left: 4px solid #27AE60;
    }
    .thinking-tip {
        background-color: #E8F4FD;
        padding: 1.5rem;
        border-radius: 8px;
        border-left: 4px solid #2E86AB;
        margin: 1rem 0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    .thinking-tip h4 {
        color: #2E86AB;
        font-size: 1.3rem;
        margin-bottom: 1rem;
    }
    .thinking-tip p, .thinking-tip li {
        color: #2C3E50;
        font-size: 1.1rem;
        line-height: 1.6;
    }
    .thinking-tip ul {
        margin-left: 1.5rem;
    }
    .thinking-tip li {
        margin-bottom: 0.5rem;
    }
    /* Sidebar styling */
    .css-1d391kg {
        background-color: #F8F9FA;
    }
    /* Button styling */
    .stButton > button {
        background-color: #2E86AB;
        color: white;
        border: none;
        border-radius: 5px;
        padding: 0.5rem 1rem;
        font-weight: bold;
    }
    .stButton > button:hover {
        background-color: #1F5F7A;
    }
    /* Input styling */
    .stNumberInput > div > div > input {
        border: 2px solid #2E86AB;
        border-radius: 5px;
    }
    .stSelectbox > div > div > select {
        border: 2px solid #2E86AB;
        border-radius: 5px;
    }
    .stTextArea > div > div > textarea {
        border: 2px solid #2E86AB;
        border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)

class AIThinkingGame:
    def __init__(self):
        self.initialize_session_state()
    
    def initialize_session_state(self):
        """Initialize all session state variables"""
        if 'current_game' not in st.session_state:
            st.session_state.current_game = None
        if 'score' not in st.session_state:
            st.session_state.score = 0
        if 'games_completed' not in st.session_state:
            st.session_state.games_completed = []
        if 'current_puzzle' not in st.session_state:
            st.session_state.current_puzzle = None
        if 'puzzle_attempts' not in st.session_state:
            st.session_state.puzzle_attempts = 0
        if 'show_hint' not in st.session_state:
            st.session_state.show_hint = False
    
    def display_header(self):
        """Display the main header and introduction"""
        st.markdown('<h1 class="main-header">🧠 AI Thinking Challenge</h1>', unsafe_allow_html=True)
        
        st.markdown("""
        <div class="game-container">
        <h2>Welcome to the AI Thinking Challenge!</h2>
        <p>This game tests the core skills you'll need to succeed in AI: <strong>flexible thinking</strong> and <strong>problem-solving</strong>.</p>
        
        <div class="thinking-tip">
        <h4>🎯 What This Game Tests:</h4>
        <ul>
            <li><strong>Pattern Recognition:</strong> Can you spot hidden patterns?</li>
            <li><strong>Logical Reasoning:</strong> Can you work through complex problems step by step?</li>
            <li><strong>Creative Problem Solving:</strong> Can you think outside the box?</li>
            <li><strong>Persistence:</strong> Will you keep trying when things get tough?</li>
        </ul>
        </div>
        
        <p><em>These are exactly the skills that make students successful in AI courses!</em></p>
        </div>
        """, unsafe_allow_html=True)
    
    def visual_pattern_game(self):
        """Game 1: Visual Pattern Recognition Challenge"""
        st.markdown("### 🎨 Visual Pattern Challenge")
        
        if st.session_state.current_puzzle != "pattern":
            st.session_state.current_puzzle = "pattern"
            st.session_state.puzzle_attempts = 0
            st.session_state.show_hint = False
        
        st.markdown("""
        <div class="puzzle-box">
        <h4>🎯 Spot the Pattern!</h4>
        <p>Look at the visual pattern below and choose what comes next:</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Visual patterns with emojis and shapes
        visual_patterns = [
            {
                "name": "Growing Shapes",
                "pattern": ["🔴", "🔴🔴", "🔴🔴🔴", "🔴🔴🔴🔴", "?"],
                "options": ["🔴🔴🔴🔴🔴", "🔴🔴🔴🔴", "🔴🔴🔴", "🔴🔴"],
                "answer": "🔴🔴🔴🔴🔴",
                "explanation": "Each row adds one more red circle"
            },
            {
                "name": "Color Sequence",
                "pattern": ["🔴", "🟡", "🔴", "🟡", "?"],
                "options": ["🔴", "🟡", "🟢", "🔵"],
                "answer": "🔴",
                "explanation": "Alternates between red and yellow"
            },
            {
                "name": "Shape Progression",
                "pattern": ["⬜", "🟨", "🟧", "🟥", "?"],
                "options": ["🟪", "🟦", "🟩", "⬛"],
                "answer": "🟪",
                "explanation": "Colors get progressively warmer (white → yellow → orange → red → purple)"
            },
            {
                "name": "Number Shapes",
                "pattern": ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "?"],
                "options": ["5️⃣", "6️⃣", "7️⃣", "8️⃣"],
                "answer": "5️⃣",
                "explanation": "Counting up: 1, 2, 3, 4, 5..."
            }
        ]
        
        current_pattern = random.choice(visual_patterns)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Display the visual pattern
            st.markdown("**Pattern:**")
            pattern_display = " → ".join(current_pattern["pattern"])
            st.markdown(f"<div style='font-size: 2rem; text-align: center; margin: 1rem 0;'>{pattern_display}</div>", unsafe_allow_html=True)
            
            st.markdown("**What comes next?**")
            
            # Create clickable buttons for options
            cols = st.columns(2)
            selected_option = None
            
            for i, option in enumerate(current_pattern["options"]):
                with cols[i % 2]:
                    if st.button(f"{option}", key=f"option_{i}", use_container_width=True):
                        selected_option = option
            
            if selected_option:
                st.session_state.puzzle_attempts += 1
                
                if selected_option == current_pattern["answer"]:
                    st.success("🎉 Excellent! You spotted the pattern!")
                    st.markdown(f"**Explanation:** {current_pattern['explanation']}")
                    st.session_state.score += 15
                    st.session_state.games_completed.append("pattern")
                    st.session_state.current_puzzle = None
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("❌ Not quite right. Look more carefully!")
                    if st.session_state.puzzle_attempts >= 2:
                        st.session_state.show_hint = True
        
        with col2:
            st.markdown(f"**Score:** <span class='score-display'>{st.session_state.score}</span>", unsafe_allow_html=True)
            st.markdown(f"**Attempts:** {st.session_state.puzzle_attempts}")
            
            if st.session_state.show_hint:
                fun_hints = {
                    "Growing Shapes": "🔍 Count the circles: 1, 2, 3, 4... what's next?",
                    "Color Sequence": "🌈 Red, yellow, red, yellow... what should come next?",
                    "Shape Progression": "🎨 White → yellow → orange → red... what color comes after red?",
                    "Number Shapes": "🔢 1, 2, 3, 4... what number comes next?"
                }
                hint = fun_hints.get(current_pattern['name'], "Look carefully at the pattern!")
                st.markdown(f"**💡 Fun Hint:** {hint}")
    
    def visual_logic_game(self):
        """Game 2: Visual Logic Challenge"""
        st.markdown("### 🧩 Visual Logic Challenge")
        
        if st.session_state.current_puzzle != "logic":
            st.session_state.current_puzzle = "logic"
            st.session_state.puzzle_attempts = 0
            st.session_state.show_hint = False
        
        st.markdown("""
        <div class="puzzle-box">
        <h4>🎯 Solve the Visual Logic!</h4>
        <p>Use the visual clues to find the answer:</p>
        </div>
        """, unsafe_allow_html=True)
        
        visual_puzzles = [
            {
                "name": "Sheep Math",
                "question": "A farmer has 17 sheep. All but 9 die. How many sheep are left?",
                "visual": "🐑🐑🐑🐑🐑🐑🐑🐑🐑🐑🐑🐑🐑🐑🐑🐑🐑",
                "options": ["8", "9", "17", "26"],
                "answer": "9",
                "explanation": "'All but 9 die' means 9 sheep survive! The total number (17) is just a distraction."
            },
            {
                "name": "Machine Logic",
                "question": "If it takes 5 machines 5 minutes to make 5 widgets, how long for 100 machines to make 100 widgets?",
                "visual": "⚙️⚙️⚙️⚙️⚙️ → 5 minutes → 📦📦📦📦📦",
                "options": ["5 minutes", "100 minutes", "20 minutes", "1 minute"],
                "answer": "5 minutes",
                "explanation": "Each machine takes 5 minutes to make 1 widget. So 100 machines = 100 widgets in 5 minutes!"
            },
            {
                "name": "Color Logic",
                "question": "If 🔴 = 2, 🟡 = 3, and 🔵 = 5, what does 🔴 + 🟡 + 🔵 equal?",
                "visual": "🔴 + 🟡 + 🔵 = ?",
                "options": ["8", "10", "12", "15"],
                "answer": "10",
                "explanation": "2 + 3 + 5 = 10. Simple addition with visual symbols!"
            },
            {
                "name": "Pattern Logic",
                "question": "If ⬜ = 1, ⬛ = 0, what does ⬜⬛⬜⬛ represent?",
                "visual": "⬜⬛⬜⬛ = ?",
                "options": ["1010", "1100", "1011", "1001"],
                "answer": "1010",
                "explanation": "White = 1, Black = 0, so ⬜⬛⬜⬛ = 1010"
            }
        ]
        
        current_puzzle = random.choice(visual_puzzles)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown(f"**Question:** {current_puzzle['question']}")
            
            # Display visual element
            st.markdown(f"<div style='font-size: 2rem; text-align: center; margin: 1rem 0; padding: 1rem; background-color: #F8F9FA; border-radius: 8px;'>{current_puzzle['visual']}</div>", unsafe_allow_html=True)
            
            # Create clickable buttons for options
            cols = st.columns(2)
            selected_option = None
            
            for i, option in enumerate(current_puzzle["options"]):
                with cols[i % 2]:
                    if st.button(f"{option}", key=f"logic_option_{i}", use_container_width=True):
                        selected_option = option
            
            if selected_option:
                st.session_state.puzzle_attempts += 1
                
                if selected_option == current_puzzle["answer"]:
                    st.success("🎉 Brilliant logical thinking!")
                    st.markdown(f"**Explanation:** {current_puzzle['explanation']}")
                    st.session_state.score += 20
                    st.session_state.games_completed.append("logic")
                    st.session_state.current_puzzle = None
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("❌ Think it through step by step!")
                    if st.session_state.puzzle_attempts >= 2:
                        st.session_state.show_hint = True
        
        with col2:
            st.markdown(f"**Score:** <span class='score-display'>{st.session_state.score}</span>", unsafe_allow_html=True)
            st.markdown(f"**Attempts:** {st.session_state.puzzle_attempts}")
            
            if st.session_state.show_hint:
                fun_hints = {
                    "Sheep Math": "🐑 'All but 9 die' means 9 sheep survive! The 17 is just a distraction.",
                    "Machine Logic": "⚙️ If 5 machines make 5 widgets in 5 minutes, each machine makes 1 widget in 5 minutes!",
                    "Color Logic": "🎨 Just add: 2 + 3 + 5 = ?",
                    "Pattern Logic": "⬜⬛ White = 1, Black = 0, so ⬜⬛⬜⬛ = 1010!"
                }
                hint = fun_hints.get(current_puzzle['name'], "Think step by step!")
                st.markdown(f"**💡 Fun Hint:** {hint}")
    
    def interactive_creative_game(self):
        """Game 3: Interactive Creative Problem Solving"""
        st.markdown("### 💡 Interactive Creative Challenge")
        
        if st.session_state.current_puzzle != "creative":
            st.session_state.current_puzzle = "creative"
            st.session_state.puzzle_attempts = 0
            st.session_state.show_hint = False
        
        st.markdown("""
        <div class="puzzle-box">
        <h4>🎯 Think Outside the Box!</h4>
        <p>Put the steps in the correct order to solve this creative challenge:</p>
        </div>
        """, unsafe_allow_html=True)
        
        creative_challenges = [
            {
                "name": "Light Switch Logic",
                "question": "You're in a room with 3 light switches. One controls a light bulb in another room. You can only go to the other room once. How do you figure out which switch controls the bulb?",
                "visual": "🔘🔘🔘 + 💡 = ?",
                "steps": [
                    "🔘 Turn on the first switch",
                    "⏱️ Wait 5 minutes",
                    "🔘 Turn off first switch, turn on second switch",
                    "🚪 Go to the other room",
                    "💡 Check if bulb is on, warm, or off"
                ],
                "correct_order": [0, 1, 2, 3, 4],
                "explanation": "Turn on first switch, wait, turn it off and turn on second switch. If bulb is on = second switch, warm = first switch, off = third switch!"
            },
            {
                "name": "Prisoner Hat Logic", 
                "question": "3 prisoners are told they can see each other's hats but not their own. There are 2 black hats and 3 white hats. The first prisoner says 'I don't know my hat color.' The second says 'I don't know either.' The third prisoner says 'I know my hat color!' What color is the third prisoner's hat?",
                "visual": "👥👥👥 + 🎩🎩🎩 = ?",
                "steps": [
                    "👀 Third prisoner looks at other two hats",
                    "🧠 Thinks: 'If I had a black hat, the others would know theirs'",
                    "🤔 Realizes: 'They don't know, so I must have white'",
                    "💡 Concludes: 'My hat is white!'"
                ],
                "correct_order": [0, 1, 2, 3],
                "explanation": "If third prisoner had black hat, others would see one black + one white and know theirs. Since they don't know, third prisoner must have white hat!"
            },
            {
                "name": "Coin Weighing Logic",
                "question": "You have 12 coins. One is fake (lighter or heavier). You have a balance scale. How do you find the fake coin in just 3 weighings?",
                "visual": "🪙🪙🪙🪙🪙🪙🪙🪙🪙🪙🪙🪙 + ⚖️ = ?",
                "steps": [
                    "⚖️ Weigh 4 coins vs 4 coins (first weighing)",
                    "🧠 If equal: fake is in remaining 4. If not: fake is in heavier/lighter group",
                    "⚖️ Take 3 from suspect group, weigh 1 vs 1 (second weighing)",
                    "⚖️ Final weighing reveals the fake coin"
                ],
                "correct_order": [0, 1, 2, 3],
                "explanation": "Divide into groups of 4, then narrow down systematically. The key is eliminating possibilities with each weighing!"
            },
            {
                "name": "Water Jug Logic",
                "question": "You have a 5-liter jug and a 3-liter jug. How do you measure exactly 4 liters of water?",
                "visual": "🪣(5L) + 🪣(3L) = 4L",
                "steps": [
                    "💧 Fill the 5-liter jug completely",
                    "🔄 Pour from 5L jug into 3L jug until 3L is full",
                    "💧 Empty the 3-liter jug",
                    "🔄 Pour remaining water from 5L jug into 3L jug",
                    "💧 Fill 5L jug again and pour into 3L jug until full"
                ],
                "correct_order": [0, 1, 2, 3, 4],
                "explanation": "Fill 5L, pour into 3L (leaves 2L in 5L), empty 3L, pour 2L into 3L, fill 5L, pour 1L into 3L = 4L in 5L jug!"
            }
        ]
        
        current_challenge = random.choice(creative_challenges)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown(f"**Challenge:** {current_challenge['question']}")
            
            # Display visual element
            st.markdown(f"<div style='font-size: 2rem; text-align: center; margin: 1rem 0; padding: 1rem; background-color: #F8F9FA; border-radius: 8px;'>{current_challenge['visual']}</div>", unsafe_allow_html=True)
            
            st.markdown("**Put these steps in the correct order:**")
            
            # Initialize session state for step ordering
            if 'step_order' not in st.session_state or len(st.session_state.step_order) != len(current_challenge['steps']):
                st.session_state.step_order = list(range(len(current_challenge['steps'])))
            
            # Display steps in current order
            for i, step_idx in enumerate(st.session_state.step_order):
                if step_idx < len(current_challenge['steps']):
                    step = current_challenge['steps'][step_idx]
                    col_a, col_b = st.columns([6, 1])
                    
                    with col_a:
                        st.markdown(f"**{i+1}.** {step}")
                    
                    with col_b:
                        if i > 0 and st.button("⬆️", key=f"up_{i}"):
                            # Move step up
                            st.session_state.step_order[i], st.session_state.step_order[i-1] = st.session_state.step_order[i-1], st.session_state.step_order[i]
                            st.rerun()
                    
                    if i < len(st.session_state.step_order) - 1:
                        with col_b:
                            if st.button("⬇️", key=f"down_{i}"):
                                # Move step down
                                st.session_state.step_order[i], st.session_state.step_order[i+1] = st.session_state.step_order[i+1], st.session_state.step_order[i]
                                st.rerun()
            
            if st.button("✅ Check My Order", key="check_order"):
                st.session_state.puzzle_attempts += 1
                
                if st.session_state.step_order == current_challenge['correct_order']:
                    st.success("🎉 Perfect! You solved it creatively!")
                    st.markdown(f"**Explanation:** {current_challenge['explanation']}")
                    st.session_state.score += 25
                    st.session_state.games_completed.append("creative")
                    st.session_state.current_puzzle = None
                    st.session_state.step_order = []
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("❌ Not quite right! Try reordering the steps!")
                    if st.session_state.puzzle_attempts >= 2:
                        st.session_state.show_hint = True
        
        with col2:
            st.markdown(f"**Score:** <span class='score-display'>{st.session_state.score}</span>", unsafe_allow_html=True)
            st.markdown(f"**Attempts:** {st.session_state.puzzle_attempts}")
            
            if st.session_state.show_hint:
                fun_hints = {
                    "Light Switch Logic": "💡 Think about what happens when a light bulb is on for a while... it gets warm!",
                    "Prisoner Hat Logic": "🎩 If you had a black hat, what would the others see? Think about it!",
                    "Coin Weighing Logic": "⚖️ Start by dividing the coins into groups - eliminate possibilities!",
                    "Water Jug Logic": "🪣 Fill one jug, pour into the other, empty it... keep going!"
                }
                hint = fun_hints.get(current_challenge['name'], "Think creatively!")
                st.markdown(f"**💡 Fun Hint:** {hint}")
            
            # Quick reset button
            if st.button("🔄 Reset Order", key="reset_order"):
                st.session_state.step_order = list(range(len(current_challenge['steps'])))
                st.rerun()
    
    def visual_persistence_game(self):
        """Game 4: Visual Persistence Challenge"""
        st.markdown("### 🏃‍♂️ Visual Persistence Challenge")
        
        if st.session_state.current_puzzle != "persistence":
            st.session_state.current_puzzle = "persistence"
            st.session_state.puzzle_attempts = 0
            st.session_state.show_hint = False
        
        st.markdown("""
        <div class="puzzle-box">
        <h4>🎯 Don't Give Up!</h4>
        <p>This puzzle is tricky, but persistence pays off:</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Visual sequence puzzle
        st.markdown("**Find the missing number in this visual sequence:**")
        
        # Create a visual grid representation
        sequence_numbers = [2, 6, 12, 20, 30, 42]
        sequence_visual = []
        
        for i, num in enumerate(sequence_numbers):
            # Create visual representation
            visual = "🔢" * (i + 1) + f" = {num}"
            sequence_visual.append(visual)
        
        # Display the sequence visually
        st.markdown("**Visual Pattern:**")
        for i, visual in enumerate(sequence_visual):
            st.markdown(f"<div style='font-size: 1.5rem; margin: 0.5rem 0; padding: 0.5rem; background-color: #F8F9FA; border-radius: 5px;'>{visual}</div>", unsafe_allow_html=True)
        
        st.markdown("**What comes next?**")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Multiple choice with visual feedback
            st.markdown("**Choose your answer:**")
            
            options = [
                {"value": 56, "display": "56", "visual": "🔢🔢🔢🔢🔢🔢🔢 = 56"},
                {"value": 48, "display": "48", "visual": "🔢🔢🔢🔢🔢🔢 = 48"},
                {"value": 64, "display": "64", "visual": "🔢🔢🔢🔢🔢🔢🔢🔢 = 64"},
                {"value": 72, "display": "72", "visual": "🔢🔢🔢🔢🔢🔢🔢🔢🔢 = 72"}
            ]
            
            cols = st.columns(2)
            selected_answer = None
            
            for i, option in enumerate(options):
                with cols[i % 2]:
                    if st.button(f"{option['display']}", key=f"persist_option_{i}", use_container_width=True):
                        selected_answer = option['value']
            
            if selected_answer:
                st.session_state.puzzle_attempts += 1
                
                if selected_answer == 56:
                    st.success("🎉 Persistence paid off! You didn't give up!")
                    st.markdown("**Explanation:** The pattern is n(n+1): 1×2=2, 2×3=6, 3×4=12, 4×5=20, 5×6=30, 6×7=42, 7×8=56")
                    st.session_state.score += 30
                    st.session_state.games_completed.append("persistence")
                    st.session_state.current_puzzle = None
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("❌ Keep trying! The pattern is there...")
                    if st.session_state.puzzle_attempts >= 3:
                        st.session_state.show_hint = True
                    
                    # Show encouragement based on attempts
                    if st.session_state.puzzle_attempts == 1:
                        st.info("💪 First attempt! Don't give up!")
                    elif st.session_state.puzzle_attempts == 2:
                        st.info("🔥 Second try! You're getting closer!")
                    else:
                        st.info("🚀 Keep going! Persistence is key in AI!")
        
        with col2:
            st.markdown(f"**Score:** <span class='score-display'>{st.session_state.score}</span>", unsafe_allow_html=True)
            st.markdown(f"**Attempts:** {st.session_state.puzzle_attempts}")
            
            if st.session_state.show_hint:
                st.markdown("**💡 Fun Hint:** 🔢 Look at the differences: 4, 6, 8, 10, 12... what comes next? Think n×(n+1)!")
            
            # Progress indicator
            if st.session_state.puzzle_attempts > 0:
                progress = min(st.session_state.puzzle_attempts / 5, 1.0)
                st.progress(progress)
                st.markdown(f"**Persistence Level:** {int(progress * 100)}%")
    
    def display_results(self):
        """Display final results and course suitability assessment"""
        st.markdown("### 🎯 Your AI Course Suitability Assessment")
        
        total_possible = 70  # 10 + 15 + 20 + 25
        percentage = (st.session_state.score / total_possible) * 100
        
        st.markdown(f"""
        <div class="game-container">
        <h3>Final Score: {st.session_state.score}/{total_possible} ({percentage:.1f}%)</h3>
        """, unsafe_allow_html=True)
        
        if percentage >= 80:
            st.success("🌟 **Excellent!** You have strong analytical thinking skills that are perfect for AI!")
            st.markdown("""
            **You demonstrated:**
            - Strong pattern recognition abilities
            - Logical reasoning skills
            - Creative problem-solving approach
            - Persistence when facing challenges
            
            **You're likely to succeed in our AI course!** The coding will be challenging, but your thinking skills will help you overcome obstacles.
            """)
        elif percentage >= 60:
            st.info("👍 **Good!** You have solid analytical thinking skills.")
            st.markdown("""
            **You showed:**
            - Some pattern recognition ability
            - Basic logical reasoning
            - Some creative thinking
            - Moderate persistence
            
            **You could succeed in our AI course** with dedication and practice. Consider brushing up on logical thinking before starting.
            """)
        elif percentage >= 40:
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
        <div class="thinking-tip">
        <h4>📚 About Our AI Course</h4>
        <p><strong>What you'll learn:</strong> Machine learning, data analysis, neural networks, and AI applications</p>
        <p><strong>Prerequisites:</strong> Strong analytical thinking (like what this game tested), basic math, and willingness to learn programming</p>
        <p><strong>Time commitment:</strong> 6 months, 10-15 hours per week</p>
        <p><strong>Outcome:</strong> Build real AI projects and understand how AI systems work</p>
        </div>
        """, unsafe_allow_html=True)
    
    def reset_game(self):
        """Reset the game state"""
        st.session_state.current_game = None
        st.session_state.score = 0
        st.session_state.games_completed = []
        st.session_state.current_puzzle = None
        st.session_state.puzzle_attempts = 0
        st.session_state.show_hint = False
        if 'step_order' in st.session_state:
            del st.session_state.step_order
        st.rerun()
    
    def run(self):
        """Main game loop"""
        self.display_header()
        
        # Sidebar for game selection
        st.sidebar.title("🎮 Game Menu")
        
        if st.sidebar.button("🏠 Home"):
            st.session_state.current_game = None
            st.rerun()
        
        st.sidebar.markdown("### Choose a Challenge:")
        
        if st.sidebar.button("🎨 Visual Pattern Challenge"):
            st.session_state.current_game = "pattern"
            st.rerun()
        
        if st.sidebar.button("🧩 Visual Logic Challenge"):
            st.session_state.current_game = "logic"
            st.rerun()
        
        if st.sidebar.button("💡 Interactive Creative Challenge"):
            st.session_state.current_game = "creative"
            st.rerun()
        
        if st.sidebar.button("🏃‍♂️ Visual Persistence Challenge"):
            st.session_state.current_game = "persistence"
            st.rerun()
        
        if st.sidebar.button("🎯 View Results"):
            st.session_state.current_game = "results"
            st.rerun()
        
        st.sidebar.markdown("---")
        st.sidebar.markdown(f"**Current Score:** {st.session_state.score}")
        st.sidebar.markdown(f"**Games Completed:** {len(st.session_state.games_completed)}/4")
        
        if st.sidebar.button("🔄 Reset Game"):
            self.reset_game()
        
        # Main game area
        if st.session_state.current_game == "pattern":
            self.visual_pattern_game()
        elif st.session_state.current_game == "logic":
            self.visual_logic_game()
        elif st.session_state.current_game == "creative":
            self.interactive_creative_game()
        elif st.session_state.current_game == "persistence":
            self.visual_persistence_game()
        elif st.session_state.current_game == "results":
            self.display_results()
        else:
            # Home screen
            st.markdown("""
            <div class="game-container">
            <h2>Ready to Test Your AI Thinking Skills?</h2>
            <p>Complete all four interactive challenges to get your AI course suitability assessment!</p>
            
            <h3>🎯 The Visual Challenges:</h3>
            <ul>
                <li><strong>🎨 Visual Pattern Challenge:</strong> Spot patterns in colorful emoji sequences!</li>
                <li><strong>🧩 Visual Logic Challenge:</strong> Solve puzzles with visual clues and symbols!</li>
                <li><strong>💡 Interactive Creative Challenge:</strong> Think outside the box with interactive elements!</li>
                <li><strong>🏃‍♂️ Visual Persistence Challenge:</strong> Don't give up on tricky visual sequences!</li>
            </ul>
            
            <p><strong>These are exactly the skills that make students successful in AI courses!</strong></p>
            
            <h3>📊 How It Works:</h3>
            <ol>
                <li>Click through each visual challenge (much more fun than text!)</li>
                <li>Earn points based on your problem-solving approach</li>
                <li>Get instant feedback and explanations</li>
                <li>Receive a personalized assessment of your AI course readiness</li>
                <li>Learn about our AI course and what it really takes to succeed</li>
            </ol>
            
            <p><em>Use the sidebar to navigate between challenges - they're all interactive and visual!</em></p>
            </div>
            """, unsafe_allow_html=True)

# Run the game
if __name__ == "__main__":
    game = AIThinkingGame()
    game.run()
