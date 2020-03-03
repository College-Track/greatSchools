---
jupyter:
  jupytext:
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.2'
      jupytext_version: 1.3.0
  kernelspec:
    display_name: Python 3
    language: python
    name: python3
---

```python
import pandas as pd
import numpy as np
import os

```

```python
STATES_TO_INCLUDE = ['CA', 'LA', 'VA', 'CO', 'DC', 'MD']
```

```python
entries = os.listdir('local-gs-census-feed-flat/')
files_to_read = []
```

```python
for entry in entries:
    if entry.split('-')[5].split('.')[0] in STATES_TO_INCLUDE:
        files_to_read.append(entry)
```

```python
_df_list = []

for i in range(len(files_to_read)):
        _df = (pd.read_csv("local-gs-census-feed-flat/"+files_to_read[i], sep='\t', header=0))
        _df['state'] = files_to_read[i].split('-')[5].split('.')[0]
        _df_list.append(_df)

```

```python
df = pd.concat(_df_list, axis=0, ignore_index=True)
```

```python
def create_column_names(data_type, breakdown):
    if pd.isnull(breakdown) == True:
        return data_type
    else:
        return data_type + "-" + breakdown
```

```python
df['column_names'] = df.apply(lambda x: create_column_names(x['data-type'], x['breakdown']),axis=1)
```

```python
df_wide = df.pivot_table(index=['universal-id', 'entity', 'state'], columns='column_names', values='value',aggfunc=np.sum)
```

```python
df_wide
```

```python
df_wide.to_csv('test.csv')
```
