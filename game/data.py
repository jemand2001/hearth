from ..card.hero import Hero
from os import path


# CLASSES = ('warrior', 'mage')
# format: 'class name': (call of Hero class, default health)
CLASSES = {
    'warrior': (Hero('The Greatest!'), 30),
    'mage': (Hero('The Most Intelligent'), 30)
}


ROOT_PATH = path.abspath('.')
IMG_PATH = path.join(ROOT_PATH, 'gui', 'images')
