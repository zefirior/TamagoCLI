"""Main game engine with game loop."""

import time
import sys
import curses
from typing import Optional

from ..models.pet import Pet, PetState
from ..display.curses_renderer import CursesGameRenderer
from ..display.action_menu import ActionMenu
from .save_manager import SaveManager


class GameEngine:
    """Main game engine that runs the game loop."""
    
    def __init__(self, pet: Pet, stdscr=None):
        """Initialize game engine."""
        self.pet = pet
        self.stdscr = stdscr
        self.renderer = CursesGameRenderer(stdscr) if stdscr else None
        self.action_menu = ActionMenu(stdscr) if stdscr else None
        self.save_manager = SaveManager()
        self.running = False
        self.events: list[str] = []
        self.last_render = time.time()
        self.last_autosave = time.time()
        self.last_update = time.time()
        
    def run(self):
        """Run the main game loop with curses."""
        self.running = True
        
        # Configure curses for non-blocking input
        self.stdscr.nodelay(True)  # Non-blocking getch()
        self.stdscr.timeout(50)    # 50ms timeout
        
        self._add_event(f"Welcome back, {self.pet.name}! 🎮")
        
        try:
            while self.running and self.pet.is_alive:
                current_time = time.time()
                
                # Update pet state every second
                if current_time - self.last_update >= 1.0:
                    pet_events = self.pet.update()
                    for event in pet_events:
                        self._add_event(event)
                    self.last_update = current_time
                
                # Render (will only update changed parts)
                self.renderer.render_game(self.pet, self.events, self.action_menu.selected)
                
                # Autosave every 30 seconds
                if current_time - self.last_autosave >= 30:
                    self.save_manager.save(self.pet)
                    self.last_autosave = current_time
                
                # Check for input (non-blocking with curses)
                try:
                    key = self.stdscr.getch()
                    if key != -1:  # Key was pressed
                        # First try arrow keys and Enter with action menu
                        if key in (curses.KEY_LEFT, curses.KEY_RIGHT, curses.KEY_ENTER, 10, 13):
                            command = self.action_menu.handle_key(key)
                            if command:  # Enter pressed, execute action
                                self._handle_command(command)
                        # Then try letter commands
                        elif 0 <= key <= 255:
                            command = chr(key).lower()
                            self._handle_command(command)
                except:
                    pass
                
                # Small sleep
                time.sleep(0.05)
            
            # Game over
            if not self.pet.is_alive:
                self.renderer.render_message(
                    f"💀 {self.pet.name} has died... 💀\n\n"
                    f"Rest in peace... 🕊️"
                )
                time.sleep(3)
                self.save_manager.delete_save()
        
        except KeyboardInterrupt:
            self._add_event("Game interrupted!")
            self._save_and_quit()
    
    
    def _handle_command(self, command: str):
        """Handle user commands."""
        if command == 'f':
            result = self.pet.feed()
            self._add_event(result)
        
        elif command == 'p':
            result = self.pet.play()
            self._add_event(result)
        
        elif command == 's':
            if self.pet.state == PetState.SLEEPING:
                result = self.pet.wake_up()
            else:
                result = self.pet.sleep()
            self._add_event(result)
        
        elif command == 'h':
            result = self.pet.heal()
            self._add_event(result)
        
        elif command == 'q':
            self._save_and_quit()
    
    def _add_event(self, event: str):
        """Add an event to the log."""
        self.events.append(event)
        # Keep only last 10 events
        if len(self.events) > 10:
            self.events = self.events[-10:]
    
    def _save_and_quit(self):
        """Save game and quit."""
        self.renderer.render_message("Saving game...")
        time.sleep(0.5)
        
        if self.save_manager.save(self.pet):
            self.renderer.render_message(
                f"Game saved! See you soon, {self.pet.name}! 👋"
            )
        else:
            self.renderer.render_message("Failed to save game! 😢")
        
        time.sleep(1)
        self.running = False

