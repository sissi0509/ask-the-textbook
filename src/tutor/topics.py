"""Physics topics: the six areas of OpenStax University Physics, by volume and chapter.

Each eval case carries an explicit "topic" so results can be broken down by area
(does retrieval do worse on optics than on mechanics?). The topic follows from the
case's first gold section, and a test checks the two agree.
"""

# (volume, first chapter, last chapter) -> topic
TOPIC_RANGES = [
    (1, 1, 14, "Mechanics"),
    (1, 15, 17, "Oscillations & Waves"),
    (2, 1, 4, "Thermodynamics"),
    (2, 5, 16, "Electricity & Magnetism"),
    (3, 1, 4, "Optics"),
    (3, 5, 11, "Modern Physics"),
]
TOPICS = [topic for *_, topic in TOPIC_RANGES]


def topic_of(ref: str) -> str:
    """Topic of a volume-qualified section ref like "1:5.2" (Vol 1, Ch 5, §5.2)."""
    volume, section = ref.split(":")
    chapter = int(section.split(".")[0])
    for vol, first, last, topic in TOPIC_RANGES:
        if int(volume) == vol and first <= chapter <= last:
            return topic
    raise ValueError(f"No topic for section {ref}")
