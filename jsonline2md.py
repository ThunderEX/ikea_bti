import glob
import json
from urllib.parse import urlparse, urlunparse


def process():
    img_with_link = r'[![alt text](res\%s)](%s)'
    path_in = glob.glob(r'res\bti_*.json')
    if len(path_in) > 1:
        print('more than one Scrapy result, use latest one.')
    elif len(path_in) == 0:
        raise ValueError('No Scrapy result find.')
    path_in = sorted(path_in)[-1]

    f_out = open(r'res.md', 'w', encoding='utf-8')
    f_in = open(path_in, encoding='utf-8')

    f_out.write('''name | type | price | family_price | image
--- | --- | --- | --- | ---
''')

    for line in f_in:
        d = json.loads(line, encoding='utf-8')

        # clear query in url in case there are any vertical bar "|" which break markdown table delimiter
        url = urlunparse(urlparse(d['url'])._replace(query=''))

        f_out.write(' | '.join([
            d['name'],
            d['type'],
            d['package_price'],
            d['family_price'],
            img_with_link % (d['image_urls'][0].split('/')[-1], url)
            ]))
        f_out.write('\n')

    f_in.close()
    f_out.close()

if __name__ == "__main__":
    process()
