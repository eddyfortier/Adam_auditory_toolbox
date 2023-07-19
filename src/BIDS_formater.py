import os
import pandas as pd
import json
import colorama as color
# import glob

from datetime import datetime as date
from shutil import copyfile

from src import BIDS_utils as utils
from src import common_functions as common

"""
SCRIPT DESCRIPTION:

This script transforms the auditory test data saved as .csv (OAE tests) or
placed in a properly formatted spreadsheet (other tests).
Spreadsheet template available here (under CC0 license)
[ https://docs.google.com/spreadsheets/d/
  1aKakQJvJnvPUouTUciGm3FMlnNAGIX8NXhulbhjq9d4/edit?usp=sharing ]

This script uses the BIDS_formater.py and common_functions.py scripts to be
able to process data and generate a BIDS-format compatible dataset out of
auditory test data. It will also activate json_sidecar_generator.py if needed.

It can either be used as a standalone script or be used through the UI master
script, Adam_auditory_toolbox.py.
"""

utf = "UTF-8-SIG"


# Specify the protocol conditions including OAE tests
#condition_OAE = ["Baseline",
#                 "Condition 2 (2-7 days post-scan)",
#                 "Condition 3A (OAEs right before the scan)",
#                 "Condition 3B (OAEs right after the scan)"]

# Specifiy the different tests used in those different protocol conditions
#ls_test = ["Tymp", "Reflex", "PTA", "MTX", "TEOAE", "DPOAE",
#           "DPGrowth_2kHz", "DPGrowth_4kHz", "DPGrowth_6kHz"]


def fetch_db(data_path):
    """This function retrieves a database to work on.
    INPUTS:
    -data_path: path to the [repo_root]/data/ folder
    OUTPUTS:
    -returns a dataframe containing the database to use
    """

    df = common.retrieve_db(data_path, "standalone")

    # Manage the empty boxes
    df.fillna(value='n/a', inplace=True)

    return df


def fetch_oae_data(data_path):
    """This function retrieves the list of OAE test data files
    INPUTS:
    -data_path: path to the [repo_root]/data/auditory_tests/ folder
    OUTPUTS
    -returns: - the path to the OAE test data folder
              - the list of all the OAE test data filenames
              - a dataframe containing a by-test breakdown information:
                  - the participant ID
                  - the session experimental condition and date
                  - the type of test
                  - the tested ear
    """

    path = os.path.join(data_path, "OAE")
    try:
        ls_file = os.listdir(path)
    except FileNotFoundError as error:
        #print(error, "\n")
        #print(error.args[1], "\n")
        #print(type(error.args[1]), "\n", "\n")
        if error.args[0] == 2 and error.args[1] == "No such file or directory":
            raise RuntimeError("The OAE data folder is missing.")
        else:
            pass

    ls_of_ls = []

    for i in ls_file:
        single_test_ls = i.rstrip(".csv").split("_")
        ls_of_ls.append(single_test_ls)

    df = pd.DataFrame(ls_of_ls,
                      columns=["Participant_ID",
                               "Condition",
                               "Test",
                               "Ear"])

    return path, ls_file, df


def subject_extractor(df, subject_ID):
    """
    This function extracts from the database all the lines that are linked to a
    single participant and returns them into a new dataframe.
    INPUTS:
    -df: database in a pandas dataframe format
    -subject_ID: the subject ID to look for in the Participant_ID column of the
                 dataframe
    OUTPUTS:
    -returns a dataframe containing only the selected participant's lines
    """

    mask = df['Participant_ID'] == subject_ID
    sub_df = df[mask].reset_index(drop=True)

    return sub_df


# Check if the session-level folders exist for each participant
# If not, create them
def create_folder_session(subject, session_count, parent_path):
    """
    This function creates by-session folders in the BIDS_data/sub-0*/ folder
    INPUTS:
    -subject: subject ID used in the database's dataframe (format: Sub0X or
              sub-0x)
    -session_count: number of line(s) in the by-subject dataframe
    OUTPUTS:
    -folders for each session in the provided subject's folder
    -returns the list of the session folder names
    """

    #print(parent_path)

    if subject.startswith("Sub"):
        sub_ID = subject.lstrip("Sub")
        children_path = os.path.join(parent_path, f"sub-{sub_ID}")

    elif subject.startswith("sub"):
        sub_ID = subject.lstrip("sub")
        children_path = os.path.join(parent_path, f"sub-{sub_ID}")

    else:
        children_path = os.path.join(parent_path, f"sub-{subject}")

    dir_content = os.listdir(children_path)

    ls_ses = []

    for j in range(1, session_count + 1):
        if dir_content.count(f"ses-{j:02d}") == 1:
            ls_ses.append(f"ses-{j:02d}")
        else:
            os.mkdir(os.path.join(children_path, f"ses-{j:02d}"))
            ls_ses.append(f"ses-{j:02d}")

    #print(children_path)

    return ls_ses, children_path


def master_run(data_path, result_path, var_json):
    """
    This is the master function that activates the others.
    INPUTS:
    -data_path: path to the data folder ([repo_root]/data/)
    -result_path: path to the results folder ([repo_root]/results/)
    -var_json: frequent-variables dictionary
    OUTPUTS:
    -NO specific return to the script (highest function level)
    -prints some feedback to the user in the terminal
    """

    # Create a list of the subjects and a reference path for the results
    subjects = var_json["subjects"]

    # Create two lists of subject IDs to establish a concordence file between
    # the original IDs and the bidsified IDs
    ls_id_og = []
    ls_id_bids = []

    # Generate the column titles to be used in the tsv files
    x_tymp = var_json["tsv_columns"]["x_tymp"]
    x_reflex = var_json["tsv_columns"]["x_reflex"]
    x_PTA = var_json["tsv_columns"]["x_PTA"]
    x_MTX = var_json["tsv_columns"]["x_MTX"]
    x_teoae = var_json["tsv_columns"]["x_teoae"]
    x_dpoae = var_json["tsv_columns"]["x_dpoae"]
    x_growth = var_json["tsv_columns"]["x_growth"]

    # Specify the protocol conditions including OAE tests
    #condition_OAE = var_json["condition_OAE"]

    # Specify the columns to be used for each test
    # -> Subject and session settings data
    columns_conditions = var_json["columns_conditions"]

    # Specifiy the different tests used in those different protocol conditions
    ls_test = var_json["ls_test"]

    # retrieve a database
    df = fetch_db(data_path)
    #print(df)
    auditory_test_path = os.path.join(data_path, "auditory_tests")

    try:
        (oae_folder_path,
         oae_file_list,
         oae_tests_df) = fetch_oae_data(auditory_test_path)

    except RuntimeError as error:
        if error.args[0] == "The OAE data folder is missing.":
            oae_folder_path = os.path.join(auditory_test_path, "OAE")
            skip_oae = True
            print(color.Fore.YELLOW
                  + (f"WARNING: The following path does not exist "
                     f"\"{oae_folder_path}\".\n"))
        else:
            skip_oae = False
            raise

    # Verifications:
    # - existence of the "results" folder
    # - existence of the "BIDS_data" folder
    # - existence of the json sidecar originals
    #   (tymp, reflex, PTA, MTX, OAE, sessions)
    # If not, creates them.
    utils.result_location(result_path)

    parent_path = os.path.join(result_path, "BIDS_data")
    
    # Add the .json sidecar files in the BIDS_data folder
    json_origin = os.path.join(result_path, "BIDS_sidecars_originals")

    copyfile(os.path.join(json_origin, "sessions.json"),
             os.path.join(parent_path, "sessions.json"))
    copyfile(os.path.join(json_origin, "task-Tymp_beh.json"),
             os.path.join(parent_path, "task-Tymp_beh.json"))
    copyfile(os.path.join(json_origin, "task-Reflex_beh.json"),
             os.path.join(parent_path, "task-Reflex_beh.json"))
    copyfile(os.path.join(json_origin, "task-PTA_beh.json"),
             os.path.join(parent_path, "task-PTA_beh.json"))
    copyfile(os.path.join(json_origin, "task-MTX_beh.json"),
             os.path.join(parent_path, "task-MTX_beh.json"))
    copyfile(os.path.join(json_origin, "task-TEOAE_beh.json"),
             os.path.join(parent_path, "task-TEOAE_beh.json"))
    copyfile(os.path.join(json_origin, "task-DPOAE_beh.json"),
             os.path.join(parent_path, "task-DPOAE_beh.json"))
    copyfile(os.path.join(json_origin, "task-DPGrowth_beh.json"),
             os.path.join(parent_path, "task-DPGrowth_beh.json"))

    # Initialize empty lists to be filled with the proper column titles
    # for each test
    columns_tymp = []
    columns_tymp_R = []
    columns_tymp_L = []

    columns_reflex = []
    columns_reflex_R = []
    columns_reflex_L = []

    columns_PTA = []
    columns_PTA_R = []
    columns_PTA_L = []

    columns_MTX = []
    columns_MTX_L1 = []
    columns_MTX_L2 = []

    # Generate column title lists to be able to extract the data for each test
    for i in df.columns:
        if i.endswith("_RE") is True:
            columns_tymp.append(i)
            columns_tymp_R.append(i)
        elif i.endswith("_LE") is True:
            columns_tymp.append(i)
            columns_tymp_L.append(i)
        elif i.startswith("REFLEX_RE_") is True:
            columns_reflex.append(i)
            columns_reflex_R.append(i)
        elif i.startswith("REFLEX_LE_") is True:
            columns_reflex.append(i)
            columns_reflex_L.append(i)
        elif i.startswith("RE_") is True:
            columns_PTA.append(i)
            columns_PTA_R.append(i)
        elif i.startswith("LE_") is True:
            columns_PTA.append(i)
            columns_PTA_L.append(i)
        elif i.startswith("MTX1") is True:
            columns_MTX.append(i)
            columns_MTX_L1.append(i)
        elif i.startswith("MTX2") is True:
            columns_MTX.append(i)
            columns_MTX_L2.append(i)

    for i in subjects:
        #print(i)

        ls_id_og.append(i)
        #print(ls_id_og)

        # Check if the subject ID is BIDS compatible
        # If not, it modifies it to comply with BIDS standards
        bids_id = common.bidsify_ID(i)

        # Check if the new bidsified ID creates a conflict with another
        # a previous bidsified ID
        if bids_id in ls_id_bids:
            index_bids_1 = ls_id_bids.index(bids_id)
            index_bids_2 = len(ls_id_bids)
            og_problem_1 = ls_id_og[index_bids_1]
            og_problem_2 = ls_id_og[index_bids_2]

            print(
                color.Style.BRIGHT
                + color.Fore.RED
                + f"CRITICAL ERROR: Two participants IDs ({og_problem_1} and "
                  f"{og_problem_2} are generating a conflict once they are "
                  f"adapted to BIDS standard: they both become sub-{bids_id}. "
                  "\nPlease modify one of the previously mentioned IDs (both "
                  "in the dataset and the variables.json file) and run this "
                  "pipeline again.\n"
            )

            raise RuntimeError("BIDSified ID conflict")

        else:
            ls_id_bids.append(bids_id)

        #print(ls_id_bids)

        # Check if the subject-level folders exist
        # If not, create them
        common.create_folder_subjects(bids_id, parent_path)

        # Extraction of all the session for the subject
        data_sub = subject_extractor(df, i)
        
        if skip_oae:
            pass
        else:
            data_oae_sub = subject_extractor(oae_tests_df, i)

        data_sub.insert(loc=3, column="Session_ID", value=None)

        # Add a session line for the post-scan OAE condition
        k = 0
        while k < len(data_sub):

            data_sub.loc[k, "Session_ID"] = f"{k+1:02d}"

            if (data_sub["Protocol condition"][k]
                    in var_json["OAE_only"]["exist_cond"]):
                key_oae_only = data_sub["Protocol condition"][k]
                txt_oae_only = var_json["OAE_only"]["cond_pair"][key_oae_only]

                sub_df_A = data_sub.iloc[:k+1]
                sub_df_B = data_sub.iloc[k+1:]

                sub_df_C = data_sub.copy()
                sub_df_C.drop(sub_df_C.index[k+1:], inplace=True)
                sub_df_C.drop(sub_df_C.index[0:k], inplace=True)

                sub_df_C.loc[k, "Protocol condition"] = txt_oae_only
                sub_df_C.loc[k, "Session_ID"] = f"{k+2:02d}"

                ls_columns = sub_df_C.columns.tolist()
                index_tests = ls_columns.index("Tymp_RE")
                del ls_columns[0:index_tests]

                for m in ls_columns:
                    sub_df_C.loc[k, m] = "n/a"

                data_sub = pd.concat([sub_df_A, sub_df_C, sub_df_B])
                data_sub.reset_index(inplace=True, drop=True)

                k += 1

            else:
                pass

            k += 1

        # Creation of a folder for each session
        ls_ses, subject_folder_path = create_folder_session(bids_id,
                                                            len(data_sub),
                                                            parent_path)

        # Extraction of the test columns
        tymp = utils.eliminate_columns(data_sub,
                                       columns_conditions,
                                       columns_tymp)
        reflex = utils.eliminate_columns(data_sub,
                                         columns_conditions,
                                         columns_reflex)
        pta = utils.eliminate_columns(data_sub,
                                      columns_conditions,
                                      columns_PTA)
        mtx = utils.eliminate_columns(data_sub,
                                      columns_conditions,
                                      columns_MTX)
        oae = data_sub[columns_conditions]

        #print(columns_PTA)
        #print(pta)

        # Replace PTA values "130" with "No response"
        for n in columns_PTA:
            for p in range(0, len(pta)):
                if pta.loc[p, n] == 130:
                    pta.loc[p, n] = "No response"
                else:
                    pass

        #print(pta)

        # Dataframe reconstruction
        utils.extract_tymp(tymp, columns_tymp_R,
                           columns_tymp_L, x_tymp,
                           subject_folder_path, bids_id)
        utils.extract_reflex(reflex, columns_reflex_R,
                             columns_reflex_L, x_reflex,
                             subject_folder_path, bids_id)
        utils.extract_pta(pta, columns_PTA_R,
                          columns_PTA_L, x_PTA,
                          subject_folder_path, bids_id)
        utils.extract_mtx(mtx, columns_MTX_L1,
                          columns_MTX_L2, x_MTX,
                          subject_folder_path, bids_id)

        if skip_oae:
            pass
        else:
            utils.extract_teoae(
                oae, data_oae_sub, oae_file_list, x_teoae,
                auditory_test_path, result_path, subject_folder_path,
                #bids_id
            )
            utils.extract_dpoae(
                oae, data_oae_sub, oae_file_list, x_dpoae,
                auditory_test_path, result_path, subject_folder_path,
                #bids_id
            )
            utils.extract_growth(
                oae, data_oae_sub, oae_file_list, x_growth,
                auditory_test_path, result_path, subject_folder_path,
                #bids_id
            )

        # .tsv session-level reference file creation
        column_reference = ["session_id", "session_name",
                            "condition", "delay", "scan_type"]

        for w in ls_test:
            column_reference.append(w)

        index_reference = []
        for x in range(0, len(ls_ses)):
            index_reference.append(x)

        ls_name = []
        ls_condition = []
        ls_delay = []
        ls_scan = []
        for y in range(0, len(data_sub)):

            # Calculation of the number of days since Baseline #1
            index_date_bsl = data_sub.index[(data_sub["Protocol name"]
                                             == "Baseline 1")].tolist()
            str_date_bsl = str(data_sub.at[index_date_bsl[0],
                               "Date"]).split(" ")
            date_bsl = date.strptime(str_date_bsl[0], "%Y-%m-%d")
            str_date_ses = str(data_sub.at[y, "Date"]).split(" ")
            date_ses = date.strptime(str_date_ses[0], "%Y-%m-%d")
            value_delay = date_ses - date_bsl

            ls_name.append(data_sub.at[y, "Protocol name"])
            ls_condition.append(data_sub.at[y, "Protocol condition"])
            ls_delay.append(value_delay.days)
            ls_scan.append(data_sub.at[y, "Scan type"])

        ref = pd.DataFrame(index=index_reference, columns=column_reference)

        for a in ref.index:
            ref.at[a, "session_id"] = ls_ses[a]
            ref.at[a, "session_name"] = ls_name[a]
            ref.at[a, "condition"] = ls_condition[a]
            ref.at[a, "delay"] = ls_delay[a]
            ref.at[a, "scan_type"] = ls_scan[a]

            ls_data = utils.retrieve_tests(subject_folder_path, ls_ses[a])

            if "Tymp" in ls_data:
                ref.at[a, "Tymp"] = "X"
            else:
                ref.at[a, "Tymp"] = ""

            if "Reflex" in ls_data:
                ref.at[a, "Reflex"] = "X"
            else:
                ref.at[a, "Reflex"] = ""

            if "PTA" in ls_data:
                ref.at[a, "PTA"] = "X"
            else:
                ref.at[a, "PTA"] = ""

            if "MTX" in ls_data:
                ref.at[a, "MTX"] = "X"
            else:
                ref.at[a, "MTX"] = ""

            if "TEOAE" in ls_data:
                ref.at[a, "TEOAE"] = "X"
            else:
                ref.at[a, "TEOAE"] = ""

            if "DPOAE" in ls_data:
                ref.at[a, "DPOAE"] = "X"
            else:
                ref.at[a, "DPOAE"] = ""

            if "Growth_2" in ls_data:
                ref.at[a, "DPGrowth_2kHz"] = "X"
            else:
                ref.at[a, "DPGrowth_2kHz"] = ""

            if "Growth_4" in ls_data:
                ref.at[a, "DPGrowth_4kHz"] = "X"
            else:
                ref.at[a, "DPGrowth_4kHz"] = ""

            if "Growth_6" in ls_data:
                ref.at[a, "DPGrowth_6kHz"] = "X"
            else:
                ref.at[a, "DPGrowth_6kHz"] = ""

        ref.set_index("session_id", inplace=True)

        ref_name = i + "_sessions"
        ref_save_path = os.path.join(subject_folder_path, ref_name + ".tsv")
        ref.to_csv(ref_save_path, sep="\t")

        print(
            f"The tsv and json files for sub-{bids_id} ({i}) have been "
            "created.\n"
        )

    dict_id_match = {"og_ID": ls_id_og, "BIDS_ID": ls_id_bids}

    df_id_match = pd.DataFrame(dict_id_match)
    #print(df_id_match)
    id_match_save_path = os.path.join(parent_path,
                                      "subject_ID_concordance.tsv")
    #print(id_match_save_path)
    df_id_match.to_csv(id_match_save_path, sep="\t")

    # This code section is present if, for any reason, the .tsv files are not
    # properly saved. You will first need to activate the "import glob" line
    # (line 3). It is then possible to replace the variable "ext"'s value in
    # the save_df function (BIDS_utils.py) with ".csv" and rerun the script
    # with this section to rename all the files with the correct ".tsv" file
    # extension.

    # file_list = glob.glob(os.path.join(parent_path, "sub-*/ses-*/*.csv"))

    # for path in file_list:
    #     new_path = os.path.splitext(path)[0]+".tsv"
    #     os.system(f"mv {path} {new_path}")


if __name__ == "__main__":
    root_path = ".."

    with open(os.path.join(root_path, "variables.json"), "r") as origin:
        var_json = json.load(origin)
    origin.close()

    # Path initializations
    data_path = os.path.join(root_path, var_json["path_var"]["data"])
    result_path = os.path.join(root_path, var_json["path_var"]["result"])

    master_run(data_path, result_path, var_json)
    print("\n")


else:
    pass
