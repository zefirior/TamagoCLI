"""Tests for Pet model."""

import pytest
from datetime import datetime

from tamagocli.models.pet import Pet, PetType, PetState, PetStats


class TestPetCreation:
    """Test suite for pet creation."""
    
    def test_create_pet_basic(self):
        """Test basic pet creation."""
        pet = Pet("TestPet", PetType.CAT)
        
        assert pet.name == "TestPet"
        assert pet.pet_type == PetType.CAT
        assert pet.state == PetState.IDLE
        assert pet.is_alive
    
    def test_create_pet_all_types(self):
        """Test creating pets of all types."""
        types = [PetType.CAT, PetType.DOG, PetType.DRAGON, PetType.BUNNY, PetType.ALIEN]
        
        for pet_type in types:
            pet = Pet(f"Test{pet_type.value}", pet_type)
            assert pet.pet_type == pet_type
            assert pet.is_alive
    
    def test_initial_stats(self):
        """Test that initial stats are correct."""
        pet = Pet("TestPet", PetType.CAT)
        
        assert pet.stats.hunger == 100
        assert pet.stats.happiness == 100
        assert pet.stats.energy == 100
        assert pet.stats.health == 100
        assert pet.stats.age == 0
        assert pet.stats.level == 1


class TestPetStats:
    """Test suite for pet stats."""
    
    def test_stats_bounds(self):
        """Test that stats stay within 0-100 bounds."""
        stats = PetStats(hunger=150, happiness=-10, energy=100, health=50)
        
        assert stats.hunger == 100  # Capped at 100
        assert stats.happiness == 0  # Floored at 0
        assert stats.energy == 100
        assert stats.health == 50
    
    def test_pet_is_alive_with_health(self):
        """Test that pet is alive with health > 0."""
        pet = Pet("TestPet", PetType.CAT)
        pet.stats.health = 50
        
        assert pet.is_alive
    
    def test_pet_is_dead_with_zero_health(self):
        """Test that pet is dead with health = 0."""
        pet = Pet("TestPet", PetType.CAT)
        pet.stats.health = 0
        
        assert not pet.is_alive


class TestPetActions:
    """Test suite for pet actions."""
    
    def test_feed_action(self):
        """Test feeding action."""
        pet = Pet("TestPet", PetType.CAT)
        pet.stats.hunger = 50
        
        result = pet.feed()
        
        assert pet.stats.hunger > 50
        assert "Fed" in result
    
    def test_play_action(self):
        """Test play action."""
        pet = Pet("TestPet", PetType.CAT)
        pet.stats.happiness = 50
        pet.stats.energy = 50
        
        initial_happiness = pet.stats.happiness
        result = pet.play()
        
        assert pet.stats.happiness > initial_happiness
        assert pet.stats.energy < 50
        assert "Playing" in result
    
    def test_sleep_action(self):
        """Test sleep action."""
        pet = Pet("TestPet", PetType.CAT)
        pet.stats.energy = 50
        
        result = pet.sleep()
        
        assert pet.state == PetState.SLEEPING
        assert "sleeping" in result
    
    def test_wake_up_action(self):
        """Test wake up action."""
        pet = Pet("TestPet", PetType.CAT)
        pet.state = PetState.SLEEPING
        
        result = pet.wake_up()
        
        assert pet.state == PetState.IDLE
        assert "woke up" in result
    
    def test_heal_action(self):
        """Test heal action."""
        pet = Pet("TestPet", PetType.CAT)
        pet.stats.health = 50
        
        result = pet.heal()
        
        assert pet.stats.health > 50
        assert "Healed" in result


class TestPetSerialization:
    """Test suite for pet save/load."""
    
    def test_to_dict(self):
        """Test converting pet to dictionary."""
        pet = Pet("TestPet", PetType.CAT)
        data = pet.to_dict()
        
        assert data["name"] == "TestPet"
        assert data["pet_type"] == "cat"
        assert "stats" in data
        assert "state" in data
    
    def test_from_dict(self):
        """Test creating pet from dictionary."""
        pet1 = Pet("TestPet", PetType.CAT)
        pet1.stats.hunger = 50
        
        data = pet1.to_dict()
        pet2 = Pet.from_dict(data)
        
        assert pet2.name == pet1.name
        assert pet2.pet_type == pet1.pet_type
        assert pet2.stats.hunger == pet1.stats.hunger
    
    def test_save_load_roundtrip(self):
        """Test that save and load preserve all data."""
        pet1 = Pet("TestPet", PetType.DRAGON)
        pet1.stats.hunger = 75
        pet1.stats.happiness = 85
        pet1.state = PetState.HAPPY
        pet1.position = 30
        
        data = pet1.to_dict()
        pet2 = Pet.from_dict(data)
        
        assert pet2.name == pet1.name
        assert pet2.pet_type == pet1.pet_type
        assert pet2.stats.hunger == pet1.stats.hunger
        assert pet2.stats.happiness == pet1.stats.happiness
        assert pet2.state == pet1.state
        assert pet2.position == pet1.position

