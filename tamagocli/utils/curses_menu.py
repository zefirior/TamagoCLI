"""Curses-based menu without flickering using double buffering."""

import curses
from typing import List, Optional, Callable


def interactive_menu_curses(
    stdscr,
    title: str,
    options: List[str],
    descriptions: Optional[List[str]] = None,
    preview_func: Optional[Callable[[int], str]] = None
) -> Optional[int]:
    """
    Display interactive menu using curses with no flickering.
    Uses noutrefresh() / doupdate() for double buffering.
    Only redraws changed elements!
    
    Args:
        stdscr: Curses window
        title: Menu title
        options: List of option names
        descriptions: Optional descriptions
        preview_func: Function returning preview text for option
    
    Returns:
        Selected index or None if cancelled
    """
    # Setup
    curses.curs_set(0)  # Hide cursor
    curses.use_default_colors()
    
    # Initialize color pairs
    curses.init_pair(1, curses.COLOR_CYAN, -1)      # Selected
    curses.init_pair(2, curses.COLOR_YELLOW, -1)    # Description
    curses.init_pair(3, curses.COLOR_MAGENTA, -1)   # Title
    curses.init_pair(4, curses.COLOR_GREEN, -1)     # Preview
    curses.init_pair(5, curses.COLOR_WHITE, -1)     # Normal
    
    selected = 0
    prev_selected = -1  # Track previous selection
    first_draw = True   # Flag for first draw
    
    # Calculate layout once
    height, width = stdscr.getmaxyx()
    menu_width = 45
    preview_width = 45
    total_width = menu_width + preview_width + 4
    start_x = max(0, (width - total_width) // 2)
    start_y = 2
    left_x = start_x
    panel_y = start_y + 2
    preview_x = left_x + menu_width + 2
    preview_y = panel_y
    
    # Draw static elements ONCE
    if first_draw:
        stdscr.erase()
        
        # Draw title
        title_text = f"🎮 {title.upper()} 🎮"
        title_x = max(0, (width - len(title_text)) // 2)
        stdscr.addstr(start_y, title_x, title_text, 
                     curses.color_pair(3) | curses.A_BOLD)
        
        # Draw left panel borders (static)
        stdscr.addstr(panel_y, left_x, "┌" + "─" * (menu_width - 2) + "┐")
        stdscr.addstr(panel_y + 1, left_x, "│ Options".ljust(menu_width - 1) + "│", 
                     curses.A_BOLD)
        stdscr.addstr(panel_y + 2, left_x, "├" + "─" * (menu_width - 2) + "┤")
        
        # Draw right panel borders (static)
        stdscr.addstr(preview_y, preview_x, "┌" + "─" * (preview_width - 2) + "┐")
        stdscr.addstr(preview_y + 2, preview_x, "├" + "─" * (preview_width - 2) + "┤")
        stdscr.addstr(preview_y + 3 + 17, preview_x, 
                     "└" + "─" * (preview_width - 2) + "┘")
        
        # Draw ALL menu options initially
        line_y = panel_y + 3
        for i, option in enumerate(options):
            if line_y >= height - 5:
                break
            
            # Option line
            if i == selected:
                prefix = "❯ "
                attr = curses.color_pair(1) | curses.A_BOLD
            else:
                prefix = "  "
                attr = curses.color_pair(5)
            
            text = f"{prefix}{option}"
            if len(text) > menu_width - 4:
                text = text[:menu_width - 7] + "..."
            
            stdscr.addstr(line_y, left_x, "│ ")
            stdscr.addstr(text.ljust(menu_width - 4), attr)
            stdscr.addstr(" │")
            line_y += 1
            
            # Description
            if descriptions and i < len(descriptions):
                desc = descriptions[i]
                if len(desc) > menu_width - 6:
                    desc = desc[:menu_width - 9] + "..."
                
                desc_attr = curses.color_pair(2) if i == selected else curses.A_DIM
                stdscr.addstr(line_y, left_x, "│ ")
                stdscr.addstr(f"  {desc}".ljust(menu_width - 4), desc_attr)
                stdscr.addstr(" │")
                line_y += 1
        
        # Fill remaining lines
        while line_y < panel_y + 20:
            stdscr.addstr(line_y, left_x, "│" + " " * (menu_width - 2) + "│")
            line_y += 1
        
        # Draw preview title
        preview_title = f"Preview: {options[selected]}"
        if len(preview_title) > preview_width - 4:
            preview_title = preview_title[:preview_width - 7] + "..."
        stdscr.addstr(preview_y + 1, preview_x, 
                     f"│ {preview_title}".ljust(preview_width - 1) + "│",
                     curses.A_BOLD)
        
        # Draw initial preview
        preview_start_y = preview_y + 3
        if preview_func:
            preview_text = preview_func(selected)
            preview_lines = preview_text.split('\n')
            
            content_height = len(preview_lines)
            available_height = 17
            offset = max(0, (available_height - content_height) // 2)
            
            for i in range(available_height):
                y = preview_start_y + i
                stdscr.addstr(y, preview_x, "│")
                
                if i >= offset and i - offset < len(preview_lines):
                    line = preview_lines[i - offset]
                    line_len = len(line)
                    x_offset = max(0, (preview_width - 4 - line_len) // 2)
                    content = " " * x_offset + line
                    if len(content) > preview_width - 4:
                        content = content[:preview_width - 4]
                    stdscr.addstr(content.ljust(preview_width - 2), 
                                curses.color_pair(4))
                else:
                    stdscr.addstr(" " * (preview_width - 2))
                
                stdscr.addstr("│")
        
        # Draw bottom of left panel (static)
        line_y = panel_y + 20
        stdscr.addstr(line_y, left_x, "├" + "─" * (menu_width - 2) + "┤")
        line_y += 1
        stdscr.addstr(line_y, left_x, "│ ↑↓ Navigate  Enter Select  Q Quit".ljust(menu_width - 1) + "│")
        line_y += 1
        stdscr.addstr(line_y, left_x, "└" + "─" * (menu_width - 2) + "┘")
        
        # Initial refresh
        stdscr.noutrefresh()
        curses.doupdate()
        
        first_draw = False
    
    while True:
        # Only redraw if selection changed
        if selected != prev_selected:
            # Redraw menu options (only changed lines!)
            line_y = panel_y + 3
            
            for i, option in enumerate(options):
                if line_y >= height - 5:
                    break
                
                # Only redraw lines that changed (prev or current selection)
                if i == selected or i == prev_selected:
                    # Option line
                    if i == selected:
                        prefix = "❯ "
                        attr = curses.color_pair(1) | curses.A_BOLD
                    else:
                        prefix = "  "
                        attr = curses.color_pair(5)
                    
                    text = f"{prefix}{option}"
                    if len(text) > menu_width - 4:
                        text = text[:menu_width - 7] + "..."
                    
                    stdscr.addstr(line_y, left_x, "│ ")
                    stdscr.addstr(text.ljust(menu_width - 4), attr)
                    stdscr.addstr(" │")
                line_y += 1
                
                # Description
                if descriptions and i < len(descriptions):
                    if i == selected or i == prev_selected:
                        desc = descriptions[i]
                        if len(desc) > menu_width - 6:
                            desc = desc[:menu_width - 9] + "..."
                        
                        desc_attr = curses.color_pair(2) if i == selected else curses.A_DIM
                        stdscr.addstr(line_y, left_x, "│ ")
                        stdscr.addstr(f"  {desc}".ljust(menu_width - 4), desc_attr)
                        stdscr.addstr(" │")
                    line_y += 1
            
            # Redraw preview title (changed)
            preview_title = f"Preview: {options[selected]}"
            if len(preview_title) > preview_width - 4:
                preview_title = preview_title[:preview_width - 7] + "..."
            stdscr.move(preview_y + 1, preview_x)
            stdscr.addstr(f"│ {preview_title}".ljust(preview_width - 1) + "│",
                         curses.A_BOLD)
            
            # Redraw preview content (changed)
            preview_start_y = preview_y + 3
            if preview_func:
                preview_text = preview_func(selected)
                preview_lines = preview_text.split('\n')
                
                # Center vertically
                content_height = len(preview_lines)
                available_height = 17
                offset = max(0, (available_height - content_height) // 2)
                
                for i in range(available_height):
                    y = preview_start_y + i
                    stdscr.move(y, preview_x)
                    stdscr.addstr("│")
                    
                    if i >= offset and i - offset < len(preview_lines):
                        line = preview_lines[i - offset]
                        # Center horizontally
                        line_len = len(line)
                        x_offset = max(0, (preview_width - 4 - line_len) // 2)
                        content = " " * x_offset + line
                        if len(content) > preview_width - 4:
                            content = content[:preview_width - 4]
                        stdscr.addstr(content.ljust(preview_width - 2), 
                                    curses.color_pair(4))
                    else:
                        stdscr.addstr(" " * (preview_width - 2))
                    
                    stdscr.addstr("│")
            
            prev_selected = selected
        
        # Double buffering: mark for refresh but don't update yet
        stdscr.noutrefresh()
        
        # Now do single screen update - no flicker!
        curses.doupdate()
        
        # Get input
        try:
            key = stdscr.getch()
            
            if key == curses.KEY_UP:
                selected = (selected - 1) % len(options)
            elif key == curses.KEY_DOWN:
                selected = (selected + 1) % len(options)
            elif key in [curses.KEY_ENTER, ord('\n'), ord('\r'), 10, 13]:
                return selected
            elif key in [ord('q'), ord('Q')]:
                return None
                
        except KeyboardInterrupt:
            return None


def yes_no_menu_curses(stdscr, question: str) -> bool:
    """
    Display yes/no menu using curses with no flickering.
    
    Args:
        stdscr: Curses window
        question: Question to ask
    
    Returns:
        True for Yes, False for No
    """
    curses.curs_set(0)
    curses.use_default_colors()
    
    curses.init_pair(1, curses.COLOR_CYAN, -1)
    curses.init_pair(2, curses.COLOR_YELLOW, -1)
    
    selected = 0
    options = ["Yes", "No"]
    
    while True:
        height, width = stdscr.getmaxyx()
        
        stdscr.erase()
        
        # Calculate position
        box_width = 50
        box_height = 8
        start_x = max(0, (width - box_width) // 2)
        start_y = max(0, (height - box_height) // 2)
        
        # Draw box
        stdscr.addstr(start_y, start_x, "┌" + "─" * (box_width - 2) + "┐")
        
        # Question
        question_y = start_y + 2
        q_x = max(start_x + 2, start_x + (box_width - len(question)) // 2)
        stdscr.addstr(question_y, start_x, "│" + " " * (box_width - 2) + "│")
        stdscr.addstr(question_y, q_x, question, 
                     curses.color_pair(2) | curses.A_BOLD)
        
        stdscr.addstr(start_y + 3, start_x, "│" + " " * (box_width - 2) + "│")
        
        # Options
        for i, option in enumerate(options):
            opt_y = start_y + 4 + i
            stdscr.addstr(opt_y, start_x, "│ ")
            
            if i == selected:
                text = f"❯ {option}"
                attr = curses.color_pair(1) | curses.A_BOLD
            else:
                text = f"  {option}"
                attr = curses.A_NORMAL
            
            stdscr.addstr(text.ljust(box_width - 4), attr)
            stdscr.addstr(" │")
        
        stdscr.addstr(start_y + 6, start_x, "│" + " " * (box_width - 2) + "│")
        
        # Instructions
        instr = "↑↓ Navigate  Enter Select"
        instr_x = start_x + (box_width - len(instr)) // 2
        stdscr.addstr(start_y + 7, start_x, "│" + " " * (box_width - 2) + "│")
        stdscr.addstr(start_y + 7, instr_x, instr)
        
        stdscr.addstr(start_y + box_height - 1, start_x, 
                     "└" + "─" * (box_width - 2) + "┘")
        
        # Double buffering
        stdscr.noutrefresh()
        curses.doupdate()
        
        try:
            key = stdscr.getch()
            
            if key in [curses.KEY_UP, curses.KEY_DOWN]:
                selected = 1 - selected
            elif key in [curses.KEY_ENTER, ord('\n'), ord('\r'), 10, 13]:
                return selected == 0
                
        except KeyboardInterrupt:
            return False

