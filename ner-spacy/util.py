import spacy
from string import punctuation

def load_data(filename):
    data = []
    with open(filename, "r") as f:
        content = f.readlines()
    for line in content:
        l = line.strip("\n").split(sep=";")
        ent = {"entities": []}
        for i in l[1:]:
            i = i.split(sep=",")
            ent["entities"].append((int(i[0]),int(i[1]),str(i[2])))
        data.append((l[0],ent))
    return data


def load_conll(filename, word_pos=0, label_pos=-1):
    data =[]
    nlp = spacy.load("en_core_web_sm")
    with open(filename, "r") as f:
        content = f.readlines()
    s = ""
    tags = []
    for line in content:
        if line != "\n":
            l = line.strip("\n").split(sep="\t")
            if l[word_pos] in punctuation:
                s = s.rstrip()
            s += l[word_pos] + " "
            tags.append(l[label_pos])
        else:
            data.append((s, {"entities": offsets_from_biluo_tags(nlp(s), tags)}))
            s = ""
            tags = []
    return data


def tags_to_entities(tags):
    entities = []
    start = None
    t = ""
    for i, tag in enumerate(tags):
        if tag is None:
            continue
        if tag.startswith('O'):
            if start is not None:
                entities.append((t, start, i-1))
                start = None
            continue
        elif tag.startswith('I'):
            if start is not None:
                t = tag[2:]
        elif tag.startswith('B'):
            t = tag[2:]
            start = i
        else:
            raise Exception(tag)
    return entities

def offsets_from_biluo_tags(doc, tags):
    """Encode per-token tags following the BILUO scheme into entity offsets.
    doc (Doc): The document that the BILUO tags refer to.
    entities (iterable): A sequence of BILUO tags with each tag describing one
        token. Each tags string will be of the form of either "", "O" or
        "{action}-{label}", where action is one of "B", "I", "L", "U".
    RETURNS (list): A sequence of `(start, end, label)` triples. `start` and
        `end` will be character-offset integers denoting the slice into the
        original string.
    """
    token_offsets = tags_to_entities(tags)
    offsets = []
    for label, start_idx, end_idx in token_offsets:
        span = doc[start_idx : end_idx + 1]
        offsets.append((span.start_char, span.end_char, label))
    return offsets


if __name__ == "__main__":
    d = load_conll("data/test.txt")
    print(d[10])
    # nlp = en_core_web_sm.load()
    # doc = nlp(d[10][0])
    # print(offsets_from_biluo_tags(doc, d[10][1]))
    # # {"entities": offsets_from_biluo_tags(nlp(s), tags)}
