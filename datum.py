

import math

def StatError(error, tol = 0.51):
    """
    Docstring for StatError
    
    :param value: Description
    :param error: Description
    :param tol: Description
    """
    str_err = str(error)
    Vals = 0
    mod_err = ""
    for char in str_err :
        if char == '0' and char == '.' and Vals == 0:
            mod_err += char
            continue
        else:
            while Vals < 2:
                if char != '0' and char != '.' and char != "1" and char != "2":
                    mod_err += char
                    Vals += 1
                    break
                else:
                    mod_err += char
                    Vals += tol
                    break
    sig = float(mod_err)
    err_ord = int(abs(math.log10(sig)// 1))
    
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
        val = self.value + other.value
        err = math.sqrt(self.error**2 + other.error**2)
        result = datum(val, err, self.units, self.analyte) #Maybe preclude analyte?
        return result


if __name__ == "__main__":
    d = datum(12.54667, 0.23445, "m", "Length")
    print(d)
