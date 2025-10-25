"""Action menu for interactive controls."""

import curses


class ActionMenu:
    """Interactive action menu with arrow key navigation."""
    
    def __init__(self, stdscr):
        """Initialize action menu."""
        self.stdscr = stdscr
        self.actions = [
            ('F', 'Feed', 'Give food to your pet'),
            ('P', 'Play', 'Play with your pet'),
            ('S', 'Sleep', 'Put pet to sleep / Wake up'),
            ('H', 'Heal', 'Use medicine'),
            ('Q', 'Quit', 'Save and exit'),
        ]
        self.selected = 0
    
    def draw(self, x, y, width, selected_action=None):
        """Draw action menu at specified position."""
        # Use selected_action if provided, otherwise use self.selected
        current_selection = selected_action if selected_action is not None else self.selected
        
        menu_width = width - 4
        
        try:
            # Draw actions horizontally
            action_x = x
            for i, (key, name, _) in enumerate(self.actions):
                if i == current_selection:
                    # Highlight selected
                    text = f"[{key}]{name}"
                    self.stdscr.addstr(y, action_x, text, curses.A_REVERSE | curses.A_BOLD)
                else:
                    text = f"[{key}]{name}"
                    self.stdscr.addstr(y, action_x, text, curses.A_DIM)
                
                action_x += len(text) + 2
            
            # Draw description on next line
            _, desc = self.actions[current_selection][1], self.actions[current_selection][2]
            desc_x = x + (menu_width - len(desc)) // 2
            self.stdscr.addstr(y + 1, desc_x, desc, curses.A_ITALIC)
        except:
            pass
    
    def handle_key(self, key):
        """Handle arrow keys and return selected action or None."""
        if key == curses.KEY_LEFT:
            self.selected = (self.selected - 1) % len(self.actions)
            return None  # Just navigation
        elif key == curses.KEY_RIGHT:
            self.selected = (self.selected + 1) % len(self.actions)
            return None  # Just navigation
        elif key in (curses.KEY_ENTER, 10, 13):  # Enter
            return self.actions[self.selected][0].lower()  # Return action key
        return None

