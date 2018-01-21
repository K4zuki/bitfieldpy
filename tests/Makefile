ifeq ($(OS),Windows_NT)
HOME = C:/Users/$(USERNAME)
endif
PANSTYLES= /var
MISC= $(PANSTYLES)/pandoc_misc
include $(MISC)/Makefile.in
PROJECT= `pwd`

## userland: uncomment and replace
# MDDIR:= markdown
# DATADIR:= data
# TARGETDIR:= Out
# IMAGEDIR:= images
# WAVEDIR:= waves
# BITDIR:= bitfields
# BIT16DIR:= bitfield16

# CONFIG:= config.yaml
# INPUT:= TITLE.md
# TARGET:= TARGET
##
include $(MISC)/Makefile
