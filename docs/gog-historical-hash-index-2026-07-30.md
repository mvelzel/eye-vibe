# GOG historical build hash index — 2026-07-30

## What this records

GOGDB exposes the historical Noita build IDs and links to GOG content-system
v2 metadata.  The metadata is public (zlib-compressed JSON) and gives exact
file hashes, but the depot chunks require an authenticated GOG `secure_link`.
This index is therefore a reproducible target for a legitimately acquired
old build, not a downloaded game snapshot.

Sources:

- [GOGDB Noita product/build list](https://www.gogdb.org/product/1310457090)
- [Example 2020-05-20 build](https://www.gogdb.org/product/1310457090/build/53351147046566224)
- [2020-05-20 v2 depot metadata](https://cdn.gog.com/content-system/v2/meta/e9/e3/e9e35a6f525aea98e5bba45351359f0a)

For a build page, take its `/meta/<hash>` link, read the first depot's
`manifest`, then fetch `https://cdn.gog.com/content-system/v2/meta/<first two
bytes>/<next two bytes>/<manifest>`.  The `data\\data.wak` item supplies the
whole-file MD5; `noita.exe` supplies a SHA-256.  No depot content was fetched
without entitlement (`secure_link` returns HTTP 401 unauthenticated).

## Selected exact fingerprints

```text
build/version       data.wak MD5                         noita.exe SHA-256
20190923-2337       2684510301388bfc0ee9ca6092f3b0d2     ad2d48b381548d21741008e261e37d6a38b3de765a64c1f1d7b58b376a9bb638
20191023-1833       dab927654da64a4283ea1f81914596c6     1fbd13a1b89d52666a157110cc3b6c71b099915bac073ba4aaefe5ca72784c06
20200108-1326       540f3fdbd00116031148d9ca83925fa6     f08ae0102dd504c63fb48509321957db89907fd3ec4690548d5691caf9d08d58
20200320-1630       9ee8d36d3d93b9f4e9498078c8f9783b     de5dd1ae4ab016ff22b057df98c18690bee0ed23b40f89238d5877f7d957c192
20200430-1833       b2db18205a9996486bf98dad648fd80a     90b502c1471aba048141ef95ad1c7d3144243dc42b58616f4f581bad637985e0
20200520-1821       3129ee3e8b556477147a866017ead0b4     c5e8a689166cadd2239f2dde79f79af3d7ae4961171c4c2d1279daa8498ab0b2
20200624-1902       1bb4e900125c3b83672d6157c68188dd     9433f8fdb9e7518692edc090c6044cce7d202259195cd4aa91eecb10e7f171d8
20200630-2057       3db8f7eeaccb4c2c03cef79d57eec454     828d104129e748428f8269296f91d2edd645c8e4cb66e5a87ca98a3af5e26d4a
20200715-1443       3db8f7eeaccb4c2c03cef79d57eec454     6e3359dd1f7c11ee67cbd78ca235d2e318f907841d7e44ac27ee84adcc8c16d9
20201015-1909       00fec0a3b4bc3fb3bf6fac8117b3c436     4827f81c6056ce5422fac98b1580f09742337076ab1e5b15981c0a9956c87244
20201201-1702       16feeaadbac85bb9c8b4f1fcf7adfdbb     dede58380accb370e5c5ffb2e05057ee0ce8fd6272f338ec5c6943544dee5659
20210205-2304       f42f087c54cafe10c1cf4469aaafb56a     08d8ffa3d488fa61f21b16e72c19f94748481a086f23f71668e1cd36fa9e2ef6
20210330-0348       3eb17f99c70b2f003a8e4b25a9a97b91     11e11b8167d8b538d8ab5e02405929fb1eebeffa1deb24ecb1cc9c996de59ffb
20210402-2249       892e48b7f79f5bd93305e1a8825b4a68     8807c2f9943a941239c061e3bff7b1565c29fe2417458c5215c275b9c4e3b26e
20210415-2049       410da4c320f9054704c6e4bad73f9aef     2c1f34fef44bd264efb2ce359185b8ef58f08851bf650e3f09cc660ea3bf9736
20210423-1929       72a04d6ecf66ff819926d03138d50d89     e0bbee32eaabd60eaccc42ae4627c003cdbf00ef14730bd55c4ef74d8fd8f0fd
```

The build metadata includes additional 2019–2021 intermediate rows; the
table retains one row per meaningful release transition.  A matching
`data.wak` hash would establish which historical asset was obtained, after
which its Eye initializer can be compared byte-for-byte with the current
corpus.  Hash continuity alone does not prove when the Eye arrays were
authored.

## Result

This closes the public-metadata side of the historical snapshot search.  It
does not recover the 2020 payload: GOG's CDN intentionally requires a user
token for chunk URLs.  No pre-2021 public mirror examined here supplied a
verified payload, and no source-side key or decoder appears in the metadata.
