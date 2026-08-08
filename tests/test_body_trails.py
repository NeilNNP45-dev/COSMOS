import pygame

from engine.physics.body import Body


def test_add_trail_point():
    body = Body(
        name="Test",
        mass=1.0,
        radius=1.0,
        position=pygame.Vector2(10, 20),
        velocity=pygame.Vector2(3, 4),
        color=(255, 255, 255),
    )

    body.add_trail_point()

    assert body.trail == [pygame.Vector2(10, 20)]
def test_trail_max_length():
    body = Body(            
        name="Test",
        mass=1.0,
        radius=1.0,
        position=pygame.Vector2(10, 20),
        velocity=pygame.Vector2(3, 4),
        color=(255, 255, 255),
        max_trail_length=3,
            )
    body.add_trail_point()

    body.position = pygame.Vector2(15,25)
    body.add_trail_point()

    body.position = pygame.Vector2(20,30)
    body.add_trail_point()

    body.position = pygame.Vector2(25,35)
    body.add_trail_point()

    assert body.trail == [
    pygame.Vector2(15, 25),
    pygame.Vector2(20, 30),
    pygame.Vector2(25, 35),
]


    
