"""Curses-based game renderer with no flickering."""

import curses
from typing import Optional
from ..models.pet import Pet, PetState
from .sprites import get_sprite


class CursesGameRenderer:
    """Renders the game using curses with double buffering."""
    
    def __init__(self, stdscr):
        """Initialize renderer with curses window."""
        self.stdscr = stdscr
        self.animation_frame = 0
        self.prev_pet_state = None
        self.prev_pet_position = None
        self.prev_stats = None
        self.prev_events = None
        self.first_draw = True
        
        # Setup curses
        curses.curs_set(0)
        curses.use_default_colors()
        
        # Color pairs
        curses.init_pair(1, curses.COLOR_WHITE, -1)    # Normal
        curses.init_pair(2, curses.COLOR_GREEN, -1)    # Happy/Health good
        curses.init_pair(3, curses.COLOR_YELLOW, -1)   # Hungry/Warning
        curses.init_pair(4, curses.COLOR_RED, -1)      # Sick/Critical
        curses.init_pair(5, curses.COLOR_CYAN, -1)     # Eating/Info
        curses.init_pair(6, curses.COLOR_BLUE, -1)     # Sleeping
        curses.init_pair(7, curses.COLOR_MAGENTA, -1)  # Sad/Title
        
        self.state_colors = {
            PetState.IDLE: 1,
            PetState.HAPPY: 2,
            PetState.HUNGRY: 3,
            PetState.EATING: 5,
            PetState.SLEEPING: 6,
            PetState.SAD: 7,
            PetState.SICK: 4,
            PetState.DEAD: 1,
        }
    
    def render_game(self, pet: Pet, events: list[str], selected_action=0):
        """Render the game screen - only update changed parts!"""
        self.animation_frame += 1
        height, width = self.stdscr.getmaxyx()
        
        # First draw - render everything
        if self.first_draw:
            self.stdscr.erase()
            self._draw_all_frames(width, height)
            self._draw_header(pet, width)
            self._draw_pet(pet, width, force=True)
            self._draw_stats(pet, width, force=True)
            self._draw_controls(width, selected_action)
            self._draw_events(events, width, height, force=True)
            self.stdscr.noutrefresh()
            curses.doupdate()
            
            self.prev_pet_state = pet.state
            self.prev_pet_position = pet.position
            self.prev_stats = (pet.stats.health, pet.stats.hunger, 
                             pet.stats.happiness, pet.stats.energy)
            self.prev_events = events.copy() if events else []
            self.prev_age = pet.stats.age
            self.prev_selected_action = selected_action
            self.first_draw = False
            return
        
        # Check what changed
        pet_changed = (pet.state != self.prev_pet_state or 
                      pet.position != self.prev_pet_position or
                      self.animation_frame % 10 == 0)  # Animation frame
        
        stats_changed = (pet.stats.health, pet.stats.hunger,
                        pet.stats.happiness, pet.stats.energy) != self.prev_stats
        
        events_changed = events != self.prev_events
        
        age_changed = pet.stats.age != self.prev_age
        
        action_changed = selected_action != self.prev_selected_action
        
        # Only redraw changed parts
        if age_changed:
            self._draw_header(pet, width)
            self.prev_age = pet.stats.age
        
        if pet_changed:
            self._draw_pet(pet, width)
            self.prev_pet_state = pet.state
            self.prev_pet_position = pet.position
        
        if stats_changed:
            self._draw_stats(pet, width)
            self.prev_stats = (pet.stats.health, pet.stats.hunger,
                             pet.stats.happiness, pet.stats.energy)
        
        if events_changed:
            self._draw_events(events, width, height)
            self.prev_events = events.copy() if events else []
        
        if action_changed:
            self._draw_controls(width, selected_action)
            self.prev_selected_action = selected_action
        
        # Double buffering - single update!
        if pet_changed or stats_changed or events_changed or age_changed or action_changed:
            self.stdscr.noutrefresh()
            curses.doupdate()
    
    def _draw_all_frames(self, width, height):
        """Draw all panel frames once."""
        # Main pet panel frame
        pet_y = 2
        pet_height = 12
        self._draw_box(1, pet_y, width - 2, pet_height, "")
        
        # Stats panel frame
        stats_y = pet_y + pet_height + 1
        stats_height = 7
        self._draw_box(1, stats_y, width - 2, stats_height, "📊 Stats")
        
        # Controls panel frame (taller for hint)
        controls_y = stats_y + stats_height + 1
        controls_height = 4
        self._draw_box(1, controls_y, width - 2, controls_height, "🎮 Controls")
        
        # Events panel frame
        events_y = controls_y + controls_height + 1
        events_height = 6
        if events_y + events_height < height - 1:
            self._draw_box(1, events_y, width - 2, events_height, "📜 Events")
    
    def _draw_box(self, x, y, width, height, title=""):
        """Draw a box with optional title."""
        screen_height, screen_width = self.stdscr.getmaxyx()
        
        # Top border
        if y < screen_height - 1:
            try:
                border = "┌" + "─" * (width - 2) + "┐"
                # Truncate if too wide
                if x + len(border) > screen_width:
                    border = border[:screen_width - x]
                self.stdscr.addstr(y, x, border)
            except:
                pass
        
        # Title if provided
        if title and y < screen_height - 1:
            try:
                title_x = x + 2
                self.stdscr.addstr(y, title_x, f" {title} ", curses.A_BOLD)
            except:
                pass
        
        # Sides
        for i in range(1, height):
            if y + i < screen_height - 1:
                try:
                    self.stdscr.addstr(y + i, x, "│")
                except:
                    pass
                try:
                    if x + width - 1 < screen_width:
                        self.stdscr.addstr(y + i, x + width - 1, "│")
                except:
                    pass
        
        # Bottom border
        if y + height < screen_height - 1:
            try:
                border = "└" + "─" * (width - 2) + "┘"
                # Truncate if too wide
                if x + len(border) > screen_width:
                    border = border[:screen_width - x]
                self.stdscr.addstr(y + height, x, border)
            except:
                pass
    
    def _draw_header(self, pet: Pet, width):
        """Draw header with pet name and age."""
        age_str = self._format_age(pet.stats.age)
        header = f"🎮 {pet.name} the {pet.pet_type.value.upper()} | Age: {age_str} | Lvl: {pet.stats.level}"
        x = max(0, (width - len(header)) // 2)
        try:
            self.stdscr.move(0, 0)
            self.stdscr.clrtoeol()
            self.stdscr.addstr(0, x, header, curses.color_pair(7) | curses.A_BOLD)
        except:
            pass
    
    def _format_age(self, seconds: int) -> str:
        """Format age in human readable format."""
        if seconds < 60:
            return f"{seconds}s"
        elif seconds < 3600:
            return f"{seconds // 60}m"
        else:
            hours = seconds // 3600
            minutes = (seconds % 3600) // 60
            return f"{hours}h {minutes}m"
    
    def _draw_pet(self, pet: Pet, width, force=False):
        """Draw pet sprite and state inside panel."""
        sprite = get_sprite(pet.pet_type, pet.state, self.animation_frame // 10)
        # Split lines but preserve leading/trailing spaces within lines
        # Filter out empty lines (including lines with only whitespace)
        sprite_lines = [line for line in sprite.split('\n') if line.strip()]
        
        # Position sprite inside pet panel
        pet_panel_y = 3  # Inside the pet panel frame
        panel_width = width - 4  # Account for borders
        
        # Calculate sprite width (maximum line length)
        max_line_width = max(len(line) for line in sprite_lines) if sprite_lines else 0
        
        # Calculate horizontal position based on pet.position (0-100)
        # Center the sprite block and then shift it based on position
        available_width = panel_width - max_line_width
        if available_width > 0:
            base_x = 3  # Start from left border
            offset = int(pet.position * available_width / 100)
            sprite_x = base_x + offset
        else:
            sprite_x = 3  # Just use margin if sprite too wide
        
        color = curses.color_pair(self.state_colors.get(pet.state, 1))
        
        # Clear pet area (inside panel)
        for i in range(10):
            y = pet_panel_y + i
            try:
                self.stdscr.move(y, 3)
                self.stdscr.addstr(" " * (width - 6))
            except:
                pass
        
        # Draw sprite - each line as-is, starting from sprite_x
        for i, line in enumerate(sprite_lines):
            y = pet_panel_y + i
            if y >= pet_panel_y + 8:
                break
            try:
                # Draw line exactly as it is, without modifying spacing
                self.stdscr.addstr(y, sprite_x, line, color)
            except:
                pass
        
        # State label below sprite
        state_text = f"State: {pet.state.value.upper()}"
        y = pet_panel_y + len(sprite_lines) + 1
        x = max(3, (width - len(state_text)) // 2)
        try:
            self.stdscr.addstr(y, x, state_text, color | curses.A_BOLD)
        except:
            pass
    
    def _draw_stats(self, pet: Pet, width, force=False):
        """Draw stats bars inside panel."""
        # Stats panel starts after pet panel
        stats_y = 16  # Inside stats panel frame
        
        stats = [
            ("❤️", " Health ", pet.stats.health, 4 if pet.stats.health < 30 else 2),
            ("🍖", "Hunger", pet.stats.hunger, 3 if pet.stats.hunger < 30 else 2),
            ("😊", "Happy", pet.stats.happiness, 3 if pet.stats.happiness < 30 else 2),
            ("⚡", "Energy", pet.stats.energy, 3 if pet.stats.energy < 30 else 5),
        ]
        
        for i, (icon, label, value, color) in enumerate(stats):
            y = stats_y + i
            
            # Draw stat bar
            bar_width = min(30, width - 25)
            filled = int(value * bar_width / 100)
            bar = "█" * filled + "░" * (bar_width - filled)
            
            # Format with proper alignment (extra space after emoji)
            text = f"{icon}  {label:<7} {bar} {value:3d}%"
            x = 4  # Inside panel
            
            try:
                # Clear line inside panel
                self.stdscr.move(y, 3)
                self.stdscr.addstr(" " * (width - 6))
                self.stdscr.addstr(y, x, text, curses.color_pair(color))
            except:
                pass
    
    def _draw_controls(self, width, selected_action=0):
        """Draw controls panel with selected action highlighted."""
        controls_y = 24  # Inside controls panel (line 1)
        hint_y = 25      # Second line for hint
        
        actions = [
            ('F', 'Feed'),
            ('P', 'Play'),
            ('S', 'Sleep'),
            ('H', 'Heal'),
            ('Q', 'Quit'),
        ]
        
        # Clear both lines
        try:
            self.stdscr.move(controls_y, 3)
            self.stdscr.addstr(" " * (width - 6))
            self.stdscr.move(hint_y, 3)
            self.stdscr.addstr(" " * (width - 6))
        except:
            pass
        
        # Draw actions on first line
        action_x = 4
        for i, (key, name) in enumerate(actions):
            text = f"[{key}]{name}"
            
            try:
                if i == selected_action:
                    # Highlight selected (reverse video)
                    self.stdscr.addstr(controls_y, action_x, text, curses.A_REVERSE | curses.A_BOLD)
                else:
                    # Normal
                    self.stdscr.addstr(controls_y, action_x, text, curses.A_BOLD)
                
                action_x += len(text) + 2
            except:
                pass
        
        # Draw hint on second line
        hint = "← → arrows to navigate, Enter to select, or press letter key"
        hint_x = max(4, (width - len(hint)) // 2)
        try:
            self.stdscr.addstr(hint_y, hint_x, hint, curses.A_DIM)
        except:
            pass
    
    def _draw_events(self, events: list[str], width, height, force=False):
        """Draw events log inside panel."""
        events_y = 31  # Inside events panel (moved down by 1)
        
        # Clear events area inside panel
        for i in range(3):
            y = events_y + i
            try:
                self.stdscr.move(y, 3)
                self.stdscr.addstr(" " * (width - 6))
            except:
                pass
        
        # Draw last 3 events
        recent_events = events[-3:] if events else []
        for i, event in enumerate(recent_events):
            y = events_y + i
            # Truncate if too long
            max_len = width - 10
            if len(event) > max_len:
                event = event[:max_len - 3] + "..."
            try:
                self.stdscr.addstr(y, 4, f"• {event}", curses.color_pair(1))
            except:
                pass
    
    def render_message(self, message: str):
        """Render a simple message."""
        height, width = self.stdscr.getmaxyx()
        self.stdscr.erase()
        
        lines = message.split('\n')
        start_y = max(0, (height - len(lines)) // 2)
        
        for i, line in enumerate(lines):
            y = start_y + i
            x = max(0, (width - len(line)) // 2)
            if y < height:
                try:
                    self.stdscr.addstr(y, x, line, curses.A_BOLD)
                except:
                    pass
        
        self.stdscr.noutrefresh()
        curses.doupdate()

