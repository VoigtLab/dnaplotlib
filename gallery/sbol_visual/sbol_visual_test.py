from .sbol_visual import make_plot

import pytest

@pytest.mark.mpl_image_compare
def test_plot():
    # The path needs to be relative to the root of the repository, pytest will run from the root of the repository
    fig, _ = make_plot("gallery/sbol_visual/gene_cassette.xml")
    return fig
