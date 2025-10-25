"""ASCII art sprites for different pets and their states."""

from ..models.pet import PetType, PetState


# Cat sprites
CAT_SPRITES = {
    PetState.IDLE: [
        r"""
   /\_/\  
  ( o.o ) 
   > ^ <
  /|   |\
 (_|   |_)
        """,
        r"""
   /\_/\  
  ( -.o ) 
   > ^ <
  /|   |\
 (_|   |_)
        """,
    ],
    PetState.HAPPY: [
        r"""
   /\_/\  
  ( ^.^ ) 
   > ◡ <
  /|   |\
 (_|   |_)
        """,
    ],
    PetState.HUNGRY: [
        r"""
   /\_/\  
  ( O.O ) 
   > w <
  /|   |\
 (_|   |_)
        """,
    ],
    PetState.EATING: [
        r"""
   /\_/\  
  ( ◡.◡ )🍖
   > ◡ <
  /|   |\
 (_|   |_)
        """,
    ],
    PetState.SLEEPING: [
        r"""
   /\_/\  
  ( -.-)zzZ
   > ^ <
  /|   |\
 (_|   |_)
        """,
    ],
    PetState.SAD: [
        r"""
   /\_/\  
  ( ;.; ) 
   > v <
  /|   |\
 (_|   |_)
        """,
    ],
    PetState.SICK: [
        r"""
   /\_/\  
  ( x.x ) 
   > ~ <
  /|   |\
 (_|   |_)
        """,
    ],
    PetState.DEAD: [
        r"""
   /\_/\  
  ( x.x )💀
   > ~ <
  /|   |\
 (_|   |_)
        """,
    ],
}

# Dog sprites
DOG_SPRITES = {
    PetState.IDLE: [
        r"""
   /\_/\  
  ( o.o )
  />  <\
  U U  U U
        """,
        r"""
   /\_/\  
  ( o.o )
  />  <\\
  U U  U U
        """,
    ],
    PetState.HAPPY: [
        r"""
   /\_/\  
  ( ^ω^ )
  />  <\
  U U  U U
        """,
    ],
    PetState.HUNGRY: [
        r"""
   /\_/\  
  ( O.O )
  />  <\
  U U  U U
        """,
    ],
    PetState.EATING: [
        r"""
   /\_/\  
  ( ◡ω◡ )🍖
  />  <\
  U U  U U
        """,
    ],
    PetState.SLEEPING: [
        r"""
   /\_/\  
  ( -.-)zzZ
  />  <\
  U U  U U
        """,
    ],
    PetState.SAD: [
        r"""
   /\_/\  
  ( ;ω; )
  />  <\
  U U  U U
        """,
    ],
    PetState.SICK: [
        r"""
   /\_/\  
  ( x.x )
  />  <\
  U U  U U
        """,
    ],
    PetState.DEAD: [
        r"""
   /\_/\  
  ( x.x )💀
  />  <\
  U U  U U
        """,
    ],
}

# Dragon sprites
DRAGON_SPRITES = {
    PetState.IDLE: [
        r"""
    />_   
   |_  \\
   (__)\' \\
    //_\\  \\
   //  \\  \\
   VV   VV  VV
        """,
        r"""
    />_   
   |_  \)
   (__)\' \\
    //_\\  \\
   //  \\  \\
   VV   VV  VV
        """,
    ],
    PetState.HAPPY: [
        r"""
    />_🔥  
   |_  \\
   (^_)\' \\
    //_\\  \\
   //  \\  \\
   VV   VV  VV
        """,
    ],
    PetState.HUNGRY: [
        r"""
    />_   
   |O  \\
   (__)\' \\
    //_\\  \\
   //  \\  \\
   VV   VV  VV
        """,
    ],
    PetState.EATING: [
        r"""
    />_🍖  
   |◡  \\
   (__)\' \\
    //_\\  \\
   //  \\  \\
   VV   VV  VV
        """,
    ],
    PetState.SLEEPING: [
        r"""
    />_zzZ 
   |_  \\
   (-_)\' \\
    //_\\  \\
   //  \\  \\
   VV   VV  VV
        """,
    ],
    PetState.SAD: [
        r"""
    />_   
   |;  \\
   (__)\' \\
    //_\\  \\
   //  \\  \\
   VV   VV  VV
        """,
    ],
    PetState.SICK: [
        r"""
    />_   
   |x  \\
   (__)\' \\
    //_\\  \\
   //  \\  \\
   VV   VV  VV
        """,
    ],
    PetState.DEAD: [
        r"""
    />_💀  
   |x  \\
   (__)\' \\
    //_\\  \\
   //  \\  \\
   VV   VV  VV
        """,
    ],
}

# Bunny sprites
BUNNY_SPRITES = {
    PetState.IDLE: [
        r"""
   (\(\
   ( -.-)
   o_(")(")
        """,
        r"""
   (\(\
   ( o.-)
   o_(")(")
        """,
    ],
    PetState.HAPPY: [
        r"""
   (\(\
   ( ^.^)
   o_(")(")
        """,
    ],
    PetState.HUNGRY: [
        r"""
   (\(\
   ( O.O)
   o_(")(")
        """,
    ],
    PetState.EATING: [
        r"""
   (\(\🥕
   ( ◡.◡)
   o_(")(")
        """,
    ],
    PetState.SLEEPING: [
        r"""
   (\(\zzZ
   ( -.-)
   o_(")(")
        """,
    ],
    PetState.SAD: [
        r"""
   (\(\
   ( ;.;)
   o_(")(")
        """,
    ],
    PetState.SICK: [
        r"""
   (\(\
   ( x.x)
   o_(")(")
        """,
    ],
    PetState.DEAD: [
        r"""
   (\(\💀
   ( x.x)
   o_(")(")
        """,
    ],
}

# Alien sprites
ALIEN_SPRITES = {
    PetState.IDLE: [
        r"""
    .---.
   /o   o\
  |   △   |
   \  ~  /
    '---'
   /|   |\
  /_|   |_\
        """,
        r"""
    .---.
   /o   o\
  |   △   |
   \  -  /
    '---'
   /|   |\
  /_|   |_\
        """,
    ],
    PetState.HAPPY: [
        r"""
    .---.
   /^   ^\\
  |   △   |
   \  ◡  /
    '---'
   /|   |\
  /_|   |_\
        """,
    ],
    PetState.HUNGRY: [
        r"""
    .---.
   /O   O\
  |   △   |
   \  w  /
    '---'
   /|   |\
  /_|   |_\
        """,
    ],
    PetState.EATING: [
        r"""
    .---.🛸
   /◡   ◡\
  |   △   |
   \  ◡  /
    '---'
   /|   |\
  /_|   |_\
        """,
    ],
    PetState.SLEEPING: [
        r"""
    .---.
   /-   -\\
  |   △   |zzZ
   \  -  /
    '---'
   /|   |\
  /_|   |_\
        """,
    ],
    PetState.SAD: [
        r"""
    .---.
   /;   ;\
  |   △   |
   \  v  /
    '---'
   /|   |\
  /_|   |_\
        """,
    ],
    PetState.SICK: [
        r"""
    .---.
   /x   x\
  |   △   |
   \  ~  /
    '---'
   /|   |\
  /_|   |_\
        """,
    ],
    PetState.DEAD: [
        r"""
    .---.💀
   /x   x\
  |   △   |
   \  ~  /
    '---'
   /|   |\
  /_|   |_\
        """,
    ],
}

# Map pet types to their sprites
SPRITES_MAP = {
    PetType.CAT: CAT_SPRITES,
    PetType.DOG: DOG_SPRITES,
    PetType.DRAGON: DRAGON_SPRITES,
    PetType.BUNNY: BUNNY_SPRITES,
    PetType.ALIEN: ALIEN_SPRITES,
}


def get_sprite(pet_type: PetType, state: PetState, frame: int = 0) -> str:
    """
    Get sprite for a pet type and state.
    
    Args:
        pet_type: Type of the pet
        state: Current state of the pet
        frame: Animation frame (cycles through available frames)
    
    Returns:
        ASCII art sprite as string
    """
    sprites = SPRITES_MAP.get(pet_type, CAT_SPRITES)
    state_sprites = sprites.get(state, sprites.get(PetState.IDLE, []))
    
    if not state_sprites:
        return "¯\\_(ツ)_/¯"
    
    frame_index = frame % len(state_sprites)
    return state_sprites[frame_index]


def get_pet_preview(pet_type: PetType) -> str:
    """Get a preview sprite for pet selection."""
    return get_sprite(pet_type, PetState.HAPPY, 0)

