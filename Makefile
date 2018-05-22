RSYNC=rsync -zcav \
	--exclude=\*~ --exclude=.\* \
	--delete-excluded --delete-after \
	--no-owner --no-group \
	--progress --stats


doc: .sphinx-stamp

doc-upload:
	$(RSYNC) build/doc/ wrobell@dcmod.org:~/public_html/decotengu

.sphinx-stamp:
	sphinx-build doc build/doc

