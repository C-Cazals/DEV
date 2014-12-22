function mult_expo_lig, ncol, nlig, dec, image

image_cen = complexarr(ncol,nlig)
x = indgen(ncol)

for i = 0, nlig-1 do begin

	image_cen(0:ncol-1,i) = image(0:ncol-1,i)*complex(cos(dec*x),sin(dec*x))

endfor

return, image_cen

end