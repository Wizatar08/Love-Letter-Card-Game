def checkIntegerInput(userInput, lowest, highest):
  input2 = str(userInput);
  lowest2 = str(lowest);
  highest2 = str(highest);
  if not input2.isdigit() or not lowest2.isdigit() or not highest2.isdigit():
    return False;
  if int(input2) >= int(lowest2) and int(input2) <= input(highest2):
    return True;
  return False;

def checkInput(playerInput, validInputs):
  for validInput in validInputs: # Loop through all valid inputs
    if playerInput == validInput: # If one value in validInputs is the user input
      return True; # Return true
  return False; # Return false