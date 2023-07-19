import os
import json
import colorama as color

from src import BIDS_formater as formater
from src import json_sidecar_generator as jsg


# Initialize colorama
color.init(autoreset=True)

# Available functions list
ls_fct = [
    "BIDS format's json sidecars creation",
    "BIDS format's auditory data exporter",
    # "Dummy line",
]

# Prompt text generation
prompt_instruction = (
    color.Style.BRIGHT
    + "Please enter the number of the pipeline functionality you want to run:"
    + color.Style.RESET_ALL
)

prompt_options = ""

for i, element_i in enumerate(ls_fct):
    prompt_options += f"\n {str(i+1)}-{element_i}"

prompt_options += f"\n {str(len(ls_fct)+1)}-Exit\n"

prompt_txt = prompt_instruction + prompt_options

# While loop condition initialization
loop_value = True

# Show welcome message
print(
    color.Style.BRIGHT
    + color.Fore.YELLOW
    + "\nWelcome to the Adam_auditory_toolbox.\n"
)

# function selection prompt
while loop_value:

    # Show options and save the user selection
    value = input(prompt_txt)
    print("\n")

    try:
        # Value validity verification
        # Is it a valid number?
        if value.isdigit():
            value = int(value)

            # Is it within the range of the options?
            if value > 0 and value <= len(ls_fct) + 1:

                # Loop breaks if the "Exit" option is selected
                if value == len(ls_fct) + 1:
                    break

                # The encased section contains the subscript calls.
                # If functionality are to be added, here is where to add them.
                # (Don't forget to also add them to the list of available
                # functions: ls_fct)
                ###############################################################

                else:

                    # BIDS format functionalities
                    if ls_fct[value - 1].count("BIDS") == 1:

                        # json sidecar files generation
                        if ls_fct[value - 1] == (
                            "BIDS format's json sidecars creation"
                        ):
                            jsg.create_sidecars(os.path.join(".", "results"))
                            print("\n")

                        # BIDS compatible dataset formating
                        elif ls_fct[value - 1] == (
                            "BIDS format's auditory data exporter"
                        ):
                            with open("variables.json", "r") as origin:
                                var_json = json.load(origin)
                            origin.close()

                            formater.master_run("data", "results", var_json)
                            print("\n")

                    # Test Dummy
                    elif ls_fct[value - 1].count("Dummy") == 1:
                        print("This is just a test line:",
                              ls_fct[value - 1],
                              "\n")

    ###########################################################################

            else:

                # If it is not within range, restart the loop
                print(
                    color.Fore.RED
                    + "The provided value is not valid (out of bound).\n"
                )
                continue

        else:

            # If it is not a number, restart the loop
            print(
                color.Fore.RED
                + "The provided value is not valid (not a digit).\n"
            )
            continue

    # RuntimeError processing
    except RuntimeError as error:

        # If the submenu "Return to the main menu" option is selected
        if error.args[0] == "Return to the main menu":
            continue
        # If there is a BIDSified ID conflict
        elif error.args[0] == "BIDSified ID conflict":
            exit()
        else:
            raise

# Exit message
print(
    color.Style.BRIGHT
    + color.Fore.YELLOW
    + "Thanks for using the Adam_auditory_toolbox.\n"
)


#if __name__ == "__main__":
#    with open("variables.json", "r") as origin:
#        var_json = json.load(origin)
#    origin.close()

#    # Path initializations
#    data_path = var_json["path_var"]["data"]
#    result_path = var_json["path_var"]["result"]

#    # Show welcome message
#    print(
#        color.Style.BRIGHT
#        + color.Fore.YELLOW
#        + "\nWelcome to the Adam_auditory_toolbox.\n"
#    )
