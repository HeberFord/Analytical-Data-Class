

import math

def StatError(error, tol = 0.34):
    """
    StateError: Function that determines the order of magnitude of the error \n
    where to round when reporting data with signficant figures \n
    determined by the first two non-zero digits in the error value \n
    with an allowance of up to tol for intermediate insignificant figures. \n
       
    :Float value: The actual value of the measurment \n
    :Float error: The actual error in the measurment\n
    :Float tol: tolerance for number of insignificant digits to include by 1/N \n
                for N insignificant digits max. Automatically set to 0.34 for \n
                3 max insignificant digits before rounding
    """
    str_err = str(error)
    Vals = 0
    mod_err = ""
    err_ord = 0
    for char in str_err :
        #print(f"Current Char: {char}")
        #print(f"Current Vals: {Vals}")
        if char == "0" and Vals == 0 or char == "." and Vals == 0:
            mod_err += char
            #print(mod_err)
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

def Errordet(error):
    """
    Errorsig: The function determines the correct function to enact for \n
    for different forms of error, whether statistical, propogated, or exact \n
    
    :float value: The Actual Measurment value \n
    :float error: The actual error in measurment \n
    """
    if error < 0:
        return ValueError("Error cannot be a negative value")
    if error == 0:
        return math.inf
    if error > 0:
        sig = StatError(error)
        return sig + 1

def rd(value, order):
    """
    rd: A function designed in order to either round values to a specific \n
    digit based on the order of the error input, or, if order is inf, \n
    return the value \n
    
    :Float value: Value desired to be rounded \n
    :Float order: Order of error in the value to be rounded \n
    """
    if order == math.inf:
        return value
    else:
        rdv = round(value, abs(order))
        return rdv
    
def sigfig(value): #Two issues rn, one if first sig fig is before decimals, and second is after, 
    str_val = str(value)
    sig = 0
    dec = -1
    for char in str_val :
        if char == "0" and sig == 0 or char == "." and sig == 0:
            if char == ".":
                dec += 1
            continue
        elif char != ".":
            if dec != -1:
                dec += 1
            sig += 1
            continue
        elif char == ".":
            dec += 1
            continue
        else:
            continue
    return (sig, dec)

class datum:
    """
    Docstring for datum
    """
    def __init__(self, value, Error, Units = "SI", Analyte = "Unk"):
        """
        Docstring for __init___ \n
        :param value: Description \n
        :param Error: Description \n
        :param Units: Description \n
        :param Analyte: Description \n
        """
        self.value = value #Actual value of the variable of interest
        self.error = Error
        self.units = Units
        self.analyte = Analyte
        self.errorder = Errordet(self.error)
        (self.sigfig, self.decsig) = sigfig(self.value)
    
    def __repr__(self):
        """
        Docstring for ___repr__
        """
        s = ""
        s += f"{rd(self.value, self.errorder)} +/- {rd(self.error, self.errorder)} {self.units} ({self.analyte}) with ({self.sigfig}) significant figures"
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
        if result.decsig > self.decsig:
            dif = result.decsig - self.decsig
            (result.sigfig, result.decsig) = (result.sigfig - dif, self.decsig)
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
    print(sigfig(d.value))
    d2 = datum(10.1234, 0.04333, "m", "Length")
    print(d2)
    d3 = d + d2
    print(d3)
    # d4 = d * d2
    # print(d4)
    # d5 = d / d2
    # print(d5)
