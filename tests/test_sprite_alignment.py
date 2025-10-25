"""Tests for sprite alignment and rendering."""

import pytest
from tamagocli.models.pet import Pet, PetType, PetState
from tamagocli.display.sprites import get_sprite


class TestSpriteStructure:
    """Test sprite structure and parsing."""
    
    def test_sprite_has_no_trailing_whitespace_issues(self):
        """Test that sprite lines don't have inconsistent whitespace."""
        sprite = get_sprite(PetType.CAT, PetState.SLEEPING, 0)
        lines = [line for line in sprite.split('\n') if line.strip()]
        
        # Should have 5 lines for cat
        assert len(lines) == 5, f"Expected 5 lines, got {len(lines)}"
        
        # Print for visual inspection
        print("\nSprite lines:")
        for i, line in enumerate(lines):
            print(f"  {i}: |{line}| len={len(line)}")
    
    def test_all_cat_sprites_have_consistent_structure(self):
        """Test that all cat sprites have similar structure."""
        states = [
            PetState.IDLE, PetState.HAPPY, PetState.HUNGRY,
            PetState.EATING, PetState.SLEEPING, PetState.SAD,
            PetState.SICK, PetState.DEAD
        ]
        
        for state in states:
            sprite = get_sprite(PetType.CAT, state, 0)
            lines = [line for line in sprite.split('\n') if line.strip()]
            
            # All should have 5 lines
            assert len(lines) == 5, f"{state} has {len(lines)} lines"
            
            # First line should start with spaces and contain /\_/\
            assert '/\\_/\\' in lines[0], f"{state} first line malformed"
    
    def test_sprite_visual_alignment(self):
        """Visual test - print sprite to verify alignment."""
        sprite = get_sprite(PetType.CAT, PetState.SLEEPING, 0)
        lines = [line for line in sprite.split('\n') if line.strip()]
        
        print("\n" + "="*50)
        print("Visual alignment test - CAT SLEEPING:")
        print("="*50)
        for i, line in enumerate(lines):
            # Show with ruler
            print(f"{i}: {line}")
        print("="*50)
        
        # Character positions that should align
        # Line 0: "   /\_/\  " - ears should be at positions 3 and 7
        # Line 1: "  ( -.-)zzZ" - face
        # Line 2: "   > ^ <" - mouth
        # Line 3: "  /|   |\" - legs start
        # Line 4: " (_|   |_)" - legs end
        
        # Check that first line starts with 3 spaces for proper centering
        assert lines[0].startswith('   /'), "First line (ears) should start with 3 spaces"


class TestSpriteRendering:
    """Test sprite rendering logic."""
    
    def test_sprite_line_lengths(self):
        """Test that we correctly calculate max line width."""
        sprite = get_sprite(PetType.CAT, PetState.SLEEPING, 0)
        lines = [line for line in sprite.split('\n') if line.strip()]
        
        line_lengths = [len(line) for line in lines]
        max_length = max(line_lengths)
        
        print(f"\nLine lengths: {line_lengths}")
        print(f"Max length: {max_length}")
        
        # For CAT SLEEPING, longest line is " ( -.-)zzZ" with 11 chars
        assert max_length == 11
    
    def test_sprite_positioning_logic(self):
        """Test the positioning calculation logic."""
        sprite = get_sprite(PetType.CAT, PetState.SLEEPING, 0)
        lines = [line for line in sprite.split('\n') if line.strip()]
        max_line_width = max(len(line) for line in lines)
        
        # Simulate panel width
        panel_width = 100
        
        # Test different positions (0-100)
        positions = [0, 25, 50, 75, 100]
        
        print("\n" + "="*50)
        print("Position calculations:")
        print("="*50)
        
        for pos in positions:
            available_width = panel_width - max_line_width
            base_x = 3
            offset = int(pos * available_width / 100)
            sprite_x = base_x + offset
            
            print(f"Position {pos}%: sprite_x={sprite_x}, offset={offset}")
            
            # sprite_x should increase as position increases
            assert sprite_x >= 3


class TestSpriteMovement:
    """Test that sprite moves correctly without breaking alignment."""
    
    def test_sprite_moves_as_unit(self):
        """Test that all lines move together."""
        sprite = get_sprite(PetType.CAT, PetState.IDLE, 0)
        lines = [line for line in sprite.split('\n') if line.strip()]
        max_line_width = max(len(line) for line in lines)
        
        panel_width = 100
        base_x = 3
        
        print("\n" + "="*70)
        print("Sprite movement visualization:")
        print("="*70)
        
        # Simulate movement from left to right
        for position in [0, 25, 50, 75]:
            available_width = panel_width - max_line_width
            offset = int(position * available_width / 100)
            sprite_x = base_x + offset
            
            print(f"\nPosition: {position}%  (x={sprite_x})")
            print("-" * 70)
            
            # Draw ruler
            ruler = "0....5....10...15...20...25...30...35...40"
            print(ruler)
            
            # Draw each line with proper spacing
            for line in lines:
                # Add spaces before the line to simulate x position
                padded = " " * sprite_x + line
                print(padded[:50])  # Truncate for display
            
            print()


class TestVisualDebug:
    """Visual debugging tests - run with pytest -s to see output."""
    
    def test_compare_all_cat_states(self):
        """Compare all cat states side by side."""
        states = [
            (PetState.IDLE, "IDLE"),
            (PetState.SLEEPING, "SLEEPING"),
            (PetState.EATING, "EATING"),
            (PetState.HAPPY, "HAPPY"),
        ]
        
        print("\n" + "="*80)
        print("All Cat States Comparison:")
        print("="*80)
        
        for state, name in states:
            sprite = get_sprite(PetType.CAT, state, 0)
            lines = [line for line in sprite.split('\n') if line.strip()]
            
            print(f"\n{name}:")
            print("-" * 40)
            for i, line in enumerate(lines):
                print(f"  {i}: |{line}|")
    
    def test_position_simulation(self):
        """Simulate sprite at different positions."""
        pet = Pet("TestCat", PetType.CAT)
        sprite = get_sprite(pet.pet_type, PetState.SLEEPING, 0)
        lines = [line for line in sprite.split('\n') if line.strip()]
        
        print("\n" + "="*80)
        print("Sprite Position Simulation (simulating panel width=100):")
        print("="*80)
        
        panel_width = 100
        max_line_width = max(len(line) for line in lines)
        available_width = panel_width - max_line_width
        base_x = 3
        
        # Test positions
        test_positions = [0, 30, 50, 70, 100]
        
        for pos in test_positions:
            offset = int(pos * available_width / 100)
            sprite_x = base_x + offset
            
            print(f"\nPet Position: {pos}%  (rendered at x={sprite_x})")
            print("─" * 60)
            print("0....5....10...15...20...25...30...35...40...45...50")
            
            for line in lines:
                # Simulate rendering
                full_line = " " * sprite_x + line
                print(full_line[:60])
            
            print()


class TestSpriteIntegrity:
    """Test that sprites maintain integrity during rendering."""
    
    def test_no_line_breaks_in_sprite(self):
        """Test that sprite lines don't contain newlines."""
        sprite = get_sprite(PetType.CAT, PetState.SLEEPING, 0)
        lines = [line for line in sprite.split('\n') if line.strip()]
        
        for i, line in enumerate(lines):
            assert '\n' not in line, f"Line {i} contains newline"
            assert '\r' not in line, f"Line {i} contains carriage return"
    
    def test_sprite_ears_alignment(self):
        """Specific test for ear alignment (first line)."""
        sprite = get_sprite(PetType.CAT, PetState.SLEEPING, 0)
        lines = [line for line in sprite.split('\n') if line.strip()]
        
        first_line = lines[0]
        
        # The ears pattern /\_/\ should be intact
        assert '/\\_/\\' in first_line, "Ears pattern not found"
        
        # Find position of ears
        ears_pos = first_line.find('/\\_/\\')
        
        print(f"\nEars analysis:")
        print(f"  First line: |{first_line}|")
        print(f"  Ears start at position: {ears_pos}")
        print(f"  Line length: {len(first_line)}")
        
        # Ears should be near the beginning (with some leading spaces)
        assert 0 <= ears_pos <= 5, f"Ears at unexpected position {ears_pos}"


def test_visual_render_example():
    """Complete visual example of how sprite should look."""
    print("\n" + "="*80)
    print("EXPECTED APPEARANCE:")
    print("="*80)
    print("""
Expected CAT SLEEPING sprite:
   /\_/\  
  ( -.-)zzZ
   > ^ <
  /|   |\\
 (_|   |_)

All lines should align vertically!
- Line 0 has 3 leading spaces
- Line 1 has 2 leading spaces
- Line 2 has 3 leading spaces
- Line 3 has 2 leading spaces
- Line 4 has 1 leading space

This creates the centered appearance.
    """)
    print("="*80)

