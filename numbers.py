def makenumbers():
    digits = {
        "ONE": 1,
        "TWO": 2,
        "THREE": 3,
        "FOUR": 4,
        "FIVE": 5,
        "SIX": 6,
        "SEVEN": 7,
        "EIGHT": 8,
        "NINE": 9
    }

    teens = {
        "TEN": 10,
        "ELEVEN": 11,
        "TWELVE": 12,
        "THIRTEEN": 13,
        "FOURTEEN": 14,
        "FIFTEEN": 15,
        "SIXTEEN": 16,
        "SEVENTEEN": 17,
        "EIGHTEEN": 18,
        "NINETEEN": 19
    }

    tens = {
        "TWENTY": 20,
        "THIRTY": 30,
        "FORTY": 40,
        "FIFTY": 50,
        "SIXTY": 60,
        "SEVENTY": 70,
        "EIGHTY": 80,
        "NINETY": 90
    }
    hundreds = {
        "ONEHUNDRED": 100,
        "TWOHUNDRED": 200
    }
    prehundred = {}
    for k, v in digits.iteritems():
        prehundred[k] = v
    for k, v in teens.iteritems():
        prehundred[k] = v
    for k, v in tens.iteritems():
        prehundred[k] = v
        for ki, vi in digits.iteritems():
            prehundred[k+ki] = v+vi

    numbers = {}
    for k, v in prehundred.iteritems():
        numbers[k] = v
    for k, v in hundreds.iteritems():
        numbers[k] = v
        for ki, vi in prehundred.iteritems():
            if not (v == 200 and vi > 55):
                numbers[k+"AND"+ki] = v+vi

    numbers["ZERO"] = 0
    return numbers

numbers = makenumbers()
del makenumbers
