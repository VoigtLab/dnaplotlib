__author__ = "user"

import dnaplotlib as dpl
import dnaplotlib.sbol as dpl_sbol
import sbol3 as sbol
import matplotlib.pyplot as plt


def make_plot(path_to_sbolv3: str):
    # Import the SBOL design file
    doc = sbol.Document()
    doc.read(path_to_sbolv3)

    # In this case, we know ahead of time the name of the design. In some cases, you may have to explore the doc's components to find the design you are looking for
    design = doc.find("GeneCassette")

    # Create the DNAplotlib renderer
    dr = dpl_sbol.SBOLRenderer()

    # Instantiate rendered
    part_renderers = dr.SBOL_part_renderers()

    # Create the figure
    fig = plt.figure()
    ax = plt.gca()
    start, end = dr.renderSBOL(
        ax, design, part_renderers
    )  # Render SBOL.  This function has parallel structure to renderDNA

    # Give the figure a title
    dpl.write_label(ax, design.name, (start + end) / 2, {"label_size": 18, "label_y_offset": 12})

    # Configure plot
    ax.set_xlim([start, end])
    ax.set_ylim([-18, 18])
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])
    ax.axis("off")
    return fig, ax


if __name__ == "__main__":
    fig, a_ = make_plot("gene_cassette.xml")
    # Save the figure
    fig.savefig("sbol_visual.pdf", transparent=True)
    fig.savefig("sbol_visual.png", dpi=300)

    # Clear the plotting cache
    # plt.close('all')
    plt.show()
