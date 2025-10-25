"""Interactive menu with arrow key navigation."""

import readchar
from typing import List, Optional, Callable
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.align import Align
from rich.columns import Columns
from rich.layout import Layout
from rich.live import Live


def interactive_menu(
    title: str,
    options: List[str],
    descriptions: Optional[List[str]] = None,
    preview_func: Optional[Callable[[int], str]] = None,
    console: Optional[Console] = None
) -> Optional[int]:
    """
    Display an interactive menu with arrow key navigation.
    
    Args:
        title: Menu title
        options: List of option names
        descriptions: Optional list of descriptions for each option
        preview_func: Optional function that returns preview text for an option index
        console: Rich console instance
    
    Returns:
        Selected option index (0-based) or None if cancelled
    """
    if console is None:
        console = Console()
    
    selected = 0
    
    while True:
        console.clear()
        
        # Build menu text
        text = Text()
        text.append(f"{title}\n\n", style="bold magenta")
        
        for i, option in enumerate(options):
            if i == selected:
                # Highlighted option
                text.append("❯ ", style="bold cyan")
                text.append(f"{option}", style="bold cyan")
                text.append("\n")
                
                # Show preview if available
                if preview_func:
                    preview = preview_func(i)
                    text.append(preview, style="green")
                    text.append("\n")
                
                # Show description if available
                if descriptions and i < len(descriptions):
                    text.append(f"  {descriptions[i]}\n", style="bold yellow")
                
                text.append("\n")
            else:
                # Normal option
                text.append("  ", style="dim")
                text.append(f"{option}", style="white")
                text.append("\n")
                
                # Show description if available
                if descriptions and i < len(descriptions):
                    text.append(f"  {descriptions[i]}\n", style="dim")
                
                text.append("\n")
        
        text.append("\n")
        text.append("↑↓ Navigate  ", style="bold white")
        text.append("Enter", style="bold green")
        text.append(" Select  ", style="bold white")
        text.append("Q", style="bold red")
        text.append(" Quit", style="bold white")
        
        panel = Panel(
            Align.center(text),
            title=f"🎮 {title.upper()} 🎮",
            border_style="magenta"
        )
        console.print(panel)
        
        # Get key input
        try:
            key = readchar.readkey()
            
            if key == readchar.key.UP:
                selected = (selected - 1) % len(options)
            elif key == readchar.key.DOWN:
                selected = (selected + 1) % len(options)
            elif key == readchar.key.ENTER or key == '\r' or key == '\n':
                return selected
            elif key.lower() == 'q':
                return None
                
        except KeyboardInterrupt:
            return None


def yes_no_menu(question: str, console: Optional[Console] = None) -> bool:
    """
    Display a yes/no menu with arrow key navigation.
    Uses Live rendering to avoid flickering.
    
    Args:
        question: Question to ask
        console: Rich console instance
    
    Returns:
        True for yes, False for no
    """
    if console is None:
        console = Console()
    
    selected = 0
    options = ["Yes", "No"]
    
    def generate_menu():
        """Generate the yes/no menu content."""
        text = Text()
        text.append(f"{question}\n\n", style="bold yellow")
        
        for i, option in enumerate(options):
            if i == selected:
                text.append("❯ ", style="bold cyan")
                text.append(f"{option}", style="bold cyan")
            else:
                text.append("  ", style="dim")
                text.append(f"{option}", style="white")
            text.append("\n")
        
        text.append("\n")
        text.append("↑↓ Navigate  ", style="bold white")
        text.append("Enter", style="bold green")
        text.append(" Select", style="bold white")
        
        return Panel(Align.center(text), border_style="yellow")
    
    # Use Live to avoid flickering (low refresh rate for stability)
    with Live(generate_menu(), console=console, refresh_per_second=4, screen=True) as live:
        try:
            import time
            while True:
                key = readchar.readkey()
                
                if key == readchar.key.UP or key == readchar.key.DOWN:
                    selected = 1 - selected  # Toggle between 0 and 1
                    live.update(generate_menu(), refresh=True)
                    time.sleep(0.05)  # Small delay to reduce flickering
                elif key == readchar.key.ENTER or key == '\r' or key == '\n':
                    return selected == 0  # True if "Yes" selected
                    
        except KeyboardInterrupt:
            return False


def interactive_menu_with_preview(
    title: str,
    options: List[str],
    descriptions: Optional[List[str]] = None,
    preview_func: Optional[Callable[[int], str]] = None,
    console: Optional[Console] = None
) -> Optional[int]:
    """
    Display an interactive menu with fixed-size preview panel on the right.
    Uses Live rendering to avoid flickering.
    
    Args:
        title: Menu title
        options: List of option names
        descriptions: Optional list of descriptions for each option
        preview_func: Optional function that returns preview text for an option index
        console: Rich console instance
    
    Returns:
        Selected option index (0-based) or None if cancelled
    """
    if console is None:
        console = Console()
    
    selected = 0
    
    def generate_menu():
        """Generate the menu content."""
        # Left panel: Menu options
        menu_text = Text()
        menu_text.append(f"{title}\n\n", style="bold magenta")
        
        for i, option in enumerate(options):
            if i == selected:
                # Highlighted option
                menu_text.append("❯ ", style="bold cyan")
                menu_text.append(f"{option}", style="bold cyan")
                menu_text.append("\n")
                
                # Show description if available
                if descriptions and i < len(descriptions):
                    menu_text.append(f"  {descriptions[i]}\n", style="bold yellow")
            else:
                # Normal option
                menu_text.append("  ", style="dim")
                menu_text.append(f"{option}", style="white")
                menu_text.append("\n")
                
                # Show description if available
                if descriptions and i < len(descriptions):
                    menu_text.append(f"  {descriptions[i]}\n", style="dim")
        
        menu_text.append("\n")
        menu_text.append("↑↓ Navigate  ", style="bold white")
        menu_text.append("Enter", style="bold green")
        menu_text.append(" Select  ", style="bold white")
        menu_text.append("Q", style="bold red")
        menu_text.append(" Quit", style="bold white")
        
        menu_panel = Panel(
            menu_text,
            title="Options",
            border_style="cyan",
            width=45
        )
        
        # Right panel: Preview
        preview_text = Text()
        if preview_func:
            preview = preview_func(selected)
            preview_text.append(preview, style="green")
        else:
            preview_text.append("No preview available", style="dim")
        
        preview_panel = Panel(
            Align.center(preview_text, vertical="middle"),
            title=f"Preview: {options[selected]}",
            border_style="green",
            width=45,
            height=20
        )
        
        # Combine panels side by side
        columns = Columns([menu_panel, preview_panel], equal=False, expand=False)
        
        # Main container
        main_panel = Panel(
            columns,
            title=f"🎮 {title.upper()} 🎮",
            border_style="magenta"
        )
        
        return main_panel
    
    # Use Live to avoid flickering (low refresh rate for stability)
    with Live(generate_menu(), console=console, refresh_per_second=4, screen=True) as live:
        try:
            import time
            while True:
                # Get key input
                key = readchar.readkey()
                
                if key == readchar.key.UP:
                    selected = (selected - 1) % len(options)
                    live.update(generate_menu(), refresh=True)
                    time.sleep(0.05)  # Small delay to reduce flickering
                elif key == readchar.key.DOWN:
                    selected = (selected + 1) % len(options)
                    live.update(generate_menu(), refresh=True)
                    time.sleep(0.05)  # Small delay to reduce flickering
                elif key == readchar.key.ENTER or key == '\r' or key == '\n':
                    return selected
                elif key.lower() == 'q':
                    return None
                    
        except KeyboardInterrupt:
            return None

