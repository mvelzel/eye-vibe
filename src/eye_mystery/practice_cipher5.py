"""Data and candidate mechanics for the ciphertext-only ``Practice Cipher #5``.

The puzzle was posted by sdlwdr in the Noita Discord's read-only
``silma-secrets-storehouse`` forum.  This is the revised, author-described
solvable encoding.  Its nine independently encoded sections use an 83-symbol
ciphertext alphabet and a recursive plaintext-selected deck shuffle.
"""

from __future__ import annotations

from collections import deque
from collections.abc import Callable, Sequence


ORIGINAL_CIPHERTEXT = r'''VDf.d75[.0+r2)knqL=CDl=Q,la]('VRPF[fb;PBcIW*;-5,.h<=SE)Kc=BLqYqN7B1C>B%H@::'8nIH9]s!?$,YqQbRZ!8hDS

WEhGHSM):'<TA'$N\)'8*6\147fm8Y%n<3WhBV_])l[%hE-MY+h]War<'<(oANmThH]-E67&.Mg,>.*BO#B+mle"Z_?<YE2OZmLj`CTM`>T>9%i,J\U*W.<B^aM+Fge/9?P*sb>n=L**T9MR?"SH/[X(?MaUMUa>(hGWo3?5@N

XFjM^Ioc5VP8TU@\iW6aX=9eV<GWWoqmFcg/4C1-c(f!K&MBpBT2NAAmr1N:D.H[(L1)8S+SZY%0#8.6`@;P0)'\O`<\QcAe1AVGO1(L5l?G1P-]a4TcM=Pq2*F:'!<,qsnV<';-bH)+8=\:-F76h#g]0:]RYq]1S?p\Yjq%D9B@![79Y+fn=_cZ:%6-/V/J\-o+]/md-LN9p?gki^Y;.%M-7NbMkBdKqW%/j-WW6NGMnns+4Uc2]9*+le;$\"oJ#UG

YGlShcF88eoq[\=2Wp,=%X:DOk?E]Pqsj)SC@3$[.2JR:bEY;9_'T4UG-bV1e$[lk(T*d:4]]I!Mq%.LS/o;,8(U=%p[4B.pB'^.IP9Z$q/3\FDV42ocA!oODoi9bK_:TPh"gVBQ"bcIL:#FR@\'nB&s5,LG#ZD]%ro[b`*Df9VmVk:-HB$BRD0+R7cgjQ6q0W!TW+V6^-m(f'YfR`0:UJm`:#CLQg$5a"cVMeKCK&3S'`NYrUJB5X</-bhdY(39\'$

ZHn[!K4QW&A=e79Uq]6>k9/r1)F^^#=\)GUr;QS'4VG1i1sFZ'%bsGFb-H\.]KcD;$m/%3-eJ_QRm@L?q/H.$V(6S61E_sV42I>Ndj<95&_2'Y-3k[^4n9oSI>L9GV&c\QJ&F+cKX2flGOL]98ZCD@VksTa)NbKD=Q/VIJ8SAE(&?D*jYU(jfTs9J%cd#j"R-1=U<OhIq(*<65>7mk:-FkE>^1B,B*AN2q`4

[IpKhcJlMT+QZ_Wq"Lm75$TpDFpfUf@c7SIm[h/nUn3WOXD2Nsb^/MEcGKN?"JD1+k4q"\X.#

\Jrc1d0>DYb,)[ZX.>2f=d[BR\1I!,*T.kE]ZD_%(%G(Cad7j*04QFMoc4`.7D"PY3?JK?]k-QX.iaC3P>YML/*N.>J!0$Z2g:d-5\i*>bV%VfssrqsMf8f?[4%HdH7N<6gd2V+=+ZeEdo#5c=[F5/-lisR>j`g(;\X(2.1f*7RQ+6`p\ckiSK+762CpcW9*NR,G&LZN^9cr>O7ab)sb&<mUHI$T"(Jh([TqH9)ALd1D*)=%e31s(XQ\,#pBW9Tb`=D@Ao;-UG6VWB#4OKShF!9q,[jC0,3<hRD#PpreK%)fjr/2J6&Af7?:PWm!Q8fH12SZcAR'NB@#3bh\V>W;2(V*8q>I1TN264dT/<(]&I2kC7Zj/bf^6Gg6jfBUG309Kl5+6PKDfaIQ^i.`LT-i_+pdgdi0<T[88-CW1i8G#MEBRSgO?>kJG:lrY2LL^a(X@8c

]K!UJgE:o?`$&1FDq^4Ka'Wd)@$n%q:DZWl:>;F+*]5m'F!K-%59k.o6-0`4=$gb#L]1OfrF+[8TnjYe0GJK(2TS(g^!chDhC)HXr<d0bGr\<U@6']<C&0\=iSF=?_?CM+)[Ho'>Cl':E>)%*23n>'+0

^L#\L]Pr8aOAsm?=R@)DA:+ikD%!3MCc`k(`T"I,\:lO)ghj!m\!2U6K\X]HeYDa"<9[&K-e@K?G/C8LMB*H]4JS>`@YX%sdO.OMce[W`"6f?CV?M+Y'3f<UJ?+Go3J^T)ZSX9:(8V"\!qgQ'+GUB041M/L=73=SJe`F9=0l$R^M<!qNo'db@g=8igMbYJ%rT8=J!ka*"kM:N)_Z$gsI77>Of/F4C2/:IC[kpOJ7r<1iABmaL4m[*QA;2I&(4#6sn'WilC]MK(Q;Lj1Ub>acNpX+FkgP7/Q`/Y52!m"YOi"eq9N>CM`9%cp<p06-M3l8.I=;@'b6H7_5#N>CKg!XCl2AA9'6qp<;5/77,_@WgR`ke5Gk=Og&b8iHnNpi5#+,>ar_T"SZTq!n/H[@)'`5Rj)kLT<W$O\8h1GYP5q%85sa<B3W3-'$)6e@;,-lYp9\AFPq'^KmhI<r>$I/])IPa-Whh[D++8Y8S@B0f`?]JG3e7UkQJ36:kIYG#4bF@#OY@D<RLCA@4V'''


ORIGINAL_SECTIONS = tuple(ORIGINAL_CIPHERTEXT.split("\n\n"))


REVISED_CIPHERTEXT = r'''<I1EWRYC,d-qed[c"c/pWj#Q0P2)181XfHJKlrAq8Ypm0;!m,Y\nO?d;dZXPf)L"/,IAOQ<)em%lNmp.g.-bU/n4]rP<1R1i#K

=L2cMs1^HLg$T_nUTZ'PXWiWh:hsM>8+_*8*T,S/!s*.aGA,)Zd`<ZF,_"5W54M4UR!jgd:j:.2^kd-I:E`F2ig7pLg[2=5'Qc\l/$qiq.)06#?<p5;@7'k@oKSKWa:)M1/\$p4*4NsRM^"9/.-N\hQiIh@N7O&SninAl3'o:]

>O3eP@2`KOi%WapXW](S[Zklkg9A9:CkM-h_cl2$Y-eDPA%iP9aFWVg;Rb]CZ)5rA(2a%A!nj0BDc?7J>?<DCM&mdm`9!9\[mW#+5@UBQkbR>hri>%bNL(gkIEBM');<h\/"+f36FYA)*(cR-(#)CM.K.qhqI`3b9c=b="%1fR/7^Hko5M-oDHp6q#9S3hNQkQI]WR`OdM6_>5q[>GL8Lcs"]lZhSNM=<=!4ilKeahI\!Sn#k.n>!5P+8YkY13gqG"'

?R4gSC3bNRk&ZBYe(!DbT$*$F71_Zgh+\nB(MOhTIdS-ZD=$M@03h;#%])Sj=KVGM+\E\C_95G-mse%\[QDa_6%"(^)S5d*;sLso4$4(Ws7D+8i/%$G]p.ighn-FcC=<(9pecLWZ=jmZ(-U`9h.K.ZRZ]b\,%_r,rmDA>_IirqGUDB%U>0c;_R1of-]d8jnjM"ha8.Oj'P^"@d^ak*2N2=J9Y\.0'>:m5mcan\8)D0d;c'7"]Z7kceF3N&]&T1#C*9%

@U5iVF4dQUm'eN\B?:^2!.r_/!/RVq)bFI6LroDhNgc%-F=jd1<0h4U4>p>[ne%pD[A[Y$`+Wa:[%HJ$PN4k`n-qH[7/+0k0$`?b.eUr>g]1*o\'`/A'W?_ZLD_&FpW=b,GPM#`DSHa+'M9mT36GTo<=!dF'F]fK\_\#;lPM*._h=r0lYUNiP-kcrhAQ)M)b8+q\qVeF0C6aiaL7gZ,Is$EULBT[m)qi]5&L

AX6S)o$Ul=YN]-lMA,a!]6b1V!^)bghLV3SE<'(R9kEQecH'D;C,(sT"cQN%g[Ie7)Nkg;Ss4

B[7m\L6hW[q)d`G84>a1S(si<79]dhcA",'k=.8q2Grl1mjs<bRf;Upa!/S-O(p;_Tc8Y9,[/:XFl)f-/3#[68@\.%#jF3^M#O,5Fod"LCc)[@(b7G2)oG.Z/:Xq<UMU^q'`K([1[nsWN\l>lds9)-ckm5L>p-G[l[3$r6h6KN1)YI#W#LA2l`!,RMSL5BV/?+W;-irZdM2bk[msN8W,N.m=&_<g<H"MXr#Na)?PLTOrg-kIK-lrAQq=OC$LHepmGr5W*DK>^0f(XDa(Y+89,L'`=`.1K1*2`>XPhn7NOVS:Fo&UF6S/CG0VkJNLf@T8o*rZP-gRYiQ@%G!:"GX@,Lqlqcock.gS1!3S3Z6D-:rHM_V(hL"(9_<RcX1]go/OVO:ASn'$`Ij"4p0l4WF#F]c8Ak^q<gI%i%VDY%hsNUg'W21]Ip1lW,eE-KIKDr!dLoC

C^8q"U-qIeks%X/E)XJs+V[#+!cZ:DSW/W(boWX=2hN?O%/Ha#0*2&"neh8:Mo-.3dA>a'ABs@6U!gnh'8=[&#/-LG47(5`5mgQ?Q;I?XCi.KZW9*p&?;U3fnV:C+'-9f/n$2Mb'+ObgaC2"YR3?(7hO

Da9m9Qs?JGePHGDFcF,%CR7_-Afq.;.oI=.OmV12eI:^*;:ZH-s]pV*VmCEeLn$eYbmWhjK1MJ'($rL>3=hPa.aM&JG(?,)m8"G,_%JHQ#/6)&1sr-_KS7Jj:A5*Sfr!97IsFh[7J4Mprs'RJ5MU:%!e4F4D#^]_A=Y=WqZ8m=k=I4nrb"$B?RL=er?3<Og:-QIXI;b$ZSIhIVq"n$9i(pQA9b9geIs`sJ1jHLakGjXj8D\JTN_`PIS9qF*(V-\Ab6<)mF"_h]3>^2Wc*"(>S2BM9IG6Go$`e"AS!RKaA=le9m!YN=6e?O+qc7,p1T"nNa?LSpc_?FiN6sSKCF<NJTP5HbH"^!^LXH$f6D1C$a+.j>6^5a-.N<?n/IXlVW2Ui:Aq6%cBPb6\?f)Jci,\kf1Xj&!&,b,>SlPp"dQpQ4WGWlNH<C79Vl#+<c7=Osa(BTh'b*"*3>%-]WFZ<lro$lDb\b!k8A&WQUTg^"^h40^f(P&C-`\e^_q/Uhi&VQE1j+j-G/.*YW'''


REVISED_SECTIONS = tuple(REVISED_CIPHERTEXT.split("\n\n"))


def common_prefix_length(left: Sequence[object], right: Sequence[object]) -> int:
    """Return the number of equal leading items in two sequences."""
    for index, (left_item, right_item) in enumerate(zip(left, right, strict=False)):
        if left_item != right_item:
            return index
    return min(len(left), len(right))


Permutation = tuple[int, ...]
PermutationFactory = Callable[[int, int], Permutation]


# The recovered plaintext ordering.  Only indices 0..41 occur in the source;
# the shuffle itself acts on all 83 ciphertext-alphabet positions.
PLAINTEXT_ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 .\n,?-"


def recursive_increasing_chunk_reversal(size: int, index: int) -> Permutation:
    """Return sdlwdr #5's plaintext-selected recursive CTA shuffle.

    Starting with a packet of ``index + 1`` cards, peel successively larger
    packets from the front.  The recursive call operates on the remainder;
    concatenating on return reverses packet *order* while preserving the order
    inside every packet::

        recurse(deck, width) = recurse(deck[width:], width + 1) + deck[:width]

    Lower plaintext indices therefore make more recursive calls, exactly as
    the puzzle author's hints describe.
    """
    if not 0 <= index < size:
        raise ValueError("index must lie in 0..size-1")

    def recurse(deck: tuple[int, ...], width: int) -> tuple[int, ...]:
        if len(deck) <= width:
            return deck
        return recurse(deck[width:], width + 1) + deck[:width]

    return recurse(tuple(range(size)), index + 1)


def interleave_packets(
    deck: Sequence[int], split: int, *, right_first: bool = False
) -> tuple[int, ...]:
    """Cut at ``split`` and alternately deal from the two packets."""
    if not 0 <= split <= len(deck):
        raise ValueError("split must lie within the deck")
    packets = (deque(deck[:split]), deque(deck[split:]))
    turn = int(right_first)
    result: list[int] = []
    while packets[0] or packets[1]:
        if packets[turn]:
            result.append(packets[turn].popleft())
        else:
            result.append(packets[1 - turn].popleft())
        turn = 1 - turn
    return tuple(result)


def recursive_increasing_interleaves(
    size: int,
    index: int,
    *,
    one_based: bool = False,
    right_first: bool = False,
    recurse_first: bool = False,
) -> Permutation:
    """Materialize the most literal family described by the author's hints.

    Starting at the plaintext-selected split, interleave packets of sizes
    ``split`` and ``n-split`` and recurse at the next split.  A lower starting
    split therefore causes more recursive layers.  ``recurse_first`` reverses
    the composition order, corresponding to performing work while the
    recursive calls unwind.
    """
    if not 0 <= index < size:
        raise ValueError("index must lie in 0..size-1")
    start = index + int(one_based)
    splits = range(max(1, start), size)
    if recurse_first:
        splits = reversed(tuple(splits))
    deck: tuple[int, ...] = tuple(range(size))
    for split in splits:
        deck = interleave_packets(deck, split, right_first=right_first)
    return deck


def recursive_fixed_interleave(
    size: int,
    index: int,
    *,
    one_based: bool = False,
    right_first: bool = False,
    recurse_first: bool = False,
) -> Permutation:
    """Peel fixed-size packets recursively and interleave them on return.

    This is the other direct reading of the hints: the selected index fixes
    the packet size, so smaller packets create more recursive levels.
    """
    if not 0 <= index < size:
        raise ValueError("index must lie in 0..size-1")
    width = index + int(one_based)
    if width < 1:
        width = 1

    def shuffle(deck: tuple[int, ...]) -> tuple[int, ...]:
        if len(deck) <= width:
            return deck
        left, right = deck[:width], deck[width:]
        if recurse_first:
            right = shuffle(right)
            return interleave_packets(
                left + right, len(left), right_first=right_first
            )
        mixed = interleave_packets(
            left + right, len(left), right_first=right_first
        )
        # Recurse on the still-unprocessed suffix while keeping the first
        # packet fixed.  This is distinct from unwinding the recursive calls.
        return mixed[:width] + shuffle(mixed[width:])

    return shuffle(tuple(range(size)))


def decode_dynamic_substitution(
    ciphertext: Sequence[int],
    operations: Sequence[Permutation],
    *,
    initial_deck: Sequence[int] | None = None,
    update_before_output: bool = False,
) -> tuple[int, ...]:
    """Decode a plaintext-indexed, dynamically permuted ciphertext alphabet.

    In the ordinary form the current rank of the observed card is the
    plaintext index, after which that index's permutation updates the deck.
    The alternate form tries every operation before observing the card and
    requires the output at the same selected index; it is retained because the
    thread does not state whether the shuffle precedes or follows emission.
    """
    size = len(operations)
    if any(len(permutation) != size for permutation in operations):
        raise ValueError("operations must be square permutations")
    deck = tuple(range(size)) if initial_deck is None else tuple(initial_deck)
    if sorted(deck) != list(range(size)):
        raise ValueError("initial deck must permute 0..size-1")
    plaintext: list[int] = []
    for card in ciphertext:
        if not 0 <= card < size:
            raise ValueError("ciphertext card lies outside the deck")
        if update_before_output:
            matches: list[tuple[int, tuple[int, ...]]] = []
            for index, permutation in enumerate(operations):
                candidate = tuple(deck[position] for position in permutation)
                if candidate[index] == card:
                    matches.append((index, candidate))
            if len(matches) != 1:
                raise ValueError(f"expected one update-before-output match, got {len(matches)}")
            index, deck = matches[0]
        else:
            index = deck.index(card)
            permutation = operations[index]
            deck = tuple(deck[position] for position in permutation)
        plaintext.append(index)
    return tuple(plaintext)


def encode_dynamic_substitution(
    plaintext: Sequence[int],
    operations: Sequence[Permutation],
    *,
    initial_deck: Sequence[int] | None = None,
) -> tuple[int, ...]:
    """Encode plaintext ranks using the emit-then-update convention."""
    size = len(operations)
    if any(len(permutation) != size for permutation in operations):
        raise ValueError("operations must be square permutations")
    deck = tuple(range(size)) if initial_deck is None else tuple(initial_deck)
    if sorted(deck) != list(range(size)):
        raise ValueError("initial deck must permute 0..size-1")
    ciphertext: list[int] = []
    for index in plaintext:
        if not 0 <= index < size:
            raise ValueError("plaintext rank lies outside the deck")
        ciphertext.append(deck[index])
        deck = tuple(deck[position] for position in operations[index])
    return tuple(ciphertext)


def decode_revised_sections() -> tuple[tuple[int, ...], ...]:
    """Decode all nine revised sections to plaintext-alphabet indices."""
    operations = tuple(
        recursive_increasing_chunk_reversal(83, index) for index in range(83)
    )
    return tuple(
        decode_dynamic_substitution(
            tuple(ord(character) - 33 for character in section), operations
        )
        for section in REVISED_SECTIONS
    )


def render_plaintext(indices: Sequence[int]) -> str:
    """Render recovered plaintext indices with the 42-symbol ordering."""
    try:
        return "".join(PLAINTEXT_ALPHABET[index] for index in indices)
    except IndexError as error:
        raise ValueError("unmapped plaintext index") from error
