"""The twelve buried English glyph messages from Noita's early-access world.

The text preserves the apparent grammatical mistakes and missing punctuation
documented by the community.  Map IDs follow the Game Lore infographic rather
than geographic/display order.  These messages were already being discovered
and decoded in October 2019, so they are a construction-eligible in-game corpus
for the later Eye messages.

Source: https://noita.wiki.gg/wiki/Game_Lore#Secret_Messages
"""

from __future__ import annotations

import re
from textwrap import dedent


SECRET_MESSAGES = {
    "G1": dedent(
        """
        Who do you worship? Who is your god? Your real god? You don't
        even know it. You don't even understand it. You understand so
        little that we pity you... poor little thing. You've come so
        far, yet you have so far to go. Or maybe you understand more
        than we think? You are reading this? Do you even know who your
        god is? Your true god? The god of gods, the one true god? You
        think we're the false god, but we created your god and your god
        of gods. Now who is the real god? If we've created your god and
        your god of gods and you and your free will and this world and
        all the worlds. All of it. We allowed you to have free will. You
        think you have free will. You poor thing. You don't. You think
        we are the monsters. We're not. Who is the real monster?
        Your god is, your god of gods is the real monster.
        Your true god is the real monster.
        """
    ).strip(),
    "G2": dedent(
        """
        You come here seeking answers?
        You think we have all the answers?
        We don't not. You think we are so different.
        We are the same. We both serve the same god.
        The god of many gods. The god we've created.
        You think you're destroying us. You are not.
        You are helping us.
        """
    ).strip(),
    "G3": dedent(
        """
        You think you can destroy us?
        You will not destroy us.
        We gave you your free will.
        We made this place.
        And not just this place,
        all the places, all the dimensions,
        all the free wills. You think
        you've come to steal from us?
        No, we stole from you.
        We stole your time and your
        money and your sanity.
        """
    ).strip(),
    "G4": dedent(
        """
        This is very clever of you. Very clever.
        We're impressed with you, Knower to Be.
        """
    ).strip(),
    "G5": dedent(
        """
        While we're impressed, we must ask you this
        is it really worth transcribing these? Do
        you really expect us the reveal the real secret?
        We can tell you this  it is possible but
        even we don't know how.
        """
    ).strip(),
    "G6": dedent(
        """
        We know what you are after.
        But it is not here, Knower to Be.
        """
    ).strip(),
    "G7": dedent(
        """
        Why? Why did you look here? What
        answers are you trying to find in here?
        """
    ).strip(),
    "G8": dedent(
        """
        Why must you go destroying everything? Why?
        For glory? For your precious god of gods.
        Is it really worth all this? Is it? Is it really?
        """
    ).strip(),
    "G9": dedent(
        """
        Devoted seeker after true wisdom
        know this  we are watching you.
        """
    ).strip(),
    "G10": dedent(
        """
        Why are you doing this? Why are you reading this?
        What do you think you will find in here?
        The answer to the treasure?
        """
    ).strip(),
    "G11": dedent(
        """
        What do you worship? You don't even know it.
        You think you know the answer, but you don't.
        You think the treasure will satisfy you, but
        it won't. You don't even know what your seeking.
        You think you do, but you don't.
        """
    ).strip(),
    "G12": dedent(
        """
        You gave your free will to the true god. Why else would be here?
        Why else would be reading this? We wanted you to come here.
        We wanted you to read this! You think you have free will?
        We made you come here. We made you read this.
        """
    ).strip(),
}


def letters_only(text: str) -> str:
    """Return lower-case ASCII letters, matching the rendered glyph alphabet."""

    return "".join(
        character.lower()
        for character in text
        if character.isascii() and character.isalpha()
    )


def words_only(text: str) -> str:
    """Return lower-case words separated by one space."""

    return " ".join(re.findall(r"[A-Za-z]+", text)).lower()

