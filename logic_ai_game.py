import streamlit as st
import random
import time

# Page configuration
st.set_page_config(
    page_title="🧠 AI Logic Challenge",
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
    
    .logic-step {
        background: linear-gradient(45deg, rgba(128, 0, 255, 0.3), rgba(255, 0, 128, 0.3));
        padding: 2rem;
        border-radius: 15px;
        margin: 1rem 0;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        transition: all 0.3s ease;
        cursor: pointer;
        position: relative;
        overflow: hidden;
    }
    
    .logic-step:hover {
        transform: translateY(-5px) scale(1.02);
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.3);
    }
    
    .logic-step.selected {
        background: linear-gradient(45deg, rgba(0, 255, 128, 0.4), rgba(255, 215, 0, 0.4));
        transform: scale(1.05);
        box-shadow: 0 0 30px rgba(255, 255, 255, 0.5);
        animation: selectedPulse 0.6s ease-in-out;
    }
    
    @keyframes selectedPulse {
        0% { transform: scale(1.05); }
        50% { transform: scale(1.1); }
        100% { transform: scale(1.05); }
    }
    
    .logic-step::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
        transition: left 0.6s;
    }
    
    .logic-step:hover::before {
        left: 100%;
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
    
    .lives-display {
        display: flex;
        gap: 1rem;
        justify-content: center;
        align-items: center;
    }
    
    .ai-assistant {
        width: 50px;
        height: 60px;
        background: linear-gradient(135deg, #4A90E2, #7B68EE);
        border-radius: 15px 15px 5px 5px;
        position: relative;
        display: inline-block;
        margin: 0 0.8rem;
        animation: robotFloat 3s ease-in-out infinite;
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
    }
    
    .ai-assistant::before {
        content: '';
        position: absolute;
        top: 8px;
        left: 50%;
        transform: translateX(-50%);
        width: 20px;
        height: 20px;
        background: #fff;
        border-radius: 50%;
        box-shadow: inset 0 0 0 3px #4A90E2;
    }
    
    .ai-assistant::after {
        content: '';
        position: absolute;
        top: 12px;
        left: 50%;
        transform: translateX(-50%);
        width: 8px;
        height: 8px;
        background: #4A90E2;
        border-radius: 50%;
        animation: robotBlink 4s ease-in-out infinite;
    }
    
    .ai-assistant .robot-body {
        position: absolute;
        bottom: 0;
        left: 50%;
        transform: translateX(-50%);
        width: 30px;
        height: 25px;
        background: linear-gradient(135deg, #5BA0F2, #8B78FE);
        border-radius: 0 0 15px 15px;
    }
    
    .ai-assistant .robot-antenna {
        position: absolute;
        top: -8px;
        left: 50%;
        transform: translateX(-50%);
        width: 2px;
        height: 12px;
        background: #FFD700;
        border-radius: 1px;
    }
    
    .ai-assistant .robot-antenna::after {
        content: '';
        position: absolute;
        top: -3px;
        left: -2px;
        width: 6px;
        height: 6px;
        background: #FF6B6B;
        border-radius: 50%;
        animation: antennaGlow 2s ease-in-out infinite;
    }
    
    @keyframes robotFloat {
        0%, 100% { 
            transform: translateY(0px) rotate(0deg); 
        }
        25% { 
            transform: translateY(-6px) rotate(1deg); 
        }
        50% { 
            transform: translateY(-3px) rotate(0deg); 
        }
        75% { 
            transform: translateY(-6px) rotate(-1deg); 
        }
    }
    
    @keyframes robotBlink {
        0%, 90%, 100% { opacity: 1; }
        95% { opacity: 0.2; }
    }
    
    @keyframes antennaGlow {
        0%, 100% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.7; transform: scale(1.2); }
    }
    
    /* Explanation Screen Styles */
    .explanation-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 25px;
        padding: 3rem;
        margin: 2rem 0;
        text-align: center;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
        position: relative;
        overflow: hidden;
    }
    
    .explanation-container::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: conic-gradient(from 0deg, #ff0080, #00ff80, #8000ff, #ff0080);
        animation: rotate 4s linear infinite;
        z-index: -1;
    }
    
    .explanation-header {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        padding: 2rem;
        margin-bottom: 2rem;
        backdrop-filter: blur(10px);
    }
    
    .explanation-title {
        font-size: 3rem;
        font-weight: bold;
        background: linear-gradient(45deg, #ff0080, #00ff80, #8000ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 0;
        animation: celebration 2s ease-in-out infinite;
    }
    
    .explanation-subtitle {
        font-size: 1.5rem;
        color: #666;
        margin-top: 1rem;
        font-weight: 600;
    }
    
    @keyframes celebration {
        0%, 100% { transform: scale(1) rotate(0deg); }
        25% { transform: scale(1.05) rotate(1deg); }
        75% { transform: scale(1.05) rotate(-1deg); }
    }
    
    .solution-showcase {
        background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 50%, #fecfef 100%);
        border-radius: 20px;
        padding: 2rem;
        margin: 2rem 0;
        box-shadow: 0 15px 30px rgba(0, 0, 0, 0.2);
    }
    
    .solution-title {
        font-size: 2rem;
        color: #333;
        margin-bottom: 1.5rem;
        text-align: center;
    }
    
    .solution-steps {
        display: flex;
        flex-direction: column;
        gap: 1rem;
    }
    
    .solution-step {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        display: flex;
        align-items: center;
        gap: 1rem;
        box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
        animation: slideInUp 0.6s ease-out forwards;
        opacity: 0;
        transform: translateY(30px);
    }
    
    .solution-number {
        background: rgba(255, 255, 255, 0.3);
        border-radius: 50%;
        width: 40px;
        height: 40px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        font-size: 1.2rem;
    }
    
    .solution-text {
        font-size: 1.1rem;
        font-weight: 500;
    }
    
    @keyframes slideInUp {
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .explanation-content {
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
        border-radius: 20px;
        padding: 2rem;
        margin: 2rem 0;
        box-shadow: 0 15px 30px rgba(0, 0, 0, 0.2);
    }
    
    .explanation-puzzle-title {
        font-size: 2.2rem;
        color: #333;
        margin-bottom: 1.5rem;
        text-align: center;
        background: linear-gradient(45deg, #ff6b6b, #4ecdc4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .logic-explanation {
        background: rgba(255, 255, 255, 0.8);
        border-radius: 15px;
        padding: 2rem;
        margin: 1rem 0;
    }
    
    .logic-explanation h3 {
        color: #2c3e50;
        font-size: 1.5rem;
        margin-bottom: 1rem;
    }
    
    .logic-explanation p {
        color: #34495e;
        line-height: 1.6;
        margin: 1rem 0;
        font-size: 1.1rem;
    }
    
    .logic-explanation ul {
        margin: 1rem 0;
        padding-left: 2rem;
    }
    
    .logic-explanation li {
        color: #34495e;
        margin: 0.5rem 0;
        font-size: 1.1rem;
    }
    
    .ai-skill {
        background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
        border-left: 5px solid #ff6b6b;
        padding: 1rem;
        border-radius: 10px;
        margin: 1.5rem 0;
        font-weight: 600;
    }
    
    .continue-section {
        text-align: center;
        margin: 3rem 0;
    }
    
    .continue-button-container {
        display: inline-block;
    }
    
    .continue-button {
        background: linear-gradient(45deg, #ff6b6b, #4ecdc4, #45b7d1, #96ceb4);
        background-size: 300% 300%;
        border: none;
        color: white;
        padding: 1.5rem 3rem;
        border-radius: 50px;
        font-size: 1.3rem;
        font-weight: bold;
        cursor: pointer;
        transition: all 0.4s ease;
        box-shadow: 0 15px 30px rgba(0, 0, 0, 0.3);
        animation: gradientShift 3s ease infinite;
        position: relative;
        overflow: hidden;
    }
    
    .continue-button:hover {
        transform: translateY(-5px) scale(1.05);
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4);
    }
    
    .continue-button:active {
        transform: translateY(-2px) scale(1.02);
    }
    
    .continue-button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.4), transparent);
        transition: left 0.6s;
    }
    
    .continue-button:hover::before {
        left: 100%;
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Style ONLY the continue button in explanation screen */
    .continue-section .stButton > button {
        background: linear-gradient(45deg, #ff6b6b, #4ecdc4, #45b7d1, #96ceb4) !important;
        background-size: 300% 300% !important;
        border: none !important;
        color: white !important;
        padding: 1.5rem 3rem !important;
        border-radius: 50px !important;
        font-size: 1.3rem !important;
        font-weight: bold !important;
        cursor: pointer !important;
        transition: all 0.4s ease !important;
        box-shadow: 0 15px 30px rgba(0, 0, 0, 0.3) !important;
        animation: gradientShift 3s ease infinite !important;
        position: relative !important;
        overflow: hidden !important;
        width: 100% !important;
        max-width: 400px !important;
        margin: 0 auto !important;
        display: block !important;
    }
    
    .continue-section .stButton > button:hover {
        transform: translateY(-5px) scale(1.05) !important;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4) !important;
    }
    
    .continue-section .stButton > button:active {
        transform: translateY(-2px) scale(1.02) !important;
    }
    
    .continue-section .stButton > button::before {
        content: '' !important;
        position: absolute !important;
        top: 0 !important;
        left: -100% !important;
        width: 100% !important;
        height: 100% !important;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.4), transparent) !important;
        transition: left 0.6s !important;
    }
    
    .continue-section .stButton > button:hover::before {
        left: 100% !important;
    }
    
    .continue-section .stButton {
        text-align: center !important;
        margin: 3rem 0 !important;
    }
    
    .step-number {
        background: linear-gradient(45deg, #FF0080, #00FF80);
        color: white;
        width: 40px;
        height: 40px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        margin-right: 1rem;
        animation: stepGlow 2s ease-in-out infinite alternate;
    }
    
    @keyframes stepGlow {
        0% { box-shadow: 0 0 10px rgba(255, 0, 128, 0.5); }
        100% { box-shadow: 0 0 20px rgba(0, 255, 128, 0.8); }
    }
    
    .visual-element {
        font-size: 3rem;
        text-align: center;
        margin: 1rem 0;
        padding: 2rem;
        background: linear-gradient(45deg, rgba(255, 0, 128, 0.2), rgba(0, 255, 128, 0.2));
        border-radius: 15px;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        animation: visualPulse 3s ease-in-out infinite;
    }
    
    @keyframes visualPulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
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
    if 'selected_steps' not in st.session_state:
        st.session_state.selected_steps = []
    if 'attempts' not in st.session_state:
        st.session_state.attempts = 0
    if 'game_completed' not in st.session_state:
        st.session_state.game_completed = False
    if 'show_explanation' not in st.session_state:
        st.session_state.show_explanation = False

def display_header():
    """Display the amazing header"""
    st.markdown('<h1 class="main-header">🧠 AI Logic Challenge</h1>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="game-container">
    <h2>🎯 Welcome to the Ultimate AI Logic Challenge!</h2>
    <p>This interactive logic puzzle tests the core skills you'll need to succeed in AI: <strong>logical reasoning</strong>, <strong>problem-solving</strong>, and <strong>analytical thinking</strong>.</p>
    
    <div class="hint-box">
    <h4>🎮 How to Play:</h4>
    <ul style="text-align: left; margin: 1rem 0;">
        <li>🧩 Read the logic problem carefully</li>
        <li>🔄 Click the steps in the correct order</li>
        <li>💡 Use hints if you get stuck</li>
        <li>🏆 Complete all levels to win!</li>
    </ul>
    </div>
    
    <p><em>These are exactly the skills that make students successful in AI courses!</em></p>
    </div>
    """, unsafe_allow_html=True)

def create_logic_puzzle(level):
    """Create a logic puzzle based on level"""
    puzzles = {
        1: {
            "name": "Light Switch Logic",
            "description": "You're in a room with 3 light switches. One controls a light bulb in another room. You can only go to the other room once. How do you figure out which switch controls the bulb?",
            "visual": "🔘🔘🔘 + 💡 = ?",
            "steps": [
                "💡 Check if bulb is on, warm, or off",
                "🔘 Turn on the first switch",
                "🚪 Go to the other room",
                "⏱️ Wait 5 minutes",
                "🔘 Turn off first switch, turn on second switch"
            ],
            "correct_order": [1, 3, 4, 2, 0],  # Shuffled order
            "hint": "💡 Think about what happens when a light bulb is on for a while... it gets warm!"
        },
        2: {
            "name": "Prisoner Hat Logic",
            "description": "3 prisoners are told they can see each other's hats but not their own. There are 2 black hats and 3 white hats. The first prisoner says 'I don't know my hat color.' The second says 'I don't know either.' The third prisoner says 'I know my hat color!' What color is the third prisoner's hat?",
            "visual": "👥👥👥 + 🎩🎩🎩 = ?",
            "steps": [
                "💡 Concludes: 'My hat is white!'",
                "🧠 Thinks: 'If I had a black hat, the others would know theirs'",
                "👀 Third prisoner looks at other two hats",
                "🤔 Realizes: 'They don't know, so I must have white'"
            ],
            "correct_order": [2, 1, 3, 0],  # Shuffled order
            "hint": "🎩 If you had a black hat, what would the others see? Think about it!"
        },
        3: {
            "name": "Water Jug Logic",
            "description": "You have a 5-liter jug and a 3-liter jug. How do you measure exactly 4 liters of water?",
            "visual": "🪣(5L) + 🪣(3L) = 4L",
            "steps": [
                "🔄 Pour remaining water from 5L jug into 3L jug",
                "💧 Fill the 5-liter jug completely",
                "💧 Fill 5L jug again and pour into 3L jug until full",
                "🔄 Pour from 5L jug into 3L jug until 3L is full",
                "💧 Empty the 3-liter jug"
            ],
            "correct_order": [1, 3, 4, 0, 2],  # Shuffled order
            "hint": "🪣 Fill one jug, pour into the other, empty it... keep going!"
        },
        4: {
            "name": "Bridge Crossing Logic",
            "description": "Four people need to cross a bridge at night. They have one flashlight. The bridge can only hold two people at a time. Person A takes 1 minute, Person B takes 2 minutes, Person C takes 5 minutes, Person D takes 10 minutes. What's the fastest way?",
            "visual": "🌉 + 🔦 + 👥👥👥👥 = ?",
            "steps": [
                "🔦 B returns with flashlight (2 minutes)",
                "👥👥 A and B cross together (2 minutes)",
                "👥👥 A and B cross together again (2 minutes)",
                "🔦 A returns with flashlight (1 minute)",
                "👥👥 C and D cross together (10 minutes)"
            ],
            "correct_order": [1, 3, 4, 0, 2],  # Shuffled order
            "hint": "🌉 Think about who should go together and who should return with the flashlight"
        },
        5: {
            "name": "Coin Weighing Logic",
            "description": "You have 12 coins. One is fake (lighter or heavier). You have a balance scale. How do you find the fake coin in just 3 weighings?",
            "visual": "🪙🪙🪙🪙🪙🪙🪙🪙🪙🪙🪙🪙 + ⚖️ = ?",
            "steps": [
                "⚖️ Final weighing reveals the fake coin",
                "🧠 If equal: fake is in remaining 4. If not: fake is in heavier/lighter group",
                "⚖️ Weigh 4 coins vs 4 coins (first weighing)",
                "⚖️ Take 3 from suspect group, weigh 1 vs 1 (second weighing)"
            ],
            "correct_order": [2, 1, 3, 0],  # Shuffled order
            "hint": "⚖️ Start by dividing the coins into groups - eliminate possibilities!"
        }
    }
    
    return puzzles.get(level, puzzles[1])

def display_explanation():
    """Display colorful explanation of the solved puzzle"""
    puzzle = create_logic_puzzle(st.session_state.current_level - 1)  # Previous level explanation
    
    st.markdown("""
    <div class="explanation-container">
        <div class="explanation-header">
            <h1 class="explanation-title">🎉 AMAZING LOGIC! 🎉</h1>
            <div class="explanation-subtitle">You've mastered this puzzle!</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Show the correct solution with animations
    st.markdown(f"""
    <div class="solution-showcase">
        <h2 class="solution-title">✨ The Perfect Solution ✨</h2>
        <div class="solution-steps">
    """, unsafe_allow_html=True)
    
    correct_order = puzzle['correct_order']
    for i, step_idx in enumerate(correct_order):
        step = puzzle['steps'][step_idx]
        st.markdown(f"""
        <div class="solution-step" style="animation-delay: {i * 0.3}s;">
            <span class="solution-number">{i+1}</span>
            <span class="solution-text">{step}</span>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div></div>", unsafe_allow_html=True)
    
    # Show the logic explanation
    explanations = {
        1: {
            "title": "🔘 Light Switch Logic Explained",
            "explanation": """
            <div class="logic-explanation">
                <h3>🧠 The Brilliant Logic:</h3>
                <p><strong>Step 1:</strong> Turn on the first switch and wait 5 minutes - this heats up the bulb!</p>
                <p><strong>Step 2:</strong> Turn off the first switch and turn on the second - now only the second switch is on</p>
                <p><strong>Step 3:</strong> Go to the other room and check the bulb:</p>
                <ul>
                    <li>💡 <strong>If ON:</strong> Second switch controls it</li>
                    <li>🔥 <strong>If OFF but WARM:</strong> First switch controls it</li>
                    <li>❄️ <strong>If OFF and COLD:</strong> Third switch controls it</li>
                </ul>
                <p class="ai-skill">🎯 <strong>AI Skill:</strong> This tests <em>causal reasoning</em> - understanding that heat is a side effect of electricity!</p>
            </div>
            """
        },
        2: {
            "title": "🎩 Prisoner Hat Logic Explained",
            "explanation": """
            <div class="logic-explanation">
                <h3>🧠 The Brilliant Logic:</h3>
                <p><strong>Step 1:</strong> Third prisoner looks at the other two hats</p>
                <p><strong>Step 2:</strong> Thinks: "If I had a black hat, the others would see one black and one white"</p>
                <p><strong>Step 3:</strong> Realizes: "They said they don't know, which means they see two white hats!"</p>
                <p><strong>Step 4:</strong> Concludes: "I must be wearing a white hat!"</p>
                <p class="ai-skill">🎯 <strong>AI Skill:</strong> This tests <em>deductive reasoning</em> - working backwards from what others know!</p>
            </div>
            """
        },
        3: {
            "title": "🪣 Water Jug Logic Explained",
            "explanation": """
            <div class="logic-explanation">
                <h3>🧠 The Brilliant Logic:</h3>
                <p><strong>Step 1:</strong> Fill 5L jug completely (5L in 5L jug, 0L in 3L jug)</p>
                <p><strong>Step 2:</strong> Pour from 5L to 3L until 3L is full (2L in 5L jug, 3L in 3L jug)</p>
                <p><strong>Step 3:</strong> Empty the 3L jug (2L in 5L jug, 0L in 3L jug)</p>
                <p><strong>Step 4:</strong> Pour remaining 2L from 5L to 3L (0L in 5L jug, 2L in 3L jug)</p>
                <p><strong>Step 5:</strong> Fill 5L jug and pour 1L into 3L jug (4L in 5L jug, 3L in 3L jug)</p>
                <p class="ai-skill">🎯 <strong>AI Skill:</strong> This tests <em>constraint satisfaction</em> - working within the jug capacities!</p>
            </div>
            """
        },
        4: {
            "title": "🌉 Bridge Crossing Logic Explained",
            "explanation": """
            <div class="logic-explanation">
                <h3>🧠 The Brilliant Logic:</h3>
                <p><strong>Step 1:</strong> A and B cross together (2 minutes) - fastest pair goes first</p>
                <p><strong>Step 2:</strong> A returns with flashlight (1 minute) - fastest person returns</p>
                <p><strong>Step 3:</strong> C and D cross together (10 minutes) - slowest pair crosses</p>
                <p><strong>Step 4:</strong> B returns with flashlight (2 minutes) - second fastest returns</p>
                <p><strong>Step 5:</strong> A and B cross together again (2 minutes) - fastest pair finishes</p>
                <p><strong>Total Time:</strong> 2 + 1 + 10 + 2 + 2 = 17 minutes</p>
                <p class="ai-skill">🎯 <strong>AI Skill:</strong> This tests <em>optimization</em> - finding the most efficient sequence!</p>
            </div>
            """
        },
        5: {
            "title": "⚖️ Coin Weighing Logic Explained",
            "explanation": """
            <div class="logic-explanation">
                <h3>🧠 The Brilliant Logic:</h3>
                <p><strong>Step 1:</strong> Weigh 4 coins vs 4 coins - this eliminates 4 coins immediately</p>
                <p><strong>Step 2:</strong> If equal: fake is in remaining 4. If not: fake is in the heavier/lighter group</p>
                <p><strong>Step 3:</strong> Take 3 from suspect group, weigh 1 vs 1 - this narrows it down to 1-2 coins</p>
                <p><strong>Step 4:</strong> Final weighing reveals the exact fake coin</p>
                <p class="ai-skill">🎯 <strong>AI Skill:</strong> This tests <em>divide and conquer</strong> - systematically eliminating possibilities!</p>
            </div>
            """
        }
    }
    
    explanation = explanations.get(st.session_state.current_level - 1, explanations[1])
    
    # Display the explanation title
    st.markdown(f"""
    <div class="explanation-content">
        <h2 class="explanation-puzzle-title">{explanation['title']}</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Display the explanation content separately to ensure proper rendering
    st.markdown(explanation['explanation'], unsafe_allow_html=True)
    
    # Continue button - big bright functional button
    st.markdown("""
    <div class="continue-section">
        <div class="continue-button-container">
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Use Streamlit button but style it to look like the big bright button
    if st.button("🚀 Continue to Next Puzzle! 🚀", key="continue_button", help="Click to proceed to the next puzzle!"):
        st.session_state.show_explanation = False
        st.rerun()

def display_puzzle():
    """Display the current puzzle with amazing visuals"""
    puzzle = create_logic_puzzle(st.session_state.current_level)
    
    st.markdown(f"""
    <div class="game-container">
    <h2>🎯 Level {st.session_state.current_level}: {puzzle['name']}</h2>
    <p>{puzzle['description']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Display visual element
    st.markdown(f"<div class='visual-element'>{puzzle['visual']}</div>", unsafe_allow_html=True)
    
    st.markdown("**Put these steps in the correct order:**")
    
    # Display steps with interactive selection
    for i, step in enumerate(puzzle['steps']):
        is_selected = i in st.session_state.selected_steps
        selection_class = "selected" if is_selected else ""
        
        if st.button(f"**{i+1}.** {step}", key=f"step_{i}", use_container_width=True):
            if i not in st.session_state.selected_steps:
                st.session_state.selected_steps.append(i)
                st.session_state.attempts += 1
                st.rerun()
    
    # Display selected steps in order
    if st.session_state.selected_steps:
        st.markdown("**Your solution:**")
        solution_html = ""
        for i, step_idx in enumerate(st.session_state.selected_steps):
            step = puzzle['steps'][step_idx]
            solution_html += f"<div class='logic-step'><span class='step-number'>{i+1}</span>{step}</div>"
        st.markdown(solution_html, unsafe_allow_html=True)
    
    # Check if puzzle is complete
    if len(st.session_state.selected_steps) == len(puzzle['correct_order']):
        if st.session_state.selected_steps == puzzle['correct_order']:
            st.session_state.score += 200 * st.session_state.current_level
            st.session_state.current_level += 1
            st.session_state.selected_steps = []
            st.session_state.attempts = 0
            st.session_state.show_explanation = True
            
            if st.session_state.current_level > 5:
                st.session_state.game_completed = True
                st.balloons()
            
            time.sleep(1)
            st.rerun()
        else:
            st.error("❌ Not quite right! Try reordering the steps!")
            st.session_state.lives -= 1
            st.session_state.selected_steps = []
            
            if st.session_state.lives <= 0:
                st.error("💀 Game Over! You ran out of lives!")
                st.session_state.current_level = 1
                st.session_state.score = 0
                st.session_state.lives = 3
                st.session_state.selected_steps = []
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
        st.session_state.selected_steps = []
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
    
    # Single robot display
    robot_html = '<div class="lives-display"><div class="ai-assistant"><div class="robot-body"></div><div class="robot-antenna"></div></div></div>'
    st.sidebar.markdown(robot_html, unsafe_allow_html=True)
    
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
        st.session_state.selected_steps = []
        st.session_state.attempts = 0
        st.session_state.game_completed = False
        st.rerun()
    
    if st.sidebar.button("🔄 Reset Game", use_container_width=True):
        initialize_session_state()
        st.rerun()

def display_results():
    """Display final results with amazing visuals"""
    st.markdown("""
    <div class="game-container">
    <h2>🎉 Congratulations! You've completed the AI Logic Challenge!</h2>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="level-indicator">
    Final Score: {st.session_state.score}
    </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.score >= 4000:
        st.success("🌟 **Excellent!** You have exceptional logical reasoning skills that are perfect for AI!")
        st.markdown("""
        **You demonstrated:**
        - Exceptional logical reasoning abilities
        - Strong analytical thinking skills
        - Creative problem-solving approach
        - Persistence when facing complex challenges
        
        **You're likely to excel in our AI course!** Your logical thinking skills will help you master complex AI concepts.
        """)
    elif st.session_state.score >= 3000:
        st.info("👍 **Very Good!** You have strong logical reasoning skills.")
        st.markdown("""
        **You showed:**
        - Strong logical reasoning ability
        - Good analytical thinking
        - Solid problem-solving skills
        - Good persistence with challenges
        
        **You could succeed very well in our AI course** with dedication and practice.
        """)
    elif st.session_state.score >= 2000:
        st.warning("⚠️ **Good.** Your logical reasoning needs some development.")
        st.markdown("""
        **Areas to improve:**
        - Logical reasoning
        - Analytical thinking
        - Problem-solving approach
        - Persistence with difficult problems
        
        **Our AI course might be challenging** for you. Consider taking a foundational logic course first.
        """)
    else:
        st.error("❌ **Needs significant improvement.**")
        st.markdown("""
        **Our AI course would be very difficult** without stronger logical reasoning skills.
        
        **We recommend:**
        - Taking basic logic and reasoning courses first
        - Practicing logic puzzles regularly
        - Building analytical thinking confidence
        - Considering if AI is the right path for you
        """)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Course information
    st.markdown("""
    <div class="game-container">
    <h4>📚 About Our AI Applications Higher Nitec Course</h4>
    <p><strong>What you'll learn:</strong> Machine learning, data analysis, neural networks, and AI applications</p>
    <p><strong>Prerequisites:</strong> Strong logical reasoning (like what this game tested), basic math, and willingness to learn programming</p>
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
    elif st.session_state.show_explanation:
        display_explanation()
    else:
        display_puzzle()

# Run the game
if __name__ == "__main__":
    main()
