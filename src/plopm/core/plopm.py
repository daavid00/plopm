# SPDX-FileCopyrightText: 2024 NORCE
# SPDX-License-Identifier: GPL-3.0
# pylint: disable=R1702,W0123,W1401,R0915

"""
Script to plot 2D maps of OPM Flow geological models.
"""

import argparse
import warnings
from plopm.utils.initialization import (
    ini_dic,
    ini_properties,
    is_summary,
    ini_summary,
)
from plopm.utils.vtk import make_vtks
from plopm.utils.write import make_summary, make_maps


def plopm():
    """Main function for the plopm executable"""
    cmdargs = load_parser()
    if int(cmdargs["warnings"]) == 0:
        warnings.warn = lambda *args, **kwargs: None
    dic = ini_dic(cmdargs)
    text = (
        "\nThe execution of plopm succeeded. "
        + f"The generated files have been written to {dic['output']}\n"
    )
    print("\nExecuting plopm, please wait.")
    if dic["mode"] == "vtk":
        make_vtks(dic)
        print(text)
        return
    if is_summary(dic):
        ini_summary(dic)
        make_summary(dic)
        print(text)
        return
    ini_properties(dic)
    make_maps(dic)
    print(text)


def load_parser():
    """Argument options"""
    parser = argparse.ArgumentParser(
        description="plopm: Simplified and flexible Python tool for quick "
        "visualization of OPM Flow geological models.",
    )
    parser.add_argument(
        "-i",
        "--input",
        default="SPE11B",
        help="The base name (or full path) of the input files; if more than"
        " one is given, separate them by spaces ' ' (e.g, "
        "'SPE11B /home/user/SPE11B_TUNED') ('SPE11B' by default).",
    )
    parser.add_argument(
        "-o",
        "--output",
        default=".",
        help="The base name (or full path) of the output folder ('.' by "
        "default, i.e., the folder where plopm is executed).",
    )
    parser.add_argument(
        "-v",
        "--variable",
        default="poro,permx,permz,porv,fipnum,satnum",
        help="Specify the name of the variable to plot, e.g., 'pressure', in "
        "addition to special variables such as 'grid', 'wells', 'faults', "
        "'permfact', 'pcfact', "
        "'krw', 'krg', 'krow', 'krog', 'pcow', 'pcog', 'pcwg', "
        "'gasm', 'dism', 'liqm', 'vapm', 'co2m', 'h2om', 'xco2l', 'xh2ov', "
        "'xco2v', 'xh2ol', 'fwcdm', and 'fgipm', as well as operations, e.g, "
        "'pressure - 0pressure' to plot the pressure increase "
        "('poro,permx,permz,porv,fipnum,satnum' by default.",
    )
    parser.add_argument(
        "-m",
        "--mode",
        default="png",
        help="Generate 'png', 'gif', or 'vtk' files ('png' by default).",
    )
    parser.add_argument(
        "-s",
        "--slide",
        default=",1,",
        help="The slide in the 3D model to plot the 2D maps, e.g, "
        "'10,,' to plot the xz plane on all cells with i=10, or "
        "',,5:10' to plot the pv average weighted quantity. If two values are "
        "given, e.g., ':,5,7', then the variable is plotted along the colon "
        "entry given the indice at the specified restart step, unless the flag "
        "'-how ' is set, then this generates a plot of the projected variable "
        "over time. If the three values are given, e.g., '2,4,9', then the "
        "variable is plotted over time at that location (',1,' by default, "
        "i.e., the xz surface at j=1).",
    )
    parser.add_argument(
        "-p",
        "--path",
        default="flow",
        help="Path to flow, e.g., '/home/build/bin/flow'."
        " This is used to generate the grid for the vtk files ('flow' by "
        "default).",
    )
    parser.add_argument(
        "-z",
        "--scale",
        default=1,
        help="Scale the axis in the 2D maps ('1' by default).",
    )
    parser.add_argument(
        "-f",
        "--size",
        default=12,
        help="The font size ('12' by default)",
    )
    parser.add_argument(
        "-x",
        "--xlim",
        default="",
        help="Set the lower and upper bounds along x, e.g., '[-100,200]' "
        "('' by default).",
    )
    parser.add_argument(
        "-y",
        "--ylim",
        default="",
        help="Set the lower and upper bounds along y, e.g., '[-10,300]' "
        "('' by default).",
    )
    parser.add_argument(
        "-u",
        "--use",
        default="resdata",
        help="Use resdata or OPM Python libraries ('resdata' by default).",
    )
    parser.add_argument(
        "-c",
        "--colors",
        default="",
        help="Specify the colormap, e.g., 'jet', or color(s) for the summary, "
        "e.g., 'b,r' ('' by default, i.e., set by plopm).",
    )
    parser.add_argument(
        "-e",
        "--linestyle",
        default="",
        help="Specify the linestyles for the summary plots, "
        "e.g., 'solid,dotted' ('' by default, i.e., set by plopm).",
    )
    parser.add_argument(
        "-b",
        "--bounds",
        default="",
        help="Specify the upper and lower bounds for the colormap, e.g., "
        " '[-0.1,11]' ('' by default, i.e., set by plopm).",
    )
    parser.add_argument(
        "-d",
        "--dimensions",
        default="7,5",
        help="Specify the dimensions in inches of the generated png, e.g., "
        "'8,16' ('7,5' by default).",
    )
    parser.add_argument(
        "-t",
        "--title",
        default="0",
        help="Specify the figure title, e.g., 'Final saturation map' ('' by "
        "default, i.e., set by plopm, set to 0 to remove).",
    )
    parser.add_argument(
        "-r",
        "--restart",
        default="-1",
        help="Restart number to plot the dynamic variable, where 0 corresponds to "
        "the initial one ('-1' by default, i.e., the last restart file). For "
        "GIFs, the default correspond to all restart steps. To make a GIF using "
        "selected restart steps, provide these separated by commas, e.g., "
        "'0,3,10,20'. To write a serie of PNGs, this can be achieve by setting "
        "'-r a:b:[step]', e.g., '-r 1:3' for rsts 1 to 3, and '-r 5:505:250' for "
        "rsts 5, 255, and 505.",
    )
    parser.add_argument(
        "-a",
        "--adjust",
        default="1.0",
        help="Scale the mass variable, e.g., 1e-9 for the color bar for "
        "the CO2 mass to be in Mt ('1' by default).",
    )
    parser.add_argument(
        "-tunits",
        "--tunits",
        default="d",
        help="For the x axis in the summary use seconds 's', minutes 'm', "
        "hours 'h', days 'd', weeks 'w', years 'y', or dates 'dates' ('s' "
        "by default).",
    )
    parser.add_argument(
        "-ylabel",
        "--ylabel",
        default="",
        help="Text for the y axis ('' by default, i.e., set by plopm).",
    )
    parser.add_argument(
        "-xlabel",
        "--xlabel",
        default="",
        help="Text for the x axis ('' by default, i.e., set by plopm).",
    )
    parser.add_argument(
        "-ylnum",
        "--ylnum",
        default="5",
        help="Number of y axis labels ('5' by default).",
    )
    parser.add_argument(
        "-xlnum",
        "--xlnum",
        default="5",
        help="Number of x axis labels ('5' by default).",
    )
    parser.add_argument(
        "-cnum",
        "--cnum",
        default="",
        help="Number of color labels ('' by default, i.e., set by plopm).",
    )
    parser.add_argument(
        "-xlog",
        "--xlog",
        default="0",
        help="Use log scale for the x axis ('0' by default).",
    )
    parser.add_argument(
        "-ylog",
        "--ylog",
        default="0",
        help="Use log scale for the y axis ('0' by default).",
    )
    parser.add_argument(
        "-clabel",
        "--clabel",
        default="",
        help="Text for the colorbar ('' by default, i.e., set by plopm).",
    )
    parser.add_argument(
        "-labels",
        "--labels",
        default="",
        help="Legend in the summary plot, separated by two spaces if more than "
        "one ('' by default, i.e., set by plopm).",
    )
    parser.add_argument(
        "-axgrid",
        "--axgrid",
        default="1",
        help="Set axis.grid to True for the summary plots ('1' by default).",
    )
    parser.add_argument(
        "-dpi",
        "--dpi",
        default="500",
        help="Dots per inch for the figure ('500' by default).",
    )
    parser.add_argument(
        "-xformat",
        "--xformat",
        default="",
        help="Format for the x numbers, e.g., .2e for exponential notation "
        "('' by default, i.e., set by plopm).",
    )
    parser.add_argument(
        "-yformat",
        "--yformat",
        default="",
        help="Format for the y numbers, e.g., .1f for one decimal "
        "('' by default, i.e., set by plopm).",
    )
    parser.add_argument(
        "-cformat",
        "--cformat",
        default="",
        help="Format for the numbers in the colormap, e.g., "
        ".2f for two decimals ('' by default, i.e., set by plopm).",
    )
    parser.add_argument(
        "-xunits",
        "--xunits",
        default="m",
        help="For the x axis in the spatial maps meters 'm', kilometers 'km', "
        "centimeters 'cm', or milimeters 'mm' ('m' by default).",
    )
    parser.add_argument(
        "-yunits",
        "--yunits",
        default="m",
        help="For the y axis in the spatial maps meters 'm', kilometers 'km', "
        "centimeters 'cm', or milimeters 'mm' ('m' by default).",
    )
    parser.add_argument(
        "-remove",
        "--remove",
        default="0,0,0,0",
        help="Set the entries to 1 to remove in the spatial maps "
        "the left axis, bottom axis, colorbar, and title ('0,0,0,0' by default).",
    )
    parser.add_argument(
        "-facecolor",
        "--facecolor",
        default="w",
        help="Color outside the spatial map ('w' by default, i.e., white).",
    )
    parser.add_argument(
        "-save",
        "--save",
        default="",
        help="Name of the output files ('' by default, i.e., set by plopm).",
    )
    parser.add_argument(
        "-log",
        "--log",
        default="0",
        help="Log scale for the color map ('0' by default).",
    )
    parser.add_argument(
        "-clogthks",
        "--clogthks",
        default="",
        help="Set the thicks for the color maps with log scale, e.g., '[1,2,3]' "
        "('' by default).",
    )
    parser.add_argument(
        "-rotate",
        "--rotate",
        default="0",
        help="Grades to rotate the grid in the 2D maps ('0' by default).",
    )
    parser.add_argument(
        "-translate",
        "--translate",
        default="[0,0]",
        help="Translate the grid in the 2D maps x,y directions ('[0,0]' "
        "by default).",
    )
    parser.add_argument(
        "-global",
        "--global",
        default=0,
        help="Min and max in the colorbars from the current 2D slide values "
        "(0) or whole 3D model '1' ('0' by default).",
    )
    parser.add_argument(
        "-ensemble",
        "--ensemble",
        default="0",
        help="Set to '1' to plot the mean and error bands for the ensemble, "
        "'2' to plot the min, mean, and max values, and '3' to plot '1' and '2' "
        "('0' by default).",
    )
    parser.add_argument(
        "-bandprop",
        "--bandprop",
        default="",
        help="Set to color and alpha values for the matplotlib.pyplot.fill_between "
        "function when the flag -ensamble is used with values '1' or '3' , e.g., "
        "-bandprop 'r,0.1,g,0.2' ('' by default, i.e., set as the same color as "
        "the mean and alpha==0.2).",
    )
    parser.add_argument(
        "-how",
        "--how",
        default="",
        help="Select how to project the given variable (-v) in a slide range (-s). "
        "By default the variables are pore volume weighted averaged along the range "
        "except for mass quantities, porv, trans, and cell dims (e.g., dz) which are summed; "
        "cell indices (e.g., index_i) which show the discrete value; harmonic average and "
        "arithmetic average for permeabilities depending on the slide range direction using "
        "the cell dim along the slide (e.g., -s ,,1:2 -v permz [harmonic averaged]); "
        "for wells/faults, 'min' show the cells when at least one cell contains them "
        "or 'max' when all cells are part of the given slide/slides range. The supported "
        "options are 'min', 'max', 'sum', 'mean', 'pvmean', 'harmonic', 'arithmetic', "
        "'first', and 'last' ('' by default, i.e., the defaults as described above).",
    )
    parser.add_argument(
        "-ncolor",
        "--ncolor",
        default="w",
        help="Color for the inactive cells in the 2D maps ('w' by default, i.e., white).",
    )
    parser.add_argument(
        "-lw",
        "--lw",
        default="",
        help="Line width separated by commas if more than one ('1' by default).",
    )
    parser.add_argument(
        "-subfigs",
        "--subfigs",
        default="",
        help="Generate separated or a single Figure (e.g., '2,2' for four "
        "subfigures) ('' by default, i.e., separate figures).",
    )
    parser.add_argument(
        "-loc",
        "--loc",
        default="best",
        help="Location of the legend by passing the value to "
        "matplotlib.pyplot.legend; set to 'empty' to remove it ('best' by "
        "default).",
    )
    parser.add_argument(
        "-delax",
        "--delax",
        default=0,
        help="Delete aligned axis labels in subfigures ('0' by default).",
    )
    parser.add_argument(
        "-printv",
        "--printv",
        default=0,
        help="Print the avaiable variables to plot ('0' by default).",
    )
    parser.add_argument(
        "-vtkformat",
        "--vtkformat",
        default="Float64",
        help="Format for each variable in the vtks, support for Float64, "
        "Float32, and UInt16 ('Float64' by default).",
    )
    parser.add_argument(
        "-vtknames",
        "--vtknames",
        default="",
        help="Label each variable in the written vtk ('' by default, "
        "i.e., the names given in the -v argument).",
    )
    parser.add_argument(
        "-mask",
        "--mask",
        default="",
        help="Static variable to use as 2D map background ('' by default).",
    )
    parser.add_argument(
        "-diff",
        "--diff",
        default="",
        help="The base name (or full path) of the input file to substract"
        " ('' by default).",
    )
    parser.add_argument(
        "-suptitle",
        "--suptitle",
        default="",
        help="Title for the subfigures ('' by default, i.e., set by plopm, "
        "if 0, then it is removed; otherwise, write the text).",
    )
    parser.add_argument(
        "-cbsfax",
        "--cbsfax",
        default="0.40,0.01,0.2,0.02",
        help="Set the global axis position and size for the colorbar "
        "('0.40,0.01,0.2,0.02' by default).",
    )
    parser.add_argument(
        "-grid",
        "--grid",
        default="",
        help="Set the edgecolors and lw in the matplotlib.pyplot.pcolormesh "
        "method, e.g., 'black,1e-3' ('' by default, i.e., no grid).",
    )
    parser.add_argument(
        "-vmin",
        "--vmin",
        default="",
        help="Set a minimum threshold to remove values in the variable "
        "('' by default).",
    )
    parser.add_argument(
        "-vmax",
        "--vmax",
        default="",
        help="Set a maximum threshold to remove values in the variable "
        "('' by default).",
    )
    parser.add_argument(
        "-distance",
        "--distance",
        default="",
        help="Compute the 'min' or 'max' distance of the variable to a 'sensor' "
        "using -s, or to the lateral boundaries ('border'), e.g., '-s 1,2,3 -v "
        "'sgas > 1e-2' -distance max,sensor' computes the maximum distance to the "
        "location using a min threshold of 1e-2 to indicate if a cell has gas or "
        "not ('' by default).",
    )
    parser.add_argument(
        "-maskthr",
        "--maskthr",
        default=1e-3,
        help="Set the threshold for the variable to mask " "('1e-3' by default).",
    )
    parser.add_argument(
        "-interval",
        "--interval",
        default=1000,
        help="Time for the frames in the GIF in milli second ('1000' by default).",
    )
    parser.add_argument(
        "-loop",
        "--loop",
        default=0,
        help="Set to 1 for infinity loop in the GIF ('0' by default).",
    )
    parser.add_argument(
        "-warnings",
        "--warnings",
        default=0,
        help="Set to 1 to print warnings ('0' by default).",
    )
    parser.add_argument(
        "-latex",
        "--latex",
        default=1,
        help="Set to 0 to not use LaTeX formatting ('1' by default).",
    )
    return vars(parser.parse_known_args()[0])


def main():
    """Main function"""
    plopm()
