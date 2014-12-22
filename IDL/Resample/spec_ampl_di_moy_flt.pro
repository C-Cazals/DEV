function spec_ampl_di_moy_flt, ncol, nlig, tab

colonne = fltarr(nlig)
lig_moy = fltarr(ncol)

for i = 0, ncol-1 do begin

	for j = 0, nlig-1 do begin
		colonne(j) = tab(i,j)
	endfor

	lig_moy(i) = mean(colonne)

endfor

return, lig_moy

end