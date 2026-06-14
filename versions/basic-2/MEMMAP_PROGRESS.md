# BBC BASIC II — memory-map document

**STATUS: COMPLETE — 52 memory-map entries across 5 groups.** The
`bbc-basic/2-memory-map.html` page renders, the disassembly listing links
memory references into it (~1300 links), and every `address:` link
(analysis docs included) resolves. Build is byte-identical and clean.

Turn the driver's sub-&8000 data labels (zero
page, the 6502 stack, the resident-integer / FP workspace, the
FOR/REPEAT/GOSUB stacks, and the buffers) into a rendered memory-map
page on the site, and make `address:` links to those locations resolve.

## How it works (from the site generator + acorn-econet-bridge)

A `d.label(addr, name, …)` that also carries `description=`, `length=`,
`group=` and `access=` kwargs is emitted into the disassembly JSON's
`memory_map` array (in addition to being a normal label). The site then:

- generates `<version>-memory-map.html` whenever the JSON has a
  `memory_map`, grouped by `group` (display titles + order come from
  `rom.json`'s `memory_map_groups`; ties broken by declaration order);
- resolves `[`name`](address:XXXX)` links — in analysis docs, in the
  listing, and within memory-map descriptions — to `#mm-NAME` on that
  page (or to `version.html#addr-XXXX` for ROM code).

So: enrich the base label of each logical location, add the group titles
to `rom.json`, rebuild. Multi-byte values get ONE entry on the base
label with `length=N`; continuation labels (`_1`, `_2`, …) stay plain.
Indexing-base/accessor labels (e.g. `for_var_lo`, `for_set_*`) stay
plain — the map describes locations, not the indexing tricks.

Group keys (declaration/display order): `zero_page`, `stack_6502`,
`resident_vars`, `basic_stacks`, `buffers`.

## Sources for descriptions

Code usage (the labelling pass), the existing inline ZP comments, and
the standard BBC BASIC zero-page map (consistent with Pharo's *Advanced
BASIC ROM User Guide* ch. 7 and J.G. Harston's reconstruction). No local
OCR of Pharo's text — descriptions are written from the code and the
established map, not quoted.

## Workflow / verification per batch

1. Enrich the base labels for a region with description/length/group/
   access. Cross-link related locations with `[`name`](address:XXXX)`.
2. `uv run fantasm disassemble 2`, `verify 2` (byte-identical — labels
   emit no bytes), `lint`, `comments check`, `driver sort --check`.
3. In the site repo: `uv run python -m generator.build`; confirm
   `bbc-basic/2-memory-map.html` and that the region's `address:` links
   no longer warn.

## Batch log

| Region | Entries | Status |
|--------|---------|--------|
| Zero page (&00-&FF) | 41 | done |
| 6502 stack (&0100) | 1 | done |
| Resident integers & FP workspace (&0400-&0480) | 3 | done |
| FOR/REPEAT/GOSUB stacks (&0500-&05E6) | 5 | done |
| Buffers (&0600, &0700) | 2 | done |
| **Total** | **52** | |

## Resume here

**COMPLETE.** All 52 entries are in; `2-memory-map.html` renders five
groups; the listing and all analysis docs link into it with no
unresolved-address warnings (the 7 previously-broken control-flow-stacks
links now resolve). Multi-byte values are single entries; accessor /
indexing-base labels (`for_var_*`, `for_set_*`, `repeat_loop_*`,
`gosub_return_*`, `frame_local_count`, `strbuf_base`, …) deliberately
stay plain.

If extending: enrich a label by adding `description=`/`length=`/`group=`/
`access=`; add any new `group` key to `rom.json`'s `memory_map_groups`;
rebuild the site to check links.
