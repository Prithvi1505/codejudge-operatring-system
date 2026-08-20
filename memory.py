PAGE_SIZE = 1024
PAGE_TABLE = {0: 5, 1: 2, 2: 9, 3: 1}
SEGMENT_TABLE = {0: (1000, 400), 1: (2200, 300), 2: (500, 150)}

def translate_paged(addr):
    page = addr // PAGE_SIZE
    offset = addr % PAGE_SIZE
    if page not in PAGE_TABLE:
        return f"Page fault for address {addr}"
    frame = PAGE_TABLE[page]
    return frame * PAGE_SIZE + offset

def translate_segmented(seg, offset):
    if seg not in SEGMENT_TABLE:
        return "Invalid segment"
    base, limit = SEGMENT_TABLE[seg]
    if offset >= limit:
        return f"Segmentation fault for ({seg}, {offset})"
    return base + offset

print("Paging:")
for a in [260, 1500, 3000, 5000]:
    print(a, "→", translate_paged(a))

print("\nSegmentation:")
for s, o in [(0, 150), (1, 350), (2, 100)]:
    print(f"({s}, {o}) →", translate_segmented(s, o))
