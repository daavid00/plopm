# SPDX-FileCopyrightText: 2024 NORCE
# SPDX-License-Identifier: GPL-3.0
# pylint: disable=R1702,R0912,C0325,R0914

"""
Utiliy function for the grid and locations in the geological models.
"""

import numpy as np
from plopm.utils.readers import (
    get_xycoords_resdata,
    get_xycoords_opm,
    get_xzcoords_resdata,
    get_xzcoords_opm,
    get_yzcoords_resdata,
    get_yzcoords_opm,
)


def handle_slide_x(dic, n):
    """
    Processing the selected yz slide to obtain the grid properties

    Args:
        dic (dict): Global dictionary

    Returns:
        dic (dict): Modified global dictionary

    """
    if dic["slide"][n][0][0] == dic["slide"][n][0][1] - 1:
        dic["tslide"] = f", slide i={dic['slide'][n][0][0]+1}"
        dic["nslide"] = f"{dic['slide'][n][0][0]+1},*,*"
    else:
        dic["tslide"] = f", slide i={dic['slide'][n][0][0]+1}:{dic['slide'][n][0][1]}"
        dic["nslide"] = f"{dic['slide'][n][0][0]+1}:{dic['slide'][n][0][1]},*,*"
    if dic["use"] == "resdata":
        get_yzcoords_resdata(dic, n)
    else:
        get_yzcoords_opm(dic, n)


def handle_slide_y(dic, n):
    """
    Processing the selected xz slide to obtain the grid properties

    Args:
        dic (dict): Global dictionary

    Returns:
        dic (dict): Modified global dictionary

    """
    if dic["slide"][n][1][0] == dic["slide"][n][1][1] - 1:
        dic["tslide"] = f", slide j={dic['slide'][n][1][0]+1}"
        dic["nslide"] = f"*,{dic['slide'][n][1][0]+1},*"
    else:
        dic["tslide"] = f", slide j={dic['slide'][n][1][0]+1}:{dic['slide'][n][1][1]}"
        dic["nslide"] = f"*,{dic['slide'][n][1][0]+1}:{dic['slide'][n][1][1]},*"
    if dic["use"] == "resdata":
        get_xzcoords_resdata(dic, n)
    else:
        get_xzcoords_opm(dic, n)


def handle_slide_z(dic, n):
    """
    Processing the selected xy slide to obtain the grid properties

    Args:
        dic (dict): Global dictionary

    Returns:
        dic (dict): Modified global dictionary

    """
    if dic["slide"][n][2][0] == dic["slide"][n][2][1] - 1:
        dic["tslide"] = f", slide k={dic['slide'][n][2][0]+1}"
        dic["nslide"] = f"*,*,{dic['slide'][n][2][0]+1}"
    else:
        dic["tslide"] = f", slide k={dic['slide'][n][2][0]+1}:{dic['slide'][n][2][1]}"
        dic["nslide"] = f"*,*,{dic['slide'][n][2][0]+1}:{dic['slide'][n][2][1]}"
    if dic["use"] == "resdata":
        get_xycoords_resdata(dic, n)
    else:
        get_xycoords_opm(dic, n)


def rotate_grid(dic, n):
    """
    Rotate the grid if requiered.

    Args:
        dic (dict): Global dictionary

    Returns:
        dic (dict): Modified global dictionary

    """
    grd = int(dic["rotate"][n])
    xc, yc = [], []
    length = dic["xc"][-1][-1] - dic["xc"][0][0]
    width = dic["yc"][0][-1] - dic["yc"][-1][0]
    x_dis = float(dic["translate"][n][0][1:])
    y_dis = float(dic["translate"][n][1][:-1])
    for rowx, rowy in zip(dic["xc"], dic["yc"]):
        xc.append([])
        yc.append([])
        for i, j in zip(rowx, rowy):
            xc[-1].append(
                1.5 * length
                + x_dis
                + (i - 1.5 * length) * np.cos(grd * np.pi / 180)
                - (j - 1.5 * width) * np.sin(grd * np.pi / 180)
            )
            yc[-1].append(
                1.5 * width
                + y_dis
                + (j - 1.5 * width) * np.cos(grd * np.pi / 180)
                + (i - 1.5 * length) * np.sin(grd * np.pi / 180)
            )
    dic["xc"] = xc
    dic["yc"] = yc


def map_xzcoords(dic, var, quan, n):
    """
    Map the properties from the simulations to the 2D slide

    Args:
        dic (dict): Global dictionary

    Returns:
        dic (dict): Modified global dictionary

    """
    for k in range(dic["nz"]):
        for i in range(dic["nx"]):
            p_v, val = 0.0, 0.0
            for sld in range(dic["slide"][n][1][0], dic["slide"][n][1][1]):
                ind = i + sld * dic["nx"] + k * dic["nx"] * dic["ny"]
                if dic["porv"][ind] > 0:
                    if var.lower() in dic["mass"] or var.lower() == "porv":
                        p_v = 1.0
                        val += quan[dic["actind"][ind]]
                    elif var.lower() == "grid":
                        p_v = 1
                        val = 1
                    elif var.lower() == "wells":
                        p_v = 1
                        val = dic["nwells"]
                    elif var.lower() == "index_i":
                        p_v = 1
                        val = i
                    elif var.lower() == "index_j":
                        p_v = 1
                        val = sld
                    elif var.lower() == "index_k":
                        p_v = 1
                        val = k
                    elif var.lower() == "faults":
                        p_v = 1
                        val = dic["nfaults"]
                    else:
                        p_v += dic["porv"][ind]
                        val += quan[dic["actind"][ind]] * dic["porv"][ind]
            dic[var + "a"][2 * i + 2 * (dic["nz"] - k - 1) * dic["mx"]] = (
                np.nan if p_v == 0 else val / p_v
            )
    for i, wells in enumerate(dic["wells"]):
        for well in wells:
            if well:
                for k in range(well[2], well[3] + 1):
                    ind = well[0] + well[1] * dic["nx"] + k * dic["nx"] * dic["ny"]
                    if dic["global"] == 0:
                        if dic["porv"][ind] > 0 and well[1] in range(
                            dic["slide"][n][1][0], dic["slide"][n][1][1]
                        ):
                            dic["wellsa"][
                                2 * well[0] + 2 * (dic["nz"] - k - 1) * dic["mx"]
                            ] = i
                    else:
                        if dic["porv"][ind] > 0:
                            dic["wellsa"][
                                2 * well[0] + 2 * (dic["nz"] - k - 1) * dic["mx"]
                            ] = i
    for i, faults in enumerate(dic["faults"]):
        for fault in faults:
            if fault:
                for k in range(fault[2], fault[3] + 1):
                    ind = fault[0] + fault[1] * dic["nx"] + k * dic["nx"] * dic["ny"]
                    if dic["global"] == 0:
                        if dic["porv"][ind] > 0 and fault[1] in range(
                            dic["slide"][n][1][0], dic["slide"][n][1][1]
                        ):
                            dic["faultsa"][
                                2 * fault[0] + 2 * (dic["nz"] - k - 1) * dic["mx"]
                            ] = (i + 1)
                    else:
                        if dic["porv"][ind] > 0:
                            dic["faultsa"][
                                2 * fault[0] + 2 * (dic["nz"] - k - 1) * dic["mx"]
                            ] = (i + 1)


def map_yzcoords(dic, var, quan, n):
    """
    Map the properties from the simulations to the 2D slide

    Args:
        dic (dict): Global dictionary

    Returns:
        dic (dict): Modified global dictionary

    """
    for k in range(dic["nz"]):
        for j in range(dic["ny"]):
            p_v, val = 0.0, 0.0
            for sld in range(dic["slide"][n][0][0], dic["slide"][n][0][1]):
                ind = sld + j * dic["nx"] + k * dic["nx"] * dic["ny"]
                if dic["porv"][ind] > 0:
                    if var.lower() in dic["mass"] or var.lower() == "porv":
                        p_v = 1.0
                        val += quan[dic["actind"][ind]]
                    elif var.lower() == "grid":
                        p_v = 1
                        val = 1
                    elif var.lower() == "wells":
                        p_v = 1
                        val = dic["nwells"]
                    elif var.lower() == "index_i":
                        p_v = 1
                        val = sld
                    elif var.lower() == "index_j":
                        p_v = 1
                        val = j
                    elif var.lower() == "index_k":
                        p_v = 1
                        val = k
                    elif var.lower() == "faults":
                        p_v = 1
                        val = dic["nfaults"]
                    else:
                        p_v += dic["porv"][ind]
                        val += quan[dic["actind"][ind]] * dic["porv"][ind]
            dic[var + "a"][2 * j + 2 * (dic["nz"] - k - 1) * dic["mx"]] = (
                np.nan if p_v == 0 else val / p_v
            )
    for i, wells in enumerate(dic["wells"]):
        for well in wells:
            if well:
                for k in range(well[2], well[3] + 1):
                    ind = well[0] + well[1] * dic["nx"] + k * dic["nx"] * dic["ny"]
                    if dic["global"] == 0:
                        if dic["porv"][ind] > 0 and well[0] in range(
                            dic["slide"][n][0][0], dic["slide"][n][0][1]
                        ):
                            dic["wellsa"][
                                2 * well[1] + 2 * (dic["nz"] - k - 1) * dic["mx"]
                            ] = (i + 1)
                    else:
                        if dic["porv"][ind] > 0:
                            dic["wellsa"][
                                2 * well[1] + 2 * (dic["nz"] - k - 1) * dic["mx"]
                            ] = (i + 1)
    for i, faults in enumerate(dic["faults"]):
        for fault in faults:
            if fault:
                for k in range(fault[2], fault[3] + 1):
                    ind = fault[0] + fault[1] * dic["nx"] + k * dic["nx"] * dic["ny"]
                    if dic["global"] == 0:
                        if dic["porv"][ind] > 0 and fault[0] in range(
                            dic["slide"][n][0][0], dic["slide"][n][0][1]
                        ):
                            dic["faultsa"][
                                2 * fault[1] + 2 * (dic["nz"] - k - 1) * dic["mx"]
                            ] = (i + 1)
                    else:
                        if dic["porv"][ind] > 0:
                            dic["faultsa"][
                                2 * fault[1] + 2 * (dic["nz"] - k - 1) * dic["mx"]
                            ] = (i + 1)


def map_xycoords(dic, var, quan, n):
    """
    Map the properties from the simulations to the 2D slide

    Args:
        dic (dict): Global dictionary

    Returns:
        dic (dict): Modified global dictionary

    """
    for j in range(dic["ny"]):
        for i in range(dic["nx"]):
            p_v, val = 0.0, 0.0
            for sld in range(dic["slide"][n][2][0], dic["slide"][n][2][1]):
                ind = i + j * dic["nx"] + sld * dic["nx"] * dic["ny"]
                if dic["porv"][ind] > 0:
                    if var.lower() in dic["mass"] or var.lower() == "porv":
                        p_v = 1.0
                        val += quan[dic["actind"][ind]]
                    elif var.lower() == "grid":
                        p_v = 1
                        val = 1
                    elif var.lower() == "wells":
                        p_v = 1
                        val = dic["nwells"]
                    elif var.lower() == "index_i":
                        p_v = 1
                        val = i
                    elif var.lower() == "index_j":
                        p_v = 1
                        val = j
                    elif var.lower() == "index_k":
                        p_v = 1
                        val = sld
                    elif var.lower() == "faults":
                        p_v = 1
                        val = dic["nfaults"]
                    else:
                        p_v += dic["porv"][ind]
                        val += quan[dic["actind"][ind]] * dic["porv"][ind]
            dic[var + "a"][2 * i + 2 * j * dic["mx"]] = (
                np.nan if p_v == 0 else val / p_v
            )
    for i, wells in enumerate(dic["wells"]):
        for _, well in enumerate(wells):
            if well:
                for k in range(well[2], well[3] + 1):
                    ind = well[0] + well[1] * dic["nx"] + k * dic["nx"] * dic["ny"]
                    if dic["global"] == 0:
                        if dic["porv"][ind] > 0 and k in range(
                            dic["slide"][n][2][0], dic["slide"][n][2][1]
                        ):
                            dic["wellsa"][2 * well[0] + 2 * well[1] * dic["mx"]] = i + 1
                    else:
                        if dic["porv"][ind] > 0:
                            dic["wellsa"][2 * well[0] + 2 * well[1] * dic["mx"]] = i + 1
    for i, faults in enumerate(dic["faults"]):
        for _, fault in enumerate(faults):
            if fault:
                for k in range(fault[2], fault[3] + 1):
                    ind = fault[0] + fault[1] * dic["nx"] + k * dic["nx"] * dic["ny"]
                    if dic["global"] == 0:
                        if dic["porv"][ind] > 0 and k in range(
                            dic["slide"][n][2][0], dic["slide"][n][2][1]
                        ):
                            dic["faultsa"][2 * fault[0] + 2 * fault[1] * dic["mx"]] = (
                                i + 1
                            )
                    else:
                        if dic["porv"][ind] > 0:
                            dic["faultsa"][2 * fault[0] + 2 * fault[1] * dic["mx"]] = (
                                i + 1
                            )
