function TFpar_lig, ncol, nlig, image

lig = complexarr(ncol)
TFlig = complexarr(ncol)
TFimage = complexarr(ncol, nlig)

for i = 0, nlig-1 do begin

	TFimage(0:ncol-1,i) = fft(image(0:ncol-1,i))

endfor

return, TFimage

end