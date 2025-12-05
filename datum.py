

import math

def StatError(error, tol = 0.34):
    """
    Docstring for StatError
    
    :param value: Description
    :param error: Description
    :param tol: Description
    """
    str_err = str(error)
    Vals = 0
    mod_err = ""
    err_ord = 0
    for char in str_err :
        print(f"Current Char: {char}")
        print(f"Current Vals: {Vals}")
        if char == "0" and Vals == 0 or char == "." and Vals == 0:
            mod_err += char
            print(mod_err)
            continue
        else:
            while Vals < 2:
                if char != '0' and char != '.' and char != '1' and char != '2':
                    mod_err += char
                    Vals += 1
                    #print(mod_err)
                    #print(err_ord)
                    #print(f"{Vals} after adding 1")
                    break
                else:
                    mod_err += "0"
                    Vals += tol
                    err_ord += 1
                    #print(mod_err)
                    #print(err_ord)
                    #print(f"{Vals} after adding tol")
                    break
    sig = float(mod_err)
    #print(sig)
    err_ord += int(abs(math.log10(sig)// 1))
    #print(err_ord)
    return err_ord
                        
def Errorsig(error):
    """
    Docstring for ErrorSig
    
    :param value: Description
    :param error: Description
    """
    if error < 0:
        return ValueError("Error cannot be a negative value")
    if error == 0:
        return math.inf
    if error > 0:
        sig = StatError(error)
        return sig + 1

def rd(value, order):
    if order == math.inf:
        return value
    else:
        rdv = round(value, abs(order))
        return rdv
    


class datum:
    """
    Docstring for datum
    """
    def __init__(self, value, Error, Units = "SI", Analyte = "Unk"):
        """
        Docstring for __init___
        
        :param self: Description
        :param value: Description
        :param Error: Description
        :param Units: Description
        :param Analyte: Description
        """
        self.value = value #Actual value of the variable of interest
        self.error = Error
        self.units = Units
        self.analyte = Analyte
        self.errorder = Errorsig(self.error)
    
    def __repr__(self):
        """
        Docstring for ___repr__
        
        :param self: Description
        """
        s = ""
        s += f"{rd(self.value, self.errorder)} +/- {rd(self.error, self.errorder)} {self.units} ({self.analyte})"
        return s

    def __add__(self, other):
        if self.units != other.units:
            raise ValueError("Units do not match, cannot perform addition")
        if self.analyte != other.analyte:
            analyte = "Unk"
        else:
            analyte = self.analyte
        val = self.value + other.value
        err = math.sqrt(self.error**2 + other.error**2)
        result = datum(val, err, self.units, analyte) #Maybe preclude analyte to force people to define it later?
        return result
    
    def __sub__(self, other):
        if self.units != other.units:
            raise ValueError("Units do not match, cannot perform addition")
        if self.analyte != other.analyte:
            analyte = "Unk"
        else:
            analyte = self.analyte
        val = self.value - other.value
        err = math.sqrt(self.error**2 + other.error**2)
        result = datum(val, err, self.units, analyte) #Maybe preclude analyte to force people to define it later?
        return result
    
    def __mul__(self, other):
        if self.units != other.units:
            units = f"({self.units}*{other.units})"
        else:
            units = f"({self.units}^2)"
        if self.analyte != other.analyte:
            analyte = "Unk"
        else:
            analyte = self.analyte
        val = self.value * other.value
        err = val * math.sqrt((self.error/self.value)**2 + (other.error/self.value)**2)
        result = datum(val, err, units, analyte)
        return result
    
    def __truediv__(self, other):
        if self.units != other.units:
            units = f"({self.units}/{other.units})"
        else:
            units = ""
        if self.analyte != other.analyte:
            analyte = "Unk"
        else:
            analyte = self.analyte
        val = self.value / other.value
        err = val * math.sqrt((self.error/self.value)**2 + (other.error/self.value)**2)
        result = datum(val, err, units, analyte)
        return result
    
    def __pow__(self, other): #self ** other
        val = self.value ** other.value
        err = abs(val * other.value * (self.error/self.value))
        units = f"({self.units}^{other.units})"
        analyte = "unk"
        result = datum(val, err, units, analyte)
        return result
    
    def __rpow__(self, other): #other ** self
        val = other.value ** self.value
        err = abs(val * self.value * (other.error/other.value))
        units = f"({other.units}^{other.units})"
        analyte = "unk"
        result = datum(val, err, units, analyte)
        return result
    
    def __neg__(self):
        val = -self.value
        err = self.error
        units = self.units
        analyte = self.analyte
        result = datum(val, err, units, analyte)
        return result
    
    def __abs__(self):
        val = abs(self.value)
        err = self.error
        units = self.units
        analyte = self.analyte
        result = datum(val, err, units, analyte)
        return result

    def __round__(self):
        val = round(self.value, self.errorder)
        err = round(self.error, self.errorder)
        units = self.units
        analyte = self.analyte
        result = datum(val, err, units, analyte)
        return result

    def log(self):
        val = math.log10(self.value)
        err = abs(0.434 * (self.error/self.value))
        units = f"Log({self.units})"
        analyte = self.analyte
        result = datum(val, err, units, analyte)
        return result
    
    def ln(self):
        val = math.log(self.value)
        err = abs((self.error/self.value))
        units = f"Ln({self.units})"
        analyte = self.analyte
        result = datum(val, err, units, analyte)
        return result
    
    def exp(self):
        value = math.exp(self.value)
        err = math.sqrt(math.e ** (2*self.value) * (self.error **2))
        units = f"Exp({self.units})"
        analyte = self.analyte
        result = datum(value, err, units, analyte)
        return result

    def __lt__(self, other):
        return self.value < other.value
    
    def __gt__(self, other):
        return self.value > other.value    

    def __le__(self, other):
        return self.value <= other.value
    
    def __ge__(self, other):
        return self.value >= other.value
    
    def __eq__(self, other):
        return self.value == other.value
    
    def __ne__(self, other):
        return self.value != other.value


if __name__ == "__main__":
    d = datum(12.1167, 0.515, "m", "Length")
    print(d)
    # d2 = datum(10.1234, 0.04333, "m", "Length")
    # print(d2)
    # d3 = d + d2
    # print(d3)
    # d4 = d * d2
    # print(d4)
    # d5 = d / d2
    # print(d5)
