# 🎯 Elastic Collision Simulation in a Circular Container

This simulation uses **Pygame** to demonstrate **2D elastic collisions** between two colored circles constrained within a **circular container**. It features velocity, trail rendering, accurate physics-based collision resolution, and a collision counter!

---

## ✅ **Key Features**
- 🎈 **Two dynamic circles** (red and blue), moving freely in a circular space.
- 🧲 **Gravity** gently pulls the balls downward.
- 🟢 **Elastic collision** with correct velocity vector decomposition and energy conservation.
- 💫 **Trails** behind circles create a motion blur effect.
- 🧱 **Wall collision handling** using vector math with minimal energy loss for realism.
- 🧮 **Accurate collision detection** and resolution using mass and momentum formulas.
- 🎯 **Collision counter** visible on screen.
- 🛑 Simulation **automatically stops** after 10 collisions.

---

## 🧪 **Physics Concepts Illustrated**
- **Elastic Collisions**
- **2D Vector Math**
- **Gravity & Velocity Integration**
- **Momentum Conservation**
- **Normal & Tangential Components**

---

## 🖼️ **Visual Highlights**
- **Clean white background** with a **black container outline**.
- Circles leave behind a **fading trail** that visualizes their recent path.
- Collisions are tracked and shown with a **collision counter** in the top-left corner.

---

## 🧠 **Educational Applications**
This simulation is ideal for:
- 👨‍🏫 **Teaching physics**: momentum, elastic collisions, motion under gravity.
- 🎓 **Computer science**: collision detection, simulation loops, object-oriented programming.
- 🎮 **Game dev learners**: 2D game physics fundamentals.

---

## 🚀 **Try It Yourself**
### Setup:
Install `pygame` if you haven't:
```bash
pip install pygame
```

### Run:
```bash
python circle_collision_sim.py
```

---

## 🛠️ **Possible Enhancements**
- Add more circles with mass and variable radius.
- Track kinetic energy and display it.
- Make collision sounds using Pygame's mixer.
- Include sliders for adjusting gravity, elasticity, or speed live.
