

import math
from mpmath import mp #Increases precision to prevent machine epsilon issues with sig figs

mp.dps = 100
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
    if error != str: #If error is not a string convert it to one
        str_err = str(error) 
    else:
        str_err = error
    Vals = 0  #Initialize variables to add to later
    mod_err = ""
    err_ord = 0
    for char in str_err : #Filter through each number in the value
        if char == "0" and Vals == 0 or char == "." and Vals == 0:
            mod_err += char
            continue #If 0 or . and have not yet hit a real digit just add and skip
        else:
            while Vals < 2: #If less than two sigfigs have been identified 
                if char != '0' and char != '.' and char != '1' and char != '2':
                    mod_err += char
                    Vals += 1
                    break #For significant digits add the character and count
                else:
                    mod_err += "0"
                    Vals += tol
                    err_ord += 1
                    break # for insignificant digits add them and count partial
    sig = float(mod_err)
    err_ord += int(abs(math.log10(sig)// 1))
    return err_ord

def Errordet(error):
    """
    Errorsig: The function determines the correct function to enact for \n
    for different forms of error, whether statistical, propogated, or exact \n
    
    :float value: The Actual Measurment value \n
    :float error: The actual error in measurment \n
    """
    if "-" in error: #If negative doesn't work
        return ValueError("Error cannot be a negative value")
    if error == "0": #If zero assume absolute precision
        return math.inf
    else: #else assume number and then just run into function 
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
    if order == math.inf: #if ind accuracy return number
        return value
    else:
        rdv = round(value, abs(order)) #Otherwise just round like normal
        return rdv
    
def sigfig(value):
    """
    sigfig takes a string input of the exact value entered strips spaces \n
    and leading zeros in order to count the number of significant digits. \n
     
    :string value: string or float of value to calculate sig figs of
    """
    if value != str: #Converts value to string if not
        str_val = str(value)
    else: str_val = value
    
    if "." in str_val: #Splitting into before and after decimal if it exists
        integ, decim = str_val.split(".")
    else:
        integ, decim = str_val, ""
    clean_int = integ.lstrip("0") #Strip leading zeroes
    int_sig = len(clean_int) #Count sig figs
    dec_clean = decim.lstrip("0")
    dec_sig = len(dec_clean)
    return (int_sig, dec_sig)

class datum:
    """
    The datum class is used for experimental data tracking and error propogation \n
    Refer to readme for more info
    """
    def __init__(self, value, Error, Units = "SI", Analyte = "Unk"):
        """
        Docstring for __init___ \n
        :float value: true value of experimental measurment \n
        :param Error: error in measured value \n
        :param Units: units of measured value \n
        :param Analyte: analyte of interest \n
        """
        self.raw_value = str(value) #Convert immediately to str
        self.raw_error = str(Error) #This preserves all info given w/o rding
        self.value = mp.mpf(value) #High precission storage for general prob
        self.error = mp.mpf(Error)
        self.units = Units
        self.analyte = Analyte
        self.errorder = Errordet(self.raw_error) #Determine order to round  
        (self.intsig, self.decsig) = sigfig(self.raw_value)
    
    def __repr__(self):
        """
        Docstring for ___repr__
        """
        s = ""
        s += f"{rd(self.value, self.errorder)} " 
        s += f"+/- {rd(self.error, self.errorder)} "
        s += f"{self.units} "
        s += f"({self.analyte}) "
        s += f"with {self.intsig + self.decsig} significant figures"
        return s

    def __add__(self, other):
        #Identify unit compatibility, analyte, then perform operation prop err
        #Last step is determining sig figs
        if self.units != other.units:
            raise ValueError("Units do not match, cannot perform addition")
        if self.analyte != other.analyte:
            analyte = "Unk"
        else:
            analyte = self.analyte
        val = self.value + other.value
        err = math.sqrt(self.error**2 + other.error**2)
        result = datum(val, err, self.units, analyte) 
        result.decsig = min(self.decsig, other.decsig)
        return result
    
    def __sub__(self, other):
        #Identify unit compatibility, analyte, then perform operation prop err
        #Last step is determining sig figs
        if self.units != other.units:
            raise ValueError("Units do not match, cannot perform addition")
        if self.analyte != other.analyte:
            analyte = "Unk"
        else:
            analyte = self.analyte
        val = self.value - other.value
        err = math.sqrt(self.error**2 + other.error**2)
        result = datum(val, err, self.units, analyte) 
        result.decsig = min(self.decsig, other.decsig)
        return result
    
    def __mul__(self, other):
        #Identify unit compatibility, analyte, then perform operation prop err
        #Last step is determining sig figs
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
        totsig = min(self.intsig + self.decsig, other.intsig + other.decsig)
        result.decsig = totsig - result.intsig
        if result.decsig < 0:
            result.intsig -= result.decsig
            result.decsig = 0
        return result
    
    def __truediv__(self, other):
        #Identify unit compatibility, analyte, then perform operation prop err
        #Last step is determining sig figs
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
        totsig = min(self.intsig + self.decsig, other.intsig + other.decsig)
        result.decsig = totsig - result.intsig
        if result.decsig < 0:
            result.intsig -= result.decsig
            result.decsig = 0
        return result
    
    def __pow__(self, other): #self ** other
        #Identify unit compatibility, analyte, then perform operation prop err
        val = self.value ** other.value
        err = abs(val * other.value * (self.error/self.value))
        units = f"({self.units}^{other.units})"
        analyte = "unk"
        result = datum(val, err, units, analyte)
        return result
    
    def __rpow__(self, other): #other ** self
        #Identify unit compatibility, analyte, then perform operation prop err
        val = other.value ** self.value
        err = abs(val * self.value * (other.error/other.value))
        units = f"({other.units}^{other.units})"
        analyte = "unk"
        result = datum(val, err, units, analyte)
        return result
    
    def __neg__(self):
        #Identify unit compatibility, analyte, then perform operation prop err
        val = -self.value
        err = self.error
        units = self.units
        analyte = self.analyte
        result = datum(val, err, units, analyte)
        return result
    
    def __abs__(self):
        #Identify unit compatibility, analyte, then perform operation prop err
        val = abs(self.value)
        err = self.error
        units = self.units
        analyte = self.analyte
        result = datum(val, err, units, analyte)
        return result

    def __round__(self):
        #Identify unit compatibility, analyte, then perform operation prop err
        val = round(self.value, self.errorder)
        err = round(self.error, self.errorder)
        units = self.units
        analyte = self.analyte
        result = datum(val, err, units, analyte)
        return result

    def log(self):
        #Identify unit compatibility, analyte, then perform operation prop err
        val = math.log10(self.value)
        err = abs(0.434 * (self.error/self.value))
        units = f"Log({self.units})"
        analyte = self.analyte
        result = datum(val, err, units, analyte)
        return result
    
    def ln(self):
        #Identify unit compatibility, analyte, then perform operation prop err
        val = math.log(self.value)
        err = abs((self.error/self.value))
        units = f"Ln({self.units})"
        analyte = self.analyte
        result = datum(val, err, units, analyte)
        return result
    
    def exp(self):
        #Identify unit compatibility, analyte, then perform operation prop err
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
    d = datum(5.1117, 0.519, "m", "Length")
    # print(d)
    # print(d.decsig+d.intsig)
    d2 = datum(5.1214, 0.04333, "m", "Length")
    # print(d2)
    # print(d2.decsig+d2.intsig)
    # d3 = d + d2
    # print(d3)
    # print(d3.intsig)
    # d4 = d * d2
    # print(d4)
    d5 = d / d2
    print(d5)
    print(d5.errorder)
