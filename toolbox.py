import pygame
import math

# returns the rotated image and the new image's rectangle
def getRotatedImage(image, rect, angle):
	new_image = pygame.transform.rotate(image, angle)
	new_rect = new_image.get_rect(center=rect.center)
	return new_image, new_rect
#returns the angle between point 1 and point 2
def angleBetweenPoints(x1, y1, x2, y2):
	x_difference = x2 - x1
	y_difference = y2 - y1
	angle = math.degrees(math.atan2(-y_difference, x_difference))
	return angle

# returns the coordinates that will put item in the centter of the screen
def centeringCoords(item, screen):
	new_x = screen.get_width()/2 - item.get_width()/2
	new_y = screen.get_height()/2 - item.get_height()/2
	return new_x, new_y
	