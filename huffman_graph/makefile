CC		= @gcc
FLAGS		= -Wall -pedantic -std=c99 -g # -ANSI -pedantic
LIBS		=

PROGNAME	= huffman
HEADERS		= common.h
SOURCE		= compress.c decompress.c graph.c
MAIN		= $(PROGNAME).c

VERSION = `eval\ date\ +%d_%m_%Y`
THIS	= makefile
ARCH 	= $(PROGNAME).tar.gz 
ARCH_SRC= $(PROGNAME)-src.tar.gz

MSG	= @echo
RM	= @rm -vf
TAR 	= @tar -czf
MSG_OK	= $(MSG) "\t\t\t\t...ok"

all: $(PROGNAME)
debug: $(DEBUG)
arch: $(ARCH)
archive: $(ARCH_SRC)

.PHONY: clean arch archive debug

clean:
	$(MSG) "Suppressing generated files..."
	$(RM) *~ *.o $(PROGNAME)
	$(RM) $(ARCH) $(ARCH_SRC)
	$(RM) core
	$(MSG_OK)

$(ARCH): $(THIS) $(PROGNAME) $(HEADERS) $(SOURCE) $(MAIN) $(SOURCE:.c=.h) $(SOURCE:.c=.o) $(MAIN:.c=.o)
	$(MSG) "Archiving project..."
	$(TAR) $@ $^
	$(MSG) "$@ created"
	$(MSG_OK)

$(ARCH_SRC): $(THIS) $(PROGNAME) $(HEADERS) $(SOURCE) $(SOURCE:.c=.h) $(MAIN)
	$(MSG) "Archiving project sources..."
	$(TAR) $@ $^
	$(MSG) "$@ created"
	$(MSG_OK)

.SUFFIXES : . c . h . o

.c.o :
	$(MSG) "Compiling $@..."
	$(CC) -c $(FLAGS) $(LIBS) $<
	$(MSG_OK)

$(DEBUG): $(SOURCE:.c=.o) $(MAIN:.c=.o)
	$(MSG) "Linking into $@..."
	$(CC) -g $(FLAGS) $(LIBS) $^ -o $@
	$(MSG_OK)

$(PROGNAME): $(SOURCE:.c=.o) $(MAIN:.c=.o)
	$(MSG) "Linking into $@..."
	$(CC) $(FLAGS) $(LIBS) $^ -o $@
	$(MSG_OK)
