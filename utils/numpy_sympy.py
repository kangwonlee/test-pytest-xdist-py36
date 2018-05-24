import ast
import os
import subprocess
import sys

import nbformat

import recursively_convert_units as rcu
import nbutils.nb_file_util as fu


def main(argv):

    # no argument
    if not argv:
        root = os.pardir
    else:
        root = argv[0]

    # Chapter folder
    for root_dir, _, filename_list in rcu.os_walk_if_not_ignore(root):

        # Notebook file loop
        for ipynb_filename in filter(rcu.is_ipynb, filename_list):

            process_one_ipynb_file(root_dir, ipynb_filename,)


def process_one_ipynb_file(root_dir, ipynb_filename,):
    ipynb_filename_name = os.path.splitext(ipynb_filename)[0]

    py_filename_full_path = os.path.join(root_dir, ipynb_filename_name + '.py')

    if os.path.exists(py_filename_full_path):
        raise IOError('file %s already exists.' % py_filename_full_path)

    # convert a .ipynb file into a .py file
    conversion_cmd = get_conversion_cmd_list(root_dir, ipynb_filename)

    print(conversion_cmd)

    p = subprocess.Popen(conversion_cmd, 
                         stdout=subprocess.PIPE, 
                         stderr=subprocess.PIPE)
    fo, fe = p.stdout, p.stderr

    stdout = fo.read().decode('utf-8')
    stderr = fe.read().decode('utf-8')

    fo.close()
    fe.close()

    if stdout:
        print('stdout:\n%s' % stdout)
    if stderr:
        print('stderr:\n%s' % stderr)

    if os.path.exists(py_filename_full_path):
        os.remove(py_filename_full_path)

    if os.path.exists(py_filename_full_path):
        raise IOError('unable to remove file %s.' % py_filename_full_path)


def get_conversion_cmd_list(root_dir, ipynb_filename):
    # convert a .ipynb file into a .py file
    conversion_cmd = ['jupyter', 'nbconvert', 
                      '--to', 'python', 
                      '--output-dir='+root_dir,
                      os.path.join(root_dir, ipynb_filename)]

    return conversion_cmd


if "__main__" == __name__:
    main(sys.argv[1:])
