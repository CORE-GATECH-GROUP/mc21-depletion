TEX_MAIN=mc21.tex
TARGET=johnson-kotlyar-mc21.pdf
REFS=references/references.bib
FIGS=hybrid_ce_dk.pdf axial_offsets.pdf fluxes.pdf
MPL=matplotlibrc
DATA=data.h5
DATA_SOURCE=https://zenodo.org/record/4554319
ANS_TEX=mc2021.cls mc2021.bst citesort.sty cites.sty
_ANS_TEX_DIR=LaTeX-Template-MC2021-DateRev

all : ${TARGET}

.PHONY: all clean prereqs ans

define canned_py =
python $< $@
endef

${TARGET} : ${TEX_MAIN} ${REFS} ${FIGS} ${ANS_TEX}
	rubber --warn refs --jobname $(basename ${TARGET}) -d ${TEX_MAIN}

%.pdf : %.py ${DATA} ${MPL}
	$(canned_py)

prereqs : ${DATA} ${ANS_TEX}

${DATA} : data.h5.sha256
	@echo Fetching ${DATA} from ${DATA_SOURCE} with curl.
	@echo If this doesn\'t work, please download manually
	curl ${DATA_SOURCE}/files/data.h5 -o $@
	sha256sum --check $^

ans : ${ANS_TEX}

${ANS_TEX} : ${_ANS_TEX_DIR}
	cp $^/$@ $@

${_ANS_TEX_DIR} :
	@echo Fetching necessary LaTeX files.
	@echo If this doesn\'t work, the files can be manually downloaded from http://mc.ans.org/info-for-authors/
	curl http://mc.ans.org/wp-content/uploads/2021/02/LaTeX-Template-MC2021-DateRev.tar | \
		tar --extract $@

clean:
	rm -f ${subst .pdf,.*,${TARGET}} ${FIGS} ${ANS_TEX}
