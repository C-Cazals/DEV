pro slc2cplx, in_name, nlig, ncol, image

im_slc=intarr(2*ncol,nlig)
openr, unit, in_name, /get_lun
readu, unit, im_slc
close, unit
free_lun, unit
flush, unit
image=complexarr(ncol,nlig)
for i=0,nlig-1 do begin
	image(indgen(ncol),i)=complex(im_slc(2*indgen(ncol),i),im_slc(2*indgen(ncol)+1,i))
endfor
end