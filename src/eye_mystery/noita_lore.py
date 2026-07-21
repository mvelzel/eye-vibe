"""Contemporaneous in-game Finnish creation-lore passages."""

from __future__ import annotations

import unicodedata


# These are the nine Orb Room glyph texts in their narrative/table order.  The
# final two are separate left/right-basin revelations for Volume X.
ORB_LORE_FINNISH = (
    (
        "volume-ii",
        """Keskikesän kuikka lenteli suon
yllä ja laskeutui suuren puun
juurelle. Vesilintu muni kolme
munaa. Ensimmäinen munista vierähti
pesästä ja halkesi. Halkeamasta vuosi
verta seitsemän päivää ja seitsemän
yötä. Verestä muodostui elämä ja kuolema""",
    ),
    (
        "volume-iv",
        """Valkuainen valui länteen ja siitä
muodostui kylmyys ja jää. Kuoresta
muodostuivat maat ja vuoret""",
    ),
    (
        "volume-v",
        """Keltuainen valui itään ja
siitä muodostui lämpö ja tuli""",
    ),
    (
        "volume-vi",
        """Viimein munasta kuoriutui Luonto.
Luonto loi lait luonnon, asetti eläimet,
niityt, joet, kummut ja vuoret""",
    ),
    (
        "volume-vii",
        """X yötä ja X päivää vierähti X kertaa.
Luonto puuhasteli itsekseen. Luonto
katseli tekojaan ja oli tyytyväinen
luomuksiinsa. Maailmassa oli harmonia""",
    ),
    (
        "volume-viii",
        """Toinen munista kuoriutui ja sieltä syntyi
Taikuus. Taikuus katseli Luonnon luomuksia
ja antoi niille sielun. Ei pelkästään
eläimille, vaan myös aineille""",
    ),
    (
        "volume-ix",
        """Sielun paino jalosti ja kieroutti luonnon
luomuksia. Kullan jalous antoi sille hohdon.
Mudan saamattomuus antoi sille pistävän hajun""",
    ),
    (
        "volume-x-oil",
        """Taikuus rikkoi luonnon lakeja. Luonto
ja Taikuus alkoivat riidellä siitä
miten maailman kuuluisi olla""",
    ),
    (
        "volume-x-sludge",
        """Munista viimeinen kuoriutui ja sieltä
syntyi teknologia. Teknologia antoi luonnon
eläimille kyvyn käyttää koneita ja laitteita""",
    ),
)


def letters_only(text: str) -> str:
    """Return uppercase Unicode letters, preserving Finnish Å/Ä/Ö."""

    return "".join(
        character.upper()
        for character in unicodedata.normalize("NFC", text)
        if character.isalpha()
    )


ORB_LORE_KEYS = tuple(
    (name, letters_only(text)) for name, text in ORB_LORE_FINNISH
)


def absolute_sum_key(
    message: tuple[int, ...],
    key: str,
    *,
    direction_values: tuple[int, int, int, int, int] = (0, 1, 2, 3, 4),
    start: int = 0,
) -> str:
    """Index a key window by the sum of each three-eye group.

    This reproduces the December 2025 community proposal: engine-valued eyes
    sum to ``0..12`` and select the correspondingly numbered glyph/letter from
    a lore passage.  Python index ``sum`` is the proposal's one-based
    ``sum + 1`` position.
    """

    if len(message) % 3:
        raise ValueError("eye stream length must be divisible by three")
    if sorted(direction_values) != list(range(5)):
        raise ValueError("direction values must permute 0..4")
    if start < 0 or start + 12 >= len(key):
        raise ValueError("key must contain the selected 13-character window")
    return "".join(
        key[
            start
            + sum(direction_values[value] for value in message[offset : offset + 3])
        ]
        for offset in range(0, len(message), 3)
    )
