# Defend the Crystal - Guard the Home 🌟

> **A Simple Battle Game Built with Pygame**  
> Experience the thrill of defending your castle and crystal!

---

## 1. Project Overview 🎮

This project is a simple battle game developed using **Pygame** as part of a Python programming assignment.  
The game addresses key challenges such as initialization, user input handling, game element updates, collision detection, and saving/loading game state.  
Players defend their castle and crystal by clicking to shoot, offering a fun and challenging gameplay experience.

---

## 2. System Requirements 🖥️

- **Operating System**: Windows / Ubuntu / macOS
- **Python Version**: Recommended Python 3.7 or above
- **Dependencies**: Pygame, etc. (see installation instructions below)

---

## 3. Project Structure 📁

```bash
├── main.py                   # Main game program
├── modules                   # Module folder
│   ├── Sprites.py            # Defines game elements (rabbit, mole, bullet) and their actions
│   └── interfaces.py         # Defines the game over interface and related functions
├── resources                 # Resource folder
│   ├── images                # Game image assets
│   └── audio                 # Game audio assets
├── game_state.txt            # File for saving/loading game state (accuracy)
└── requirements.txt          # List of dependencies
```

---

## 4. Installation and Running 🚀

### 4.1 Install Dependencies 📦

1. After cloning the project locally, it is recommended to create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate    # Linux/macOS
   venv\Scripts\activate       # Windows
   ```
2. Install the project dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### 4.2 Run the Game 🎲

With the virtual environment activated, run the following command to start the game:

```bash
python main.py
```

The game window will open automatically. Follow the on-screen instructions to enjoy the game.

---

## 5. Gameplay and Features 🎯

- **Game Initialization**: Loads the window, images, and audio resources, and initializes game modules.
- **User Input**: Supports mouse clicks for shooting, with corresponding sound effects.
- **Game Element Updates**: Manages the movement, collision detection, and health calculation of characters (rabbit), enemies (moles), and bullets.
- **State Saving**: Automatically saves the current shooting accuracy when the game ends for future reference or analysis.

---

## 6. Design Summary 📝

- **Game Development Fundamentals**: Gain a deeper understanding of Pygame's basic usage, including graphics, sound, and user input handling.
- **Object-Oriented Programming**: Learn how to write structured and maintainable code through modular design and class definitions.
- **File Operations**: Understand how to save and load game states, enhancing your knowledge of file handling.
- **Debugging and Optimization**: Accumulate valuable debugging experience, laying a solid foundation for tackling more complex projects in the future.

---

💖 **Thank you for your interest, and enjoy the game!** 💖

```

```
