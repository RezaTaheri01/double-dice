
# Telegram Bot with Cooldown and Inline Keyboard

A Telegram bot built using the `python-telegram-bot` library. This bot includes interactive inline keyboard buttons, user cooldown functionality, and robust error handling.

---

## 🌟 Features
- **Commands**:
  - `/start`: Displays a welcome message with interactive buttons.
  - `/roll1`: Rolls a single dice.
  - `/roll2`: Rolls two dice.

- **Interactive Inline Keyboard**:
  - Buttons for rolling dice or triggering other actions.

- **Cooldown System**:
  - Prevents users from spamming dice rolls (default: 4 seconds).

- **Error Logging**:
  - Logs errors and warnings to a `logs.log` file for easy debugging.

- **Sponsor Button**:
  - Links to a customizable sponsor URL.

---

## 🛠️ Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/RezaTaheri01/double-dice.git
   ```

2. **Navigate to the project directory**:
   ```bash
   cd double-dice
   ```

3. **Install dependencies** (using a virtual environment is recommended):
   ```bash
   pip install -r req.txt
   ```

4. **Set up your bot token**:
   - Create a `.env` file in the project directory.
   - Add the following line, replacing `<your-telegram-bot-token>` with your bot token:
     ```
     token=<your-telegram-bot-token>
     ```

5. **Run the bot**:
   ```bash
   python bot.py
   ```

---

## ⏳ Cooldown System

Users can only roll dice once every 4 seconds by default. To adjust this duration:

1. Open the `bot.py` file.
2. Modify the `COOLDOWN_DURATION` value.

Example:
```python
COOLDOWN_DURATION = 10  # Sets cooldown to 10 seconds
```

---

## 🤝 Customizing the Sponsor Button

The sponsor button links to a URL. To update this URL:

1. Open the `bot.py` file.
2. Modify the `url` parameter in the `empty_key` variable.

Example:
```python
empty_key = [[InlineKeyboardButton("Sponsor", url="https://your-sponsor-url.com")]]
```

---

## 📂 File Overview
- **`bot.py`**: Main script for the bot.
- **`logs.log`**: Log file for errors and warnings (auto-generated).
- **`req.txt`**: Contains the required Python dependencies.

---

## 📜 License

This project is licensed under the [GPL-3.0 License](https://opensource.org/license/gpl-3-0).

---
