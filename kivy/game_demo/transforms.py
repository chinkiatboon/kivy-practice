def transform(self, x, y):
    # return self.transform_2D(x,y)
    return self.transform_perspective(x,y)

def transform_2D(self, x, y):
    """
    To be used if we want to see the game board from the top (2D).
    For debugging purposes.
    """
    return int(x), int(y)

def transform_perspective(self, x, y):
    """
    Transforms (x,y) coordinates to give a more 3D feel.
    """
    # Calculate new y based on proportion 
    y = y / self.height * self.perspective_point_y
    if y > self.perspective_point_y:
        y = self.perspective_point_y

    # Calculate new x. We can visually note that new x is dependent on y.
    x_diff = x - self.perspective_point_x  
    y_factor = ((self.perspective_point_y - y )/self.perspective_point_y)**2    # Squared to account for proportion of 
                                                                                # horizontal lines

    x = self.perspective_point_x + x_diff * y_factor                            # Recalculate x based on 
                                                                                # proportion of y 

    y = self.perspective_point_y - y_factor * self.perspective_point_y

    return int(x), int(y)