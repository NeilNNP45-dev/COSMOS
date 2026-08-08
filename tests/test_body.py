import pygame

from engine.physics.body import Body

def test_body_speed():
    body = Body(
        name="Test",
        mass=1.0,
        radius=1.0,
        position=pygame.Vector2(0, 0),
        velocity=pygame.Vector2(3, 4),
        color=(255, 255, 255),
        
    )

    assert body.speed == 5.0