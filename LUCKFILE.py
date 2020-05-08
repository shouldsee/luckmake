#-*- coding: future_fstrings -*- 
_ = '''
The new LUCK system aims at mimicing the Makefile syntax by leveraging delayed evaluation.
It's aimed at capturing the dependency relations using pure python.

It uses f-string for string-replacement
It uses lambda expression for deference.
It uses DelayedNameSpace(AttrDict) to allow synchronised evaluation.
It uses 
'''


from luck.types import DNS,DNSUB,DelayedNameSpace
from luck.types import Rule
from luck.types import RuleNameSpace
from luck.types import RuleNameSpace as RNS
from luck.types import LSC
from luck.types import MakefilePattern, AutoCmd
from attrdict import AttrDict



CC = "gcc"
AR = "ar"
RANLIB = "ranlib"

CPPFLAGS = ""
# TODO: make the 64-bit support for VCF optional via configure, for now add -DVCF_ALLOW_INT64
#       to CFLAGS manually, here or in config.mk if the latter exists.
# TODO: probably update cram code to make it compile cleanly with -Wc++-compat
# For testing strict C99 support add -std=c99 -D_XOPEN_SOURCE=600
#CFLAGS   = -g -Wall -O2 -pedantic -std=c99 -D_XOPEN_SOURCE=600
CFLAGS   = "-g -Wall -O2 -fvisibility=hidden"
EXTRA_CFLAGS_PIC = "-fpic"
LDFLAGS  = "-fvisibility=hidden"
# LIBS     = f"{htslib_default_libs}"



prefix="/usr/local"
exec_prefix = f"{prefix}"

BUILT_PROGRAMS = '''
bgzip
htsfile
tabix
'''.strip().splitlines()

BUILT_TEST_PROGRAM = '''\
test/hts_endian \
test/fieldarith \
test/hfile \
test/pileup \
test/sam \
test/test_bgzf \
test/test_kstring \
test/test_realn \
test/test-regidx \
test/test_str2int \
test/test_view \
test/test_index \
test/test-vcf-api \
test/test-vcf-sweep \
test/test-bcf-sr \
test/fuzz/hts_open_fuzzer.o \
test/test-bcf-translate \
test/test-parse-reg
'''.strip().split()

BUILT_THRASH_PROGRAMS = '''
test/thrash_threads1 \
test/thrash_threads2 \
test/thrash_threads3 \
test/thrash_threads4 \
test/thrash_threads5 \
test/thrash_threads6 \
test/thrash_threads7	
'''.strip().split()


_ = '''

%.o : %.c
	$(CC) $(CFLAGS) -I. $(CPPFLAGS) -c -o $@ $<

%.pico: %.c
	$(CC) $(CFLAGS) -I. $(CPPFLAGS) $(EXTRA_CFLAGS_PIC) -c -o $@ $<
# % : RCS/%.v
# 	$(CO) $(COFLAGS) $<

%:;
	touch $(basename $@).undefined

'''


patterns = AttrDict([
(0, MakefilePattern('%.o', '%.c',   
	lambda x: LSC(f'{CC} -I. -c {CFLAGS} {CPPFLAGS} -c -o {x.outputs[0]} {x.inputs[0]}')) ), ### x.inputs is a list, x.output is a string
(1, MakefilePattern('%.pico','%.c', 
	lambda x: LSC(f'{CC} {CFLAGS} -I. {CPPFLAGS} {EXTRA_CFLAGS_PIC} -c -o {x.outputs[0]} {x.inputs[0]}'))),
])


### expanding all into a list of nodes
# dict( key='all', inputs = f'lib-static lib-shared {BUILT_PROGRAMS} plugins {BUILT_PROGRAMS} {BUILT_TEST_PROGRAM}\
#  htslib_static.mk htslib-uninstalled.pc',func=None)


h = DNSUB('HtslibDict')
h.htslib_sam_h = lambda: 'htslib_sam.h'
h.htslib_hts_endian_h = lambda: 'htslib_hts_endian.h'
h.htslib_thread_pool_h = lambda: 'htslib_thread_pool_h'
h.htslib_cram_h = lambda: 'htslib_cram_h'
h.htslib_khash_h = lambda: 'htslib_khash_h'
h.htslib_synced_bcf_reader_h = lambda: 'htslib_synced_bcf_reader_h'
h.htslib_kbitset_h  = lambda: 'htslib_kbitset_h'
h.htslib_kstring_h  = lambda: 'htslib_kstring_h'
h.htslib_hts_h      = lambda: 'htslib_hts_h'
h.htslib_hts_defs_h = lambda: 'htslib_hts_defs_h'
h.htslib_hfile_h    = lambda: 'htslib_hfile_h'
h.htslib_bgzf_h     = 'htslib_bgzf_h'


d = DNSUB('CramDict')
d.cram_h          = lambda : f'cram/cram.h {d.cram_samtools_h} {d.header_h} {d.cram_structs_h} {d.cram_io_h} \
cram/cram_encode.h cram/cram_decode.h cram/cram_stats.h cram/cram_codecs.h cram/cram_index.h {h.htslib_cram_h}'
d.cram_io_h       = lambda : f'cram/cram_io.h {d.cram_misc_h}'
d.cram_misc_h     = lambda : f'cram/cram_misc_h'
d.cram_os_h       = lambda : f'cram/os.h {h.htslib_hts_endian_h}'
d.cram_samtools_h = lambda : f'cram/cram_samtools.h {h.htslib_sam_h}'
d.cram_structs_h  = lambda : f'cram/cram_structs.h {h.htslib_thread_pool_h} {h.htslib_cram_h} cram/string_alloc.h cram/mFILE.h {h.htslib_khash_h}'
d.cram_open_trace_file_h = lambda :f'cram/open_trace_file.h cram/mFILE.h'
d.bcf_sr_sort_h   = lambda : f'bcf_sr_sort.h {h.htslib_synced_bcf_reader_h} {h.htslib_kbitset_h}'
d.header_h        = lambda : f'header.h cram/string_alloc.h cram/pooled_alloc.h {h.htslib_khash_h} {h.htslib_kstring_h} {h.htslib_sam_h}'
d.hfile_internal_h= lambda : f'hfile_internal.h {h.htslib_hts_defs_h} {h.htslib_hfile_h} {h.textutils_internal_h}'
h.hts_internal_h  = lambda : f'hts_internal.h {h.htslib_hts_h} {h.textutils_internal_h}'
d.sam_internal_h  = lambda : f'sam_internal.h {h.htslib_sam_h}'
h.textutils_internal_h   = lambda: f'textutils_internal.h {h.htslib_kstring_h}'
d.thread_pool_internal_h = lambda: f'thread_pool_internal.h {h.htslib_thread_pool_h}'


from pprint import pprint
d = d.fiwic()
h = h.fiwic()


_='''
x.output must not be delayed!
'''
x = DelayedNameSpace.subclass('_anon')()
x.input = lambda: f'bgzf.c config.h {h.htslib_hts_h} {h.htslib_bgzf_h} {h.htslib_hfile_h} {h.htslib_thread_pool_h} {h.htslib_hts_endian_h} cram/pooled_alloc.h {h.hts_internal_h} {h.htslib_khash_h}'
x.output= 'bgzf.o bgzf.pico'
x.cmd   = AutoCmd(patterns)
x = x.fiwic()
pprint(x)
# ns['bgzf']


ns = RNS.subclass('MainRuleNameSpace')()
'kstring.o kstring.pico: kstring.c config.h $(htslib_kstring_h)'

ns['kstring.o kstring.pico'] = (lambda: f'kstring.c config.h',  AutoCmd(patterns))
ns['config.h'] = ('', lambda i,o: LSC(f'''
	# {{ echo hi; }}
	echo '/* Default config.h generated by Makefile */' > {i[0]}
	echo '#define HA0VE_LIBBZ2 1' >> {i[0]}
	echo '#define HAVE_LIBLZMA 1' >> {i[0]}
	echo '#ifndef __APPLE__'  >> {i[0]}
	echo '#define HAVE_LZMA_H 1' >>{i[0]}
	echo '#endif'  >>{i[0]}
	'''))
ns['kstring.c'] = None

from path import Path
Path('config.h').unlink_p()
(ns['kstring.o'].build())
# (ns['kstring.o kstring.pico'].build())
'should raise UnspecifiedName recipe not found for config.h'


'''
'''
# print(d)

# kstring.o kstring.pico: kstring.c config.h $(htslib_kstring_h)

'''

# And similarly for htslib.pc.tmp ("pkg-config template").  No dependency
# on htslib.pc.in listed, as if that file is newer the usual way to regenerate
# this target is via configure or config.status rather than this rule.
htslib.pc.tmp:
	sed -e '/^static_libs=/s/@static_LIBS@/$(htslib_default_libs)/;s#@[^-][^@]*@##g' htslib.pc.in > $@

# Create a makefile fragment listing the libraries and LDFLAGS needed for
# static linking.  This can be included by projects that want to build
# and link against the htslib source tree instead of an installed library.
htslib_static.mk: htslib.pc.tmp
	sed -n '/^static_libs=/s/[^=]*=/HTSLIB_static_LIBS = /p;/^static_ldflags=/s/[^=]*=/HTSLIB_static_LDFLAGS = /p' $< > $@

'''