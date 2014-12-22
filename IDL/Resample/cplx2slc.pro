function cplx2slc, ncol, nlig, tab_cplx

tab_slc = intarr(2*ncol,nlig)

for i = 0, ncol-1 do begin

	tab_slc(2*i,0:nlig-1) = fix(round(float(tab_cplx(i,0:nlig-1))))
	tab_slc(2*i+1,0:nlig-1) = fix(round(imaginary(tab_cplx(i,0:nlig-1))))

endfor
return, tab_slc

end