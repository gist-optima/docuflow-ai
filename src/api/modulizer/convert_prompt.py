# %%
import json

# %%
with open('prompt.txt', 'r') as f:
    content=f.read()

content=json.dumps(content, ensure_ascii=False, indent=4)
prompt={"content": content}
print(prompt)

with open('prompt.json', 'w') as f:
    f.write(json.dumps(prompt, ensure_ascii=False, indent=4))

# %%
