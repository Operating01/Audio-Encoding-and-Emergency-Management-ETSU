import tones
import pandas
import time


# NEW ACSCII USES 7 BITS, MOST SIGNIFICANT BIT IS 0
# ALSO LOOK INTO UTF8 OVER ASCII
# Look into if decoding libraies already decode using isochronous 

# Tones Documentation: https://tones.readthedocs.io/en/latest/ 
################## SET-UP ##################
from tones import SINE_WAVE, SAWTOOTH_WAVE
from tones.mixer import Mixer

# Create mixer, set sample rate and amplitude
mixer = Mixer(44100, 0.5)

# Create two monophonic tracks that will play simultaneously, and set
# initial values for note attack, decay and vibrato frequency (these can
# be changed again at any time, see documentation for tones.Mixer
mixer.create_track(0, SINE_WAVE, vibrato_frequency=0, vibrato_variance=0, attack=0, decay=0)

bit_duration = .03
last_bit_duration = .05
bit_rate = 1 / bit_duration


################## FUNCTIONS ##################

def createMessage(input):
    # Encodes the text into binary, resembling utf-8
    binary_output = ''.join(format(byte, '08b') for byte in input.encode('utf-8'))
    print("Binary output:", binary_output)
    print("Number of bits:", len(binary_output))
    # If the bit is detected to be the last, then the tone is increased to .05s instead of .03s
    for i, digit in enumerate(binary_output):
        duration = last_bit_duration if i == len(binary_output) - 1 else bit_duration

        if digit == "1":
            mixer.add_tone(0, frequency=2308.5, duration=duration)
        else:
            mixer.add_tone(0, frequency=1312.5, duration=duration)

    mixer.write_wav('tones.wav')


def menuHandling(filename):
    menu = pandas.read_csv(filename)

    while True:
        i = 1

        for row in menu.itertuples():
            print(i, "). ", row[1])
            i += 1

        selection = input("Input the number corresponding to what you would like to select: ")

        try:
            # Check whether this is a location/building menu
            if ("location" in filename.lower() or
                "loc" in filename.lower() or
                "building" in filename.lower()):

                # Break the input into individual selections
                selections = selection.split(",")

                # Convert selections into integers
                selections = [int(number.strip()) for number in selections]

                # Check that every selection is within the menu range
                for number in selections:
                    if number < 1 or number > len(menu):
                        print(
                            "Selection", number,
                            "isn't within the range of possible options!"
                        )
                        print("Please enter a number between 1 and", len(menu), "!")
                        break
                else:
                    # Retrieve each selected row using its zero-based index
                    result = [menu.iloc[number - 1] for number in selections]
                    print(result)
                    return result

            else:
                # Standard single-selection menu
                result = menu.iloc[int(selection) - 1]
                return result

        except (ValueError, TypeError):
            print("Please enter a basic number, with no letters or decimals!")
            time.sleep(1)

        except IndexError:
            print("This isn't within the range of possible options!")
            print("Please enter a number between 1 and", len(menu), "!")


################## MAIN LOOP ##################

