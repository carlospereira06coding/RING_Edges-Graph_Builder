from config import *

color_map = {
        "IONIC" : "#A32F2F",
        "VDW" : "#CF8151",
        "HBOND" : "#5C50DE",
        "PICATION": "#0F6321",
        "PIPISTACK":"#41741E",
    }

#ONE-LETTER CODE @overload
#Domain numeric interval @overload


def hbar_stacked(df: pd.DataFrame, ax:Axes|None=None, reverse=False, title="", colors: dict|None = None, bar_height=0.6, **bar_kwargs): #-> plt.axes.Axes
    
    if ax is None: _,ax = plt.subplots()
    
    categories = list(df.index)
    y_pos = np.arange(len(categories))

    #DEFINE STANDARD GRAPH COLORS
    if colors is None:
        #TEMPORARY: eventualy color grade using type of bond
        color_map = ["#66A9E0"]

    elif isinstance(colors, dict):
        color_map = colors

    #REVERSE ORDER OF DATA: LEFT GRAPH
    segment_order = list(df.columns)[::-1] if reverse else list(df.columns)

    #Tracking Column object position on the x-axis
    left = np.zeros(len(categories))#all columns start at 0

    for col in segment_order:
        #BUILDING EACH COLUMN ITERATIVELY
        values = df[col].to_numpy(dtype=float)
        bars = ax.barh(
            y_pos,values,left=left,
            height=bar_height,
            align="center",
            label=col,
            color=color_map[0] if colors is None else colors.get(col)
        )
        left+=values

    """
    Common set axes:

    Every y-axis has its own real category labels (deactivate matplotlib's default numeric autoticks);
    Set title
    Run regardless of reverse/non-reverse

    """

    #SET axes and labels 
    ax.set_yticks(y_pos)#Set a tick for each category/interaction pair. Garanteee that 2 subplots line up with sharey=True
    ax.set_yticklabels(categories)
    ax.set_ylim(-0.7, len(categories)-0.7)
    ax.set_title(title, pad=60.0)
    ax.set_xlabel("Frequency", labelpad=10)
    ax.xaxis.set_label_position('top')

    """
    SET axes and labels for each type of file: reversed=TRUE, reversed=FALSE
        - Reversed image: Y-axis is on the RIGHT, the labels are TRUE and on the LEFT
        - Normal image: Y-axis is on the LEFT, the labels are TRUE and on the LEFT
    """    
    if reverse:
        ax.tick_params(axis='y', right=True, labelright=True, left=False, labelleft=False)
        ax.tick_params(axis='x', top=True)
        ax.xaxis.tick_top()
        ax.invert_xaxis()

    else:
        ax.tick_params(axis='y', left=True, labelleft=True) 
        ax.xaxis.tick_top()

    handles, labels = ax.get_legend_handles_labels()
    order = [labels.index(col) for col in df.columns if col in labels]
    ax.legend([handles[i] for i in order], [labels[i] for i in order])

    return ax, y_pos



def butterfly(df_left, df_right,left_title="", right_title="", colors=True, figsize=(10,5)) ->tuple[Figure, tuple[Axes,Axes]]:

    #CENTRAL ROW LABELS
    categories = list(df_left.index)

    #IMAGE SETTINGS
    colors = colors or {} #Dicionario de cores especifico ou pre-definido na funçaão


    fig, (ax_left,ax_right) = plt.subplots(
        nrows=1,ncols=2,figsize=figsize#the two graphs share the y-axis
    )

    #GENERATING GRAPHS, while generating individual graphs
    _, y_pos_left = hbar_stacked(df_left, title=left_title, ax=ax_left, reverse=True, colors=color_map)
    _, y_pos_right = hbar_stacked(df_right, title=right_title, ax=ax_right, reverse=False, colors=color_map)


    for ax in (ax_left,ax_right):
        #Gridlines for x, y Axis objets after being created in plt.subplots() above.
        ax.grid(visible=True, which="both", linestyle='--', linewidth=0.5, color='gray')
        
    fig.subplots_adjust(wspace=0.55)

    
    """
    1. Set shared ticks/labels on ax_right
    2. Set hidden ticks in ax_left

    ax_right, ax_left: created in hbar_stacked, 
    it has its own labels, labeleft=True, labelright=True, respectively

    """

    ax_right.tick_params(axis="y",left=False)
    ax_left.tick_params(axis="y",right=False, labelright=False)
    
    max_total = max(df_left.sum(axis=1).max(), df_right.sum(axis=1).max())

    """
    Center a single shared label; 
    Pad and ha=center sets label in-between graph space
    
    """
    ax_right.tick_params(axis="y", pad=50)
    plt.setp(ax_right.get_yticklabels(), ha='center')


    if ax_left.xaxis_inverted():
        ax_left.set_xlim(max_total,0)

    else:
        ax_left.set_xlim(0, max_total)

    ax_right.set_xlim(0, max_total)


    return fig, (ax_left, ax_right)