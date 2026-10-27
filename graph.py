from config import *

color_map = {
        "IONIC" : "#A32F2F",
        "VDW" : "#CF8151",
        "HBOND" : "#5C50DE",
        "PICATION": "#0F6321",
        "PIPISTACK":"#CEC23C",
    }




#ONE-LETTER CODE @overload
#Domain numeric interval @overload


def hbar_stacked(df: pd.DataFrame, ax:Axes|None=None, reverse=False, title="", colors: dict|None = color_map): #-> plt.axes.Axes
    
    if ax is None: _,ax = plt.subplots()
    
    y_pos = np.arange(len(df))
  
    #Tracking Column object position on the x-axis
    left = np.zeros(len(df))#all columns start at 0

    segment_order = [x for x in df.columns if x != 'Pair']

    for col in segment_order:
        #BUILDING EACH COLUMN ITERATIVELY
        values = pd.Series(df[col])
        ax.barh(
            y=y_pos,
            width=values,
            left=left, #parameter 'x'
            height=HBAR_CONFIG["BAR_HEIGHT"],
            align="center",
            label=col,
            color= "#66A9E0" if colors is None else colors.get(col),
            zorder=1
        )
        left+=values

    """
    Common set axes:

    Every y-axis has its own real category labels (deactivate matplotlib's default numeric autoticks);
    Set title
    Run regardless of reverse/non-reverse

    """

    #SET axes and labels 
    #    ax.set_yticks(y_pos)#Set a tick for each category/interaction pair. Garanteee that 2 subplots line up with sharey=True
    ax.set_yticks(y_pos)
    ax.set_yticklabels(list(df.index))
    ax.set_ylim(*HBAR_CONFIG["YLIM"])
    ax.set_title(title, pad=HBAR_CONFIG["TITLE_PAD"])
    ax.set_xlabel("Frequency", labelpad=HBAR_CONFIG["LABEL_PAD"])
    ax.xaxis.set_label_position('top')

    """
    SET axes and labels for each type of file: reversed=TRUE, reversed=FALSE
        - Reversed image: Y-axis is on the RIGHT, the labels are TRUE and on the LEFT
        - Normal image: Y-axis is on the LEFT, the labels are TRUE and on the LEFT
    """    

    #ADD: locator_params


    #ax.xaxis.set_major_locator(locator=MultipleLocator(1.0))

    if reverse:
        ax.tick_params(axis='y', right=True, labelright=True, left=False, labelleft=False)
        ax.tick_params(axis='x', top=True)
        ax.xaxis.tick_top()
        ax.invert_xaxis()

    else:
        ax.tick_params(axis='y', left=True, labelleft=True, length=1.0) 
        ax.xaxis.tick_top()

    return ax, y_pos

def butterfly(max_total:int, df_left, df_right,left_title="", right_title="", colors=True) ->tuple[Figure, tuple[Axes,Axes]]:

    #CENTRAL ROW LABELS
    categories = list(df_left.index)
    #IMAGE SETTINGS
    colors = colors or {} #Dicionario de cores especifico ou pre-definido na funçaão


    nrows=max(len(df_left), len(df_right))
    fig_h=max(4.0, nrows*0.25+1.5)
    HBAR_CONFIG["YLIM"] = [nrows-0.5, -0.5]

    fig, (ax_left,ax_right) = plt.subplots(
        nrows=1,
        ncols=2,
        figsize=(9, fig_h),
        sharey=True,
        layout='constrained'
    )

    #GENERATING GRAPHS, while generating individual graphs
    hbar_stacked(df_left, title=left_title, ax=ax_left, reverse=True, colors=color_map)
    hbar_stacked(df_right, title=right_title, ax=ax_right, reverse=False, colors=color_map)

    for ax in (ax_left,ax_right):
        #Gridlines for x, y Axis objets after being created in plt.subplots() above.
        ax.grid(visible=True, which="both", linestyle='--', linewidth=0.5, color='gray', zorder=3)
    
    fig.align_ylabels()
    ax_left.yaxis.tick_right()
    ax_left.set_ylabel("")

    ax_left.tick_params(
        axis="y", 
        labelleft=False,
        labelright=True,
        pad=fig.get_figwidth()*1.5,
        left=False,
        right=False
    )

    ax_right.tick_params(
        axis="y",
        labelleft=False,
        left=False
    )

    new_max_total = max(df_left.sum(axis=1).max(), df_right.sum(axis=1).max())
    max_total = max(max_total, new_max_total)
    

    """
    Center a single shared label; 
    Pad and ha=center sets label in-between graph space
    
    """ 
    
    if ax_left.xaxis_inverted():
        ax_left.set_xlim(max_total,0)

    else:
        ax_left.set_xlim(0, max_total)

    ax_right.set_xlim(0, max_total)

    return fig, (ax_left, ax_right)