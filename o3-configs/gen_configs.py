#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import shutil
from pathlib import Path
from jinja2 import Environment, FileSystemLoader

"""
Util for generating cpu model folders with different parameters.
"""

template_folder = Path('./templates/')
init_template = template_folder / '__init__.py'
out_folder = Path('./models/')
out_list = Path('./configs.txt')

env = Environment(loader=FileSystemLoader(str(template_folder)))

cpus = ['A76', 'HP']
template_files = {'A76':'A76.py.jinja', 'HP':'HP.py.jinja'}
simdFU = {'A76':[1, 2], 'HP':[1, 2, 3]}
penalty = [0, 1]
fuseCap = [0, 3]

out_folder.mkdir(parents=True, exist_ok=True)
with open(str(out_folder / '__init__.py'), 'w') as f:
    f.write('')

folder_list = []
for cpu in cpus:
    template = env.get_template(template_files[cpu])

    # Generate empty init.
    path = out_folder / cpu
    path.mkdir(parents=True, exist_ok=True)
    with open(str(path / '__init__.py'), 'w') as f:
        f.write('')

    for fu in simdFU[cpu]:
        for pen in penalty:
            for cap in fuseCap:
                parsed = template.render(simdFU=fu, penalty=pen, fuseCap=cap)

                # Create cpu model.
                folder_name = '{0}/{0}_{1}fu_{2}pen_{3}cap'.format(cpu, fu, pen, cap)
                path = out_folder / folder_name
                path.mkdir(parents=True, exist_ok=True)
                with open(str(path / 'O3_ARM_v7a.py'), 'w') as f:
                    f.write(parsed)

                # Copy __init__.py.
                init = path / '__init__.py'
                shutil.copy(init_template, init)

                # Add path to list.
                folder_list.append(folder_name.replace('/', '.'))

# Print modules list.
with open(str(out_list), 'w') as f:
    f.write('\n'.join(folder_list))
