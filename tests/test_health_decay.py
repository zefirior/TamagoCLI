"""Tests for health decay mechanics."""

import time
import pytest

from tamagocli.models.pet import Pet, PetType, PetState


class TestHealthDecayFromHunger:
    """Test health decay when pet is hungry."""
    
    def test_health_drops_when_starving(self):
        """Test that health decreases when hunger is 0."""
        pet = Pet("TestCat", PetType.CAT)
        pet.stats.hunger = 0
        initial_health = pet.stats.health
        
        # Simulate multiple updates
        for _ in range(20):
            time.sleep(0.1)
            pet.update()
        
        # Health should have decreased
        assert pet.stats.health < initial_health
        print(f"\nHealth dropped from {initial_health} to {pet.stats.health}")
    
    def test_health_stable_when_well_fed(self):
        """Test that health stays stable when hunger is good."""
        pet = Pet("TestCat", PetType.CAT)
        pet.stats.hunger = 100
        pet.stats.happiness = 100
        pet.stats.energy = 100
        initial_health = pet.stats.health
        
        # Simulate updates
        for _ in range(10):
            time.sleep(0.1)
            pet.update()
        
        # Health should remain stable
        assert pet.stats.health == initial_health
    
    def test_accumulated_damage_system(self):
        """Test that accumulated damage works correctly."""
        pet = Pet("TestCat", PetType.CAT)
        pet.stats.hunger = 0
        
        print("\nAccumulated damage test:")
        for i in range(15):
            time.sleep(0.1)
            events = pet.update()
            print(f"  Update {i+1}: HP={pet.stats.health}, "
                  f"AccDamage={pet.accumulated_damage:.2f}, Events={events}")
        
        # Should have lost some health
        assert pet.stats.health < 100


class TestHealthDecayFromLowHappiness:
    """Test health decay when pet is sad."""
    
    def test_health_drops_when_very_sad(self):
        """Test that health decreases when happiness is very low."""
        pet = Pet("TestCat", PetType.CAT)
        pet.stats.hunger = 100  # Keep hunger good
        pet.stats.happiness = 10  # Very sad
        pet.stats.energy = 100
        initial_health = pet.stats.health
        
        # Simulate multiple updates
        for _ in range(20):
            time.sleep(0.1)
            pet.update()
        
        # Health should have decreased
        assert pet.stats.health < initial_health
        print(f"\nHealth dropped from {initial_health} to {pet.stats.health}")


class TestHealthDecayFromLowEnergy:
    """Test health decay when pet is exhausted."""
    
    def test_health_drops_when_exhausted(self):
        """Test that health decreases when energy is 0."""
        pet = Pet("TestCat", PetType.CAT)
        pet.stats.hunger = 100  # Keep hunger good
        pet.stats.happiness = 100
        pet.stats.energy = 0  # Exhausted
        initial_health = pet.stats.health
        
        # Simulate multiple updates
        for _ in range(20):
            time.sleep(0.1)
            pet.update()
        
        # Health should have decreased
        assert pet.stats.health < initial_health
        print(f"\nHealth dropped from {initial_health} to {pet.stats.health}")


class TestCombinedHealthDecay:
    """Test health decay from multiple sources."""
    
    def test_multiple_decay_sources(self):
        """Test that multiple negative conditions stack."""
        pet = Pet("TestCat", PetType.CAT)
        pet.stats.hunger = 0
        pet.stats.happiness = 10
        pet.stats.energy = 0
        initial_health = pet.stats.health
        
        # Simulate updates
        for _ in range(20):
            time.sleep(0.1)
            pet.update()
        
        # Health should drop faster with multiple issues
        health_lost = initial_health - pet.stats.health
        print(f"\nHealth lost with all issues: {health_lost}")
        assert health_lost > 5  # Should lose significant health
    
    def test_health_decay_rate(self):
        """Test that health decays at expected rate."""
        pet = Pet("TestCat", PetType.CAT)
        pet.stats.hunger = 0  # Starving: 3 HP per second
        
        print("\nHealth decay rate test:")
        for i in range(15):
            time.sleep(0.2)
            events = pet.update()
            print(f"  t={i*0.2:.1f}s: HP={pet.stats.health}, Events={len(events)}")
        
        # After ~3 seconds at 3 HP/sec, should lose ~9 HP
        # But decay_rate is time_delta/10, so it's 0.3 HP/sec
        # So after 3 seconds, ~0.9 HP lost
        # Actually with the new system: decay_rate * 30 per update
        # decay_rate = 0.2/10 = 0.02, so 0.02*30 = 0.6 per update
        # 15 updates = 9 damage accumulated
        expected_loss = 9  # Approximately
        actual_loss = 100 - pet.stats.health
        print(f"Expected loss: ~{expected_loss}, Actual: {actual_loss}")
        assert actual_loss >= 5  # Should lose at least 5 HP


class TestHealthRecovery:
    """Test that health stops decaying when conditions improve."""
    
    def test_health_stops_decaying_after_feeding(self):
        """Test that feeding stops hunger-based health decay."""
        pet = Pet("TestCat", PetType.CAT)
        pet.stats.hunger = 0
        
        # Let health drop
        for _ in range(10):
            time.sleep(0.1)
            pet.update()
        
        health_before_feed = pet.stats.health
        
        # Feed the pet
        pet.stats.hunger = 100
        
        # Continue updating
        for _ in range(10):
            time.sleep(0.1)
            pet.update()
        
        # Health should not drop further (or very little from accumulated_damage)
        assert abs(pet.stats.health - health_before_feed) <= 1
    
    def test_pet_dies_from_starvation(self):
        """Test that pet eventually dies from starvation."""
        pet = Pet("TestCat", PetType.CAT)
        pet.stats.hunger = 0
        pet.stats.health = 20  # Start with low health
        
        # Simulate until death
        max_iterations = 100
        for i in range(max_iterations):
            time.sleep(0.1)
            events = pet.update()
            
            if not pet.is_alive:
                print(f"\nPet died after {i} updates")
                assert pet.state == PetState.DEAD
                break
        
        # Should have died
        assert not pet.is_alive


class TestHealthMessages:
    """Test health-related event messages."""
    
    def test_starving_message(self):
        """Test that starving message appears."""
        pet = Pet("TestCat", PetType.CAT)
        pet.stats.hunger = 0
        
        # First update should show starving message
        time.sleep(0.5)
        events = pet.update()
        
        # Check for starving or suffering message
        messages = [e.lower() for e in events]
        assert any("starving" in msg or "suffering" in msg for msg in messages)
    
    def test_exhausted_message(self):
        """Test that exhausted message appears."""
        pet = Pet("TestCat", PetType.CAT)
        pet.stats.energy = 0
        pet.stats.hunger = 100  # Keep hunger good
        
        time.sleep(0.5)
        events = pet.update()
        
        messages = [e.lower() for e in events]
        assert any("exhausted" in msg or "suffering" in msg for msg in messages)


def test_health_decay_summary():
    """Visual summary of health decay system."""
    print("\n" + "="*60)
    print("HEALTH DECAY SUMMARY")
    print("="*60)
    
    pet = Pet("TestCat", PetType.CAT)
    pet.stats.hunger = 0
    pet.stats.happiness = 15
    
    print(f"Initial: HP={pet.stats.health}, Hunger={pet.stats.hunger}, "
          f"Happiness={pet.stats.happiness}")
    print("\nSimulating damage over time:")
    
    for i in range(20):
        time.sleep(0.2)
        events = pet.update()
        print(f"  t={i*0.2:.1f}s: HP={pet.stats.health:3d}, "
              f"AccDmg={pet.accumulated_damage:.2f}, Events={events}")
        
        if not pet.is_alive:
            print("  → Pet died!")
            break
    
    print(f"\nFinal: HP={pet.stats.health}")
    print("="*60)
    
    assert pet.stats.health < 100

