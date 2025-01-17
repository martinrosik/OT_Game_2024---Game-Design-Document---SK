# **Tears Of The Lizard King** 🦎

---

## **1. Introduction** ✨

The proposed game, **Tears Of The Lizard King**, is a demonstration project for the subject **Object Technologies**, showcasing a functional prototype for the exam. The game adheres to the assigned theme, **Dark and Light**, and challenges the player to survive a relentless onslaught of enemies for **3 minutes** and collecting coins. 🌑🌞⚔️

### **1.1 Inspiration** 💡

<ins>**The Binding of Isaac**</ins>

"The Binding of Isaac" is a randomly generated action RPG shooter with strong roguelike elements. Players guide Isaac on a journey to escape his mother, battling mysterious creatures, uncovering secrets, and facing fearsome bosses. Along the way, Isaac collects bizarre treasures that alter his abilities and appearance. Surviving this perilous journey is no easy feat! ⚔️❤

<p align="center">
  <img src="https://github.com/martinrosik/TearsOfTheLizardKing/blob/master/TheBindingofIsaac.jpg" alt="The Binding of Isaac">
  <br>
  <em>Figure 1: Preview of The Binding of Isaac</em>
</p>

### **1.2 Player Experience** 🎮

The player’s goal is to survive a **3-minute interval** (★ 180 seconds) while fending off numerous enemies and collecting coins. Movement across the map, eliminating enemies, and strategically using objects and items like (**heart**, **coin**) found on the map increase the chances of survival. 💪✨

### **1.3 Development Software** 🛠️

- **Pygame-CE**: Programming library for game development.
- **PyCharm 2024.1**: IDE used for coding.
- **Tiled 1.10.2**: Tool for graphical level creation.
- **Itch.io**: Source of graphic assets and sounds.
- **Freesound**: Source for sound effects.

---

## **2. Concept** 🎨

### **2.1 Gameplay Overview** 🎮⚔️

The player controls a character attempting to survive a **3-minute interval** in a hostile environment. Enemies spawn at fixed intervals and locations, rushing toward the player to deal damage. Success requires strategic movement, eliminating enemies, and collecting items. Occasionally, a **healing item** spawns on the map to restore one heart. Also coin item spawns on the map which you can collect. 🪙♥️

### **2.2 Theme Interpretation** 🕹️✨

"The Binding of Isaac" draws inspiration from the Biblical story of the same name, delivering a randomly generated roguelike adventure. Similarly, **Tears Of The Lizard King** captures the essence of survival and action-packed gameplay with a unique narrative and mechanics.

### **2.3 Primary Mechanics** 🛡️

- **Obstacles**: Objects on the map serve as barriers for both the player and enemies, adding a layer of strategy. 🔲
- **Bonus Items**: Collectible items grant buffs such as extra health, increased attack power, or reduced round time. 🎁✨
- **Fixed Enemy Spawn Locations**: Enemies spawn at designated spots, preventing unfair gameplay situations like spawning directly on the player. 🕳️
- **Player Attacks**: The player can shoot snowballs to damage and eliminate enemies. ❄️🔥

### **2.4 Class Design** 🧑‍💻

- **Game**: Manages primary game logic, including the start screen, game loop, and end screen. 🔄
- **Player**: Represents the player, handling movement, rendering, and abilities. 🕺
- **Enemies**: Defines enemy behavior, movement, rendering, and abilities. 👾
- **Dark Mode**: Handles the integration of the light-and-dark theme for the project. 🌗

---

## **3. Art** 🎨🖌️

### **3.1 Theme Interpretation** 🖼️

The game adopts a visually appealing style using assets from **Itch.io**. Enemy designs include knights and slimes, adding variety to the challenges faced by the player. The 2D cartoon-style assets emphasize minimalistic animations to maintain the game’s aesthetic. ✨👑

<p align="center">
  <img src="https://github.com/martinrosik/TearsOfTheLizardKing/blob/master/enemies.png" alt="Enemies">
  <br>
  <em>Figure 3: Preview of enemy sprites</em>
</p>

### **3.2 Design** 🏰

The game utilizes the **DungeonTileset** (https://0x72.itch.io/dungeontileset-ii) for its levels, blending various terrains and environments in a medieval fantasy style. Active obstacles on the map enhance gameplay by introducing tactical elements. 🔲⚔️

<p align="center">
  <img src="https://github.com/martinrosik/TearsOfTheLizardKing/blob/master/levels.png" alt="Levels">
  <br>
  <em>Figure 4: Level design concept</em>
</p>

---

## **4. Audio** 🎵🔊

### **4.1 Music** 🎶

Background music is selected from the **Free RPG Music Pack** (https://davidkbd.itch.io/concerto-classical-music-turned-to-metal-assets-pack). This selection enhances the medieval RPG theme, pairing the visual design with immersive melodies. 🎵🎸

### **4.2 Sound Effects** 🔊🎯

Sound effects are sourced from **Freesound** (https://freesound.org), ensuring alignment with the RPG genre. Key sound effects include those for snowball shooting and enemy hits. 🔪❄️

---

## **5. Game Experience** 🕹️✨

### **5.1 Gameplay** 🎮

The player’s mission is to survive for 3 minutes in a hostile environment. Enemies spawn at fixed locations and pursue the player aggressively. The player can shoot snowballs, collect health-restoring items, and strategically use obstacles for survival. ⚡✨❄️

<p align="center">
  <img src="https://github.com/martinrosik/TearsOfTheLizardKing/blob/master/gameplay.png" alt="Gameplay">
  <br>
  <em>Figure 5: Gameplay preview</em>
</p>

### **5.2 UI** 📋

The user interface aligns seamlessly with the game’s visual theme. The start screen offers options to **START** the game and select difficulty levels (**EASY**, **NORMAL**, **HARD**). 🕹🎛️

### **5.3 Controls** 🎮🖱️

#### **Keyboard**
- **WASD**: Move the player across the map. ↗️⬆️⬇️⬅️➡️

#### **Mouse**
- **Left Button**: Shoot snowballs. ❄️
