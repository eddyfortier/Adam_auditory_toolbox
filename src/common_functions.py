import os
import pandas as pd
# import numpy as np
# import matplotlib.cm as cm
import colorama as color

# Initialize colorama
color.init(autoreset=True)

"""
SCRIPT DESCRIPTION:

This script contains general use functions that are used by multiple scripts
during a variety of different tasks:
    - BIDS-compatible dataset generation
    - test data graph generation
    - data analysis reports

It is not designed to be used as a standalone script, but rather as a slave to
another script:
    - BIDS_formater.py
"""


if __name__ == "__main__":
    print(
        color.Fore.RED
        + ("ERROR: This script is not designed to be used as a "
           "standalone script.")
    )


else:
    def retrieve_db(data_path, method):
        """
        This function gives the user a choice on how to retrieve the database.
        Available options are:
            -> The user manually supplies a URL to a properly formated
               Google Spreadsheet
            -> The user provides the URL through the use of a URL.tsv file
               in the data folder ([repo_root]/data/URL.tsv)
            -> The user provides a properly formated database in a
               test_database.xlsx file in the data folder
               ([repo_root]/data/test_database.xlsx)
        INPUTS:
        -data_path: path to the [repo_root]/data folder
        -method: method used to activate this function.
                 The valid means are:
                    -"master_script": the Adam_auditory_toolbox.py script
                                      activates this function.
                    -"standalone": one of the scripts in the src/ folder is
                                   activated as a standalone script and is
                                   using this fonction.
        OUTPUTS:
        -returns the database in a pandas dataframe
        """

        # Available functions list
        ls_fct = ["Retrieve from a user supplied URL (Google Spreadsheet)",
                  "Use the URL listed in the [repo_root]/data/URL.tsv file",
                  ("Retrieve locally from the "
                   "[repo_root]/data/test_database.xlsx file"),
                 # "Dummy line",
                 ]

        # Prompt text generation
        prompt_instruction = ("Please specify the database retrieval "
                              "method you want to use:")

        prompt_options = ""

        for i, element_i in enumerate(ls_fct):
            prompt_options += f"\n {str(i+1)}-{element_i}"

        if method == "master_script":
            prompt_options += (f"\n {str(len(ls_fct)+1)}"
                               "-Return to the main menu\n")
        elif method == "standalone":
            prompt_options += f"\n {str(len(ls_fct)+1)}-Exit\n"
        else:
            print(color.Fore.RED
                  + (f"ERROR: The specified database retrieval method "
                     f"variable (\"{method}\") is invalid.\n")
                  + ("\nValid method variables are \"master_script\" and "
                     "\"standalone\".\n"))
            exit()

        prompt_txt = prompt_instruction + prompt_options

        # While loop condition initialization
        loop_value = True

        # function selection prompt
        while loop_value:

            value = input(prompt_txt)
            print("\n")

            # Value validity verification
            # Is it a valid number?
            if value.isdigit():
                value = int(value)

                # Is it within the range of the options?
                if value > 0 and value <= len(ls_fct) + 1:

                    # Loop breaks if the "Exit" option is selected
                    if value == len(ls_fct) + 1 and method == "master_script":
                        raise RuntimeError("Return to the main menu")
                    
                    elif value == len(ls_fct) + 1 and method == "standalone":
                        #print(color.Fore.RED
                        #      + ("ERROR: The provided value is not valid "
                        #         "(out of bound).\n"))
                        #continue
                        exit()

                    # The encased section contains the subscript calls.
                    # If functionality are to be added, here is where to
                    # add them (Don't forget to also add them to the list
                    # of available functions: ls_fct).
                    ###########################################################

                    else:

                        # User is to supply a URL
                        if ls_fct[value - 1].count("user supplied URL") == 1:
                            url_share = input("Enter the Google "
                                              "Spreadsheet URL: ")
                            print("\n")
                            url_csv = url_share.replace("/edit#gid=",
                                                        "/export?"
                                                        "format=csv&gid=")
                            df = pd.read_csv(url_csv, sep=',', na_filter=True)
                            return df

                        # Use the URL.tsv file
                        elif ls_fct[value - 1].count("URL.tsv") == 1:
                            filename = os.path.join(data_path, "URL.tsv")
                            df_URL = pd.read_csv(filename, sep="\t")
                            url_share = df_URL["test_database"][0]
                            url_csv = url_share.replace("/edit#gid=",
                                                        "/export?"
                                                        "format=csv&gid=")
                            df = pd.read_csv(url_csv, sep=',', na_filter=True)
                            return df

                        # Test Dummy
                        elif ls_fct[value - 1].count("Dummy") == 1:
                            print("This is just a test line:",
                                  ls_fct[value - 1], "\n")

                    ###########################################################

                else:
                    # If it is not within range, restart the loop
                    print(color.Fore.RED
                          + ("ERROR: The provided value is not valid "
                             "(out of bound).\n"))
                    continue

            else:
                # If it is not a number, restart the loop
                print(color.Fore.RED
                      + ("ERROR: The provided value is not valid "
                         "(not a digit).\n"))
                continue

    def bidsify_ID(ID):
        """
        This function verifies that a subject ID is compliant with BIDS
        standards. If it is not, it modifies it to comply with BIDS standards.
        INPUTS:
        -ID: subject ID to be evaluated
        OUTPUT:
        -returns the original ID if it is compliant, returns an adapted ID if
         the original was not compliant
        """

        #print("ID before", ID)

        if ID.count(" ") != 0:
            ls_ID = ID.split(" ")
            ID = "".join(ls_ID)
        else:
            pass

        if ID.count("-") != 0:
            ls_ID = ID.split("-")
            ID = "".join(ls_ID)
        else:
            pass

        if ID.count("_") != 0:
            ls_ID = ID.split("_")
            ID = "".join(ls_ID)
        else:
            pass

        if ID.startswith("sub"):
            ID = ID.lstrip("sub")
        elif ID.startswith("Sub"):
            ID = ID.lstrip("Sub")
        elif ID.startswith("SUB"):
            ID = ID.lstrip("SUB")
        else:
            pass

        #print("ID after", ID)

        return ID

    def create_folder_subjects(subject, parent_path):
        """
        This function creates by-subject folders in a specified folder
        INPUTS:
        -subject: subject ID used by the script or the database's
                  dataframe
        -parent_path: path to get inside the specified folder
        OUTPUTS:
        -folder for the provided subject ID in the BIDS_data/ folder
        -NO specific return to the script
        USED BY:
        -BIDS_formater.py
        -report_PTA.py
        """

        dir_content = os.listdir(parent_path)
        dir_content.sort()

        sub_lower = subject.lower()

        if sub_lower.startswith("sub"):
            sub_ID = ""

            for i in sub_lower:
                if i.isdigit():
                    sub_ID += i
                else:
                    continue

            subject = sub_ID

        else:
            pass

        if dir_content.count(f"sub-{subject}") == 1:
            print(f"The subject's subfolder for sub-{subject} is present.\n")
        else:
            os.mkdir(os.path.join(parent_path, f"sub-{subject}"))
            print(f"The subject's subfolder for sub-{subject} was created.\n")

    def baseline_ID():
        """
        This function prompt the user with a list of possible baseline
        sessions to be used as a reference and returns the index value of the
        selected session
        INPUTS:
        -NO specific input
        OUTPUTS:
        -returns the index of the selected baseline session (for the
         sub-0X_sessions.tsv file)
        USED BY:
        -
        """

        ls_baseline = ["Baseline #1 (November 2018 - July 2019)",
                       "Baseline #2 (January - February 2021)"]

        prompt_instruction = ("Please select which one of the available "
                              "baseline sessions you want to use as "
                              "reference.")

        prompt_options = ""

        for i in range(0, len(ls_baseline)):
            prompt_options += ("\n " + str(i+1) + "-" + ls_baseline[i])

        prompt_options += ("\n "
                           + str(len(ls_baseline)+1)
                           + "-Return to the main menu\n"
                          )

        prompt_text = prompt_instruction + prompt_options

        loop_value = True

        while loop_value:
            value = input(prompt_text)
            print("\n")

            if value.isdigit():
                value = int(value)

                # Is it within the range of the options?
                if value > 0 and value <= len(ls_baseline) + 1:

                    # Loop breaks if the "Exit" option is selected
                    if value == len(ls_baseline) + 1:
                        raise RuntimeError("Return to the main menu")

                    else:
                        if ls_baseline[value - 1].startswith("Baseline #1"):
                            bsl_ID = 0
                        elif ls_baseline[value - 1].startswith("Baseline #2"):
                            bsl_ID = 1

                        print("\n")
                        loop_value = False

                else:

                    # If it is not within range, restart the loop
                    print(color.Fore.RED
                          + ("The provided value is not valid (out of "
                             "bound).\n"))
                    continue

            else:

                # If it is not a number, restart the loop
                print(color.Fore.RED
                      + "The provided value is not valid (not a digit).\n")
                continue

        return bsl_ID
