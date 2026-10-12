"""
The runs your test needs. ← UNIT 4, MILESTONE 3

Each of your five criteria needs something run against it. A criterion about
the empty-search branch needs an impossible query. One about the fit card needs
the same item run more than once. Working that out is Milestone 3's first step,
and this file is where you write it down.

`run_eval.py` runs everything here five times and writes the run log — five
because your criteria are written out of five.

Three scenarios are filled in to show the shape. Add or change whatever your
own criteria need — these are a starting point, not a fixed set.
"""

SCENARIOS = [
    {
        # A query the data can match. Criterion 1.
        "name": "matching query completes",
        "query": "vintage graphic tee under $30",
        "wardrobe": "example",
        "criterion": 1,
    },
    {
        # A query nothing can match. Criterion 2 — the branch.
        "name": "impossible query stops early",
        "query": "designer ballgown size XXS under $5",
        "wardrobe": "example",
        "criterion": 2,
    },
    {
        # A user with nothing saved. One of unit 4's three failure modes.
        "name": "empty wardrobe",
        "query": "denim jacket under $50",
        "wardrobe": "empty",
        "criterion": None,
    },
    {
        # A query the data matches and passes the same matched item to the other two tools
        "name": "matching selected_item",
        "query": "denim jeans under $40",
        "wardrobe": "empty",
        "criterion": 3,
    },
    {
        # Distinct Fit card with unique opening sentence. Criterion 4
        "name": "fit card - jeans",
        "query": "vintage Levi's 501 jeans under $50",
        "wardrobe": "example",
        "criterion": 4,
    },
    {
        # Distinct Fit card with unique opening sentence. Criterion 4
        "name": "fit card - baby tee",
        "query": "Y2K butterfly baby tee under $30",
        "wardrobe": "example",
        "criterion": 4,
    },
    {
        # Distinct Fit card with unique opening sentence. Criterion 4
        "name": "fit card - flannel",
        "query": "red black plaid flannel shirt under $40",
        "wardrobe": "example",
        "criterion": 4,
    },
    {
        # Distinct Fit card with unique opening sentence. Criterion 4
        "name": "fit card - slip dress",
        "query": "floral silk slip dress under $30",
        "wardrobe": "example",
        "criterion": 4,
    },
    {
        # Distinct Fit card with unique opening sentence. Criterion 4
        "name": "fit card - sneakers",
        "query": "white platform sneakers under $50",
        "wardrobe": "example",
        "criterion": 4,
    },
    {
        # Outfit suggestion using an empty wardrobe
        "name": "empty wardrobe - jeans styling",
        "query": "Vintage Levi's 501 Jeans Medium Wash under $40",
        "wardrobe": "empty",
        "criterion": 5,
    },
    {
        "name": "empty wardrobe - baby tee styling",
        "query": "Y2K Baby Tee Butterfly Print under $35",
        "wardrobe": "empty",
        "criterion": 5,
    },
    {
        "name": "empty wardrobe - flannel styling",
        "query": "Oversized Flannel Shirt Plaid Red Black under $40",
        "wardrobe": "empty",
        "criterion": 5,
    },
    {
        "name": "empty wardrobe - slip dress styling",
        "query": "90s Silk Slip Dress Floral Midi under $30",
        "wardrobe": "empty",
        "criterion": 5,
    },
    {
        "name": "empty wardrobe - platform sneakers styling",
        "query": "Platform Sneakers White Chunky Sole under $50",
        "wardrobe": "empty",
        "criterion": 5,
    }
]

WARDROBES = ("example", "empty")


def validate() -> list[str]:
    """Complain about anything malformed, before a long run rather than during."""
    problems = []
    for i, scenario in enumerate(SCENARIOS, 1):
        if not scenario.get("query", "").strip():
            problems.append(f"scenario {i} has no query")
        if scenario.get("wardrobe") not in WARDROBES:
            problems.append(
                f"scenario {i} has wardrobe {scenario.get('wardrobe')!r} — "
                f"it should be one of {WARDROBES}"
            )
    return problems
