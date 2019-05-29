import gutenberg.query as q
import gutenberg.acquire as ac
import gutenberg.cleanup as cl
import re


def get_metadata(idx):
    ret = {}
    keys = q.list_supported_metadatas()
    for key in keys:
        ret[key] = list(q.get_metadata(key, idx))
    content = get_content(idx)
    ret['length'] = len(content)
    print(ret)
    return ret


def search_by_title(title):
    result = q.get_etexts('title', title)
    return list(result)


def get_content(idx):
    raw = cl.strip_headers(ac.load_etext(idx)).strip()
    pattern = re.compile('[ \n\t]')
    return pattern.split(raw)
