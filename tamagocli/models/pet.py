"""Pet model with different types and states."""

from enum import Enum
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Optional
import random


BOUNCE_LEFT_EDGE = 10
BOUNCE_RIGHT_EDGE = 90


class PetType(Enum):
    """Different types of pets available."""
    CAT = "cat"
    DOG = "dog"
    DRAGON = "dragon"
    BUNNY = "bunny"
    ALIEN = "alien"


class PetState(Enum):
    """Different states/moods of the pet."""
    IDLE = "idle"
    HAPPY = "happy"
    HUNGRY = "hungry"
    EATING = "eating"
    SLEEPING = "sleeping"
    SAD = "sad"
    SICK = "sick"
    DEAD = "dead"


@dataclass
class PetStats:
    """Pet statistics."""
    hunger: int = 100  # 0-100, higher is better
    happiness: int = 100  # 0-100
    energy: int = 100  # 0-100
    health: int = 100  # 0-100
    age: int = 0  # in seconds
    level: int = 1
    
    def __post_init__(self):
        """Ensure stats are within bounds."""
        self.hunger = max(0, min(100, self.hunger))
        self.happiness = max(0, min(100, self.happiness))
        self.energy = max(0, min(100, self.energy))
        self.health = max(0, min(100, self.health))


@dataclass
class Pet:
    """Main pet class with all game logic."""
    name: str
    pet_type: PetType
    stats: PetStats = field(default_factory=PetStats)
    state: PetState = PetState.IDLE
    position: int = 50  # 0-100, position on screen
    direction: int = 1  # -1 left, 1 right
    created_at: datetime = field(default_factory=datetime.now)
    last_update: datetime = field(default_factory=datetime.now)
    eating_started_at: Optional[datetime] = None  # Track when eating started
    accumulated_damage: float = 0.0  # Accumulated health damage for smooth decay
    # Accumulated stat changes for smooth updates
    accumulated_hunger_decay: float = 0.0
    accumulated_happiness_decay: float = 0.0
    accumulated_energy_decay: float = 0.0
    
    # Type-specific multipliers
    _type_traits: dict = field(default_factory=dict, init=False)
    
    def __post_init__(self):
        """Initialize type-specific traits."""
        self._type_traits = {
            PetType.CAT: {
                "hunger_decay": 1.0,
                "happiness_decay": 0.8,
                "energy_decay": 0.7,
                "food_efficiency": 1.2,
            },
            PetType.DOG: {
                "hunger_decay": 1.2,
                "happiness_decay": 1.5,
                "energy_decay": 1.0,
                "food_efficiency": 1.0,
            },
            PetType.DRAGON: {
                "hunger_decay": 1.5,
                "happiness_decay": 0.9,
                "energy_decay": 0.8,
                "food_efficiency": 0.8,
            },
            PetType.BUNNY: {
                "hunger_decay": 0.8,
                "happiness_decay": 1.0,
                "energy_decay": 0.9,
                "food_efficiency": 1.5,
            },
            PetType.ALIEN: {
                "hunger_decay": 0.5,
                "happiness_decay": 1.2,
                "energy_decay": 0.6,
                "food_efficiency": 2.0,
            },
        }
    
    @property
    def traits(self) -> dict:
        """Get traits for current pet type."""
        return self._type_traits.get(self.pet_type, {})
    
    @property
    def is_alive(self) -> bool:
        """Check if pet is alive."""
        return self.stats.health > 0
    
    def update(self) -> list[str]:
        """Update pet state based on time passed. Returns list of events."""
        if not self.is_alive:
            self.state = PetState.DEAD
            return []
        
        now = datetime.now()
        time_delta = (now - self.last_update).total_seconds()
        self.last_update = now
        
        # Update age
        self.stats.age = int((now - self.created_at).total_seconds())
        
        events = []
        
        # Check if eating should finish (after 3 seconds)
        if self.state == PetState.EATING:
            if self.eating_started_at:
                eating_duration = (now - self.eating_started_at).total_seconds()
                if eating_duration >= 3.0:
                    self.state = PetState.IDLE
                    self.eating_started_at = None
                    events.append(f"{self.name} finished eating!")
            else:
                # Safety: if eating but no timestamp (old save), finish immediately
                self.state = PetState.IDLE
                events.append(f"{self.name} finished eating!")
        
        # Decay stats over time - accumulate fractional changes
        decay_rate = time_delta / 10.0  # Base decay per 10 seconds
        
        # Accumulate decay (per second rates: hunger=5, happiness=3, energy=2)
        self.accumulated_hunger_decay += decay_rate * 50 * self.traits.get("hunger_decay", 1.0)
        self.accumulated_happiness_decay += decay_rate * 30 * self.traits.get("happiness_decay", 1.0)
        # Energy doesn't decay while sleeping
        if self.state != PetState.SLEEPING:
            self.accumulated_energy_decay += decay_rate * 20 * self.traits.get("energy_decay", 1.0)
        
        # Apply accumulated decay when it reaches 1 or more
        if self.accumulated_hunger_decay >= 1.0:
            decay = int(self.accumulated_hunger_decay)
            self.stats.hunger -= decay
            self.accumulated_hunger_decay -= decay
        
        if self.accumulated_happiness_decay >= 1.0:
            decay = int(self.accumulated_happiness_decay)
            self.stats.happiness -= decay
            self.accumulated_happiness_decay -= decay
        
        if self.accumulated_energy_decay >= 1.0:
            decay = int(self.accumulated_energy_decay)
            self.stats.energy -= decay
            self.accumulated_energy_decay -= decay
        
        # Health consequences (accumulate damage for smooth decay)
        if self.stats.hunger <= 0:
            self.accumulated_damage += decay_rate * 30  # 3 damage per second
            if self.stats.hunger == 0:  # Only show message once
                events.append(f"{self.name} is starving!")
            
        if self.stats.happiness <= 20:
            self.accumulated_damage += decay_rate * 10  # 1 damage per second
            
        if self.stats.energy <= 0:
            self.accumulated_damage += decay_rate * 20  # 2 damage per second
            if self.stats.energy == 0:  # Only show message once
                events.append(f"{self.name} is exhausted!")
        
        # Apply accumulated damage when it reaches 1 or more
        if self.accumulated_damage >= 1.0:
            damage = int(self.accumulated_damage)
            self.stats.health -= damage
            self.accumulated_damage -= damage  # Keep fractional part
            if damage > 0 and not any("starving" in e or "exhausted" in e for e in events):
                events.append(f"{self.name} is suffering! (-{damage} HP)")
        
        # Energy regeneration when sleeping (fast rate - 10 per second)
        if self.state == PetState.SLEEPING:
            energy_gain = 10  # Fixed 10 per update for fast recovery
            self.stats.energy = min(100, self.stats.energy + energy_gain)
            # Auto wake up when fully rested
            if self.stats.energy >= 100:
                self.state = PetState.IDLE
                events.append(f"{self.name} woke up feeling refreshed!")
        
        # Clamp stats
        self.stats = PetStats(**self.stats.__dict__)
        
        # Update state based on stats
        self._update_state()
        
        # Move pet
        self._move()
        
        return events
    
    def _update_state(self):
        """Update pet state based on current stats."""
        if not self.is_alive:
            self.state = PetState.DEAD
        elif self.state in [PetState.EATING, PetState.SLEEPING]:
            # Don't interrupt these actions (they manage their own state)
            pass
        elif self.stats.health < 30:
            self.state = PetState.SICK
        elif self.stats.hunger < 20:
            self.state = PetState.HUNGRY
        elif self.stats.happiness < 30:
            self.state = PetState.SAD
        elif self.stats.happiness > 80 and self.stats.energy > 60:
            self.state = PetState.HAPPY
        else:
            self.state = PetState.IDLE
    
    def _move(self):
        """Move pet around the screen."""
        if self.state in [PetState.SLEEPING, PetState.DEAD, PetState.EATING]:
            return
        
        # Random movement
        if random.random() < 0.1:  # 10% chance to change direction
            self.direction *= -1
        
        self.position += self.direction * random.randint(0, 2)
        
        # Bounce off edges
        if self.position <= BOUNCE_LEFT_EDGE:
            self.position = BOUNCE_LEFT_EDGE
            self.direction = 1
        elif self.position >= BOUNCE_RIGHT_EDGE:
            self.position = BOUNCE_RIGHT_EDGE
            self.direction = -1
    
    def feed(self) -> str:
        """Feed the pet."""
        if not self.is_alive:
            return "Cannot feed a dead pet..."
        
        if self.state == PetState.EATING:
            return f"{self.name} is already eating!"
        
        if self.stats.hunger >= 95:
            return f"{self.name} is not hungry!"
        
        self.state = PetState.EATING
        self.eating_started_at = datetime.now()  # Track when eating started
        food_value = int(30 * self.traits.get("food_efficiency", 1.0))
        self.stats.hunger = min(100, self.stats.hunger + food_value)
        self.stats.happiness = min(100, self.stats.happiness + 10)
        
        return f"Fed {self.name}! Yum yum! 🍖"
    
    def play(self) -> str:
        """Play with the pet."""
        if not self.is_alive:
            return "Cannot play with a dead pet..."
        
        if self.state == PetState.EATING:
            return f"{self.name} is busy eating!"
        
        if self.state == PetState.SLEEPING:
            return f"{self.name} is sleeping! Zzz..."
        
        if self.stats.energy < 20:
            return f"{self.name} is too tired to play!"
        
        self.stats.happiness = min(100, self.stats.happiness + 20)
        self.stats.energy -= 15
        self.stats.hunger -= 10
        self.state = PetState.HAPPY
        
        return f"Playing with {self.name}! So much fun! 🎾"
    
    def sleep(self) -> str:
        """Put pet to sleep."""
        if not self.is_alive:
            return "Cannot put a dead pet to sleep..."
        
        if self.state == PetState.EATING:
            return f"{self.name} is busy eating!"
        
        if self.stats.energy >= 95:
            return f"{self.name} is not tired!"
        
        self.state = PetState.SLEEPING
        return f"{self.name} is sleeping... Zzz 😴"
    
    def wake_up(self) -> str:
        """Wake up the pet."""
        if self.state == PetState.SLEEPING:
            self.state = PetState.IDLE
            return f"{self.name} woke up!"
        return f"{self.name} is not sleeping!"
    
    def heal(self) -> str:
        """Heal the pet."""
        if not self.is_alive:
            return "Cannot heal a dead pet... 💀"
        
        if self.state == PetState.EATING:
            return f"{self.name} is busy eating!"
        
        if self.stats.health >= 95:
            return f"{self.name} is healthy!"
        
        self.stats.health = min(100, self.stats.health + 30)
        return f"Healed {self.name}! 💊"
    
    def to_dict(self) -> dict:
        """Convert pet to dictionary for saving."""
        return {
            "name": self.name,
            "pet_type": self.pet_type.value,
            "stats": self.stats.__dict__,
            "state": self.state.value,
            "position": self.position,
            "direction": self.direction,
            "created_at": self.created_at.isoformat(),
            "last_update": self.last_update.isoformat(),
            "eating_started_at": self.eating_started_at.isoformat() if self.eating_started_at else None,
            "accumulated_damage": self.accumulated_damage,
            "accumulated_hunger_decay": self.accumulated_hunger_decay,
            "accumulated_happiness_decay": self.accumulated_happiness_decay,
            "accumulated_energy_decay": self.accumulated_energy_decay,
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "Pet":
        """Create pet from dictionary."""
        eating_started_at = None
        if data.get("eating_started_at"):
            eating_started_at = datetime.fromisoformat(data["eating_started_at"])
        
        pet = cls(
            name=data["name"],
            pet_type=PetType(data["pet_type"]),
            stats=PetStats(**data["stats"]),
            state=PetState(data["state"]),
            position=data["position"],
            direction=data["direction"],
            created_at=datetime.fromisoformat(data["created_at"]),
            last_update=datetime.fromisoformat(data["last_update"]),
            eating_started_at=eating_started_at,
            accumulated_damage=data.get("accumulated_damage", 0.0),
            accumulated_hunger_decay=data.get("accumulated_hunger_decay", 0.0),
            accumulated_happiness_decay=data.get("accumulated_happiness_decay", 0.0),
            accumulated_energy_decay=data.get("accumulated_energy_decay", 0.0),
        )
        return pet

