from os import path
from card.hero import Hero


# CLASSES = ('warrior', 'mage')
# format: 'class name': (call of Hero class, default health)
CLASSES = {
    'warrior': (Hero('Warrior'), 30),
    'mage': (Hero('Mage'), 30)
}


ROOT_PATH = path.abspath('..')
IMG_PATH = path.join(ROOT_PATH, 'gui', 'images')
