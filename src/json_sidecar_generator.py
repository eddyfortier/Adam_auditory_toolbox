import os
import pandas as pd
import json
from pathlib import Path

utf = "UTF-8-SIG"

long_order = "Order of acquisition"

long_side = "Side of ear tested"

lvl_order = {"1": "First sequence acquired",
             "2": "Second sequence acquired"}

lvl_side = {"R": "Right ear", "L": "Left ear"}

lvl_ses_test = {"1": "Test data available for this type of test",
                "0": "No test data available for this type of test"}

ls_task = ["Tymp", "Reflex", "PTA",
           "MTX", "TEOAE", "DPOAE",
           "Growth"]

index = ["LongName", "Description", "Levels", "Units"]


def gen_df_tymp(var_json):
    """
    This function generates the tympanometry test (Tymp)
    sidecar dataframe.
    INPUTS:
    -var_json: config file with user-supplied values
    OUTPUTS:
    -returns a dataframe ready to be saved in a json format
    """

    keys_tymp = var_json["json"]["keys"]["tymp"]

    df_tymp = pd.DataFrame(index=index, columns=keys_tymp)

    dict_longname_tymp = {keys_tymp[3]: "Tympanometric peak pressure/"
                                        "Middle ear pressure",
                          keys_tymp[4]: "Equivalent ear canal volume",
                          keys_tymp[5]: "Static admittance/Compliance",
                          keys_tymp[6]: "Tympanometric width"}

    dict_desc_tymp = {keys_tymp[3]: "Maximal acoustic energy absorbance "
                                    "capacity of the tympanic membrane.",
                      keys_tymp[4]: "Volume of the auditory canal between "
                                    "the probe and the tympanic membrane.",
                      keys_tymp[5]: "Maximal acoustic energy absorbance "
                                    "capacity of the middle ear ossicles.",
                      keys_tymp[6]: "Pressure level at 50% of the "
                                    "tympanogram's peak."}

    dict_units_tymp = {keys_tymp[3]: "daPa",
                       keys_tymp[4]: "mL",
                       keys_tymp[5]: "mL",
                       keys_tymp[6]: "daPa"}

    for k_tymp in keys_tymp:
        if k_tymp == keys_tymp[0]:
            df_tymp.at[index[0],
                       k_tymp] = long_order
            df_tymp.at[index[2],
                       k_tymp] = lvl_order

        elif k_tymp == keys_tymp[1]:
            df_tymp.at[index[0],
                       k_tymp] = long_side
            df_tymp.at[index[2],
                       k_tymp] = lvl_side

        elif k_tymp == keys_tymp[2]:
            df_tymp.at[index[0],
                       k_tymp] = "Type of curve"
            df_tymp.at[index[1], k_tymp] = ("The type parameter is a "
                                            "simplified representation of the "
                                            "actual tympanogram curve. It "
                                            "provides an indication on the "
                                            "shape of the response curve and "
                                            "a clinical judgement on the "
                                            "normality of the result.")
            df_tymp.at[index[2],
                       k_tymp] = {"A": "Within normal mobility range",
                                  "Ad": "Presents a higher than expected "
                                        "mobility of the tympanic membrane",
                                  "As": "Presents a lower than expected "
                                        "mobility of the tympanic membrane",
                                  "B": "Presents a very low mobility of the "
                                       "tympanic membrane",
                                  "C": "Presents a lower fluid pressure in "
                                       "the middle ear than in the ear canal",
                                  "D": " *** DESCRIPTION TO BE ADDED *** ",
                                  "E": " *** DESCRIPTION TO BE ADDED *** "}

        else:
            df_tymp.at[index[0], k_tymp] = dict_longname_tymp[k_tymp]
            df_tymp.at[index[1], k_tymp] = dict_desc_tymp[k_tymp]
            df_tymp.at[index[3], k_tymp] = dict_units_tymp[k_tymp]

    return df_tymp


def gen_df_reflex(var_json):
    """
    This function generates the stapedial reflex test (Reflex)
    sidecar dataframe.
    INPUTS:
    -var_json: config file with user-supplied values
    OUTPUTS:
    -returns a dataframe ready to be saved in a json format
    """

    keys_reflex = var_json["json"]["keys"]["reflex"]

    df_reflex = pd.DataFrame(index=index, columns=keys_reflex)

    dict_desc_reflex = {"500_hz": "",
                        "1000_hz": "",
                        "2000_hz": "",
                        "4000_hz": ""}

    for k_ref in keys_reflex:
        if k_ref == keys_reflex[0]:
            df_reflex.at[index[0], k_ref] = long_order
            df_reflex.at[index[2], k_ref] = lvl_order

        elif k_ref == keys_reflex[1]:
            df_reflex.at[index[0], k_ref] = long_side
            df_reflex.at[index[2], k_ref] = lvl_side

        elif k_ref == keys_reflex[6]:
            df_reflex.at[index[0], k_ref] = (f"Stapedial reflex threshold "
                                             f"for broadband {k_ref}")
            df_reflex.at[index[1], k_ref] = ""
            df_reflex.at[index[3], k_ref] = "dB HL"

        else:
            keys_word_reflex = k_ref.replace("_", " ").title()
            df_reflex.at[index[0], k_ref] = (f"Stapedial reflex threshold "
                                             f"at {keys_word_reflex}")
            df_reflex.at[index[1], k_ref] = dict_desc_reflex[k_ref]
            df_reflex.at[index[3], k_ref] = "dB HL"

    return df_reflex


def gen_df_pta(var_json):
    """
    This function generates the pure-tone audiometry test (PTA)
    sidecar dataframe.
    INPUTS:
    -var_json: config file with user-supplied values
    OUTPUTS:
    -returns a dataframe ready to be saved in a json format
    """

    keys_pta = var_json["json"]["keys"]["pta"]

    df_pta = pd.DataFrame(index=index, columns=keys_pta)

    for k_pta in keys_pta:
        if k_pta == keys_pta[0]:
            df_pta.at[index[0], k_pta] = long_order
            df_pta.at[index[2], k_pta] = lvl_order

        elif k_pta == keys_pta[1]:
            df_pta.at[index[0], k_pta] = long_side
            df_pta.at[index[2], k_pta] = lvl_side

        else:
            keys_word_pta = k_pta.replace("_", " ").title()
            df_pta.at[index[0], k_pta] = f"Threshold at {keys_word_pta}"
            df_pta.at[index[1], k_pta] = (f"The participants are asked to "
                                          f"press a button when they hear a "
                                          f"sound. This value represents the "
                                          f"hearing threshold obtained with "
                                          f"a pure-tone at {keys_word_pta}.")
            df_pta.at[index[3], k_pta] = "dB HL"

    return df_pta


def gen_df_mtx(var_json):
    """
    This function generates the matrix speech-in-noise perception
    test (MTX) sidecar dataframe.
    INPUTS:
    -var_json: config file with user-supplied values
    OUTPUTS:
    -returns a dataframe ready to be saved in a json format
    """

    keys_mtx = var_json["json"]["keys"]["mtx"]

    df_mtx = pd.DataFrame(index=index, columns=keys_mtx)

    dict_longname_mtx = {"practice": "First condition of the sequence "
                                     "(see Description).",
                         "sp_bin_no_bin": "Second condition of the sequence "
                                          "(see Description).",
                         "sp_l_no_bin": "Third condition of the sequence "
                                        "(see Description).",
                         "sp_r_no_bin": "Fourth condition of the sequence "
                                        "(see Description).",
                         "sp_l_no_l": "Fifth condition of the sequence "
                                      "(see Description).",
                         "sp_r_no_r": "Sixth condition of the sequence "
                                      "(see Description)."}

    dict_desc_mtx = {"practice": "Speech presentation = Binaural/"
                                 "Noise presentation = Binaural. "
                                 "This condition is used as a practice/"
                                 "warm-up condition",
                     "sp_bin_no_bin": "Speech presentation = Binaural/"
                                      "Noise presentation = Binaural",
                     "sp_l_no_bin": "Speech presentation = Left ear/"
                                    "Noise presentation = Binaural",
                     "sp_r_no_bin": "Speech presentation = Right ear/"
                                    "Noise presentation = Binaural",
                     "sp_l_no_l": "Speech presentation = Left ear/"
                                  "Noise presentation = Left ear",
                     "sp_r_no_r": "Speech presentation = Right ear/"
                                  "Noise presentation = Right ear"}

    for k_mtx in keys_mtx:
        if k_mtx == keys_mtx[0]:
            df_mtx.at[index[0], k_mtx] = long_order
            df_mtx.at[index[2], k_mtx] = lvl_order

        elif k_mtx == keys_mtx[1]:
            df_mtx.at[index[0],
                      k_mtx] = "Language used for this sequence of acquisition"
            df_mtx.at[index[2], k_mtx] = {"French": "French",
                                          "English": "English"}

        else:
            df_mtx.at[index[0], k_mtx] = dict_longname_mtx[k_mtx]
            df_mtx.at[index[1], k_mtx] = (f"The participants are asked to "
                                          f"repeat out loud the sentences "
                                          f"that are presented to them. This "
                                          f"value represents the hearing "
                                          f"threshold for a 50% rate of "
                                          f"correct answers with these "
                                          f"conditions: "
                                          f"{dict_desc_mtx[k_mtx]}.")
            df_mtx.at[index[3], k_mtx] = "dB SNR"

    return df_mtx


def gen_df_teoae(var_json):
    """
    This function generates the transient-evoked otoacoustic
    emissions test (TEOAE) sidecar dataframe.
    INPUTS:
    -var_json: config file with user-supplied values
    OUTPUTS:
    -returns a dataframe ready to be saved in a json format
    """

    keys_teoae = var_json["json"]["keys"]["teoae"]

    df_teoae = pd.DataFrame(index=index, columns=keys_teoae)

    dict_longname_teoae = {keys_teoae[2]: "Frequency",
                           keys_teoae[3]: "Otoacoustic emissions response",
                           keys_teoae[4]: "Noise relative strength",
                           keys_teoae[5]: "Signal-to-noise ratio",
                           keys_teoae[6]: "Confidence level"}

    dict_desc_teoae = {keys_teoae[2]: "Frequency for which the intensity of "
                                      "the transient-evoked otoacoustic "
                                      "emission is reported.",
                       keys_teoae[3]: "Amplitude of the "
                                      "transient-evoked otoacoustic "
                                      "emissions at a specific frequency.",
                       keys_teoae[4]: "Measured level of the noise relative "
                                      "strength.",
                       keys_teoae[5]: "Difference between the measured level "
                                      "of the transient-evoked otoacoustic "
                                      "emissions and the measured noise "
                                      "relative strength (TEOAE level - "
                                      "Noise level).",
                       keys_teoae[6]: "Level of confidence linked to the "
                                      "obtained signal-to-noise ratio."}

    dict_units_teoae = {keys_teoae[2]: "Hz",
                        keys_teoae[3]: "dB SPL",
                        keys_teoae[4]: "dB",
                        keys_teoae[5]: "dB",
                        keys_teoae[6]: "%"}

    for k_teoae in keys_teoae:
        if k_teoae == keys_teoae[0]:
            df_teoae.at[index[0],
                        k_teoae] = long_order
            df_teoae.at[index[2],
                        k_teoae] = lvl_order

        elif k_teoae == keys_teoae[1]:
            df_teoae.at[index[0],
                        k_teoae] = long_side
            df_teoae.at[index[2],
                        k_teoae] = lvl_side

        else:
            df_teoae.at[index[0], k_teoae] = dict_longname_teoae[k_teoae]
            df_teoae.at[index[1], k_teoae] = dict_desc_teoae[k_teoae]
            df_teoae.at[index[3], k_teoae] = dict_units_teoae[k_teoae]

    return df_teoae


def gen_df_dpoae(var_json):
    """
    This function generates the distortion product otoacoustic
    emissions test (DPOAE) sidecar dataframe.
    INPUTS:
    -var_json: config file with user-supplied values
    OUTPUTS:
    -returns a dataframe ready to be saved in a json format
    """

    keys_dpoae = var_json["json"]["keys"]["dpoae"]

    df_dpoae = pd.DataFrame(index=index, columns=keys_dpoae)

    dict_longname_dpoae = {keys_dpoae[2]: "Frequency #1",
                           keys_dpoae[3]: "Frequency #2",
                           keys_dpoae[4]: "Level for frequency #1",
                           keys_dpoae[5]: "Level for frequency #2",
                           keys_dpoae[6]: "Distortion product",
                           keys_dpoae[7]: "Signal-to-noise ratio",
                           keys_dpoae[8]: "Noise level plus two standard "
                                          "deviations",
                           keys_dpoae[9]: "Noise level plus standard "
                                          "deviation",
                           keys_dpoae[10]: "Frequency #2 times two minus "
                                           "frequency #1",
                           keys_dpoae[11]: "Frequency #1 times three minus "
                                           "frequency #2 times two",
                           keys_dpoae[12]: "Frequency #2 times three minus "
                                           "frequency #1 times two",
                           keys_dpoae[13]: "Frequency #1 times four minus "
                                           "frequency #2 times three"}

    dict_desc_dpoae = {keys_dpoae[2]: "Lower frequency (F1) used to produce "
                                      "distortion product otoacoustic "
                                      "emissions. The F2/F1 ratio = 1,22.",
                       keys_dpoae[3]: "Higher frequency (F2) used to produce "
                                      "distortion product otoacoustic "
                                      "emissions. The F2/F1 ratio = 1,22.",
                       keys_dpoae[4]: "Frequency #1's presentation level.",
                       keys_dpoae[5]: "Frequency #2's presentation level.",
                       keys_dpoae[6]: "Measured level of the distortion "
                                      "product (2F1 - F2) otoacoustic "
                                      "emissions at the nominal "
                                      "frequency F2.",
                       keys_dpoae[7]: "Difference between the measured level "
                                      "of the distortion product otoacoustic "
                                      "emissions and the measured noise "
                                      "relative strength plus two standard "
                                      "deviations (TEOAE level - (Noise "
                                      "level + 2 * SD)).",
                       keys_dpoae[8]: "Measured noise relative strength "
                                      "level plus two standard deviations.",
                       keys_dpoae[9]: "Measured noise relative strength "
                                      "level plus one standard deviation.",
                       keys_dpoae[10]: "Frequency #2 intensity times two "
                                       "minus frequency #1 intensity (2 * "
                                       "F2 - F1).",
                       keys_dpoae[11]: "Frequency #1 intensity times three "
                                       "minus frequency #2 times two "
                                       "(3 * F1 - 2 * F2).",
                       keys_dpoae[12]: "Frequency #2 intensity times three "
                                       "minus frequency #1 times two "
                                       "(3 * F2 - 2 * F1).",
                       keys_dpoae[13]: "Frequency #1 intensity times four "
                                       "minus frequency #2 times three "
                                       "(4 * F1 - 3 * F2)."}

    dict_units_dpoae = {keys_dpoae[2]: "Hz",
                        keys_dpoae[3]: "Hz",
                        keys_dpoae[4]: "dB SPL",
                        keys_dpoae[5]: "dB SPL",
                        keys_dpoae[6]: "dB SPL",
                        keys_dpoae[7]: "dB",
                        keys_dpoae[8]: "dB",
                        keys_dpoae[9]: "dB",
                        keys_dpoae[10]: "dB",
                        keys_dpoae[11]: "dB",
                        keys_dpoae[12]: "dB",
                        keys_dpoae[13]: "dB"}

    for k_dpoae in keys_dpoae:
        if k_dpoae == keys_dpoae[0]:
            df_dpoae.at[index[0],
                        k_dpoae] = long_order
            df_dpoae.at[index[2],
                        k_dpoae] = lvl_order

        elif k_dpoae == keys_dpoae[1]:
            df_dpoae.at[index[0],
                        k_dpoae] = long_side
            df_dpoae.at[index[2],
                        k_dpoae] = lvl_side

        else:
            df_dpoae.at[index[0], k_dpoae] = dict_longname_dpoae[k_dpoae]
            df_dpoae.at[index[1], k_dpoae] = dict_desc_dpoae[k_dpoae]
            df_dpoae.at[index[3], k_dpoae] = dict_units_dpoae[k_dpoae]

    return df_dpoae


def gen_df_growth(var_json):
    """
    This function generates the distortion product otoacoustic
    emissions growth function test (DP-Growth) sidecar dataframe.
    INPUTS:
    -var_json: config file with user-supplied values
    OUTPUTS:
    -returns a dataframe ready to be saved in a json format
    """

    keys_growth = var_json["json"]["keys"]["growth"]

    df_growth = pd.DataFrame(index=index, columns=keys_growth)

    dict_longname_growth = {keys_growth[2]: "Frequency #1",
                            keys_growth[3]: "Frequency #2",
                            keys_growth[4]: "Level for frequency #1",
                            keys_growth[5]: "Level for frequency #2",
                            keys_growth[6]: "Distortion product",
                            keys_growth[7]: "Signal-to-noise ratio",
                            keys_growth[8]: "Noise level plus two standard "
                                            "deviations",
                            keys_growth[9]: "Noise level plus standard "
                                            "deviation",
                            keys_growth[10]: "Frequency #2 times two minus "
                                             "frequency #1",
                            keys_growth[11]: "Frequency #1 times three minus "
                                             "frequency #2 times two",
                            keys_growth[12]: "Frequency #2 times three minus "
                                             "frequency #1 times two",
                            keys_growth[13]: "Frequency #1 times four minus "
                                             "frequency #2 times three"}

    dict_desc_growth = {keys_growth[2]: "Lower frequency (F1) used to "
                                        "produce distortion product "
                                        "otoacoustic emissions. The F2/F1 "
                                        "ratio = 1,22.",
                        keys_growth[3]: "Higher frequency (F2) used to "
                                        "produce distortion product "
                                        "otoacoustic emissions. The F2/F1 "
                                        "ratio = 1,22.",
                        keys_growth[4]: "Frequency #1's presentation level.",
                        keys_growth[5]: "Frequency #2's presentation level.",
                        keys_growth[6]: "Measured level of the distortion "
                                        "product otoacoustic emissions.",
                        keys_growth[7]: "Difference between the measured "
                                        "level of the distortion product "
                                        "otoacoustic emissions and the "
                                        "measured noise relative strength "
                                        "plus two standard deviations (TEOAE "
                                        "level - (Noise level + 2 * SD)).",
                        keys_growth[8]: "Measured noise relative strength "
                                        "level plus two standard deviations.",
                        keys_growth[9]: "Measured noise relative strength "
                                        "level plus one standard deviation.",
                        keys_growth[10]: "Frequency #2 intensity times two "
                                         "minus frequency #1 intensity (2 * "
                                         "F2 - F1).",
                        keys_growth[11]: "Frequency #1 intensity times three "
                                         "minus frequency #2 times two "
                                         "(3 * F1 - 2 * F2).",
                        keys_growth[12]: "Frequency #2 intensity times three "
                                         "minus frequency #1 times two "
                                         "(3 * F2 - 2 * F1).",
                        keys_growth[13]: "Frequency #1 intensity times four "
                                         "minus frequency #2 times three "
                                         "(4 * F1 - 3 * F2)."}

    dict_units_growth = {keys_growth[2]: "Hz",
                         keys_growth[3]: "Hz",
                         keys_growth[4]: "dB SPL",
                         keys_growth[5]: "dB SPL",
                         keys_growth[6]: "dB SPL",
                         keys_growth[7]: "dB",
                         keys_growth[8]: "dB",
                         keys_growth[9]: "dB",
                         keys_growth[10]: "dB",
                         keys_growth[11]: "dB",
                         keys_growth[12]: "dB",
                         keys_growth[13]: "dB"}

    for k_growth in keys_growth:
        if k_growth == keys_growth[0]:
            df_growth.at[index[0],
                         k_growth] = long_order
            df_growth.at[index[2],
                         k_growth] = lvl_order

        elif k_growth == keys_growth[1]:
            df_growth.at[index[0],
                         k_growth] = long_side
            df_growth.at[index[2],
                         k_growth] = lvl_side

        else:
            df_growth.at[index[0], k_growth] = dict_longname_growth[k_growth]
            df_growth.at[index[1], k_growth] = dict_desc_growth[k_growth]
            df_growth.at[index[3], k_growth] = dict_units_growth[k_growth]

    return df_growth


def gen_df_sessions(var_json):
    """
    This function generates the session-level sessions.tsv sidecar dataframe.
    INPUTS:
    -var_json: config file with user-supplied values
    OUTPUTS:
    -returns a dataframe ready to be saved in a json format
    """

    keys_ses = var_json["json"]["keys"]["ses"]

    df_ses = pd.DataFrame(index=index, columns=keys_ses)

    dict_longname_sessions = {keys_ses[0]: "Session identification number",
                              keys_ses[1]: "Session name and/or type",
                              keys_ses[2]: "Experimental condition",
                              keys_ses[3]: "Number of days since the first "
                                           "baseline",
                              keys_ses[4]: "MRI scan type",
                              keys_ses[5]: "Tympanometry",
                              keys_ses[6]: "Stapedial reflex",
                              keys_ses[7]: "Pure tone audiometry",
                              keys_ses[8]: "Matrix speech-in-noise "
                                           "perception test",
                              keys_ses[9]: "Transient-evoked otoacoustic "
                                           "emissions",
                              keys_ses[10]: "Distortion product otoacoustic "
                                            "emissions",
                              keys_ses[11]: "Distortion product otoacoustic "
                                            "emissions growth function"}

    dict_desc_sessions = {keys_ses[0]: "Identification number of the sessions "
                                       "using the BIDS format (ses-XX, "
                                       "starting with ses-01)",
                          keys_ses[1]: "Type of session. Can be a baseline "
                                       "session where reference values are "
                                       "established for each of the hearing "
                                       "tests or an experimental protocol "
                                       "session (Month X) linked to a scan "
                                       "session to investigate potential "
                                       "changes in the auditory health of "
                                       "the research participants.",
                          keys_ses[2]: "Type of experimental condition. Can "
                                       "either be a baseline (Baseline or "
                                       "Suppl. PTA (Baseline)) or one of "
                                       "the experimental conditions (1[A, B], "
                                       "2, 3[A, B] or Suppl. PTA [A, B]). ",
                          keys_ses[3]: "Delay (in days) between a specific "
                                       "test session and the first auditory "
                                       "test session (baseline #1) acquired "
                                       "with the participant when they joined "
                                       "the study.",
                          keys_ses[4]: "Type of MRI scan linked to the "
                                       "acquisition session (anatomical, "
                                       "functional or no scan in the case of "
                                       "baseline sessions).",
                          keys_ses[5]: "Tympanic membrane and middle ear "
                                       "structures mobility test.",
                          keys_ses[6]: "Test of the reactivity of the "
                                       "stapedial reflex.",
                          keys_ses[7]: "Behavioral measurement of the earing "
                                       "thresholds using pure tones at "
                                       "different frequencies.",
                          keys_ses[8]: "Behavioral speech-in-noise perception "
                                       "test using five words sentences built "
                                       "from a matrix of words.",
                          keys_ses[9]: "Otoacoustic emissions test using "
                                       "brief transient stimuli",
                          keys_ses[10]: "Otoacoustic emissions test using the "
                                        "simultaneous presentation of two "
                                        "pure tones (f1 and f2) with a f2/f1 "
                                        "ratio of 1,22 and target intensities "
                                        "L1 = 65 dB SPL (for f1) and L2 = 55 "
                                        "dB SPL (for f2).",
                          keys_ses[11]: "Otoacoustic emissions test using the "
                                        "simultaneous presentation of two "
                                        "fixed pure tones (f1 and f2) with "
                                        "a f2/f1 ratio of 1,22. The pair of "
                                        "frequencies f1-f2 is presented with "
                                        "decreasing intensities."}

    for k_ses in keys_ses:
        if k_ses == keys_ses[0]:
            df_ses.at[index[0], k_ses] = dict_longname_sessions[k_ses]
            df_ses.at[index[1], k_ses] = dict_desc_sessions[k_ses]

        elif k_ses == keys_ses[1]:
            df_ses.at[index[0], k_ses] = dict_longname_sessions[k_ses]
            df_ses.at[index[1], k_ses] = dict_desc_sessions[k_ses]
            df_ses.at[index[2], k_ses] = var_json["json"]["lvl"]["ses_name"]

        elif k_ses == keys_ses[2]:
            df_ses.at[index[0], k_ses] = dict_longname_sessions[k_ses]
            df_ses.at[index[1], k_ses] = dict_desc_sessions[k_ses]
            df_ses.at[index[2], k_ses] = var_json["json"]["lvl"]["cond"]

        elif k_ses == keys_ses[3]:
            df_ses.at[index[0], k_ses] = dict_longname_sessions[k_ses]
            df_ses.at[index[1], k_ses] = dict_desc_sessions[k_ses]
            df_ses.at[index[3], k_ses] = "days"

        elif k_ses == keys_ses[4]:
            df_ses.at[index[0], k_ses] = dict_longname_sessions[k_ses]
            df_ses.at[index[1], k_ses] = dict_desc_sessions[k_ses]
            df_ses.at[index[2], k_ses] = var_json["json"]["lvl"]["scan"]

        else:
            df_ses.at[index[0], k_ses] = dict_longname_sessions[k_ses]
            df_ses.at[index[1], k_ses] = dict_desc_sessions[k_ses]
            df_ses.at[index[2], k_ses] = lvl_ses_test

    return df_ses


def save_json(df, save_folder, test):
    """
    This function saves the provided dataframe in a json file and formats it
    to comply with BIDS standards.
    INPUTS:
    -df: dataframe to save in a json format
    -save_folder: path to save the json file
    -test: string containing the name of the test to insert in the json
           file name.
    OUTPUTS:
    -prints a user feedback: Saved [name of the saved file]
    -NO specific return to the script
    """

    if test == "sessions":
        filename = test + ".json"
    else:
        filename = "task-" + test + "_beh.json"

    df.to_json(os.path.join(save_folder, filename), indent=2)

    with open(os.path.join(save_folder, filename), "r") as origin:
        json_file = json.load(origin)
    origin.close()

    for i in list(json_file.keys()):
        for j in list(json_file[i].keys()):
            if json_file[i][j] is None:
                del json_file[i][j]

    to_write = Path(os.path.join(save_folder, filename))
    to_write.write_text(json.dumps(json_file,
                                   indent=2,
                                   ensure_ascii=False),
                        encoding=utf)
    print("Saved", filename)


def create_sidecars(results_folder, var_json):
    """
    This function serves a master function for this script. It runs the
    complete json sidecar generation and saves the newly created files.
    INPUTS:
    -results_folder: path where to save the created files
    -var_json: config file with user-supplied values
    OUTPUTS:
    -NO specific return to the script
    """

    content_parent_path = os.listdir(results_folder)
    content_parent_path.sort()

    if content_parent_path.count("BIDS_sidecars_originals") == 1:
        pass
    else:
        os.mkdir(os.path.join(results_folder, "BIDS_sidecars_originals"))

    save_folder = os.path.join(results_folder, "BIDS_sidecars_originals")

    df_tymp = gen_df_tymp(var_json)
    df_reflex = gen_df_reflex(var_json)
    df_pta = gen_df_pta(var_json)
    df_mtx = gen_df_mtx(var_json)
    df_teoae = gen_df_teoae(var_json)
    df_dpoae = gen_df_dpoae(var_json)
    df_growth = gen_df_growth(var_json)
    df_sessions = gen_df_sessions(var_json)

    save_json(df_tymp, save_folder, "Tymp")
    save_json(df_reflex, save_folder, "Reflex")
    save_json(df_pta, save_folder, "PTA")
    save_json(df_mtx, save_folder, "MTX")
    save_json(df_teoae, save_folder, "TEOAE")
    save_json(df_dpoae, save_folder, "DPOAE")
    save_json(df_growth, save_folder, "DPGrowth")
    save_json(df_sessions, save_folder, "sessions")


if __name__ == "__main__":

    root_path = ".."
    parent_path = os.path.join("..", "results")

    with open(os.path.join(root_path, "variables.json"), "r") as origin:
        var_json = json.load(origin)
    origin.close()

    create_sidecars(parent_path, var_json)


else:
    pass
