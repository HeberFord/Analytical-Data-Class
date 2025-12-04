

import math

def StatError(value, error):
    str_err = str(error)
    Vals = 0
    #for Vals < 2:
    for char in str_err :
        if char != '0' and char != '.' and Vals == 0:
            mod_err = char
            continue
        else:
            while Vals < 2:
                if char != '0' and char != '.':
                    mod_err += char
                    Vals += 1
                    break
                else:
                    mod_err += char
                    vals += 0.51
                    break
    sig = float(mod_err)
    err_ord = abs(math.log10(sig)// 1)
    
    return err_ord
                        

    


def ErrorSig(value, error):
    if error < 0:
        return ValueError("Error cannot be a negative value")
    if error == 0:
        return math.inf
    if error > 0:
        sig = StatError(value, error)
        return sig


class datum:
    
    def __init___(self, value, Error, Units, Analyte):
        self.value = value #Actual value of the variable of interest
        self.error = Error
        self.units = Units
        self.analyte = Analyte
        self.sig = ErrorSig(self.value, self.error)
    



if __name__ == "__main__":
    d = datum(12.54667, 0.23445, "m", "Length")
    