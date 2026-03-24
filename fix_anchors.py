import codecs

with codecs.open('index.html', 'r', 'utf-8') as f:
    html = f.read()

# The missing closing anchor tags because of \r\n
html = html.replace('opacity(0.8);">\r\n          </div>', 'opacity(0.8);"></a>\r\n          </div>')
html = html.replace('opacity(0.8);">\n          </div>', 'opacity(0.8);"></a>\n          </div>')

with codecs.open('index.html', 'w', 'utf-8') as f:
    f.write(html)
