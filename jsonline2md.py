import json

img_with_link = '[![alt text](%s)](%s)'

f_out = open(r'res\res.md', 'w', encoding='utf-8')
f_in = open(r'res\bti_2016-10-29T09-32-23.json', encoding='utf-8')

f_out.write('''name | type | price | image
--- | --- | --- | ---
''')

for line in f_in:
    d = json.loads(line, encoding='utf-8')
    f_out.write(' | '.join([
        d['name'],
        d['type'],
        d['package_price'],
        img_with_link % (d['image_urls'][0].split('/')[-1], d['url'])
        ]))
    f_out.write('\n')

f_in.close()
f_out.close()
