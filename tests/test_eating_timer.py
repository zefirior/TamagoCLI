"""Tests for eating timer functionality."""

import time
from datetime import datetime
import pytest

from tamagocli.models.pet import Pet, PetType, PetState


class TestEatingTimer:
    """Test suite for eating timer."""
    
    def test_eating_starts_correctly(self):
        """Test that eating state is set correctly when feeding."""
        pet = Pet("TestCat", PetType.CAT)
        pet.stats.hunger = 50
        
        result = pet.feed()
        
        assert pet.state == PetState.EATING
        assert pet.eating_started_at is not None
        assert "Yum yum" in result
    
    def test_eating_finishes_after_3_seconds(self):
        """Test that eating automatically finishes after 3 seconds."""
        pet = Pet("TestCat", PetType.CAT)
        pet.stats.hunger = 50
        
        # Feed the pet
        pet.feed()
        assert pet.state == PetState.EATING
        
        # Wait and update
        time.sleep(3.5)
        events = pet.update()
        
        assert pet.state != PetState.EATING
        assert pet.eating_started_at is None
        assert "finished eating" in events[0]
    
    def test_eating_duration_tracking(self):
        """Test that eating duration is tracked correctly."""
        pet = Pet("TestCat", PetType.CAT)
        pet.stats.hunger = 50
        
        pet.feed()
        start_time = pet.eating_started_at
        
        # Wait 1 second - should still be eating
        time.sleep(1.0)
        pet.update()
        assert pet.state == PetState.EATING
        
        # Wait 2 more seconds - should finish
        time.sleep(2.5)
        pet.update()
        assert pet.state != PetState.EATING
    
    def test_cannot_feed_while_eating(self):
        """Test that pet cannot be fed twice while eating."""
        pet = Pet("TestCat", PetType.CAT)
        pet.stats.hunger = 50
        
        # First feed
        result1 = pet.feed()
        assert pet.state == PetState.EATING
        
        # Try to feed again
        result2 = pet.feed()
        assert "already eating" in result2
        assert pet.state == PetState.EATING
    
    def test_game_loop_simulation(self):
        """Test eating timer in simulated game loop."""
        pet = Pet("TestCat", PetType.CAT)
        pet.stats.hunger = 50
        
        pet.feed()
        
        # Simulate game loop (update every second)
        for _ in range(5):
            time.sleep(1.0)
            pet.update()
        
        # After 5 seconds, should have finished eating
        assert pet.state != PetState.EATING
        assert pet.eating_started_at is None
    
    def test_old_save_compatibility(self):
        """Test that old saves with EATING state but no timestamp are handled."""
        pet = Pet("TestCat", PetType.CAT)
        
        # Simulate old save: EATING state but no timestamp
        pet.state = PetState.EATING
        pet.eating_started_at = None
        
        # Update should fix this immediately
        events = pet.update()
        
        assert pet.state != PetState.EATING
        assert "finished eating" in events[0]


class TestEatingActions:
    """Test suite for actions during eating."""
    
    def test_cannot_play_while_eating(self):
        """Test that pet cannot play while eating."""
        pet = Pet("TestCat", PetType.CAT)
        pet.stats.hunger = 50
        pet.stats.energy = 50
        
        pet.feed()
        result = pet.play()
        
        assert "busy eating" in result
        assert pet.state == PetState.EATING
    
    def test_cannot_sleep_while_eating(self):
        """Test that pet cannot sleep while eating."""
        pet = Pet("TestCat", PetType.CAT)
        pet.stats.hunger = 50
        pet.stats.energy = 50
        
        pet.feed()
        result = pet.sleep()
        
        assert "busy eating" in result
        assert pet.state == PetState.EATING
    
    def test_cannot_heal_while_eating(self):
        """Test that pet cannot be healed while eating."""
        pet = Pet("TestCat", PetType.CAT)
        pet.stats.hunger = 50
        pet.stats.health = 50
        
        pet.feed()
        result = pet.heal()
        
        assert "busy eating" in result
        assert pet.state == PetState.EATING
    
    def test_actions_available_after_eating(self):
        """Test that all actions are available after eating finishes."""
        pet = Pet("TestCat", PetType.CAT)
        pet.stats.hunger = 50
        pet.stats.energy = 50
        pet.stats.health = 50
        
        # Feed and wait
        pet.feed()
        time.sleep(3.5)
        pet.update()
        
        # All actions should work now
        assert pet.state != PetState.EATING
        
        # Test each action doesn't return "busy" message
        result_play = pet.play()
        assert "busy" not in result_play
        
        pet.stats.energy = 50  # Reset for sleep
        result_sleep = pet.sleep()
        assert "busy" not in result_sleep


class TestEatingStats:
    """Test suite for stat changes during eating."""
    
    def test_hunger_increases_after_feeding(self):
        """Test that hunger increases after feeding."""
        pet = Pet("TestCat", PetType.CAT)
        pet.stats.hunger = 50
        
        initial_hunger = pet.stats.hunger
        pet.feed()
        
        assert pet.stats.hunger > initial_hunger
    
    def test_happiness_increases_after_feeding(self):
        """Test that happiness increases after feeding."""
        pet = Pet("TestCat", PetType.CAT)
        pet.stats.hunger = 50
        pet.stats.happiness = 50
        
        initial_happiness = pet.stats.happiness
        pet.feed()
        
        assert pet.stats.happiness >= initial_happiness
    
    def test_cannot_feed_when_full(self):
        """Test that pet cannot be fed when hunger is high."""
        pet = Pet("TestCat", PetType.CAT)
        pet.stats.hunger = 98
        
        result = pet.feed()
        
        assert "not hungry" in result
        assert pet.state != PetState.EATING

