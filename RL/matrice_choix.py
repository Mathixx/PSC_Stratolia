class MatriceChoix:
    def __init__(self, size=1000, initial_value=0):
        """Initialize the MatriceChoix with a specific size and initial value."""
        self.data = [initial_value] * size
        self.sum = initial_value * size
        self.average = initial_value

    def update_element(self, index, value):
        """Update the element at a specific index and recalculate sum and average."""
        if index < 0 or index >= len(self.data):
            raise IndexError("Index out of range")

        # Update sum by subtracting the old value and adding the new value
        self.sum -= self.data[index]
        self.sum += value
        
        # Update the data list
        self.data[index] = value
        
        # Recalculate the average
        self.average = self.sum / len(self.data)

    def add(self, index, value):
        """Add a value to the element at a specific index and update sum and average."""
        if index < 0 or index >= len(self.data):
            raise IndexError("Index out of range")

        # Perform the addition
        self.data[index] += value
        
        # Update the sum
        self.sum += value

        # Recalculate the average
        self.average = self.sum / len(self.data)

    def get_element(self, index):
        """Return the value of the element at the specified index."""
        if index < 0 or index >= len(self.data):
            raise IndexError("Index out of range")
        return self.data[index]

    def get_sum(self):
        """Return the current sum of all elements."""
        return self.sum

    def get_average(self):
        """Return the current average of all elements."""
        return self.average

    def __str__(self):
        """Return a string representation of the internal data list."""
        return str(self.data)
