"""Game renderer using Rich library."""

from typing import Optional
from rich.console import Console
from rich.panel import Panel
from rich.layout import Layout
from rich.text import Text
from rich.progress import BarColumn, Progress, TextColumn
from rich.table import Table
from rich.align import Align

from ..models.pet import Pet, PetState
from .sprites import get_sprite


class GameRenderer:
    """Renders the game interface."""
    
    def __init__(self):
        """Initialize the renderer."""
        self.console = Console()
        self.animation_frame = 0
        
        # Color schemes for different states
        self.state_colors = {
            PetState.IDLE: "white",
            PetState.HAPPY: "green",
            PetState.HUNGRY: "yellow",
            PetState.EATING: "cyan",
            PetState.SLEEPING: "blue",
            PetState.SAD: "magenta",
            PetState.SICK: "red",
            PetState.DEAD: "bright_black",
        }
    
    def clear(self):
        """Clear the console."""
        self.console.clear()
    
    def render_game(self, pet: Pet, events: list[str]):
        """Render the main game screen."""
        self.animation_frame += 1
        
        # Create main layout
        layout = Layout()
        layout.split_column(
            Layout(name="header", size=3),
            Layout(name="main"),
            Layout(name="stats", size=8),
            Layout(name="controls", size=8),
            Layout(name="events", size=6),
        )
        
        # Header
        header_text = Text(f"🎮 TAMAGOCLI - {pet.name} the {pet.pet_type.value.upper()} 🎮", 
                          style="bold magenta")
        layout["header"].update(Panel(Align.center(header_text), style="bold"))
        
        # Main pet display
        sprite = get_sprite(pet.pet_type, pet.state, self.animation_frame // 10)
        
        # Add padding based on position
        sprite_lines = sprite.strip().split("\n")
        max_width = 80
        padding = int(pet.position * max_width / 100)
        padded_sprite = "\n".join(" " * padding + line for line in sprite_lines)
        
        state_color = self.state_colors.get(pet.state, "white")
        sprite_text = Text(padded_sprite, style=state_color)
        
        state_label = Text(f"\n\n{pet.state.value.upper()}", 
                          style=f"bold {state_color}")
        
        layout["main"].update(Panel(sprite_text + state_label, 
                                   title=f"Age: {self._format_age(pet.stats.age)} | Level: {pet.stats.level}",
                                   border_style=state_color))
        
        # Stats display
        stats_table = self._create_stats_display(pet)
        layout["stats"].update(Panel(stats_table, title="📊 Stats", border_style="cyan"))
        
        # Controls
        controls_text = self._create_controls_text(pet)
        layout["controls"].update(Panel(controls_text, title="🎮 Controls", border_style="yellow"))
        
        # Events log
        events_text = self._create_events_text(events)
        layout["events"].update(Panel(events_text, title="📜 Events", border_style="blue"))
        
        self.console.print(layout)
    
    def _create_stats_display(self, pet: Pet) -> Table:
        """Create stats display with progress bars."""
        table = Table(show_header=False, box=None, padding=(0, 1))
        table.add_column("Icon", width=3)
        table.add_column("Stat", width=12)
        table.add_column("Bar", ratio=1)
        
        stats_data = [
            ("♥", "Health", pet.stats.health, "red"),
            ("🍖", "Hunger", pet.stats.hunger, "green"),
            ("😊", "Happiness", pet.stats.happiness, "yellow"),
            ("⚡", "Energy", pet.stats.energy, "cyan"),
        ]
        
        for icon, name, value, color in stats_data:
            bar = self._create_bar(value, color)
            table.add_row(icon, f"{name}:", bar)
        
        return table
    
    def _create_bar(self, value: int, color: str) -> Text:
        """Create a text-based progress bar."""
        bar_width = 30
        filled = int(value * bar_width / 100)
        empty = bar_width - filled
        
        # Color based on value
        if value >= 70:
            bar_color = color
        elif value >= 40:
            bar_color = "yellow"
        else:
            bar_color = "red"
        
        bar_text = Text()
        bar_text.append("█" * filled, style=f"bold {bar_color}")
        bar_text.append("░" * empty, style="dim")
        bar_text.append(f" {value:3d}%", style="bold")
        
        return bar_text
    
    def _create_controls_text(self, pet: Pet) -> Text:
        """Create controls display."""
        text = Text()
        
        controls = [
            ("F", "Feed", "green"),
            ("P", "Play", "yellow"),
            ("S", "Sleep/Wake", "blue"),
            ("H", "Heal", "red"),
            ("Q", "Save & Quit", "magenta"),
        ]
        
        for key, action, color in controls:
            text.append(f"[{key}]", style=f"bold {color}")
            text.append(f" {action}  ", style="white")
        
        return text
    
    def _create_events_text(self, events: list[str]) -> Text:
        """Create events log display."""
        text = Text()
        
        if not events:
            text.append("No recent events...", style="dim")
        else:
            # Show last 3 events
            for event in events[-3:]:
                text.append(f"• {event}\n", style="white")
        
        return text
    
    def _format_age(self, seconds: int) -> str:
        """Format age in human readable format."""
        if seconds < 60:
            return f"{seconds}s"
        elif seconds < 3600:
            return f"{seconds // 60}m {seconds % 60}s"
        else:
            hours = seconds // 3600
            minutes = (seconds % 3600) // 60
            return f"{hours}h {minutes}m"
    
    def render_pet_selection(self, pet_types: list) -> Panel:
        """Render pet selection screen."""
        from ..models.pet import PetType
        
        text = Text()
        text.append("🌟 Choose Your Pet! 🌟\n\n", style="bold magenta")
        
        for i, pet_type in enumerate(pet_types, 1):
            preview = get_sprite(pet_type, PetState.HAPPY, 0)
            
            text.append(f"\n[{i}] {pet_type.value.upper()}\n", style=f"bold cyan")
            text.append(preview + "\n", style="green")
            
            # Add traits description
            traits = self._get_pet_description(pet_type)
            text.append(f"  {traits}\n", style="dim")
        
        text.append("\n\nPress 1-5 to select or Q to quit", style="bold yellow")
        
        return Panel(Align.center(text), title="🎮 TAMAGOCLI", border_style="magenta")
    
    def _get_pet_description(self, pet_type) -> str:
        """Get description for pet type."""
        from ..models.pet import PetType
        
        descriptions = {
            PetType.CAT: "🐱 Independent, efficient eater, less needy",
            PetType.DOG: "🐶 Loyal, needs lots of attention, always hungry",
            PetType.DRAGON: "🐉 Powerful, eats a lot, low energy drain",
            PetType.BUNNY: "🐰 Cute, efficient eater, moderate needs",
            PetType.ALIEN: "👽 Mysterious, minimal hunger, needs entertainment",
        }
        return descriptions.get(pet_type, "Unknown creature")
    
    def render_message(self, message: str, style: str = "bold green"):
        """Render a simple message."""
        self.console.print(Panel(Align.center(Text(message, style=style))))
    
    def prompt_input(self, prompt: str) -> str:
        """Prompt user for input."""
        self.console.print(f"\n{prompt}", style="bold yellow", end="")
        return input(" ").strip().lower()

