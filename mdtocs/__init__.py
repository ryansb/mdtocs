import os
import re
import md5
from argparse import ArgumentParser


def strip_existing_toc(lines):
    skip = 0
    if '#Table of Contents' in lines[0]:
        skip += 1
        for l in lines[1:]:
            if l.startswith('#'):
                break
            skip += 1
    return lines[skip:]


def get_headers(lines):
    # Header forms
    # h1   h2  #h1  ##h2  ###h3  ...
    # ==   --
    underlined_h1 = re.compile(r'^=+$')
    underlined_h2 = re.compile(r'^-+$')
    hashed_re = re.compile(r'^#+')
    for idx in range(len(lines)):
        if hashed_re.match(lines[idx]):
            h = re.sub(r'[ #]+$', '', lines[idx]) # remove trailing #'s
            yield (# H<N> where N=number of #'s
                len(re.search('^(#+)', h).group()) - 1,
                hashed_re.sub('', h).strip()
            )
        elif underlined_h1.match(lines[idx]):
            yield (0, lines[idx - 1].strip())

        elif underlined_h2.match(lines[idx]):
            yield (1, lines[idx - 1].strip())


def tocify(lines):
    slugify_re = re.compile(r'[^a-z0-9-]')
    TOC = [
        '#Table of Contents\n\ngenerated by [mtdocs](http://mdtocs.rsb.io/)\n']
    TOC_line = "{indent}- [{header}](#{slug})"
    for level, header in get_headers(lines):
        TOC.append(TOC_line.format(
                indent=('\t' * level),
                header=header,
                slug=slugify_re.sub('', header.lower().replace(' ', '-'))
        ))
    return '\n'.join(TOC) + '\n\n' + ''.join(lines)


def tocify_file_list(fnames):
    for fname in fnames:
        with open(fname, 'rw+') as f:
            lines = f.readlines()
            orig_hash = md5.new('\n'.join(lines)).hexdigest()
            out = tocify(strip_existing_toc(lines))
            if not md5.new(out).hexdigest() == orig_hash:
                print 'Updated TOC in', fname
            f.seek(0)
            f.write(out)


def find_files(names, recurse):
    if not len(names):
        names = os.listdir(os.getcwd())
    for name in [n for n in names if os.path.exists(n)]:
        if os.path.isfile(name) and (name.endswith('.md')
                                     or name.endswith('.markdown')):
            yield name
            continue
        if os.path.isdir(name) and recurse:
            for path, _, files in os.walk(name):
                for f in files:
                    if f.endswith('.md') or f.endswith('.markdown'):
                        yield os.path.join(path, f)


def run_tests():
    import unittest

    class TestMDTOCS(unittest.TestCase):
        def setUp(self):
            self.corpus = """#My Cool Document

Is a document

##Subheading

Subheadings are key to nirvana

With Underlined subheader
-------------------------

And information

###And Subsubheadings

The end, dude.
"""
            self.expected = """#Table of Contents

generated by [mtdocs](http://mdtocs.rsb.io/)

- [My Cool Document](#my-cool-document)
	- [Subheading](#subheading)
	- [With Underlined subheader](#with-underlined-subheader)
		- [And Subsubheadings](#and-subsubheadings)

""" + self.corpus
            self.modified_toc = self.expected.replace(
                '- [My Cool Document](#my-cool-document)', '')

        def test_underline(self):
            h = get_headers([
                'Hello H1',
                '========',
                'Hello H2',
                '--------'
            ])
            self.assertListEqual(list(h), [(0, 'Hello H1'), (1, 'Hello H2')])

        def test_hash(self):
            h = get_headers([
                '#Hello H1',
                '##Hello H2',
                '###Hello H3',
                '####Hello H4',
                '#####Hello H5',
            ])
            self.assertListEqual(list(h), [
                (0, 'Hello H1'),
                (1, 'Hello H2'),
                (2, 'Hello H3'),
                (3, 'Hello H4'),
                (4, 'Hello H5'),
            ])

        def test_toc_generation(self):
            from StringIO import StringIO
            self.assertEqual(tocify(StringIO(self.corpus).readlines()),
                             self.expected)

        def test_toc_detection(self):
            from StringIO import StringIO
            self.assertEqual(tocify(strip_existing_toc(StringIO(self.expected).readlines())),
                             self.expected)

        def test_toc_update(self):
            from StringIO import StringIO
            self.assertEqual(tocify(strip_existing_toc(StringIO(self.modified_toc).readlines())),
                             self.expected)

    suite = unittest.TestLoader().loadTestsFromTestCase(TestMDTOCS)
    unittest.TextTestRunner(verbosity=2).run(suite)


def main():
    parser = ArgumentParser(
        description='MDTOCS: MarkDown Table Of Contents System'
    )
    parser.add_argument('locations', type=str, nargs='*',
                        help='Markdown files or directories containing '
                        'markdown files.')
    parser.add_argument('--recurse', '-r', dest='recurse', default=False,
                        action='store_true',
                        help='Recurse into subdirectories looking for '
                        'markdown files.')
    parser.add_argument('--test', action='store_true', dest='test',
                        default=False, help='Run unittest tests')
    args = parser.parse_args()
    if args.test:
        run_tests()
        return
    else:
        tocify_file_list(find_files(args.locations, recurse=args.recurse))

if __name__ == '__main__':
    main()
