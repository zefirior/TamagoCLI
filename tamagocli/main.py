"""Main entry point for Tamagochi game."""

import sys
import os
import termios
import tty
import curses
from typing import Optional

from .models.pet import Pet, PetType, PetState
from .display.renderer import GameRenderer
from .display.sprites import get_sprite
from .game.engine import GameEngine
from .game.save_manager import SaveManager
from .utils.curses_menu import interactive_menu_curses, yes_no_menu_curses


def setup_terminal():
    """Setup terminal for character-by-character input."""
    if sys.platform != 'win32':
        # Save old settings
        old_settings = termios.tcgetattr(sys.stdin)
        # Set terminal to cbreak mode (read chars without Enter)
        tty.setcbreak(sys.stdin.fileno())
        return old_settings
    return None


def restore_terminal(old_settings):
    """Restore terminal settings."""
    if old_settings is not None and sys.platform != 'win32':
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)


def select_pet(renderer: GameRenderer) -> Optional[PetType]:
    """Let user select a pet type with arrow keys using curses."""
    pet_types = list(PetType)
    
    # Prepare options and descriptions
    options = [pet_type.value.upper() for pet_type in pet_types]
    descriptions = [
        "🐱 Independent, efficient eater, less needy",
        "🐶 Loyal, needs lots of attention, always hungry",
        "🐉 Powerful, eats a lot, low energy drain",
        "🐰 Cute, efficient eater, moderate needs",
        "👽 Mysterious, minimal hunger, needs entertainment",
    ]
    
    # Preview function to show pet sprite
    def preview_func(index: int):
        sprite = get_sprite(pet_types[index], PetState.HAPPY, 0)
        return sprite
    
    # Show interactive menu with curses (no flickering!)
    def curses_wrapper_func(stdscr):
        return interactive_menu_curses(
            stdscr,
            title="Choose Your Pet",
            options=options,
            descriptions=descriptions,
            preview_func=preview_func
        )
    
    try:
        selected_index = curses.wrapper(curses_wrapper_func)
        if selected_index is None:
            return None
        return pet_types[selected_index]
    except Exception as e:
        renderer.render_message(f"Error: {e}", style="bold red")
        return None


def get_pet_name(renderer: GameRenderer) -> str:
    """Get pet name from user."""
    # Restore terminal for text input
    if sys.platform != 'win32':
        import termios
        import tty
        # Temporarily restore normal terminal mode for input
        try:
            old_settings = termios.tcgetattr(sys.stdin)
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
        except:
            pass
    
    renderer.clear()
    renderer.render_message("🎮 Name Your Pet! 🎮", style="bold magenta")
    
    while True:
        name = input("\nEnter pet name: ").strip()
        if name:
            return name
        print("Please enter a valid name!")


def main():
    """Main entry point."""
    renderer = GameRenderer()
    save_manager = SaveManager()
    old_terminal_settings = None
    
    try:
        # Check for existing save
        pet: Optional[Pet] = None
        
        if save_manager.has_save():
            # Ask if user wants to load save using curses
            def curses_yesno_wrapper(stdscr):
                return yes_no_menu_curses(stdscr, "Found existing save! Load it?")
            
            try:
                load_save = curses.wrapper(curses_yesno_wrapper)
            except:
                load_save = False
            
            if load_save:
                pet = save_manager.load()
                if pet:
                    renderer.clear()
                    renderer.render_message(
                        f"Loaded {pet.name} the {pet.pet_type.value}! 🎉",
                        style="bold green"
                    )
                    import time
                    time.sleep(1)
                else:
                    renderer.clear()
                    renderer.render_message(
                        "Failed to load save! Starting new game...",
                        style="bold red"
                    )
                    import time
                    time.sleep(1)
        
        # Create new pet if no save or load failed
        if pet is None:
            # Select pet type
            pet_type = select_pet(renderer)
            if pet_type is None:
                renderer.render_message("Goodbye! 👋", style="bold magenta")
                return
            
            # Get pet name
            name = get_pet_name(renderer)
            
            # Create pet
            pet = Pet(name=name, pet_type=pet_type)
            
            renderer.clear()
            renderer.render_message(
                f"Welcome, {name} the {pet_type.value}! 🎉\n\n"
                f"Take good care of your pet!\n"
                f"Remember to feed, play, and let them rest! 💕",
                style="bold green"
            )
            
            import time
            time.sleep(2)
        
        # Start game with curses
        def game_loop(stdscr):
            engine = GameEngine(pet, stdscr)
            engine.run()
        
        curses.wrapper(game_loop)
    
    except KeyboardInterrupt:
        renderer.clear()
        renderer.render_message("Game interrupted! Goodbye! 👋", style="bold yellow")
    
    except Exception as e:
        renderer.clear()
        renderer.render_message(f"Error: {e}", style="bold red")
        import traceback
        traceback.print_exc()
    
    finally:
        # Restore terminal
        restore_terminal(old_terminal_settings)


if __name__ == "__main__":
    main()

