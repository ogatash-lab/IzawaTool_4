import os
import difflib

dir_path = 'verification-tool/linkfailure-log/'

file1_name = 'linkfailure-link-Cf1-Cf3-before-Cf3.txt'
file2_name = 'linkfailure-link-Cf1-Cf3-after-Cf3.txt'

file1_path = os.path.join(dir_path, file1_name)
file2_path = os.path.join(dir_path, file2_name)

file1 = open(file1_path)
file2 = open(file2_path)
diff = difflib.HtmlDiff()

output_name = 'diff.html'
output_path = os.path.join(dir_path, output_name)

output = open(output_path, 'w')
output.writelines(diff.make_file(file1, file2, fromdesc='linkfailure-link-Cf1-Cf3-before-Cf3', todesc="linkfailure-link-Cf1-Cf3-after-Cf3"))

file1.close()
file2.close()
output.close()