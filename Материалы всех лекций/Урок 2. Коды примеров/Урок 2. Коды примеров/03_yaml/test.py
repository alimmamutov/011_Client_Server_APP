from chardet import detect

with open('yaml_examples.yaml', 'rb') as f_obj:
    content_bytes = f_obj.read()
detected = detect(content_bytes)
encoding = detected['encoding']
content_text = content_bytes.decode(encoding)
with open('yaml_examples.yaml', 'w', encoding='utf-8') as f_obj:
    f_obj.write(content_text)