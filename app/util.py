def formats(text):
    sentences = text.split('\n')
    return sentences

def extract(pattern):
    sections = {}
    sections['name'] = pattern['name']
    sections['description'] = formats(pattern['description'])
    sections['url'] = pattern['external_references'][0]['url']
    return sections
