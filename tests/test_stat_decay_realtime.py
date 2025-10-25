"""Tests for real-time stat decay during gameplay."""

import time
import pytest

from tamagocli.models.pet import Pet, PetType


class TestHungerDecay:
    """Test hunger decay in real-time."""
    
    def test_hunger_decreases_over_time(self):
        """Test that hunger decreases during gameplay."""
        pet = Pet("TestCat", PetType.CAT)
        initial_hunger = pet.stats.hunger
        
        print(f"\nInitial hunger: {initial_hunger}")
        
        # Simulate game loop for 2 seconds
        for i in range(20):
            time.sleep(0.1)
            pet.update()
            print(f"  Update {i+1}: Hunger={pet.stats.hunger}, Acc={pet.accumulated_hunger_decay:.2f}")
        
        # Hunger should have decreased
        assert pet.stats.hunger < initial_hunger
        print(f"Final hunger: {pet.stats.hunger}")
    
    def test_hunger_decay_rate(self):
        """Test hunger decays at expected rate (5 per second)."""
        pet = Pet("TestCat", PetType.CAT)
        initial_hunger = pet.stats.hunger
        
        # Run for exactly 2 seconds
        start = time.time()
        while time.time() - start < 2.0:
            time.sleep(0.05)
            pet.update()
        
        # Expected: ~10 hunger lost (5 per second * 2 seconds)
        hunger_lost = initial_hunger - pet.stats.hunger
        print(f"\nHunger lost in 2s: {hunger_lost} (expected ~10)")
        assert 8 <= hunger_lost <= 12  # Allow some variance


class TestHappinessDecay:
    """Test happiness decay in real-time."""
    
    def test_happiness_decreases_over_time(self):
        """Test that happiness decreases during gameplay."""
        pet = Pet("TestCat", PetType.CAT)
        initial_happiness = pet.stats.happiness
        
        print(f"\nInitial happiness: {initial_happiness}")
        
        # Simulate game loop for 2 seconds
        for i in range(20):
            time.sleep(0.1)
            pet.update()
            print(f"  Update {i+1}: Happiness={pet.stats.happiness}, Acc={pet.accumulated_happiness_decay:.2f}")
        
        # Happiness should have decreased
        assert pet.stats.happiness < initial_happiness
        print(f"Final happiness: {pet.stats.happiness}")
    
    def test_happiness_decay_rate(self):
        """Test happiness decays at expected rate (3 per second)."""
        pet = Pet("TestCat", PetType.CAT)
        initial_happiness = pet.stats.happiness
        
        # Run for exactly 2 seconds
        start = time.time()
        while time.time() - start < 2.0:
            time.sleep(0.05)
            pet.update()
        
        # Expected: ~6 happiness lost (3 per second * 2 seconds)
        # But CAT has happiness_decay = 0.8, so ~4.8
        happiness_lost = initial_happiness - pet.stats.happiness
        print(f"\nHappiness lost in 2s: {happiness_lost} (expected ~5 for cat)")
        assert 3 <= happiness_lost <= 7


class TestEnergyDecay:
    """Test energy decay in real-time."""
    
    def test_energy_decreases_over_time(self):
        """Test that energy decreases during gameplay."""
        pet = Pet("TestCat", PetType.CAT)
        initial_energy = pet.stats.energy
        
        print(f"\nInitial energy: {initial_energy}")
        
        # Simulate game loop for 2 seconds
        for i in range(20):
            time.sleep(0.1)
            pet.update()
            print(f"  Update {i+1}: Energy={pet.stats.energy}, Acc={pet.accumulated_energy_decay:.2f}")
        
        # Energy should have decreased
        assert pet.stats.energy < initial_energy
        print(f"Final energy: {pet.stats.energy}")
    
    def test_energy_decay_rate(self):
        """Test energy decays at expected rate (2 per second)."""
        pet = Pet("TestCat", PetType.CAT)
        initial_energy = pet.stats.energy
        
        # Run for exactly 2 seconds
        start = time.time()
        while time.time() - start < 2.0:
            time.sleep(0.05)
            pet.update()
        
        # Expected: ~4 energy lost (2 per second * 2 seconds)
        # But CAT has energy_decay = 0.7, so ~2.8
        energy_lost = initial_energy - pet.stats.energy
        print(f"\nEnergy lost in 2s: {energy_lost} (expected ~3 for cat)")
        assert 2 <= energy_lost <= 5


class TestCombinedStatDecay:
    """Test all stats decay together."""
    
    def test_all_stats_decay_simultaneously(self):
        """Test that all stats decay during gameplay."""
        pet = Pet("TestCat", PetType.CAT)
        
        initial_hunger = pet.stats.hunger
        initial_happiness = pet.stats.happiness
        initial_energy = pet.stats.energy
        
        print("\nInitial stats:")
        print(f"  Hunger: {initial_hunger}")
        print(f"  Happiness: {initial_happiness}")
        print(f"  Energy: {initial_energy}")
        
        # Simulate 3 seconds
        for _ in range(30):
            time.sleep(0.1)
            pet.update()
        
        print("\nFinal stats:")
        print(f"  Hunger: {pet.stats.hunger} (lost {initial_hunger - pet.stats.hunger})")
        print(f"  Happiness: {pet.stats.happiness} (lost {initial_happiness - pet.stats.happiness})")
        print(f"  Energy: {pet.stats.energy} (lost {initial_energy - pet.stats.energy})")
        
        # All should have decreased
        assert pet.stats.hunger < initial_hunger
        assert pet.stats.happiness < initial_happiness
        assert pet.stats.energy < initial_energy


class TestPetTypeDifferences:
    """Test that different pet types have different decay rates."""
    
    def test_dog_vs_cat_hunger_decay(self):
        """Test that dogs get hungry faster than cats."""
        cat = Pet("Cat", PetType.CAT)
        dog = Pet("Dog", PetType.DOG)
        
        # Run for 2 seconds
        start = time.time()
        while time.time() - start < 2.0:
            time.sleep(0.05)
            cat.update()
            dog.update()
        
        cat_hunger_lost = 100 - cat.stats.hunger
        dog_hunger_lost = 100 - dog.stats.hunger
        
        print(f"\nCat hunger lost: {cat_hunger_lost}")
        print(f"Dog hunger lost: {dog_hunger_lost}")
        
        # Dog has hunger_decay=1.2, Cat has hunger_decay=1.0
        assert dog_hunger_lost > cat_hunger_lost


class TestAccumulationSystem:
    """Test the accumulation system itself."""
    
    def test_fractional_accumulation(self):
        """Test that fractional changes accumulate correctly."""
        pet = Pet("TestCat", PetType.CAT)
        
        print("\nAccumulation test (small updates):")
        initial_hunger = pet.stats.hunger
        
        # Many small updates
        for i in range(50):
            time.sleep(0.01)  # Very small time steps
            pet.update()
            if i % 10 == 0:
                print(f"  Update {i}: Hunger={pet.stats.hunger}, "
                      f"Acc={pet.accumulated_hunger_decay:.3f}")
        
        # Should still have lost some hunger despite tiny time steps
        assert pet.stats.hunger < initial_hunger
        print(f"Final: Hunger={pet.stats.hunger} (lost {initial_hunger - pet.stats.hunger})")


def test_realtime_decay_summary():
    """Visual summary of real-time stat decay."""
    print("\n" + "="*70)
    print("REAL-TIME STAT DECAY SUMMARY")
    print("="*70)
    
    pet = Pet("TestCat", PetType.CAT)
    
    print(f"Initial: Hunger={pet.stats.hunger}, Happiness={pet.stats.happiness}, "
          f"Energy={pet.stats.energy}, Health={pet.stats.health}")
    print("\nSimulating 5 seconds of gameplay:")
    
    start_time = time.time()
    update_count = 0
    
    while time.time() - start_time < 5.0:
        time.sleep(0.05)  # 50ms updates (like real game)
        pet.update()
        update_count += 1
        
        elapsed = time.time() - start_time
        if elapsed >= (update_count // 20) * 1.0:  # Print every ~1 second
            print(f"  t={elapsed:.1f}s: H={pet.stats.hunger:3d}, "
                  f"Hap={pet.stats.happiness:3d}, E={pet.stats.energy:3d}, HP={pet.stats.health:3d}")
    
    print(f"\nTotal updates: {update_count}")
    print(f"Final: Hunger={pet.stats.hunger}, Happiness={pet.stats.happiness}, "
          f"Energy={pet.stats.energy}, Health={pet.stats.health}")
    print("="*70)
    
    # All should have decreased
    assert pet.stats.hunger < 100
    assert pet.stats.happiness < 100
    assert pet.stats.energy < 100

